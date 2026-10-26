"""Volglijst: extra beleggingen die alleen worden BEKEKEN, nooit automatisch gekocht.

Per belegging: koers, rendement over een week / maand / 3 maanden, de trend (slot t.o.v. de gemiddelden van
50 en 200 dagen), of de trend-agent hem volgens zijn eigen regels zou kopen, en of hij bij Trading 212 te koop is
(uit de instrumentenlijst die de koppeling met het oefenaccount al ophaalt). Koersen komen van Yahoo: de
Trading 212-API geeft geen koersgeschiedenis.

Schrijft dashboard/volglijst.json. Verandert niets aan de bots of het oefenaccount.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from .broker_t212 import map_ticker
from .core.config import Settings
from .data import Bar, DataError
from .signals import MIN_BARS, analyse
from .universe import BY_TICKER, Instrument


def load(config: Path) -> list[Instrument]:
    d = json.loads(config.read_text(encoding="utf-8"))
    out = []
    for it in d.get("items", []):
        t = str(it.get("ticker", "")).strip().upper()
        if not t or t in BY_TICKER:
            continue  # al in de lijst van de bots: daar wordt hij al bekeken
        eu = "." in t
        out.append(Instrument(t, it.get("naam") or t, "EU" if eu else "US", "EUR" if eu else "USD",
                              it.get("soort", "STOCK")))
    return out


def _t212_items(state_dir: Path) -> list[dict] | None:
    try:
        return json.loads((state_dir / "t212_instrumenten.json").read_text(encoding="utf-8")).get("items") or None
    except (OSError, ValueError):
        return None


def row(inst: Instrument, bars: list[Bar], today: date, s: Settings, t212: list[dict] | None) -> dict:
    closes = [b.close for b in bars]

    def ret(n: int):
        return round(closes[-1] / closes[-n - 1] - 1, 5) if len(closes) > n else None

    a = analyse(inst.ticker, bars, today, s)
    if len(bars) >= MIN_BARS:
        if a.close > a.sma50 > a.sma200:
            trend = "stijgend"
        elif a.close < a.sma50 < a.sma200:
            trend = "dalend"
        else:
            trend = "zijwaarts"
    else:
        trend = "onbekend"
    if a.is_candidate:
        oordeel = "Zou de trend-agent kopen: alle regels kloppen."
    else:
        oordeel = "Nu niet: " + "; ".join(a.reasons[:2]) + "."
    t212_ticker = map_ticker(inst.ticker, inst.currency, t212) if t212 else None
    return {
        "id": inst.ticker, "ticker": inst.ticker, "naam": inst.name, "soort": inst.kind, "regio": inst.region,
        "valuta": inst.currency, "dag": bars[-1].day.isoformat(), "koers": round(closes[-1], 4),
        "week": ret(5), "maand": ret(21), "kwartaal": ret(63),
        "afstand_sma50": round(a.close / a.sma50 - 1, 5) if a.sma50 else None,
        "trend": trend, "kandidaat": a.is_candidate, "score": a.score, "oordeel": oordeel,
        "bij_t212": None if t212 is None else bool(t212_ticker), "t212": t212_ticker or "",
        "lijn": ",".join(f"{c:.4g}" for c in closes[-60:]),
        "_ctx": _ctx(a, bars) if a.is_candidate else None,
    }


def _ctx(a, bars) -> dict:
    """Situatie voor de indicatie (zelfde meetwaarden als bij de kansen van de trend-agent)."""
    from .features import snapshot
    from .insights import kans_context, moment
    snap = snapshot(bars)
    return kans_context(a, snap, moment(snap)[0])


def build(config: Path, state_dir: Path, provider, s: Settings, today: date | None = None) -> list[dict]:
    today = today or date.today()
    t212 = _t212_items(state_dir)
    rows = []
    for inst in load(config):
        try:
            bars = provider.history(inst, 300)
        except DataError as exc:
            rows.append({"id": inst.ticker, "ticker": inst.ticker, "naam": inst.name, "soort": inst.kind,
                         "regio": inst.region, "valuta": inst.currency, "fout": str(exc), "trend": "onbekend",
                         "kandidaat": False, "oordeel": "Geen koersen opgehaald; volgende keer opnieuw."})
            continue
        if bars:
            rows.append(row(inst, bars, today, s, t212))
    from datetime import datetime, timezone
    nu = datetime.now(timezone.utc).isoformat(timespec="seconds")
    from . import trend_indicatie as ti
    onderzoek_ti = ti.laad(Path("onderzoek") / ti.BESTAND)
    for r in rows:
        r["gemaakt"] = nu
        ctx = r.pop("_ctx", None)
        ind = ti.beoordeel(ctx, onderzoek_ti) if ctx else {"oordeel": "onbekend"}
        r["indicatie"] = "" if ind["oordeel"] == "onbekend" else ind["oordeel"]
        r["indicatie_tekst"] = ind.get("tekst", "") if r["indicatie"] else ""
    # Eerst wat de trend-agent zou kopen (hoogste score), dan de rest op rendement over 3 maanden.
    return sorted(rows, key=lambda r: (not r.get("kandidaat"), -(r.get("score") or 0), -(r.get("kwartaal") or -9)))


def write(rows: list[dict], path: Path) -> Path:
    if not rows:
        rows = [{"id": "leeg", "leeg": True, "reden": "Geen beleggingen op de volglijst (config/volglijst.json)."}]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    return path
