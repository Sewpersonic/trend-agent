"""Test van de daytrade-bot op de koersen per 5 minuten: de laatste ~60 beursdagen van Yahoo plus het eigen archief
(daytrade_archief.py), dat elke week groeit.

Schrijft backtest/daytrade/RAPPORT.md, resultaat.json en trades.csv. Verandert niets aan de bots.
"""

from __future__ import annotations

import csv
import json
import time as _time
from datetime import datetime, timezone
from pathlib import Path

from .daytrader import NY, Bar5, Params, backtest, split_days, variant
from .universe import UNIVERSE

TICKERS = [i.ticker for i in UNIVERSE if i.region == "US"]


def download(tickers=TICKERS, period: str = "60d") -> dict[str, list[Bar5]]:
    import yfinance as yf
    out: dict[str, list[Bar5]] = {}
    for tk in tickers:
        for _poging in range(3):
            try:
                df = yf.Ticker(tk).history(period=period, interval="5m", auto_adjust=False, prepost=False)
                break
            except Exception:  # noqa: BLE001
                df = None
                _time.sleep(5)
        if df is None or df.empty:
            continue
        bars = []
        for idx, r in df.iterrows():
            if r["Close"] != r["Close"]:
                continue
            t = idx.to_pydatetime()
            if NY is not None and t.tzinfo is not None:
                t = t.astimezone(NY)
            bars.append(Bar5(t, float(r["Open"]), float(r["High"]), float(r["Low"]), float(r["Close"]), float(r["Volume"])))
        out[tk] = drop_unfinished_day(bars)
        _time.sleep(0.5)
    return out


def drop_unfinished_day(bars: list[Bar5]) -> list[Bar5]:
    """Een dag die nog bezig is (laatste blok vóór 15:55) telt niet mee."""
    if not bars:
        return bars
    last = bars[-1]
    if last.t.time() < datetime.strptime("15:55", "%H:%M").time():
        d = last.t.date()
        return [b for b in bars if b.t.date() != d]
    return bars


def baselines(data: dict[str, list[Bar5]], first_day: str, start: float = 10_000.0, slip: float = 0.0005) -> dict:
    spy = split_days(data.get("SPY", []))
    days = sorted(d for d in spy if d.isoformat() >= first_day)
    if not days:
        return {}
    hold = spy[days[-1]][-1].c / spy[days[0]][0].o - 1
    eq = start
    for d in days:
        bs = spy[d]
        uit = next((b.o for b in bs if b.t.strftime("%H:%M") >= "15:45"), bs[-1].c)
        eq *= (uit * (1 - slip)) / (bs[0].o * (1 + slip))
    return {"spy_vasthouden": round(hold, 4), "spy_elke_dag_in_en_uit": round(eq / start - 1, 4)}


VARIANTEN = {
    "basis": {},
    "alleen als de daggrafiek van het aandeel stijgt": {"dagtrend_filter": True},
    "niet als de daggrafiek van de markt daalt": {"markt_trend_filter": True},
    "zonder winstdoel (alleen stop of einde dag)": {"use_target": False},
    "zonder marktfilter": {"market_filter": False},
    "openingsrange 15 minuten": {"or_min": 15},
    "minder streng op volume (1,0x)": {"min_rvol": 1.0},
}


def download_daily(tickers=TICKERS) -> dict:
    """Dagkoersen van ongeveer een jaar extra (voor de daggrafiek: 50- en 200-daags gemiddelde)."""
    from .data import YahooProvider
    from .universe import BY_TICKER
    yp = YahooProvider()
    out = {}
    for tk in tickers:
        try:
            out[tk] = yp.history(BY_TICKER[tk], 600)   # ook voor oudere dagen uit het archief
        except Exception:  # noqa: BLE001 - zonder daggrafiek telt dit aandeel als 'onbekend'
            continue
    return out


def run(out_dir: Path = Path("backtest/daytrade"), data: dict[str, list[Bar5]] | None = None,
        daily: dict | None = None, base: Params | None = None) -> dict:
    from .daytrade_leren import leer, samenvatting
    if data is None:
        # Nieuwe koersen bewaren en aanvullen met het archief van eerdere weken (zo groeit de testperiode).
        from . import daytrade_archief
        nieuw = download()
        daytrade_archief.bewaar(nieuw)
        data = daytrade_archief.samen(daytrade_archief.laad(), nieuw)
        daily = download_daily() if daily is None else daily
    out_dir.mkdir(parents=True, exist_ok=True)
    base = base or Params()
    res = {naam: backtest(data, variant(base, **kw), daily=daily) for naam, kw in VARIANTEN.items()}
    b = res["basis"]
    first = b["curve"][0][0] if b["curve"] else ""
    last = b["curve"][-1][0] if b["curve"] else ""
    bl = baselines(data, first)
    summary = {"gemaakt": datetime.now(timezone.utc).isoformat(timespec="seconds"), "van": first, "tot": last,
               "aandelen": sorted(data), "vergelijk": bl,
               "varianten": {k: {"stats": v["stats"], "eind": v["eind"]} for k, v in res.items()},
               "basis_dagen": b["dagen"], "basis_curve": b["curve"],
               "regels": {k: v for k, v in b["params"].items() if k in ("dagtrend_filter", "markt_trend_filter")}}
    geleerd = leer(b["trades"])
    summary["leren"] = geleerd
    summary["lessen"] = samenvatting(geleerd, "Test op oude koersen")
    summary["voorstel"] = voorstel(summary)
    # Indicatie per kans: alle uitbraken uit de koersgeschiedenis, met hoe ze afliepen
    from .daytrade_indicatie import samenvoegen, tabel, toets, uitbraken, zin
    # Yahoo geeft maar ~60 dagen 5-minutenkoersen; door eerdere uitbraken te bewaren groeit de ervaring elke week.
    archief = out_dir / "uitbraken.json"
    try:
        oud = json.loads(archief.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        oud = []
    events = samenvoegen(oud, uitbraken(data, base, daily))
    archief.write_text(json.dumps(events, ensure_ascii=False), encoding="utf-8")
    ts = toets(events)
    summary["indicatie"] = {"uitbraken": len(events), "toets": ts, "zin": zin(ts)}
    (out_dir / "indicatie.json").write_text(json.dumps({"gemaakt": summary["gemaakt"], "uitbraken": len(events),
                                                        "tabel": tabel(events), "toets": ts, "zin": zin(ts)},
                                                       ensure_ascii=False, indent=1), encoding="utf-8")
    (out_dir / "resultaat.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    with (out_dir / "trades.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        cols = ["dag", "ticker", "qty", "instap", "uitstap", "t_in", "t_uit", "reden", "resultaat", "r"]
        w.writerow(cols)
        for t in b["trades"]:
            w.writerow([t[c] for c in cols])
    (out_dir / "RAPPORT.md").write_text(rapport(summary), encoding="utf-8")
    return summary


def voorstel(s: dict) -> dict | None:
    """Werkt een regel uit de grafiekanalyse duidelijk beter dan de huidige regels? Dan een voorstel (jij beslist).
    Duidelijk = hoger rendement, hogere gemiddelde R, niet veel diepere daling, en nog genoeg trades."""
    v = s["varianten"]
    b = v["basis"]["stats"]
    beste = None
    for naam in ("alleen als de daggrafiek van het aandeel stijgt", "niet als de daggrafiek van de markt daalt"):
        x = (v.get(naam) or {}).get("stats")
        if not x or not x["trades"] or x["gem_r"] is None or b["gem_r"] is None:
            continue
        if (x["trades"] >= max(15, b["trades"] * 0.5) and x["gem_r"] >= b["gem_r"] + 0.1
                and x["rendement"] > b["rendement"] and x["max_daling"] >= b["max_daling"] - 0.01):
            if not beste or x["gem_r"] > beste[1]["gem_r"]:
                beste = (naam, x)
    if not beste:
        return None
    return {"naam": beste[0], "gem_r": beste[1]["gem_r"], "rendement": beste[1]["rendement"], "trades": beste[1]["trades"],
            "tekst": f"Op de oude koersen werkte '{beste[0]}' beter dan de huidige regels. Dat is nog geen bewijs "
                     "(korte periode). Wil je het proberen? Zeg het, dan zet ik het aan; de bot doet dat nooit zelf."}


def _p(x) -> str:
    return "–" if x is None else f"{x * 100:+.1f}%".replace(".", ",")


def rapport(s: dict) -> str:
    v = s["varianten"]
    b = v["basis"]["stats"]
    L = ["# Test daytrade-bot (nepgeld)", "",
         f"Periode: {s['van']} t/m {s['tot']} ({b['dagen']} beursdagen; de eerste 10 dagen daarvoor dienden alleen om "
         "'normaal volume' te leren). Startbedrag 10.000 nepgeld. Kosten: geen commissie, wel 0,05% slippage per kant.", "",
         "Belangrijk: dit zijn maar ongeveer 2 maanden. Dat is te kort om iets te bewijzen; het zegt alleen of de regels "
         "in deze periode zinnig werkten. Het echte bewijs moet uit het oefenen komen.", "",
         "## Uitkomst van de regels", "",
         "| Variant | Rendement | Trades | Winst-% | Gem. R | Grootste daling |", "|---|---|---|---|---|---|"]
    for naam, x in v.items():
        st = x["stats"]
        L.append(f"| {naam} | {_p(st['rendement'])} | {st['trades']} | "
                 f"{'–' if st['winst_pct'] is None else str(round(st['winst_pct'] * 100)) + '%'} | "
                 f"{'–' if st['gem_r'] is None else str(st['gem_r']).replace('.', ',')} | {_p(st['max_daling'])} |")
    c = s.get("vergelijk") or {}
    L += ["", "## Ter vergelijking", "",
          f"- S&P 500 (SPY) de hele periode vasthouden: {_p(c.get('spy_vasthouden'))}",
          f"- SPY elke dag bij de opening kopen en om 15:45 verkopen: {_p(c.get('spy_elke_dag_in_en_uit'))}", "",
          "## Hoe de basisregels eindigden", "",
          f"- Gestopt door stop-loss: {b['redenen'].get('stop-loss', 0)}",
          f"- Winstdoel gehaald: {b['redenen'].get('winstdoel', 0)}",
          f"- Verkocht aan het einde van de dag: {b['redenen'].get('einde van de dag', 0)}",
          f"- Dagen met minstens één trade: {b['dagen_met_trade']} van {b['dagen']}", "",
          "## Indicatie per kans", "",
          f"Uit {(s.get('indicatie') or {}).get('uitbraken', 0)} uitbraken in de koersgeschiedenis (ook die de bot niet kocht). "
          + (s.get("indicatie") or {}).get("zin", ""), "",
          "## Wat leert hij van de grafieken?", ""] + [f"- {z}" for z in s.get("lessen", [])] + (
          ["", f"**Voorstel:** {s['voorstel']['tekst']}"] if s.get("voorstel") else []) + ["",
          "Gem. R: gemiddelde winst of verlies per trade, gemeten in 'risico-eenheden' (1 R = het bedrag dat hij "
          "verliest als de stop-loss geraakt wordt). Boven 0 betekent: de winsten wogen zwaarder dan de verliezen.", ""]
    return "\n".join(L)
