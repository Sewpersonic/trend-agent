"""De trend-agent: één ronde per handelsdag.

Volgorde van een ronde (elke stap kan de ronde stoppen):
 1. Kill switch aan?                         -> niets kopen of verkopen
 2. Wisselkoers EUR/USD ophalen              -> mislukt = niets doen
 3. Koersen van alle instrumenten ophalen    -> te veel fouten = niets kopen
 4. Open posities nalopen: stop geraakt of trend gebroken -> verkopen;
    anders de stop omhoog laten meeschuiven
 5. Risicoremmen controleren: dagverlies, drawdown, verliezen op rij
    -> zo nodig kill switch aan
 6. Nieuwe aankopen: de sterkste trends, binnen alle risicolimieten
 7. Alles opslaan, auditlog bijwerken en een leesbaar rapport schrijven

Alles gebeurt in de nep-portefeuille. Er bestaat geen code die een echte
order kan versturen.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import date

from . import insights, uitleg
from .core.audit_log import AuditLog
from .core.config import Settings
from .core.kill_switch import KillSwitch
from .data import Bar, DataError, DataProvider
from .features import UNKNOWN, data_issues, market_regime, snapshot, stale_issues
from .portfolio import Portfolio
from .strategies import trend_version
from .reports import write_daily_note, write_excel
from .signals import Analysis, analyse, trend_broken
from .universe import BY_TICKER, select

HISTORY_DAYS = 260
MAX_DATA_FAILURE_SHARE = 0.3   # meer dan 30% van de reeksen kapot = datastroom onbetrouwbaar
ACTOR = "trend_agent"


@dataclass
class RunReport:
    day: str
    status: str = "OK"
    equity_eur: float = 0.0
    cash_eur: float = 0.0
    actions: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    ranking: list[Analysis] = field(default_factory=list)
    buys_allowed: bool = True
    regime: str = "onbekend"
    version: str = ""
    health: dict = field(default_factory=dict)
    risk_rows: list[dict] = field(default_factory=list)
    brakes: dict = field(default_factory=dict)
    kansen: list[dict] = field(default_factory=list)
    analyse: dict = field(default_factory=dict)


class TrendAgent:
    def __init__(self, settings: Settings, provider: DataProvider):
        if not settings.paper_trading:
            raise RuntimeError("Deze agent draait alleen met een nep-portefeuille")
        self.s = settings
        self.provider = provider
        d = settings.state_dir
        self.portfolio_path = d / "portfolio.json"
        self.audit = AuditLog(d / "audit.jsonl")
        self.kill_switch = KillSwitch(d / "kill_switch.json")
        self.version = trend_version(settings)
        self.regime = UNKNOWN
        self._bench_eur: float | None = None

    # ------------------------------------------------------------------ ronde

    def run(self, today: date) -> RunReport:
        rep = RunReport(day=today.isoformat(), version=self.version)
        self.regime, self._bench_eur = UNKNOWN, None
        pf = Portfolio.load(self.portfolio_path, self.s.starting_cash_eur)
        if not pf.equity_history:   # eerste ronde: startkapitaal vastleggen als nulpunt
            pf.record_equity("start", self.s.starting_cash_eur)
        self.audit.append("run_started", ACTOR, {"day": rep.day, "provider": self.provider.name})

        # 1. kill switch: geen nieuwe aankopen, maar bestaande posities blijven beschermd
        #    (stop-loss en trendbreuk mogen nog verkopen; verkopen verkleint alleen risico).
        if self.kill_switch.is_active():
            ks = self.kill_switch.status()
            rep.status = "GESTOPT"
            rep.buys_allowed = False
            rep.warnings.append(f"Kill switch staat aan ({ks.get('reason')}). Geen aankopen; "
                                "stop-losses blijven actief.")
            self.audit.append("buys_blocked", ACTOR, {"reason": "kill switch actief"})
            if not pf.positions:
                return self._finish(rep, pf, {}, {"EUR": 1.0, "USD": None})

        # 2. wisselkoers
        try:
            fx = {"EUR": 1.0, "USD": self.provider.usd_to_eur()}
        except DataError as exc:
            rep.status = "GEEN HANDEL"
            rep.warnings.append(f"Wisselkoers ontbreekt: {exc}")
            self.audit.append("run_aborted", ACTOR, {"reason": str(exc)})
            pf.save(self.portfolio_path)
            return rep

        # 3. koersdata
        instruments = select(self.s.tickers_override)
        wanted = {i.ticker: i for i in instruments}
        for t in pf.positions:              # open posities altijd meenemen
            wanted.setdefault(t, BY_TICKER[t])
        bars: dict[str, list[Bar]] = {}
        failures = 0
        for ticker, inst in wanted.items():
            try:
                bars[ticker] = self.provider.history(inst, HISTORY_DAYS)
            except DataError as exc:
                failures += 1
                rep.warnings.append(str(exc))
        if failures / max(len(wanted), 1) > MAX_DATA_FAILURE_SHARE:
            rep.buys_allowed = False
            rep.warnings.append(f"{failures} van {len(wanted)} koersreeksen mislukt: vandaag geen aankopen")
        # Verdachte reeksen (bevroren koers, sprong, geen volume): niet kopen, wel beheren.
        src_issues = getattr(self.provider, "source_issues", lambda t: [])
        stale, stale_warn = stale_issues(bars, today, {t: BY_TICKER[t].region for t in bars})
        rep.warnings += stale_warn
        suspicious = {t: data_issues(b) + src_issues(t) + stale.get(t, []) for t, b in bars.items()}
        suspicious = {t: i for t, i in suspicious.items() if i}
        for t, issues in suspicious.items():
            rep.warnings.append(f"{t}: verdachte data ({'; '.join(issues)}), niet gekocht")
        analyses = {t: analyse(t, b, today, self.s) for t, b in bars.items()}
        prices = {t: b[-1].close for t, b in bars.items()}
        self.regime = market_regime(bars)
        rep.regime = self.regime.label
        self._snapshots = {t: snapshot(b) for t, b in bars.items()}
        bench = next((t for t in ("IWDA.AS", "SPY") if t in bars), None)
        if bench:
            self._bench_eur = prices[bench] * fx[BY_TICKER[bench].currency]
        rep.health = {"gevraagd": len(wanted), "ok": len(bars), "mislukt": failures,
                      "verdacht": {t: i for t, i in suspicious.items()}, "wisselkoers": "ok",
                      "regime": rep.regime, "verouderd": len(stale)}
        self.last_bars = bars
        self._bars = bars
        if hasattr(self.provider, "summary"):
            rep.health["bronnen"] = self.provider.summary()

        # 4. open posities
        for ticker in list(pf.positions):
            if ticker not in bars:
                rep.warnings.append(f"{ticker}: geen data, positie ongewijzigd gelaten")
                continue
            if ticker in suspicious:
                # Regel: geen trade op onbetrouwbare data. Niet verkopen op een koers die misschien niet klopt;
                # de stop-loss blijft staan en morgen wordt opnieuw gekeken.
                rep.warnings.append(f"{ticker}: verdachte data, positie vandaag niet aangepast (stop blijft {pf.positions[ticker].stop:.2f})")
                self.audit.append("exit_skipped_bad_data", ACTOR, {"ticker": ticker, "issues": suspicious[ticker]})
                continue
            self._manage_position(pf, ticker, bars[ticker], analyses[ticker], fx, rep)

        # 5. risicoremmen (alleen als de kill switch nog niet aan staat)
        equity = pf.equity(prices, fx)
        if rep.buys_allowed or rep.status != "GESTOPT":
            self._risk_brakes(pf, equity, rep)

        # 6. nieuwe aankopen
        ranked = sorted((a for a in analyses.values() if a.is_candidate and a.ticker not in suspicious),
                        key=lambda a: -a.score)
        rep.ranking = ranked[:10]
        if self.s.regime_filter and self.regime.onzeker and rep.buys_allowed:
            rep.buys_allowed = False
            rep.warnings.append(f"Markt te onzeker ({rep.regime}): geen nieuwe aankopen (regimefilter)")
            self.audit.append("buys_blocked", ACTOR, {"reason": "regimefilter", "regime": rep.regime})
        if rep.buys_allowed and not self.kill_switch.is_active():
            self._buy_candidates(pf, ranked, fx, equity, rep)
        # Uitleg voor de mens: verandert niets meer aan de portefeuille.
        try:
            blocked = None
            if self.kill_switch.is_active():
                blocked = "de kill switch staat aan"
            elif not rep.buys_allowed:
                blocked = "vandaag geen aankopen (zie waarschuwingen)"
            rep.kansen = insights.opportunities(rep, pf, self._snapshots, self.s, pf.equity(prices, fx), fx,
                                                BY_TICKER, self._costs, blocked)
            region_of = {t: BY_TICKER[t].region for t in bars}
            market = uitleg.market_view(bars, self.regime, region_of)
            zeef = uitleg.funnel(analyses, suspicious)
            bought = [t.ticker for t in pf.trades if t.day == rep.day and t.side == "BUY"]
            rep.analyse = {"markt": market, "zeef": zeef,
                           "conclusies": uitleg.market_conclusions(market) + uitleg.trend_conclusions(
                               zeef, rep.kansen, self.s.max_positions - len(pf.positions), bought, region_of)}
        except Exception as exc:  # noqa: BLE001
            self.audit.append("report_failed", ACTOR, {"error": f"kansen: {type(exc).__name__}: {exc}"})
        return self._finish(rep, pf, prices, fx)

    # ------------------------------------------------------------ posities

    def _manage_position(self, pf: Portfolio, ticker: str, bars: list[Bar],
                         a: Analysis, fx: dict, rep: RunReport) -> None:
        pos = pf.positions[ticker]
        rate = fx[pos.currency]
        # Alle nieuwe dagen sinds de vorige controle aflopen: is de stop ergens geraakt?
        new_bars = [b for b in bars if b.day.isoformat() > max(pos.opened, pos.last_checked)]
        for b in new_bars:
            if b.low <= pos.stop:
                fill = min(b.open, pos.stop) * (1 - self.s.slippage)   # bij een gat: openingskoers
                t = pf.sell(b.day.isoformat(), ticker, fill, rate,
                            self._costs(pos.qty * fill * rate), "stop-loss geraakt",
                            exit_context=self._ctx(ticker, a), regime=self.regime.label)
                self._log_trade(t, rep)
                return
            pos.highest_close = max(pos.highest_close, b.close)
            pos.last_checked = b.day.isoformat()
        if not new_bars:
            return
        if trend_broken(a):
            fill = a.close * (1 - self.s.slippage)
            t = pf.sell(rep.day, ticker, fill, rate, self._costs(pos.qty * fill * rate),
                        "trend gebroken (slot onder 50-daags gemiddelde)",
                        exit_context=self._ctx(ticker, a), regime=self.regime.label)
            self._log_trade(t, rep)
            return
        if self.s.ha_exit and heikin_ashi_red(bars, 2):
            fill = a.close * (1 - self.s.slippage)
            t = pf.sell(rep.day, ticker, fill, rate, self._costs(pos.qty * fill * rate),
                        "2 rode trendkaarsen op rij (trend verzwakt)",
                        exit_context=self._ctx(ticker, a), regime=self.regime.label)
            self._log_trade(t, rep)
            return
        trail = pos.highest_close - self.s.trail_atr_multiple * a.atr14
        if trail > pos.stop:
            self.audit.append("stop_raised", ACTOR, {"ticker": ticker, "old": round(pos.stop, 4),
                                                     "new": round(trail, 4)})
            rep.actions.append(f"{ticker}: stop omhoog van {pos.stop:.2f} naar {trail:.2f}")
            pos.stop = trail

    def _risk_brakes(self, pf: Portfolio, equity: float, rep: RunReport) -> None:
        reason = None
        earlier = [h for h in pf.equity_history if h["day"] < rep.day]   # ook bij een tweede ronde op dezelfde dag
        prev = earlier[-1]["equity"] if earlier else None
        if prev and equity < prev * (1 - self.s.daily_loss_limit):
            reason = f"dagverlies groter dan {self.s.daily_loss_limit:.0%}"
        peak = pf.peak_equity() or equity
        if pf.peak_from_index == 0:      # vóór een eerste herstart telt het startkapitaal als top
            peak = max(peak, self.s.starting_cash_eur)
        if equity < peak * (1 - self.s.max_drawdown):
            reason = f"totale daling groter dan {self.s.max_drawdown:.0%} vanaf de top"
        if pf.consecutive_losses >= self.s.max_consecutive_losses:
            reason = f"{pf.consecutive_losses} verliestrades op rij"
        if reason:
            self.kill_switch.activate(reason, by="risk_manager")
            rep.status = "GESTOPT"
            rep.buys_allowed = False
            rep.warnings.append(f"Kill switch aangezet: {reason}. Zet hem zelf weer uit met 'resume'.")
            self.audit.append("kill_switch_activated", ACTOR, {"reason": reason, "equity": round(equity, 2)})

    def _buy_candidates(self, pf: Portfolio, ranked: list[Analysis], fx: dict,
                        equity: float, rep: RunReport) -> None:
        slots = self.s.max_positions - len(pf.positions)
        for a in ranked:
            if slots <= 0:
                break
            if a.ticker in pf.positions:
                continue
            rsi_now = self._snapshots.get(a.ticker, {}).get("rsi14")
            if rsi_now is not None and rsi_now > self.s.max_rsi_entry:
                rep.actions.append(f"{a.ticker}: overgeslagen (RSI {rsi_now:.0f} boven {self.s.max_rsi_entry:.0f})")
                continue
            why_not = self._pattern_blocks(a.ticker)
            if why_not:
                rep.actions.append(f"{a.ticker}: overgeslagen ({why_not})")
                continue
            inst = BY_TICKER[a.ticker]
            rate = fx[inst.currency]
            entry = a.close * (1 + self.s.slippage)
            stop = entry - self.s.stop_atr_multiple * a.atr14
            risk_per_share = (entry - stop) * rate
            if stop <= 0 or risk_per_share <= 0:
                continue
            risk_left = equity * self.s.max_open_risk - pf.open_risk_eur(fx)
            budget = min(equity * self.s.risk_per_trade, risk_left)
            qty = math.floor(budget / risk_per_share)
            qty = min(qty, math.floor(equity * self.s.max_position_weight / (entry * rate)))
            # Kosten meetellen bij het geld dat nodig is.
            while qty > 0 and qty * entry * rate + self._costs(qty * entry * rate) > pf.cash_eur:
                qty -= 1
            if qty < 1:
                rep.actions.append(f"{a.ticker}: overgeslagen (één aandeel past niet binnen het risicobudget)")
                self.audit.append("buy_skipped", ACTOR, {"ticker": a.ticker, "reason": "budget"})
                continue
            t = pf.buy(rep.day, a.ticker, inst.currency, qty, entry, stop, rate,
                       self._costs(qty * entry * rate), " · ".join(a.reasons),
                       context=self._ctx(a.ticker, a), version=self.version, regime=self.regime.label)
            self._log_trade(t, rep, extra={"stop": round(stop, 4), "score": a.score})
            slots -= 1

    # ------------------------------------------------------------------ hulp

    def _pattern_blocks(self, ticker: str) -> str | None:
        """Patroonfilter bij instap (alleen als entry_filter aan staat). Geeft de reden om niet te kopen, of None."""
        mode = getattr(self.s, "entry_filter", "geen")
        if mode == "geen":
            return None
        closes = [b.close for b in getattr(self, "_bars", {}).get(ticker, [])]
        if len(closes) < 64:
            return "te weinig historie voor het patroonfilter"
        if mode == "terugval" and not closes[-1] < closes[-6]:
            return "patroonfilter: geen terugval in de laatste week"
        if mode == "uitbraak" and not closes[-1] >= max(closes[-64:-1]):
            return "patroonfilter: geen nieuwe 3-maands top"
        return None

    def _ctx(self, ticker: str, a: Analysis) -> dict:
        """Marktomstandigheden van één instrument, voor het journaal en de uitleg."""
        ctx = dict(getattr(self, "_snapshots", {}).get(ticker, {}))
        ctx.update({"score": a.score, "rend_1m": round(a.ret21, 4), "rend_3m": round(a.ret63, 4),
                    "volume_rel": round(a.rel_volume, 2), "atr14": round(a.atr14, 4),
                    "beweeglijkheid_regime": self.regime.beweeglijkheid, "trend_regime": self.regime.trend})
        return ctx

    def _costs(self, value_eur: float) -> float:
        return max(self.s.commission_min_eur, value_eur * self.s.commission_pct)

    def _log_trade(self, t, rep: RunReport, extra: dict | None = None) -> None:
        details = {"ticker": t.ticker, "side": t.side, "qty": t.qty, "price": t.price,
                   "value_eur": t.value_eur, "costs_eur": t.costs_eur, "reason": t.reason,
                   "pnl_eur": t.pnl_eur} | (extra or {})
        self.audit.append("paper_trade", ACTOR, details)
        pnl = f", resultaat €{t.pnl_eur:+.2f}" if t.pnl_eur is not None else ""
        rep.actions.append(f"{t.side} {t.qty:g} x {t.ticker} @ {t.price:.2f} ({t.reason}{pnl})")

    def _finish(self, rep: RunReport, pf: Portfolio, prices: dict, fx: dict) -> RunReport:
        if fx.get("USD") is not None:
            rep.equity_eur = round(pf.equity(prices, fx), 2)
            try:
                rep.risk_rows = insights.trend_positions(pf, prices, fx, self._costs)
                rep.brakes = insights.trend_brakes(pf, rep.equity_eur, rep.day, self.s)
            except Exception as exc:  # noqa: BLE001
                self.audit.append("report_failed", ACTOR, {"error": f"risico: {type(exc).__name__}: {exc}"})
            pf.record_equity(rep.day, rep.equity_eur, bench=self._bench_eur)
        rep.cash_eur = round(pf.cash_eur, 2)
        pf.save(self.portfolio_path)
        r_values = [t.r_multiple for t in pf.trades if t.side == "SELL" and t.r_multiple is not None]
        insights.save(self.s.state_dir, "trend", {"dag": rep.day, "posities": rep.risk_rows,
                                                  "remmen": rep.brakes, "kansen": rep.kansen,
                                                  "conclusies": rep.analyse.get("conclusies", []),
                                                  "zag": (uitleg.market_lines(rep.analyse["markt"])
                                                          + uitleg.funnel_lines(rep.analyse["zeef"])) if rep.analyse else [],
                                                  "klaar": uitleg.readiness("trend", pf.equity_history, r_values),
                                                  "markt": rep.analyse.get("markt", {}),
                                                  "zeef": rep.analyse.get("zeef", {}),
                                                  "vrije_plekken": self.s.max_positions - len(pf.positions),
                                                  "gekocht": [t.ticker for t in pf.trades if t.day == rep.day and t.side == "BUY"],
                                                  "verkocht": [t.ticker for t in pf.trades if t.day == rep.day and t.side == "SELL"]})
        markdown = render_report(rep, pf)
        (self.s.state_dir / "report.md").write_text(markdown, encoding="utf-8")
        # Rapporten voor de mens. Een fout hierin mag de handel nooit beïnvloeden.
        if self.s.write_reports:
            try:
                write_daily_note(rep.day, markdown, self.s.reports_dir)
                write_excel(pf, rep.ranking, self.s.reports_dir / "trend-agent.xlsx")
            except Exception as exc:  # noqa: BLE001
                self.audit.append("report_failed", ACTOR, {"error": f"{type(exc).__name__}: {exc}"})
        self.audit.append("run_finished", ACTOR, {"status": rep.status, "equity_eur": rep.equity_eur,
                                                   "actions": len(rep.actions)})
        return rep


def heikin_ashi_red(bars: list[Bar], n: int) -> bool:
    """True als de laatste n trendkaarsen (Heikin-Ashi) rood zijn. Gebruikt de laatste 30 dagen."""
    view = bars[-30:]
    if len(view) < n + 2:
        return False
    po = pc = None
    colors = []
    for b in view:
        c = (b.open + b.high + b.low + b.close) / 4
        o = (b.open + b.close) / 2 if po is None else (po + pc) / 2
        colors.append(c >= o)
        po, pc = o, c
    return not any(colors[-n:])


def render_report(rep: RunReport, pf: Portfolio) -> str:
    """Leesbaar dagrapport in Markdown (GitHub toont dit netjes)."""
    start = pf.equity_history[0]["equity"] if pf.equity_history else None
    lines = [f"# Trend-agent rapport {rep.day}", "",
             "_Oefenportefeuille met nepgeld. Geen beleggingsadvies; resultaten uit het verleden zeggen niets over de toekomst._",
             "", f"**Status:** {rep.status}  ", f"**Waarde:** €{rep.equity_eur:,.2f}  ",
             f"**Kas:** €{rep.cash_eur:,.2f}  ", f"**Marktregime:** {rep.regime}  ",
             f"**Strategieversie:** {rep.version}  "]
    src = rep.health.get("bronnen")
    if src:
        k = src["koersen"]
        lines.append(f"**Koersbronnen:** {k.get('bevestigd', 0)} bevestigd door 2 bronnen, "
                     f"{k.get('1 bron', 0)} uit 1 bron, {k.get('afwijking', 0)} afwijkend; "
                     f"wisselkoers {src['wisselkoers']}  ")
    if start:
        lines.append(f"**Sinds start:** {rep.equity_eur / start - 1:+.2%}  ")
    if rep.analyse:
        lines += ["", "## Analyse van vandaag", "", "**Wat de bot zag**", ""]
        lines += uitleg.market_lines(rep.analyse["markt"]) + uitleg.funnel_lines(rep.analyse["zeef"])
        lines += ["", "**Wat de bot eruit haalt**", ""] + [f"- {c}" for c in rep.analyse["conclusies"]]
    lines += ["", "## Vandaag gedaan", ""]
    lines += [f"- {a}" for a in rep.actions] or ["- Niets"]
    todays = [t for t in pf.trades if t.day == rep.day]
    if todays:
        lines += ["", "## Waarom", ""]
        for t in todays:
            c = t.context if t.side == "BUY" else t.context.get("uitstap", {})
            bits = [f"RSI {c['rsi14']:.0f}" if "rsi14" in c else "",
                    f"MACD-histogram {c['macd_hist_pct']:+.2f}%" if "macd_hist_pct" in c else "",
                    f"ATR {c['atr_pct']:.1f}% per dag" if "atr_pct" in c else "",
                    f"{c['afstand_sma200_pct']:+.1f}% boven SMA200" if "afstand_sma200_pct" in c else "",
                    f"markt {t.regime}" if t.regime else ""]
            extra = f", R = {t.r_multiple:+.2f} na {t.hold_days} dagen" if t.r_multiple is not None else ""
            lines.append(f"- **{t.side} {t.ticker}**: {t.reason}. Omstandigheden: "
                         + ", ".join(b for b in bits if b) + extra)
    if rep.warnings:
        lines += ["", "## Waarschuwingen", ""] + [f"- {w}" for w in rep.warnings]
    if rep.risk_rows or rep.brakes:
        lines += [""] + insights.render_trend_risk(rep.risk_rows, rep.brakes)
    if rep.kansen:
        lines += [""] + insights.render_opportunities(rep.kansen)
    closed_r = [t.r_multiple for t in pf.trades if t.side == "SELL" and t.r_multiple is not None]
    lines += ["", "## Wat de bot tot nu toe geleerd heeft", ""]
    lines += uitleg.learning_lines(closed_r, sum(t.pnl_eur or 0 for t in pf.trades if t.side == "SELL"))
    lines += ["", "## Klaar voor echt geld?", ""]
    lines += uitleg.readiness_lines("Trend-agent", uitleg.readiness("trend", pf.equity_history, closed_r))
    lines += ["", uitleg.TREND_METHOD]
    lines += ["", "## Open posities", "", "| Ticker | Aantal | Instap | Stop | Sinds |", "| --- | --- | --- | --- | --- |"]
    lines += [f"| {p.ticker} | {p.qty:g} | {p.entry_price:.2f} {p.currency} | {p.stop:.2f} | {p.opened} |"
              for p in pf.positions.values()] or ["| geen | | | | |"]
    lines += ["", "## Sterkste trends vandaag", "", "| # | Ticker | Score | 3 mnd | 1 mnd |", "| --- | --- | --- | --- | --- |"]
    lines += [f"| {i} | {a.ticker} | {a.score:.3f} | {a.ret63:+.1%} | {a.ret21:+.1%} |"
              for i, a in enumerate(rep.ranking, 1)] or ["| - | geen kandidaten | | | |"]
    closed = [t for t in pf.trades if t.side == "SELL"]
    if closed:
        wins = [t for t in closed if (t.pnl_eur or 0) > 0]
        lines += ["", "## Afgesloten trades", "",
                  f"{len(closed)} trades, {len(wins)} winst ({len(wins) / len(closed):.0%}), "
                  f"totaal €{sum(t.pnl_eur or 0 for t in closed):+,.2f} na kosten."]
    return "\n".join(lines) + "\n"
