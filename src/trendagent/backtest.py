"""Backtest: laat de agent de afgelopen jaren opnieuw beleven, dag voor dag.

Hoe het werkt
- De koershistorie van alle instrumenten wordt één keer gedownload.
- Daarna draait precies dezelfde TrendAgent als in het echt, één ronde per
  handelsdag. Op elke dag krijgt hij alleen koersen t/m die dag te zien
  (geen blik in de toekomst).
- Kosten en slippage tellen mee, net als bij het oefenen.
- Gaat de kill switch aan, dan doen we alsof jij na 5 handelsdagen 'resume'
  doet. Hoe vaak dat gebeurt, staat in het rapport.

Waar je op moet letten (staat ook in het rapport)
- Survivorship bias: de lijst instrumenten is vandaag gekozen. Bedrijven die
  de afgelopen jaren groot zijn geworden (zoals Nvidia of Palantir) staan er
  dus in. Dat maakt de backtest waarschijnlijk te rooskleurig.
- Een goed verleden zegt niets zeker over de komende weken.
"""

from __future__ import annotations

import bisect
import math
import statistics
import tempfile
from dataclasses import dataclass, field, replace
from datetime import date
from pathlib import Path

from .agent import TrendAgent
from .core.config import Settings
from .core.kill_switch import HUMAN, KillSwitch
from .data import Bar, DataError, validate_bars
from .portfolio import Portfolio
from .universe import BY_TICKER, CRYPTO, UNIVERSE, Instrument

WINDOW_DAYS = 20          # "een paar weken" = 20 handelsdagen, ongeveer 4 weken
RESUME_AFTER_DAYS = 5     # gesimuleerde mens zet de agent na 5 handelsdagen weer aan
BENCHMARKS = ("IWDA.AS", "SPY")


# --------------------------------------------------------------------- data

class HistoricalProvider:
    """Geeft per gesimuleerde dag alleen de koersen t/m die dag terug."""

    name = "historical"

    def __init__(self, bars: dict[str, list[Bar]], usd_to_eur: dict[date, float]):
        self._bars = bars
        self._days = {t: [b.day for b in bs] for t, bs in bars.items()}
        self._fx_days = sorted(usd_to_eur)
        self._fx = usd_to_eur
        self.today: date | None = None

    def set_day(self, d: date) -> None:
        self.today = d

    def history(self, instrument: Instrument, days: int) -> list[Bar]:
        t = instrument.ticker
        if t not in self._bars:
            raise DataError(f"{t}: geen historische data")
        i = bisect.bisect_right(self._days[t], self.today)
        if i == 0:
            raise DataError(f"{t}: nog geen koersen op {self.today}")
        return self._bars[t][max(0, i - days):i]

    def usd_to_eur(self) -> float:
        i = bisect.bisect_right(self._fx_days, self.today)
        if i == 0 or (self.today - self._fx_days[i - 1]).days > 5:
            raise DataError(f"geen wisselkoers rond {self.today}")
        return self._fx[self._fx_days[i - 1]]

    def trading_days(self, start: date, end: date) -> list[date]:
        days = sorted({d for ds in self._days.values() for d in ds if start <= d <= end})
        return days


def download_history(years: int, instruments=UNIVERSE + CRYPTO) -> tuple[dict[str, list[Bar]], dict[date, float]]:
    """Haalt dagkoersen op via yfinance (alleen gebruikt op GitHub of je eigen computer)."""
    import yfinance as yf

    tickers = [i.ticker for i in instruments]
    period = f"{years + 1}y"   # één jaar extra om de 200-daagse gemiddelden op te bouwen
    df = yf.download(tickers, period=period, interval="1d", auto_adjust=True,
                     group_by="ticker", threads=True, progress=False)
    bars: dict[str, list[Bar]] = {}
    for t in tickers:
        try:
            sub = df[t].dropna()
        except KeyError:
            continue
        rows = [Bar(idx.date(), float(r["Open"]), float(r["High"]), float(r["Low"]),
                    float(r["Close"]), float(r["Volume"])) for idx, r in sub.iterrows()]
        try:
            bars[t] = validate_bars(rows, t)
        except DataError:
            # Een enkele kapotte regel: sla die regel over in plaats van het hele instrument.
            clean = [b for b in rows if min(b.open, b.high, b.low, b.close) > 0 and b.high >= b.low]
            if clean:
                bars[t] = clean
    fxdf = yf.download("EURUSD=X", period=period, interval="1d", progress=False, auto_adjust=False)
    close = fxdf["Close"]
    if hasattr(close, "columns"):        # nieuwere yfinance geeft een tabel met één kolom
        close = close.iloc[:, 0]
    fx = {idx.date(): 1.0 / float(v) for idx, v in close.dropna().items() if 0.5 < float(v) < 2.0}
    if not fx:
        raise DataError("geen historische wisselkoers EUR/USD")
    return bars, fx


# ------------------------------------------------------------------ backtest

@dataclass
class BacktestResult:
    start: date
    end: date
    equity: list[tuple[date, float]]
    trades: list
    halts: list[tuple[date, str]] = field(default_factory=list)
    benchmarks: dict[str, list[tuple[date, float]]] = field(default_factory=dict)
    tickers_used: int = 0


def run_backtest(base: Settings, provider: HistoricalProvider, start: date, end: date,
                 resume_after: int = RESUME_AFTER_DAYS) -> BacktestResult:
    state = Path(tempfile.mkdtemp(prefix="backtest-"))
    s = replace(base, state_dir=state, reports_dir=state / "rapporten", write_reports=False)
    agent = TrendAgent(s, provider)
    ks = KillSwitch(state / "kill_switch.json")
    days = provider.trading_days(start, end)
    if not days:
        raise ValueError("geen handelsdagen in de gekozen periode")

    equity: list[tuple[date, float]] = []
    halts: list[tuple[date, str]] = []
    halted_days = 0
    for d in days:
        provider.set_day(d)
        was_active = ks.is_active()
        rep = agent.run(d)
        if ks.is_active():
            if not was_active:
                halts.append((d, ks.status().get("reason", "")))
                halted_days = 0
            halted_days += 1
            if halted_days >= resume_after:          # gesimuleerde mens: 'resume'
                ks.deactivate(by=HUMAN)
                pf = Portfolio.load(agent.portfolio_path, s.starting_cash_eur)
                pf.reset_risk_baseline()
                pf.save(agent.portfolio_path)
        if rep.equity_eur:
            equity.append((d, rep.equity_eur))

    pf = Portfolio.load(agent.portfolio_path, s.starting_cash_eur)
    result = BacktestResult(days[0], days[-1], equity, pf.trades, halts,
                            tickers_used=len(provider._bars))
    for b in BENCHMARKS:
        series = buy_and_hold(provider, b, days, s.starting_cash_eur)
        if series:
            result.benchmarks[b] = series
    return result


def run_investor_backtest(base: Settings, provider: HistoricalProvider, start: date, end: date,
                          mix=None) -> BacktestResult:
    """Zelfde idee als run_backtest, maar dan voor de investeerder (maandelijks herverdelen)."""
    from .investor import Book, Investor
    from .strategies import production_mix

    state = Path(tempfile.mkdtemp(prefix="investor-"))
    s = replace(base, state_dir=state, write_reports=False)
    inv = Investor(s, provider, mix or production_mix())
    # Alleen werkdagen: crypto handelt ook in het weekend, maar we kijken net als live op werkdagen.
    days = [d for d in provider.trading_days(start, end) if d.weekday() < 5]
    equity = []
    for d in days:
        provider.set_day(d)
        out = inv.run(d)
        if out.get("equity_eur"):
            equity.append((d, out["equity_eur"]))
    book = Book.load(inv.path, s.starting_cash_eur)
    result = BacktestResult(days[0], days[-1], equity, book.trades, [], tickers_used=len(provider._bars))
    for b in BENCHMARKS:
        series = buy_and_hold(provider, b, days, s.starting_cash_eur)
        if series:
            result.benchmarks[b] = series
    return result


def buy_and_hold(provider: HistoricalProvider, ticker: str, days: list[date], cash: float):
    """Vergelijking: op dag 1 alles in één ETF stoppen en niets meer doen."""
    inst = BY_TICKER.get(ticker)
    if inst is None or ticker not in provider._bars:
        return []
    out, first = [], None
    for d in days:
        provider.set_day(d)
        try:
            price = provider.history(inst, 1)[-1].close
            fx = 1.0 if inst.currency == "EUR" else provider.usd_to_eur()
        except DataError:
            continue
        if first is None:
            first = price * fx
        out.append((d, cash * price * fx / first))
    return out


# ------------------------------------------------------------------- cijfers

def returns_between(series: list[tuple[date, float]]) -> list[float]:
    return [series[i][1] / series[i - 1][1] - 1 for i in range(1, len(series))]


def max_drawdown(series: list[tuple[date, float]]) -> float:
    peak, worst = -math.inf, 0.0
    for _, v in series:
        peak = max(peak, v)
        worst = min(worst, v / peak - 1)
    return worst


def summary(series: list[tuple[date, float]]) -> dict:
    if len(series) < 2:
        return {}
    total = series[-1][1] / series[0][1] - 1
    years = max((series[-1][0] - series[0][0]).days / 365.25, 1e-9)
    daily = returns_between(series)
    vol = statistics.pstdev(daily) * math.sqrt(252) if len(daily) > 1 else 0.0
    mean = statistics.fmean(daily) * 252 if daily else 0.0
    return {
        "total": total,
        "cagr": (1 + total) ** (1 / years) - 1 if total > -1 else -1.0,
        "max_dd": max_drawdown(series),
        "vol": vol,
        "sharpe": mean / vol if vol > 0 else 0.0,
    }


def per_year(series: list[tuple[date, float]]) -> dict[int, float]:
    out: dict[int, float] = {}
    by_year: dict[int, list[tuple[date, float]]] = {}
    for d, v in series:
        by_year.setdefault(d.year, []).append((d, v))
    prev_close = None
    for y in sorted(by_year):
        pts = by_year[y]
        start_v = prev_close if prev_close is not None else pts[0][1]
        out[y] = pts[-1][1] / start_v - 1
        prev_close = pts[-1][1]
    return out


def windows(series: list[tuple[date, float]], n: int = WINDOW_DAYS) -> list[float]:
    """Rendement over elk aaneengesloten blok van n handelsdagen (glijdend venster)."""
    vals = [v for _, v in series]
    return [vals[i + n] / vals[i] - 1 for i in range(0, len(vals) - n)]


def window_stats(rets: list[float]) -> dict:
    if not rets:
        return {}
    srt = sorted(rets)
    pct = lambda q: srt[min(len(srt) - 1, max(0, int(q * len(srt))))]
    return {
        "count": len(rets),
        "positive_share": sum(r > 0 for r in rets) / len(rets),
        "median": statistics.median(rets),
        "p05": pct(0.05),
        "p95": pct(0.95),
        "worst": srt[0],
        "best": srt[-1],
    }


def trade_stats(trades) -> dict:
    closed = [t for t in trades if t.side == "SELL" and t.pnl_eur is not None]
    buys = {}
    holding = []
    for t in trades:
        if t.side == "BUY":
            buys[t.ticker] = t.day
        elif t.ticker in buys:
            holding.append((date.fromisoformat(t.day) - date.fromisoformat(buys.pop(t.ticker))).days)
    wins = [t.pnl_eur for t in closed if t.pnl_eur > 0]
    losses = [t.pnl_eur for t in closed if t.pnl_eur <= 0]
    return {
        "buys": sum(1 for t in trades if t.side == "BUY"),
        "closed": len(closed),
        "win_rate": len(wins) / len(closed) if closed else 0.0,
        "avg_win": statistics.fmean(wins) if wins else 0.0,
        "avg_loss": statistics.fmean(losses) if losses else 0.0,
        "profit_factor": sum(wins) / -sum(losses) if losses and sum(losses) < 0 else float("inf") if wins else 0.0,
        "pnl": sum(t.pnl_eur for t in closed),
        "costs": sum(t.costs_eur for t in trades),
        "avg_hold_days": statistics.fmean(holding) if holding else 0.0,
    }
