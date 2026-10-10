"""Leren van eigen resultaten: wat werkte, wat niet, en onder welke omstandigheden.

Uitgangspunten
- Alleen gemeten uitkomsten tellen. Elke afgesloten trade heeft een R-multiple:
  resultaat gedeeld door het risico bij instap. R = +2 betekent: twee keer het
  geriskeerde bedrag verdiend; R = -1: precies het geriskeerde bedrag verloren.
- Groepjes met minder dan MIN_SAMPLE trades worden getoond maar NIET beoordeeld:
  bij zo weinig trades is een verschil meestal toeval.
- Een verschil heet pas een "sterkte" of "zwakte" als het groot genoeg is én
  statistisch overtuigend (t-waarde boven 2). Ook dan is het een HYPOTHESE: die
  moet eerst in het onderzoek op ongeziene data worden getest voordat er een
  regel verandert. Deze module verandert zelf nooit iets.
- Drift: presteert de strategie live duidelijk slechter dan in de backtest, dan
  meldt het rapport dat. Mogelijk zijn de marktomstandigheden veranderd.
"""

from __future__ import annotations

import math
import statistics
from dataclasses import dataclass

MIN_SAMPLE = 20
MIN_EFFECT_R = 0.15
T_THRESHOLD = 2.0


@dataclass
class Stats:
    n: int
    win_rate: float
    avg_r: float
    median_r: float
    sd_r: float
    pnl: float
    avg_hold: float

    @property
    def stderr(self) -> float:
        return self.sd_r / math.sqrt(self.n) if self.n > 1 else float("inf")


def closed(trades) -> list:
    return [t for t in trades if t.side == "SELL" and t.r_multiple is not None]


def stats(trades) -> Stats | None:
    if not trades:
        return None
    rs = [t.r_multiple for t in trades]
    return Stats(
        n=len(rs),
        win_rate=sum(r > 0 for r in rs) / len(rs),
        avg_r=statistics.fmean(rs),
        median_r=statistics.median(rs),
        sd_r=statistics.stdev(rs) if len(rs) > 1 else 0.0,
        pnl=sum(t.pnl_eur or 0 for t in trades),
        avg_hold=statistics.fmean(t.hold_days or 0 for t in trades),
    )


def _entry(t) -> dict:
    return (t.context or {}).get("instap", {}) or {}


def _bucket(value, edges: list[float], labels: list[str]) -> str:
    if value is None:
        return "onbekend"
    for edge, label in zip(edges, labels):
        if value < edge:
            return label
    return labels[-1]


# Elke dimensie: naam -> functie die een trade in een groepje plaatst.
DIMENSIONS = {
    "Markttrend bij instap": lambda t: _entry(t).get("trend_regime", "onbekend"),
    "Marktbeweeglijkheid bij instap": lambda t: _entry(t).get("beweeglijkheid_regime", "onbekend"),
    "RSI bij instap": lambda t: _bucket(_entry(t).get("rsi14"), [50, 60, 70, 80],
                                        ["onder 50", "50-60", "60-70", "70-80", "80 of hoger"]),
    "MACD-histogram bij instap": lambda t: ("onbekend" if _entry(t).get("macd_hist_pct") is None
                                            else "positief" if _entry(t)["macd_hist_pct"] >= 0 else "negatief"),
    "Volume t.o.v. normaal": lambda t: _bucket(_entry(t).get("volume_rel"), [0.9, 1.1],
                                               ["lager (<0,9)", "normaal", "hoger (>1,1)"]),
    "Afstand tot SMA200": lambda t: _bucket(_entry(t).get("afstand_sma200_pct"), [10, 25],
                                            ["tot 10%", "10-25%", "meer dan 25%"]),
    "Beweeglijkheid aandeel (ATR%)": lambda t: _bucket(_entry(t).get("atr_pct"), [1.5, 3.0],
                                                      ["rustig (<1,5%)", "normaal", "wild (>3%)"]),
    "Uitstapreden": lambda t: t.reason,
    "Houdduur": lambda t: _bucket(t.hold_days, [10, 30], ["kort (<10 d)", "middel", "lang (>30 d)"]),
    "Strategieversie": lambda t: t.version or "onbekend",
}

# Deze dimensies zijn UITKOMSTEN (pas bekend na de trade), geen voorspellers bij instap.
# Ze staan in de tabellen ter informatie, maar leveren nooit een "sterkte" of "zwakte" op:
# dat winnaars langer worden vastgehouden is een gevolg van de regels, geen les.
OUTCOME_DIMENSIONS = {"Uitstapreden", "Houdduur", "Strategieversie"}

# Welke instelling past bij welke dimensie (voor de suggestie wat te testen).
KNOBS = {
    "Markttrend bij instap": "regime_filter",
    "Marktbeweeglijkheid bij instap": "regime_filter",
    "RSI bij instap": "max_rsi_entry",
}


@dataclass
class Finding:
    dimension: str
    group: str
    kind: str          # "sterkte" of "zwakte"
    stats: Stats
    diff_r: float
    t_value: float

    def text(self) -> str:
        knob = KNOBS.get(self.dimension)
        hint = f" Te testen via instelling `{knob}`." if knob else ""
        return (f"{self.kind.capitalize()}: {self.dimension} = {self.group}: gemiddeld {self.stats.avg_r:+.2f} R "
                f"over {self.stats.n} trades ({self.diff_r:+.2f} R t.o.v. de rest, t = {self.t_value:.1f}).{hint}")


def analyse(trades) -> tuple[Stats | None, dict[str, list[tuple[str, Stats]]], list[Finding]]:
    """Geeft (totaal, per dimensie de groepjes, bevindingen)."""
    done = closed(trades)
    total = stats(done)
    tables: dict[str, list[tuple[str, Stats]]] = {}
    findings: list[Finding] = []
    for dim, fn in DIMENSIONS.items():
        groups: dict[str, list] = {}
        for t in done:
            groups.setdefault(str(fn(t)), []).append(t)
        rows = [(g, stats(ts)) for g, ts in groups.items()]
        rows.sort(key=lambda r: -r[1].n)
        tables[dim] = rows
        if dim in OUTCOME_DIMENSIONS or len(groups) < 2:
            continue
        for g, ts in groups.items():
            if g == "onbekend" or len(ts) < MIN_SAMPLE:
                continue
            rest = [t for t in done if str(fn(t)) != g]
            if len(rest) < MIN_SAMPLE:
                continue
            a, b = stats(ts), stats(rest)
            se = math.sqrt(a.stderr ** 2 + b.stderr ** 2)
            diff = a.avg_r - b.avg_r
            tv = diff / se if se > 0 else 0.0
            if abs(diff) >= MIN_EFFECT_R and abs(tv) >= T_THRESHOLD:
                findings.append(Finding(dim, g, "sterkte" if diff > 0 else "zwakte", a, diff, tv))
    findings.sort(key=lambda f: -abs(f.t_value))
    return total, tables, findings


def drift(live, reference) -> str | None:
    """Vergelijkt live trades met de backtest. Geeft een waarschuwing of None."""
    lv, ref = stats(closed(live)), stats(closed(reference))
    if not lv or not ref:
        return None
    if lv.n < MIN_SAMPLE:
        return (f"Live pas {lv.n} afgesloten trades (gemiddeld {lv.avg_r:+.2f} R); vanaf {MIN_SAMPLE} trades "
                f"is een vergelijking met de backtest ({ref.avg_r:+.2f} R) zinvol.")
    low = ref.avg_r - 2 * lv.sd_r / math.sqrt(lv.n)
    if lv.avg_r < low:
        return (f"LET OP: live gemiddeld {lv.avg_r:+.2f} R over {lv.n} trades, duidelijk slechter dan de backtest "
                f"({ref.avg_r:+.2f} R). Mogelijk zijn de marktomstandigheden veranderd; overweeg de agent te pauzeren.")
    return f"Live ({lv.avg_r:+.2f} R over {lv.n} trades) ligt in lijn met de backtest ({ref.avg_r:+.2f} R)."


def vs_benchmark(equity_history: list[dict]) -> dict | None:
    """Live rendement van de bot tegenover de vergelijkings-ETF over dezelfde dagen."""
    pts = [e for e in equity_history if "bench" in e and e.get("day") != "start"]
    if len(pts) < 2:
        return None
    bot = pts[-1]["equity"] / pts[0]["equity"] - 1
    bench = pts[-1]["bench"] / pts[0]["bench"] - 1
    return {"van": pts[0]["day"], "tot": pts[-1]["day"], "dagen": len(pts), "bot": bot, "etf": bench,
            "verschil": bot - bench}


def render(title: str, trades, reference=None, equity_history=None) -> str:
    total, tables, findings = analyse(trades)
    lines = [f"## {title}", ""]
    if equity_history:
        vb = vs_benchmark(equity_history)
        if vb:
            lines.append(f"Live van {vb['van']} t/m {vb['tot']} ({vb['dagen']} handelsdagen): bot {vb['bot']:+.2%}, "
                         f"wereld-ETF {vb['etf']:+.2%}, verschil {vb['verschil']:+.2%}.")
            lines.append("")
    if reference is not None:
        d = drift(trades, reference)
        if d:
            lines += [d, ""]
    if not total:
        lines.append("Nog geen afgesloten trades om van te leren.")
        return "\n".join(lines) + "\n"
    lines += [f"{total.n} afgesloten trades, {total.win_rate:.0%} winst, gemiddeld {total.avg_r:+.2f} R per trade "
              f"(mediaan {total.median_r:+.2f} R), totaal €{total.pnl:,.0f}, gemiddeld {total.avg_hold:.0f} dagen vastgehouden.",
              ""]
    lines += ["### Bevindingen", ""]
    if findings:
        lines += [f"- {f.text()}" for f in findings[:8]]
        lines += ["", "_Dit zijn hypotheses. Een regel verandert pas na een test op ongeziene data (zie het onderzoeksrapport)._"]
    else:
        lines.append(f"- Geen overtuigende verschillen (minimaal {MIN_SAMPLE} trades per groep, "
                     f"verschil ≥ {MIN_EFFECT_R} R en t ≥ {T_THRESHOLD}).")
    for dim, rows in tables.items():
        note = " (uitkomst, ter informatie)" if dim in OUTCOME_DIMENSIONS else ""
        lines += ["", f"### {dim}{note}", "", "| Groep | Trades | Winst | Gem. R | Totaal € |", "| --- | --- | --- | --- | --- |"]
        for g, st in rows:
            flag = "" if st.n >= MIN_SAMPLE else " (te weinig)"
            lines.append(f"| {g}{flag} | {st.n} | {st.win_rate:.0%} | {st.avg_r:+.2f} | {st.pnl:,.0f} |")
    return "\n".join(lines) + "\n"
