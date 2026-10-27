"""Archief van de 5-minutenkoersen van de daytrader.

Yahoo geeft gratis maar ~60 dagen aan 5-minutenkoersen terug. Door elke week op te slaan wat er binnenkomt,
groeit de geschiedenis waarop het daytrade-onderzoek test: na een jaar is dat een jaar in plaats van 2 maanden.

Eén bestand per week (backtest/daytrade/koersen/2026-W43.csv.gz): oude weken veranderen niet meer, dus de
repository groeit maar een paar honderd kilobyte per week. Het bestand wordt zo geschreven dat dezelfde
inhoud altijd dezelfde bytes geeft (geen onnodige wijzigingen in git).
"""

from __future__ import annotations

import csv
import gzip
import io
from datetime import datetime
from pathlib import Path

from .daytrader import NY, Bar5

MAP = Path("backtest/daytrade/koersen")
MAX_DAGEN = 250      # het onderzoek kijkt hooguit zo ver terug (rekentijd)


def _key(t: datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M")


def _week(t: datetime) -> str:
    y, w, _ = t.isocalendar()
    return f"{y}-W{w:02d}"


def laad(map_: Path = MAP) -> dict[str, list[Bar5]]:
    out: dict[str, list[Bar5]] = {}
    for f in sorted(map_.glob("*.csv.gz")):
        out = samen(out, _lees_week(f), max_dagen=10_000)
    return out


def samen(oud: dict[str, list[Bar5]], nieuw: dict[str, list[Bar5]], max_dagen: int = MAX_DAGEN) -> dict[str, list[Bar5]]:
    """Oude en nieuwe koersen samen (bij hetzelfde blok telt de nieuwe), hooguit de laatste max_dagen beursdagen."""
    out = {}
    for tk in set(oud) | set(nieuw):
        m = {_key(b.t): b for b in oud.get(tk, [])}
        m.update({_key(b.t): b for b in nieuw.get(tk, [])})
        bars = [m[k] for k in sorted(m)]
        dagen = sorted({b.t.date() for b in bars})[-max_dagen:]
        if dagen:
            bars = [b for b in bars if b.t.date() >= dagen[0]]
        out[tk] = bars
    return out


def bewaar(data: dict[str, list[Bar5]], map_: Path = MAP) -> list[Path]:
    """Schrijft de koersen per week weg, samengevoegd met wat er al stond. Geeft de gewijzigde bestanden."""
    per_week: dict[str, dict[str, list[Bar5]]] = {}
    for tk, bars in data.items():
        for b in bars:
            per_week.setdefault(_week(b.t), {}).setdefault(tk, []).append(b)
    map_.mkdir(parents=True, exist_ok=True)
    gewijzigd = []
    for wk, nieuw in sorted(per_week.items()):
        pad = map_ / f"{wk}.csv.gz"
        oud = _lees_week(pad) if pad.exists() else {}
        alles = samen(oud, nieuw, max_dagen=10_000)
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(["ticker", "t", "o", "h", "l", "c", "v"])
        for tk in sorted(alles):
            for b in alles[tk]:
                w.writerow([tk, _key(b.t), f"{b.o:.4f}", f"{b.h:.4f}", f"{b.l:.4f}", f"{b.c:.4f}", f"{b.v:.0f}"])
        raw = gzip.compress(buf.getvalue().encode("utf-8"), mtime=0)
        if not pad.exists() or pad.read_bytes() != raw:
            pad.write_bytes(raw)
            gewijzigd.append(pad)
    return gewijzigd


def _lees_week(pad: Path) -> dict[str, list[Bar5]]:
    alles: dict[str, list[Bar5]] = {}
    with gzip.open(pad, "rt", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            t = datetime.strptime(r["t"], "%Y-%m-%dT%H:%M")
            if NY is not None:
                t = t.replace(tzinfo=NY)
            alles.setdefault(r["ticker"], []).append(Bar5(t, float(r["o"]), float(r["h"]), float(r["l"]),
                                                          float(r["c"]), float(r["v"])))
    return alles
