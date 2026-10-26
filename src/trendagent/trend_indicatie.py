"""Indicatie per kans voor de trend-agent (en dus het oefenaccount): hoe liepen vergelijkbare koopsignalen eerder af?

Zelfde idee als bij de daytrader (daytrade_indicatie.py), maar dan op dagkoersen van de afgelopen jaren:

1. signalen(): loopt alle aandelen van de bot dag voor dag na en noteert elk NIEUW koopsignaal volgens zijn eigen regels
   (stijgende trend, 1 en 3 maanden omhoog, genoeg handel, RSI-grens), ook als hij geen plek vrij had.
   Per signaal: de situatie (instapmoment, RSI, markt, afstand tot het 200-daags gemiddelde, ...) en de uitkomst als
   je toen had gekocht met zijn gewone uitstapregels (beginstop, meeschuivende stop, verkopen onder het 50-daags
   gemiddelde), in R: 1 R = het verlies als de beginstop geraakt wordt.
2. Daaruit een tabel per kenmerk, een label per kans (gunstig / gemiddeld / ongunstig) en een eerlijke toets:
   de tabel uit de eerste 60% van de dagen, beoordeeld op de latere dagen die hij nooit zag.

Alleen informatie. De bot koopt en verkoopt hierdoor niets anders; een regel die hierop leunt kan pas na de toets
en met jouw ja (via het onderzoek en een voorstel).
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from .daytrade_indicatie import indicatie, tabel, toets, zin
from .features import REGIME_BENCHMARKS, market_regime, snapshot
from .insights import moment
from .signals import MIN_BARS, analyse

RUST = 10          # pas een nieuw signaal als het aandeel 10 beursdagen geen signaal gaf (anders tel je hetzelfde dubbel)
MAX_DAGEN = 250    # langer dan een jaar vasthouden komt bijna niet voor; dan op dat moment de uitkomst nemen
VENSTER = 300      # zoveel dagen terug zijn genoeg voor het 200-daags gemiddelde
WOORD = "koopsignalen"
BESTAND = "trend_indicatie.json"


def _b(v, grenzen, namen):
    if v is None:
        return "onbekend"
    for g, n in zip(grenzen, namen):
        if v < g:
            return n
    return namen[-1]


KENMERKEN = {
    "Instapmoment": lambda c: c.get("moment") or "onbekend",
    "RSI bij instap": lambda c: _b(c.get("rsi14"), [60, 70, 80], ["onder 60", "60-70", "70-80", "80 of hoger"]),
    "Markttrend": lambda c: c.get("trend_regime") or "onbekend",
    "Onrust op de markt": lambda c: c.get("beweeglijkheid_regime") or "onbekend",
    "Stijging 3 maanden": lambda c: _b(c.get("rend_3m"), [0.10, 0.25], ["tot 10%", "10-25%", "meer dan 25%"]),
    "Afstand tot 200-daags gemiddelde": lambda c: _b(c.get("afstand_sma200_pct"), [10, 25],
                                                     ["tot 10%", "10-25%", "meer dan 25%"]),
    "Beweeglijkheid aandeel": lambda c: _b(c.get("atr_pct"), [1.5, 3.0], ["rustig", "normaal", "wild"]),
    "Handel t.o.v. normaal": lambda c: _b(c.get("volume_rel"), [0.9, 1.1], ["minder", "normaal", "meer"]),
}


def context(a, bars, regime) -> dict:
    """De situatie bij een koopsignaal; zelfde meetwaarden als de bot bij een echte aankoop vastlegt."""
    snap = snapshot(bars)
    ctx = dict(snap)
    ctx.update({"rend_1m": round(a.ret21, 4), "rend_3m": round(a.ret63, 4), "volume_rel": round(a.rel_volume, 2),
                "moment": moment(snap)[0]})
    if regime is not None:
        ctx.update({"trend_regime": regime.trend, "beweeglijkheid_regime": regime.beweeglijkheid})
    return ctx


def uitkomst(bars, i: int, a, s) -> tuple[float, str, int] | None:
    """Resultaat in R als je op dag i (slot) had gekocht, met de uitstapregels van de trend-agent."""
    entry = bars[i].close * (1 + s.slippage)
    stop = entry - s.stop_atr_multiple * a.atr14
    if stop <= 0 or stop >= entry:
        return None
    risk = entry - stop
    hoogste = bars[i].close
    closes = [b.close for b in bars]
    for j in range(i + 1, min(len(bars), i + 1 + MAX_DAGEN)):
        b = bars[j]
        if b.low <= stop:
            return (min(b.open, stop) * (1 - s.slippage) - entry) / risk, "stop-loss", j - i
        if j >= 50 and b.close < sum(closes[j - 49:j + 1]) / 50:
            return (b.close * (1 - s.slippage) - entry) / risk, "trend gebroken", j - i
        hoogste = max(hoogste, b.close)
        stop = max(stop, hoogste - s.trail_atr_multiple * a.atr14)   # benadering: ATR van de instapdag
    if len(bars) - 1 - i < MAX_DAGEN:
        return None    # loopt nog: uitkomst nog niet bekend
    j = i + MAX_DAGEN
    return (bars[j].close * (1 - s.slippage) - entry) / risk, "na een jaar", MAX_DAGEN


def signalen(bars_by_ticker: dict, s, tickers=None) -> list[dict]:
    """Alle nieuwe koopsignalen in de koersgeschiedenis, met situatie en uitkomst."""
    bench_t = next((t for t in REGIME_BENCHMARKS if t in bars_by_ticker), None)
    bench = bars_by_ticker[bench_t] if bench_t else None
    bench_idx = {b.day: k for k, b in enumerate(bench)} if bench else {}
    regimes: dict[date, object] = {}
    out = []
    for tk in tickers or sorted(bars_by_ticker):
        bars = bars_by_ticker.get(tk) or []
        stil = RUST
        for i in range(MIN_BARS, len(bars)):
            win = bars[max(0, i + 1 - VENSTER):i + 1]
            a = analyse(tk, win, bars[i].day, s)
            if not a.is_candidate:
                stil += 1
                continue
            nieuw, stil = stil >= RUST, 0
            if not nieuw:
                continue
            snap_rsi = snapshot(win).get("rsi14")
            if snap_rsi is not None and snap_rsi > s.max_rsi_entry:
                continue
            u = uitkomst(bars, i, a, s)
            if u is None:
                continue
            d = bars[i].day
            if d not in regimes:
                k = bench_idx.get(d)
                regimes[d] = market_regime({bench_t: bench[max(0, k + 1 - VENSTER):k + 1]}) if k is not None else None
            out.append({"dag": d.isoformat(), "ticker": tk, "r": round(u[0], 3), "reden": u[1], "dagen": u[2],
                        "ctx": context(a, win, regimes[d])})
    return out


def maak(bars_by_ticker: dict, s, out_dir: Path, tickers=None) -> dict:
    """Signalen zoeken, tabel en toets maken, en wegschrijven naar <out_dir>/trend_indicatie.json."""
    events = signalen(bars_by_ticker, s, tickers)
    ts = toets(events, kenmerken=KENMERKEN)
    uit = {"gemaakt": date.today().isoformat(), "signalen": len(events),
           "van": min((e["dag"] for e in events), default=""), "tot": max((e["dag"] for e in events), default=""),
           "tabel": tabel(events, KENMERKEN), "toets": ts, "zin": zin(ts, WOORD)}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / BESTAND).write_text(json.dumps(uit, ensure_ascii=False, indent=1), encoding="utf-8")
    return uit


def laad(pad: Path) -> dict:
    try:
        return json.loads(pad.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def beoordeel(ctx: dict, uit: dict) -> dict:
    """Label voor één kans uit het laatste onderzoek (of 'onbekend' als dat er nog niet is)."""
    t = (uit or {}).get("tabel")
    if not t:
        return {"oordeel": "onbekend", "tekst": "Nog geen onderzoek naar eerdere koopsignalen.", "score": None}
    return indicatie(ctx or {}, t, KENMERKEN, WOORD)
