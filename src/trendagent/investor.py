"""De investeerder: blijft belegd en verdeelt één keer per maand opnieuw.

Verdeling (instelbaar):
  60% kern       een wereldwijde ETF (MSCI World, IWDA). Volgt de hele markt.
  30% satelliet  de 5 sterkste aandelen/ETF's: hoogste rendement over 12 maanden
                 (de laatste maand niet meegeteld), mits in een stijgende trend
                 (slotkoers boven het 200-daags gemiddelde). Te weinig kandidaten?
                 Dan gaat dat deel naar de kern.
  10% crypto     Bitcoin en Ethereum, elk de helft, ALLEEN als de koers boven het
                 200-daags gemiddelde staat. Anders blijft dat deel in kas.

Waarom zo
- De kern zorgt dat je meeprofiteert van de groei van de wereldeconomie;
  de backtest liet zien dat juist dát het meeste opleverde.
- De satelliet en de crypto proberen daar iets bij te verdienen, maar zijn
  begrensd zodat ze de kern niet kunnen wegvagen.
- Eén keer per maand handelen: weinig kosten, weinig ruis.

Veiligheid
- Alleen nepgeld. Er is geen brokerkoppeling.
- Kill switch: blokkeert alle aankopen (verkopen blijft mogelijk).
- Een koers of wisselkoers die ontbreekt: niet herverdelen, alles laten staan.
- Alleen instrumenten uit universe.py; nooit kleine of onbekende munten.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

from . import insights, uitleg
from .core.audit_log import AuditLog
from .core.config import Settings
from .core.kill_switch import KillSwitch
from .data import Bar, DataError, DataProvider
from .portfolio import Trade
from .features import UNKNOWN, Regime, data_issues, market_regime, stale_issues
from .signals import sma
from .strategies import investor_version
from .universe import BY_TICKER, CRYPTO, UNIVERSE

ACTOR = "investeerder"
HISTORY_DAYS = 270


@dataclass(frozen=True)
class Mix:
    core_ticker: str = "IWDA.AS"
    core_weight: float = 0.60
    satellite_weight: float = 0.30
    satellite_count: int = 5
    crypto_weight: float = 0.10
    min_trade_share: float = 0.01     # verschillen kleiner dan 1% van het vermogen niet bijhandelen
    min_traded_value: float = 20_000_000
    satellite_kinds: tuple[str, ...] = ("STOCK", "ETF")   # ("ETF",) = alleen ETF's
    # Alleen aanzetten als het onderzoek bewijst dat het helpt (standaard uit):
    regime_filter: bool = False   # dalende markt: satelliet en crypto naar kas, kern blijft


@dataclass
class Book:
    """De nep-portefeuille van de investeerder: kas en aantallen (gebroken aantallen toegestaan)."""

    cash_eur: float
    qty: dict[str, float] = field(default_factory=dict)
    cost_eur: dict[str, float] = field(default_factory=dict)    # totale aankoopwaarde per positie
    trades: list[Trade] = field(default_factory=list)
    equity_history: list[dict] = field(default_factory=list)
    last_rebalance: str = ""

    @classmethod
    def load(cls, path: Path, cash: float) -> "Book":
        if not path.exists():
            return cls(cash_eur=cash)
        raw = json.loads(path.read_text(encoding="utf-8"))
        raw["trades"] = [Trade(**t) for t in raw.get("trades", [])]
        return cls(**raw)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = asdict(self)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=1), encoding="utf-8")
        tmp.replace(path)

    def value(self, prices_eur: dict[str, float]) -> float:
        return self.cash_eur + sum(q * prices_eur[t] for t, q in self.qty.items())


def _momentum(bars: list[Bar]) -> float | None:
    """Rendement over 12 maanden zonder de laatste maand (klassieke momentummaat)."""
    if len(bars) < 253:
        return None
    return bars[-22].close / bars[-253].close - 1


def target_weights(bars: dict[str, list[Bar]], mix: Mix, regime: Regime = UNKNOWN,
                   exclude: frozenset[str] = frozenset()) -> tuple[dict[str, float], list[str]]:
    """Bepaalt de gewenste verdeling. Geeft (gewichten, uitleg) terug. Rest = kas.

    exclude: instrumenten met verdachte data; die worden niet nieuw gekozen.
    """
    notes: list[str] = []
    defensive = mix.regime_filter and regime.trend == "dalend"
    w: dict[str, float] = {}
    core = mix.core_ticker if mix.core_ticker in bars and len(bars[mix.core_ticker]) >= 200 else "SPY"
    if core not in bars:
        raise DataError("geen koersen voor de kern-ETF")
    core_w = mix.core_weight

    # Satelliet: sterkste momentum, alleen in een stijgende trend en met genoeg handel.
    scored = []
    for inst in UNIVERSE:
        t = inst.ticker
        b = bars.get(t)
        if t == core or t in exclude or inst.kind not in mix.satellite_kinds or not b or len(b) < 253:
            continue
        closes = [x.close for x in b]
        traded = sum(x.close * x.volume for x in b[-20:]) / 20
        mom = _momentum(b)
        if mom is None or mom <= 0 or closes[-1] <= sma(closes, 200) or traded < mix.min_traded_value:
            continue
        scored.append((mom, t))
    scored.sort(reverse=True)
    picks = [t for _, t in scored[:mix.satellite_count]]
    if defensive:
        # Kapitaal beschermen: de kern blijft, satelliet en crypto gaan naar kas.
        notes.append(f"Regimefilter: markt {regime.label}, satelliet en crypto blijven in kas")
    elif picks:
        each = mix.satellite_weight / mix.satellite_count
        for t in picks:
            w[t] = each
        core_w += each * (mix.satellite_count - len(picks))
        notes.append("Satelliet: " + ", ".join(f"{t} ({m:+.0%})" for m, t in scored[:len(picks)]))
    else:
        core_w += mix.satellite_weight
        notes.append("Satelliet: geen aandelen in een stijgende trend; dat deel gaat naar de kern")
    w[core] = core_w
    if defensive:
        return w, notes

    # Crypto: alleen boven het 200-daags gemiddelde, anders kas.
    for inst in CRYPTO if mix.crypto_weight > 0 else ():
        b = bars.get(inst.ticker)
        half = mix.crypto_weight / len(CRYPTO)
        if b and len(b) >= 200 and b[-1].close > sma([x.close for x in b], 200):
            w[inst.ticker] = half
            notes.append(f"{inst.name}: boven 200-daags gemiddelde, {half:.0%} belegd")
        else:
            notes.append(f"{inst.name}: onder 200-daags gemiddelde of geen data, {half:.0%} in kas")
    return w, notes


class Investor:
    def __init__(self, settings: Settings, provider: DataProvider, mix: Mix = Mix()):
        if not settings.paper_trading:
            raise RuntimeError("De investeerder draait alleen met nepgeld")
        self.s, self.provider, self.mix = settings, provider, mix
        self.path = settings.state_dir / "investeerder.json"
        self.audit = AuditLog(settings.state_dir / "investeerder_audit.jsonl")
        self.kill_switch = KillSwitch(settings.state_dir / "kill_switch.json")
        self.version = investor_version(mix)
        self.regime = UNKNOWN
        self._momentum: dict[str, float] = {}

    def _costs(self, value: float) -> float:
        return max(self.s.commission_min_eur, abs(value) * self.s.commission_pct)

    def run(self, today: date, force_rebalance: bool = False) -> dict:
        book = Book.load(self.path, self.s.starting_cash_eur)
        if not book.equity_history:
            book.equity_history.append({"day": "start", "equity": round(self.s.starting_cash_eur, 2)})
        out = {"day": today.isoformat(), "status": "OK", "actions": [], "notes": [], "warnings": [],
               "version": self.version, "regime": "onbekend", "health": {}}

        try:
            fx = {"EUR": 1.0, "USD": self.provider.usd_to_eur()}
        except DataError as exc:
            out["status"] = "GEEN HANDEL"
            out["warnings"].append(f"wisselkoers ontbreekt: {exc}")
            book.save(self.path)
            return out

        wanted = {i.ticker: i for i in UNIVERSE + CRYPTO}
        bars: dict[str, list[Bar]] = {}
        for t, inst in wanted.items():
            try:
                bars[t] = self.provider.history(inst, HISTORY_DAYS)
            except DataError as exc:
                if t in book.qty:
                    out["warnings"].append(str(exc))
        missing_held = [t for t in book.qty if t not in bars]
        prices = {t: b[-1].close * fx[BY_TICKER[t].currency] for t, b in bars.items()}
        src_issues = getattr(self.provider, "source_issues", lambda t: [])
        stale, stale_warn = stale_issues(bars, today, {t: BY_TICKER[t].region for t in bars})
        out["warnings"] += stale_warn
        suspicious = {t: i for t, i in ((t, (data_issues(b) if BY_TICKER[t].kind != "CRYPTO" else [])
                                         + src_issues(t) + stale.get(t, [])) for t, b in bars.items()) if i}
        for t, issues in suspicious.items():
            out["warnings"].append(f"{t}: verdachte data ({'; '.join(issues)}), niet nieuw gekozen")
        self.regime = market_regime(bars)
        out["regime"] = self.regime.label
        self._momentum = {t: round(b[-22].close / b[-253].close - 1, 4) for t, b in bars.items() if len(b) >= 253}
        bench_eur = prices.get("IWDA.AS") or prices.get("SPY")
        out["health"] = {"gevraagd": len(wanted), "ok": len(bars), "mislukt": len(wanted) - len(bars),
                         "verdacht": suspicious, "wisselkoers": "ok", "regime": out["regime"],
                         "verouderd": len(stale)}
        self.last_bars = bars
        if hasattr(self.provider, "summary"):
            out["health"]["bronnen"] = self.provider.summary()
        if missing_held:
            # Zonder actuele prijs kunnen we niet eerlijk waarderen of herverdelen.
            out["status"] = "GEEN HANDEL"
            out["warnings"].append("geen koers voor: " + ", ".join(missing_held))
            book.save(self.path)
            return out

        equity = book.value(prices)
        month = today.strftime("%Y-%m")
        due = force_rebalance or not book.qty or book.last_rebalance[:7] != month
        if due and self.mix.core_ticker in stale:
            # Herverdelen op verouderde koersen van de kern is niet verstandig: een dag later opnieuw proberen.
            out["warnings"].append(f"Niet herverdeeld: koers van {self.mix.core_ticker} is niet bijgewerkt")
            due = False
        if due:
            try:
                weights, notes = target_weights(bars, self.mix, self.regime, frozenset(suspicious))
                out["notes"] += notes
                self._rebalance(book, weights, prices, equity, today, out)
                book.last_rebalance = today.isoformat()
            except DataError as exc:
                out["warnings"].append(f"niet herverdeeld: {exc}")

        equity = book.value(prices)
        entry = {"day": today.isoformat(), "equity": round(equity, 2)}
        if bench_eur:
            entry["bench"] = round(bench_eur, 4)
        if book.equity_history[-1]["day"] == today.isoformat():
            book.equity_history[-1].update(entry)
        else:
            book.equity_history.append(entry)
        out["equity_eur"] = round(equity, 2)
        out["cash_eur"] = round(book.cash_eur, 2)
        out["weights"] = {t: round(book.qty[t] * prices[t] / equity, 4) for t in book.qty} if equity else {}
        try:
            weights, _ = target_weights(bars, self.mix, self.regime, frozenset(suspicious))
            crypto = [c.ticker for c in CRYPTO]
            picks = [t for t in weights if t not in crypto and t != self.mix.core_ticker]
            view = uitleg.investor_view(bars, self._momentum, set(book.qty), picks, crypto)
            market = uitleg.market_view(bars, self.regime, {t: BY_TICKER[t].region for t in bars})
            nxt = date(today.year + today.month // 12, today.month % 12 + 1, 1).strftime("%Y-%m")
            out["analyse"] = {"markt": market, "beeld": view,
                              "conclusies": uitleg.market_conclusions(market, "investeerder")
                              + uitleg.investor_conclusions(view, f"eerste handelsdag van {nxt}")}
        except Exception as exc:  # noqa: BLE001  (uitleg mag de ronde nooit laten mislukken)
            out["warnings"].append(f"analyse-uitleg mislukt: {type(exc).__name__}: {exc}")
        out["verlies"] = insights.investor_holdings(book, prices)
        out["daling"] = insights.drawdown(book.equity_history)
        book.save(self.path)
        insights.save(self.s.state_dir, "investeerder", {
            "dag": out["day"], "posities": out["verlies"], "daling": out["daling"],
            "conclusies": out.get("analyse", {}).get("conclusies", []),
            "zag": (uitleg.market_lines(out["analyse"]["markt"])
                    + uitleg.investor_lines(out["analyse"]["beeld"], {t: i.name for t, i in BY_TICKER.items()}))
            if out.get("analyse") else [],
            "klaar": uitleg.readiness("investeerder", book.equity_history, []),
            "markt": out.get("analyse", {}).get("markt", {}),
            "beeld": out.get("analyse", {}).get("beeld", {}),
            "volgende_herverdeling": date(today.year + today.month // 12, today.month % 12 + 1, 1).isoformat()})
        self.audit.append("run_finished", ACTOR, {"day": out["day"], "equity_eur": out["equity_eur"],
                                                   "rebalanced": due, "actions": len(out["actions"])})
        return out

    def _rebalance(self, book: Book, weights: dict[str, float], prices: dict[str, float],
                   equity: float, today: date, out: dict) -> None:
        buys_allowed = not self.kill_switch.is_active()
        if not buys_allowed:
            out["warnings"].append("kill switch actief: alleen verkopen")
        threshold = equity * self.mix.min_trade_share
        diffs = {}
        for t in set(book.qty) | set(weights):
            current = book.qty.get(t, 0.0) * prices[t]
            diffs[t] = equity * weights.get(t, 0.0) - current
        # Eerst verkopen (maakt kas vrij), dan kopen.
        for t, diff in sorted(diffs.items(), key=lambda kv: kv[1]):
            if diff >= 0:
                continue
            sell_all = weights.get(t, 0.0) == 0.0
            if not sell_all and -diff < threshold:
                continue
            q_now = book.qty[t]
            q = q_now if sell_all else min(q_now, -diff / prices[t])
            fill = prices[t] * (1 - self.s.slippage)
            value = q * fill
            costs = self._costs(value)
            avg_cost = book.cost_eur[t] / q_now
            pnl = value - avg_cost * q - costs
            book.cash_eur += value - costs
            book.qty[t] = q_now - q
            book.cost_eur[t] -= avg_cost * q
            if book.qty[t] < 1e-9:
                book.qty.pop(t); book.cost_eur.pop(t)
            self._record(book, today, t, "SELL", q, fill, value, costs,
                         "niet meer gekozen" if sell_all else "terug naar doelgewicht", pnl, out)
        if not buys_allowed:
            return
        for t, diff in sorted(diffs.items(), key=lambda kv: -kv[1]):
            if diff < threshold:
                continue
            fill = prices[t] * (1 + self.s.slippage)
            budget = min(diff, book.cash_eur)
            costs = self._costs(budget)
            value = budget - costs
            if value <= 0:
                continue
            q = value / fill
            book.cash_eur -= value + costs
            book.qty[t] = book.qty.get(t, 0.0) + q
            book.cost_eur[t] = book.cost_eur.get(t, 0.0) + value + costs
            self._record(book, today, t, "BUY", q, fill, value, costs,
                         f"doelgewicht {weights.get(t, 0):.0%}", None, out)

    def _record(self, book, today, t, side, q, fill_eur, value, costs, reason, pnl, out):
        ctx = {"momentum_12m": self._momentum.get(t), "soort": BY_TICKER[t].kind if t in BY_TICKER else ""}
        trade = Trade(today.isoformat(), t, side, round(q, 6), round(fill_eur, 4), 1.0,
                      round(value, 2), round(costs, 2), reason, None if pnl is None else round(pnl, 2),
                      strategy="investeerder", version=self.version, regime=self.regime.label, context=ctx)
        book.trades.append(trade)
        self.audit.append("paper_trade", ACTOR, asdict(trade))
        out["actions"].append(f"{side} {q:.4g} x {t} (€{value:,.0f}, {reason})")


def render(out: dict, book: Book) -> str:
    start = book.equity_history[0]["equity"] if book.equity_history else None
    eq = out.get("equity_eur", 0)
    lines = [f"# Investeerder {out['day']}", "",
             "_Oefenportefeuille met nepgeld. Geen beleggingsadvies._", "",
             f"**Status:** {out['status']}  ", f"**Waarde:** €{eq:,.2f}  ",
             f"**Marktregime:** {out.get('regime', 'onbekend')}  ",
             f"**Strategieversie:** {out.get('version', '')}  "]
    src = out.get("health", {}).get("bronnen")
    if src:
        k = src["koersen"]
        lines.append(f"**Koersbronnen:** {k.get('bevestigd', 0)} bevestigd door 2 bronnen, "
                     f"{k.get('1 bron', 0)} uit 1 bron, {k.get('afwijking', 0)} afwijkend; "
                     f"wisselkoers {src['wisselkoers']}  ")
    if start and eq:
        lines.append(f"**Sinds start:** {eq / start - 1:+.2%}  ")
    lines += ["", "## Verdeling", "", "| Instrument | Aandeel |", "| --- | --- |"]
    for t, w in sorted(out.get("weights", {}).items(), key=lambda kv: -kv[1]):
        name = BY_TICKER[t].name if t in BY_TICKER else t
        lines.append(f"| {name} ({t}) | {w:.1%} |")
    if eq:
        lines.append(f"| Kas | {out.get('cash_eur', 0) / eq:.1%} |")
    a = out.get("analyse")
    if a:
        names = {t: i.name for t, i in BY_TICKER.items()}
        lines += ["", "## Analyse van vandaag", "", "**Wat de bot zag**", ""]
        lines += uitleg.market_lines(a["markt"]) + uitleg.investor_lines(a["beeld"], names)
        lines += ["", "**Wat de bot eruit haalt**", ""] + ([f"- {c}" for c in a["conclusies"]] or ["- Niets bijzonders."])
    if out.get("verlies"):
        lines += [""] + insights.render_investor_risk(out["verlies"], out.get("daling", {}))
    lines += ["", "## Vandaag gedaan", ""] + ([f"- {a}" for a in out["actions"]] or ["- Niets (herverdelen gebeurt één keer per maand)"])
    if out["notes"]:
        lines += ["", "## Keuzes", ""] + [f"- {n}" for n in out["notes"]]
    lines += ["", "## Klaar voor echt geld?", ""]
    lines += uitleg.readiness_lines("Investeerder", uitleg.readiness("investeerder", book.equity_history, []))
    if out["warnings"]:
        lines += ["", "## Waarschuwingen", ""] + [f"- {w}" for w in out["warnings"]]
    lines += ["", uitleg.INVESTOR_METHOD]
    return "\n".join(lines) + "\n"
