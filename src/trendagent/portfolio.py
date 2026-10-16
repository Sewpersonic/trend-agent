"""De nep-portefeuille (paper trading).

Er gaat nooit echt geld om. Kopen en verkopen gebeurt alleen in dit bestand,
met realistische tegenvallers: slippage (iets slechtere prijs) en kosten.
Alles staat in euro's; Amerikaanse posities worden met de wisselkoers omgerekend.

De toestand wordt opgeslagen in state/portfolio.json, zodat de agent elke
dag verder kan waar hij gebleven was.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class Position:
    ticker: str
    currency: str
    qty: float
    entry_price: float      # in lokale valuta, inclusief slippage
    stop: float             # in lokale valuta
    highest_close: float
    opened: str             # datum ISO
    entry_fx: float         # lokale valuta -> EUR bij aankoop
    risk_eur: float         # verlies in EUR als de beginstop wordt geraakt
    last_checked: str = ""  # laatste handelsdag die tegen de stop is gecontroleerd
    # Journaal: waarom gekocht en onder welke omstandigheden (voor het leren achteraf).
    entry_reason: str = ""
    entry_context: dict = field(default_factory=dict)
    version: str = ""


@dataclass
class Trade:
    day: str
    ticker: str
    side: str               # "BUY" of "SELL"
    qty: float
    price: float            # lokale valuta
    fx: float
    value_eur: float
    costs_eur: float
    reason: str
    pnl_eur: float | None = None
    # Journaal (leeg bij trades van vóór deze versie)
    strategy: str = ""
    version: str = ""
    regime: str = ""
    context: dict = field(default_factory=dict)   # instap- en (bij verkoop) uitstapomstandigheden
    r_multiple: float | None = None               # resultaat gedeeld door het risico bij instap
    hold_days: int | None = None


@dataclass
class Portfolio:
    cash_eur: float
    positions: dict[str, Position] = field(default_factory=dict)
    trades: list[Trade] = field(default_factory=list)
    equity_history: list[dict] = field(default_factory=list)   # [{"day":..., "equity":...}]
    consecutive_losses: int = 0
    # Vanaf deze positie in equity_history telt de top voor de drawdown-rem.
    # 'resume' zet hem op de laatste dag, zodat een oude top de rem niet direct weer aanzet.
    peak_from_index: int = 0

    # ---------------------------------------------------------------- opslag

    @classmethod
    def load(cls, path: Path, starting_cash: float) -> Portfolio:
        if not path.exists():
            return cls(cash_eur=starting_cash)
        raw = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            cash_eur=raw["cash_eur"],
            positions={k: Position(**v) for k, v in raw["positions"].items()},
            trades=[Trade(**t) for t in raw["trades"]],
            equity_history=raw["equity_history"],
            consecutive_losses=raw.get("consecutive_losses", 0),
            peak_from_index=raw.get("peak_from_index", 0),
        )

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "cash_eur": round(self.cash_eur, 2),
            "positions": {k: asdict(v) for k, v in self.positions.items()},
            "trades": [asdict(t) for t in self.trades],
            "equity_history": self.equity_history,
            "consecutive_losses": self.consecutive_losses,
            "peak_from_index": self.peak_from_index,
        }
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        tmp.replace(path)

    # ------------------------------------------------------------ waardering

    def equity(self, prices: dict[str, float], fx: dict[str, float]) -> float:
        """Totale waarde in EUR. Zonder actuele prijs telt de instapprijs (voorzichtig: geen winst bijtellen)."""
        total = self.cash_eur
        for p in self.positions.values():
            price = prices.get(p.ticker, p.entry_price)
            total += p.qty * price * fx[p.currency]
        return total

    def open_risk_eur(self, fx: dict[str, float]) -> float:
        """Hoeveel er verloren gaat als ALLE stops nu worden geraakt (alleen verliezen tellen)."""
        risk = 0.0
        for p in self.positions.values():
            risk += max(0.0, (p.entry_price - p.stop) * p.qty * fx[p.currency])
        return risk

    def peak_equity(self) -> float | None:
        return max((e["equity"] for e in self.equity_history[self.peak_from_index:]), default=None)

    def reset_risk_baseline(self) -> None:
        """Na een bewuste herstart door de mens: verliesteller op 0 en de huidige waarde als nieuwe top."""
        self.consecutive_losses = 0
        self.peak_from_index = max(len(self.equity_history) - 1, 0)

    def record_equity(self, day: str, equity: float, bench: float | None = None) -> None:
        """Waarde van de dag vastleggen, met (optioneel) de koers van de vergelijkings-ETF in euro."""
        entry = {"day": day, "equity": round(equity, 2)}
        if bench is not None:
            entry["bench"] = round(bench, 4)
        if self.equity_history and self.equity_history[-1]["day"] == day:
            self.equity_history[-1].update(entry)
        else:
            self.equity_history.append(entry)

    # ------------------------------------------------------------- handelen

    def buy(self, day: str, ticker: str, currency: str, qty: float, price: float,
            stop: float, fx: float, costs_eur: float, reason: str,
            context: dict | None = None, version: str = "", regime: str = "",
            strategy: str = "trend") -> Trade:
        value = qty * price * fx
        if value + costs_eur > self.cash_eur + 1e-6:
            raise ValueError("onvoldoende (nep)geld")
        if ticker in self.positions:
            raise ValueError("bijkopen in een bestaande positie is niet toegestaan")
        self.cash_eur -= value + costs_eur
        self.positions[ticker] = Position(
            ticker, currency, qty, price, stop, price, day, fx,
            risk_eur=round((price - stop) * qty * fx + costs_eur, 2), last_checked=day,
            entry_reason=reason, entry_context=dict(context or {}, regime=regime), version=version)
        t = Trade(day, ticker, "BUY", qty, round(price, 4), fx, round(value, 2), round(costs_eur, 2), reason,
                  strategy=strategy, version=version, regime=regime, context=dict(context or {}))
        self.trades.append(t)
        return t

    def sell(self, day: str, ticker: str, price: float, fx: float, costs_eur: float, reason: str,
             exit_context: dict | None = None, regime: str = "", strategy: str = "trend") -> Trade:
        p = self.positions.pop(ticker)
        value = p.qty * price * fx
        cost_basis = p.qty * p.entry_price * p.entry_fx
        buy_costs = next((t.costs_eur for t in reversed(self.trades)
                          if t.ticker == ticker and t.side == "BUY"), 0.0)
        pnl = value - cost_basis - costs_eur - buy_costs
        self.cash_eur += value - costs_eur
        self.consecutive_losses = self.consecutive_losses + 1 if pnl < 0 else 0
        from datetime import date as _date
        hold = (_date.fromisoformat(day) - _date.fromisoformat(p.opened)).days
        context = {"instap": p.entry_context, "instap_reden": p.entry_reason, "uitstap": dict(exit_context or {}),
                   "risico_bij_instap_eur": p.risk_eur}
        t = Trade(day, ticker, "SELL", p.qty, round(price, 4), fx, round(value, 2),
                  round(costs_eur, 2), reason, pnl_eur=round(pnl, 2), strategy=strategy, version=p.version,
                  regime=regime, context=context,
                  r_multiple=round(pnl / p.risk_eur, 3) if p.risk_eur > 0 else None, hold_days=hold)
        self.trades.append(t)
        return t
