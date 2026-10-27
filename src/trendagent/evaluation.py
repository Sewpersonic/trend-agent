"""Evaluatie: is een variant van de strategie aantoonbaar beter dan productie?

Werkwijze
1. Elke variant draait over dezelfde jaren met echte koersen, dag voor dag, zonder
   blik in de toekomst (zelfde backtest-machine als altijd).
2. De periode wordt verdeeld in:
   - ontwikkeldeel: de eerste 70% van de dagen;
   - holdout: de laatste 30%, als "ongeziene" toets;
   - 5 opeenvolgende blokken (folds) om te zien of een voordeel in ELKE periode
     terugkomt, of alleen in één toevallig gunstige periode.
3. Kostenstress: dezelfde test met dubbele kosten en dubbele slippage.
4. Per marktregime: hoe deed de strategie het in stijgende, dalende en
   zijwaartse markten, en bij hoge of lage beweeglijkheid?
5. Walk-forward selectie: stel dat de bot zelf elke periode de variant kiest die
   tot dan toe het best was. Werkt dat beter dan gewoon productie houden?
   Zo niet, dan is automatisch bijsturen op basis van het verleden niet zinvol.

Acceptatiepoort (alle punten moeten kloppen, anders "NIET AANBEVOLEN"):
  a. holdout: Sharpe minstens 0,10 hoger dan productie;
  b. ontwikkeldeel: niet slechter dan productie;
  c. in minstens 60% van de folds beter dan productie;
  d. grootste daling (hele periode) hooguit 2 procentpunt dieper;
  e. met dubbele kosten nog steeds minstens zo goed als productie;
  f. (trend-agent) minstens 30 afgesloten trades, anders te weinig bewijs.

Er worden bewust maar een paar varianten getest: hoe meer je probeert, hoe
groter de kans dat er één toevallig goed uitkomt (overfitting).
De uitkomst is altijd een aanbeveling. Productie verandert alleen als een mens
de instelling aanpast.
"""

from __future__ import annotations

import math
import statistics
from dataclasses import dataclass, field, replace
from datetime import date

from .backtest import (
    HistoricalProvider,
    max_drawdown,
    run_backtest,
    run_investor_backtest,
    trade_stats,
)
from .core.config import Settings
from .features import market_regime
from .universe import BY_TICKER

FOLDS = 5
HOLDOUT_SHARE = 0.30
MIN_SHARPE_GAIN = 0.10
MAX_EXTRA_DD = 0.02
MIN_FOLD_WIN_SHARE = 0.60
MIN_TRADES = 30

TREND_VARIANTS: dict[str, dict] = {
    "productie": {},
    "rem-pas-na-5-verliezen": {"max_consecutive_losses": 5},
    "regimefilter": {"regime_filter": True},
    "niet-kopen-boven-rsi-75": {"max_rsi_entry": 75.0},
    # Patronen uit de grafieken, getoetst als regels:
    "koop-na-terugval": {"entry_filter": "terugval"},
    "koop-bij-nieuwe-top": {"entry_filter": "uitbraak"},
    "verkoop-na-2-rode-trendkaarsen": {"ha_exit": True},
    # Meer tegelijk vasthouden (nu staat het meeste geld stil als 3 plekken bezet zijn); risico per aankoop blijft gelijk.
    "4-plekken": {"max_positions": 4},
    "5-plekken": {"max_positions": 5, "max_open_risk": 0.0125},
}

# In gewone taal: wat elke variant test.
UITLEG = {
    "productie": "De huidige regels van de bot.",
    "rem-pas-na-5-verliezen": "Noodstop pas na 5 verliestrades op rij in plaats van 3.",
    "regimefilter": "Niets nieuws kopen als de hele markt daalt of erg onrustig is.",
    "niet-kopen-boven-rsi-75": "Niet kopen als een aandeel net heel snel is gestegen (RSI boven 75).",
    "koop-na-terugval": "Patroon: alleen kopen na een terugval in de laatste week (kopen in de dip).",
    "koop-bij-nieuwe-top": "Patroon: alleen kopen als het aandeel een nieuwe 3-maands top maakt (uitbraak).",
    "verkoop-na-2-rode-trendkaarsen": "Patroon: ook verkopen zodra er 2 rode trendkaarsen op rij komen.",
    "4-plekken": "4 aandelen tegelijk in plaats van 3 (zelfde risico per aankoop).",
    "5-plekken": "5 aandelen tegelijk in plaats van 3 (zelfde risico per aankoop).",
    "satelliet-3-aandelen": "Investeerder: 3 in plaats van 5 sterke aandelen.",
}

# Wijzigingen ten opzichte van de huidige productie-instellingen.
INVESTOR_VARIANTS: dict[str, dict] = {
    "productie": {},
    "regimefilter": {"regime_filter": True},
    "satelliet-3-aandelen": {"satellite_count": 3},
}


# --------------------------------------------------------------- metingen

def sharpe(series: list[tuple[date, float]]) -> float:
    if len(series) < 3:
        return 0.0
    r = [series[i][1] / series[i - 1][1] - 1 for i in range(1, len(series))]
    sd = statistics.pstdev(r)
    return statistics.fmean(r) / sd * math.sqrt(252) if sd > 0 else 0.0


def total_return(series) -> float:
    return series[-1][1] / series[0][1] - 1 if len(series) >= 2 else 0.0


def slice_series(series, start: date, end: date):
    return [(d, v) for d, v in series if start <= d <= end]


@dataclass
class VariantResult:
    name: str
    params: dict
    equity: list
    trades: list
    stressed: list = field(default_factory=list)   # equity met dubbele kosten


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


@dataclass
class Verdict:
    variant: str
    accepted: bool
    checks: list[Check]


# ------------------------------------------------------------- uitvoeren

def run_variants(kind: str, base: Settings, provider: HistoricalProvider, start: date, end: date) -> list[VariantResult]:
    stressed_settings = replace(base, slippage=base.slippage * 2, commission_pct=base.commission_pct * 2,
                                commission_min_eur=base.commission_min_eur * 2)
    out = []
    if kind == "trend":
        for name, overrides in TREND_VARIANTS.items():
            if name != "productie" and all(getattr(base, k) == v for k, v in overrides.items()):
                continue    # zit al in productie: niets te vergelijken
            s = replace(base, **overrides)
            r = run_backtest(s, provider, start, end)
            st = run_backtest(replace(stressed_settings, **overrides), provider, start, end)
            out.append(VariantResult(name, overrides, r.equity, r.trades, st.equity))
    else:
        from .strategies import production_mix
        prod_mix = production_mix()
        for name, overrides in INVESTOR_VARIANTS.items():
            if name != "productie" and all(getattr(prod_mix, k) == v for k, v in overrides.items()):
                continue
            mix = replace(prod_mix, **overrides)
            r = run_investor_backtest(base, provider, start, end, mix=mix)
            st = run_investor_backtest(stressed_settings, provider, start, end, mix=mix)
            out.append(VariantResult(name, overrides, r.equity, r.trades, st.equity))
    return out


def periods(days: list[date]) -> tuple[tuple[date, date], tuple[date, date], list[tuple[date, date]]]:
    cut = int(len(days) * (1 - HOLDOUT_SHARE))
    dev, hold = (days[0], days[cut - 1]), (days[cut], days[-1])
    size = len(days) // FOLDS
    folds = [(days[i * size], days[min((i + 1) * size, len(days)) - 1]) for i in range(FOLDS)]
    return dev, hold, folds


def judge(prod: VariantResult, cand: VariantResult, days: list[date], kind: str) -> Verdict:
    dev, hold, folds = periods(days)
    checks = []
    sp_h, sc_h = sharpe(slice_series(prod.equity, *hold)), sharpe(slice_series(cand.equity, *hold))
    checks.append(Check("Holdout (ongeziene laatste 30%)", sc_h >= sp_h + MIN_SHARPE_GAIN,
                        f"Sharpe {sc_h:.2f} vs productie {sp_h:.2f} (nodig: +{MIN_SHARPE_GAIN:.2f})"))
    sp_d, sc_d = sharpe(slice_series(prod.equity, *dev)), sharpe(slice_series(cand.equity, *dev))
    checks.append(Check("Ontwikkeldeel (eerste 70%)", sc_d >= sp_d, f"Sharpe {sc_d:.2f} vs {sp_d:.2f}"))
    wins = sum(sharpe(slice_series(cand.equity, a, b)) > sharpe(slice_series(prod.equity, a, b)) for a, b in folds)
    checks.append(Check("Consistent over periodes", wins / len(folds) >= MIN_FOLD_WIN_SHARE,
                        f"beter in {wins} van {len(folds)} periodes (nodig: {MIN_FOLD_WIN_SHARE:.0%})"))
    dd_p, dd_c = max_drawdown(prod.equity), max_drawdown(cand.equity)
    checks.append(Check("Grootste daling", dd_c >= dd_p - MAX_EXTRA_DD, f"{dd_c:.1%} vs {dd_p:.1%}"))
    ss_p, ss_c = sharpe(prod.stressed), sharpe(cand.stressed)
    checks.append(Check("Dubbele kosten en slippage", ss_c >= ss_p, f"Sharpe {ss_c:.2f} vs {ss_p:.2f}"))
    if kind == "trend":
        n = trade_stats(cand.trades)["closed"]
        checks.append(Check("Genoeg trades", n >= MIN_TRADES, f"{n} afgesloten trades (nodig: {MIN_TRADES})"))
    return Verdict(cand.name, all(c.ok for c in checks), checks)


def walk_forward_selection(results: list[VariantResult], days: list[date]) -> dict:
    """Kiest per periode de variant die tot dan toe de hoogste Sharpe had, en meet hoe dat uitpakt."""
    _, _, folds = periods(days)
    chosen, sel_rets, prod_rets = [], [], []
    prod = next(r for r in results if r.name == "productie")
    for k in range(1, len(folds)):
        past = (folds[0][0], folds[k - 1][1])
        best = max(results, key=lambda r: sharpe(slice_series(r.equity, *past)))
        chosen.append(best.name)
        sel_rets.append(total_return(slice_series(best.equity, *folds[k])))
        prod_rets.append(total_return(slice_series(prod.equity, *folds[k])))
    sel = math.prod(1 + r for r in sel_rets) - 1
    prd = math.prod(1 + r for r in prod_rets) - 1
    return {"gekozen": chosen, "selectie": sel, "productie": prd}


def regime_breakdown(results: list[VariantResult], provider: HistoricalProvider, days: list[date]) -> dict:
    """Gemiddeld rendement per dag, gegroepeerd naar het regime van de VORIGE slotkoers (geen look-ahead)."""
    labels = {}
    bench = BY_TICKER["IWDA.AS"] if "IWDA.AS" in provider._bars else BY_TICKER["SPY"]
    for d in days:
        provider.set_day(d)
        try:
            labels[d] = market_regime({bench.ticker: provider.history(bench, 260)}).label
        except Exception:  # noqa: BLE001
            labels[d] = "onbekend"
    out: dict[str, dict[str, tuple[float, int]]] = {}
    for r in results:
        eq = dict(r.equity)
        groups: dict[str, list[float]] = {}
        for prev, cur in zip(days, days[1:]):
            if prev in eq and cur in eq:
                groups.setdefault(labels[prev], []).append(eq[cur] / eq[prev] - 1)
        out[r.name] = {g: (statistics.fmean(v) * 252, len(v)) for g, v in groups.items()}
    return out


# ---------------------------------------------------------------- rapport

def metrics_row(r: VariantResult, days: list[date]) -> dict:
    dev, hold, _ = periods(days)
    ts = trade_stats(r.trades)
    years = (r.equity[-1][0] - r.equity[0][0]).days / 365.25 if len(r.equity) > 1 else 1
    tot = total_return(r.equity)
    return {
        "totaal": tot,
        "per_jaar": (1 + tot) ** (1 / max(years, 1e-9)) - 1 if tot > -1 else -1,
        "max_daling": max_drawdown(r.equity),
        "sharpe": sharpe(r.equity),
        "sharpe_holdout": sharpe(slice_series(r.equity, *hold)),
        "sharpe_dubbele_kosten": sharpe(r.stressed),
        "trades": ts["closed"],
        "winst_pct": ts["win_rate"],
        "winst_verlies": ts["avg_win"] / -ts["avg_loss"] if ts["avg_loss"] < 0 else float("nan"),
        "profit_factor": ts["profit_factor"],
    }


def render(kind: str, results: list[VariantResult], provider: HistoricalProvider) -> tuple[str, list[Verdict]]:
    days = [d for d, _ in next(r for r in results if r.name == "productie").equity]
    dev, hold, folds = periods(days)
    prod = next(r for r in results if r.name == "productie")
    verdicts = [judge(prod, r, days, kind) for r in results if r.name != "productie"]
    title = "Trend-agent" if kind == "trend" else "Investeerder"
    lines = [f"## {title}", "",
             f"Periode {days[0]} t/m {days[-1]}. Ontwikkeldeel {dev[0]} t/m {dev[1]}, holdout {hold[0]} t/m {hold[1]}. "
             f"{len(results) - 1} varianten getest tegen productie.", ""]
    lines += ["### Uitkomst", ""]
    for v in verdicts:
        lines.append(f"- **{v.variant}: {'AANBEVOLEN' if v.accepted else 'NIET AANBEVOLEN'}**")
        for c in v.checks:
            lines.append(f"    - {'✓' if c.ok else '✗'} {c.name}: {c.detail}")
    if not any(v.accepted for v in verdicts):
        lines += ["", "Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is."]
    lines += ["", "### Cijfers per variant (hele periode, na kosten)", "",
              "| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for r in results:
        m = metrics_row(r, days)
        wl = "–" if math.isnan(m["winst_verlies"]) else f"{m['winst_verlies']:.2f}"
        lines.append(f"| {r.name} | {m['totaal']:+.1%} | {m['per_jaar']:+.1%} | {m['max_daling']:.1%} | {m['sharpe']:.2f} | "
                     f"{m['sharpe_holdout']:.2f} | {m['sharpe_dubbele_kosten']:.2f} | {m['trades']} | {m['winst_pct']:.0%} | {wl} |")
    lines += ["", "### Per periode (rendement)", "",
              "| Variant | " + " | ".join(f"{a:%b %Y}–{b:%b %Y}" for a, b in folds) + " |",
              "| --- | " + " | ".join("---" for _ in folds) + " |"]
    for r in results:
        lines.append(f"| {r.name} | " + " | ".join(f"{total_return(slice_series(r.equity, a, b)):+.1%}" for a, b in folds) + " |")
    wf = walk_forward_selection(results, days)
    lines += ["", "### Zelf bijsturen op basis van het verleden?", "",
              f"Als de bot elke periode de variant had gekozen die tot dan toe het best was ({', '.join(wf['gekozen'])}), "
              f"was het resultaat over de laatste {FOLDS - 1} periodes {wf['selectie']:+.1%}, tegen {wf['productie']:+.1%} "
              f"voor gewoon productie houden. "
              + ("Automatisch bijsturen voegde hier dus niets toe." if wf["selectie"] <= wf["productie"]
                 else "Bijsturen hielp hier, maar met zo weinig periodes kan dat toeval zijn.")]
    rb = regime_breakdown(results, provider, days)
    regimes = sorted({g for v in rb.values() for g in v})
    lines += ["", "### Per marktregime (gemiddeld rendement op jaarbasis)", "",
              "| Variant | " + " | ".join(regimes) + " |", "| --- | " + " | ".join("---" for _ in regimes) + " |"]
    for name, groups in rb.items():
        lines.append(f"| {name} | " + " | ".join(
            f"{groups[g][0]:+.0%} ({groups[g][1]} d)" if g in groups else "–" for g in regimes) + " |")
    return "\n".join(lines) + "\n", verdicts
