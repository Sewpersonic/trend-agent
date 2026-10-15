"""Patronen in de grafieken: per aandeel een samenvatting van trend en opvallende bewegingen,
en een samenvatting over alle grafieken samen.

Alleen beschrijving van wat er al gebeurd is, met vaste rekenregels. Het voorspelt niets: een
patroon zegt niet zeker wat de koers morgen doet. De bots gebruiken dit niet om te beslissen.
Invoer: de grafiekgegevens die de bots elke ronde schrijven (rapporten/grafieken/<dag>/<bot>-<ticker>.json).
"""

from __future__ import annotations

import json
from pathlib import Path

from .universe import BY_TICKER


def _pct(x: float) -> str:
    return f"{x:+.1%}".replace(".", ",")


def _day(iso: str) -> str:
    m = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
    y, mo, d = iso.split("-")
    return f"{int(d)} {m[int(mo) - 1]}"


def analyse(item: dict) -> dict | None:
    """Patronen van één aandeel uit zijn grafiekgegevens (ongeveer 3 maanden dagkoersen)."""
    c = item.get("koers") or []
    n = len(c)
    if n < 15:
        return None
    hi = item.get("hoog") or c
    lo = item.get("laag") or c
    op = item.get("open") or c
    s50, s200 = item.get("sma50") or [None] * n, item.get("sma200") or [None] * n
    vol = item.get("volume") or []
    days = item.get("iso") or [""] * n
    last = c[-1]
    ret = lambda k: last / c[-1 - k] - 1 if n > k else None  # noqa: E731
    d5, d21, dall = ret(5), ret(21), last / c[0] - 1

    # Trend
    a, b = s50[-1], s200[-1]
    if a and b and last > a > b:
        trend = "stijgend"
    elif a and b and last < a < b:
        trend = "dalend"
    else:
        trend = "zijwaarts"
    slope50 = (s50[-1] / s50[-11] - 1) if s50[-1] and n > 11 and s50[-11] else None

    pats: list[str] = []
    top, bottom = max(hi), min(lo)
    plek = (last - bottom) / (top - bottom) if top > bottom else 0.5
    if max(hi[-3:]) >= top:
        pats.append("nieuwe 3-maands top")
    elif last >= top * 0.98:
        pats.append("vlak bij de 3-maands top")
    if min(lo[-3:]) <= bottom:
        pats.append("nieuwe 3-maands bodem")
    elif last <= bottom * 1.02:
        pats.append("vlak bij de 3-maands bodem")

    # Kruisen van de gemiddelden binnen de getoonde periode
    for i in range(1, n):
        if None in (s50[i - 1], s200[i - 1], s50[i], s200[i]):
            continue
        if s50[i - 1] <= s200[i - 1] and s50[i] > s200[i]:
            pats.append(f"50-daags gemiddelde kruiste omhoog door het 200-daagse op {_day(days[i])}")
        if s50[i - 1] >= s200[i - 1] and s50[i] < s200[i]:
            pats.append(f"50-daags gemiddelde zakte door het 200-daagse op {_day(days[i])}")
    # Koers door het 50-daags gemiddelde in de laatste 3 dagen
    for i in range(max(1, n - 3), n):
        if s50[i] and s50[i - 1]:
            if c[i - 1] >= s50[i - 1] and c[i] < s50[i]:
                pats.append("net onder het 50-daags gemiddelde gezakt")
            elif c[i - 1] <= s50[i - 1] and c[i] > s50[i]:
                pats.append("net boven het 50-daags gemiddelde gestegen")

    # Reeks stijgende of dalende dagen
    streak, sign = 0, 0
    for i in range(n - 1, 0, -1):
        s = 1 if c[i] > c[i - 1] else -1 if c[i] < c[i - 1] else 0
        if s == 0 or (sign and s != sign):
            break
        sign, streak = s, streak + 1
    if streak >= 3:
        pats.append(f"{streak} dagen op rij {'gestegen' if sign > 0 else 'gedaald'}")

    # Grote beweging op de laatste dag en beweeglijkheid
    moves = [abs(c[i] / c[i - 1] - 1) for i in range(1, n)]
    normal = sum(moves[:-1]) / max(len(moves) - 1, 1)
    if moves and normal and moves[-1] > 2.2 * normal and moves[-1] > 0.015:
        pats.append(f"grote beweging op de laatste dag ({_pct(c[-1] / c[-2] - 1)})")
    if len(moves) >= 40:
        recent, before = sum(moves[-10:]) / 10, sum(moves[-40:-10]) / 30
        if recent > before * 1.5:
            pats.append("beweegt de laatste 2 weken veel meer dan daarvoor")
        elif recent < before * 0.6:
            pats.append("is de laatste 2 weken rustiger dan daarvoor")
    if trend == "stijgend" and d5 is not None and d5 < -0.02:
        pats.append("terugval binnen een stijgende trend")
    if trend == "dalend" and d5 is not None and d5 > 0.02:
        pats.append("opleving binnen een dalende trend")
    if len(vol) == n and vol[-1] and sum(vol[-21:-1]) > 0:
        avg = sum(vol[-21:-1]) / 20
        if vol[-1] > 1.8 * avg:
            pats.append(f"veel handel op de laatste dag ({vol[-1] / avg:.1f}x normaal)".replace(".", ","))
    if op and len(op) == n:
        greens = sum(1 for i in range(n - 10, n) if c[i] >= op[i])
        if greens >= 8:
            pats.append(f"{greens} van de laatste 10 dagen groen")
        elif greens <= 2:
            pats.append(f"{10 - greens} van de laatste 10 dagen rood")

    naam = item.get("titel", "").split(" (")[0] or item.get("ticker", "")
    zin = {"stijgend": "Stijgende trend", "dalend": "Dalende trend", "zijwaarts": "Geen duidelijke richting"}[trend]
    zin += f": {_pct(dall)} in 3 maanden, {_pct(d21)} in de laatste maand" if d21 is not None else f": {_pct(dall)} in 3 maanden"
    zin += f" en {_pct(d5)} in de laatste week." if d5 is not None else "."
    if slope50 is not None and trend != "zijwaarts":
        zin += " Het 50-daags gemiddelde " + ("loopt nog op." if slope50 > 0.003 else "daalt." if slope50 < -0.003 else "vlakt af.")
    if pats:
        zin += " Opvallend: " + "; ".join(pats[:3]) + "."
    return {"naam": naam, "trend": trend, "week": round(d5, 4) if d5 is not None else None,
            "maand": round(d21, 4) if d21 is not None else None, "drie_mnd": round(dall, 4),
            "plek_in_bereik": round(plek, 3), "slot": round(last, 4), "dag": days[-1],
            "patronen": " · ".join(pats), "samenvatting": zin}


def per_ticker(chart_folder: Path) -> list[dict]:
    rows = []
    if not chart_folder.exists():
        return rows
    for f in sorted(chart_folder.glob("*.json"), key=lambda p: (not p.name.startswith("trend"), p.name)):
        try:
            item = json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            continue
        bot_key, _, ticker = f.stem.partition("-")
        res = analyse(item)
        if not res:
            continue
        inst = BY_TICKER.get(ticker)
        res.update(ticker=ticker, naam=inst.name if inst else res["naam"],
                   bot="Trend-agent" if bot_key == "trend" else "Investeerder", valuta=item.get("valuta", ""))
        rows.append(res)
    return rows


def samenvatting(rows: list[dict]) -> list[str]:
    """Wat de grafieken samen laten zien, in een paar zinnen."""
    if not rows:
        return []
    n = len(rows)
    up = [r for r in rows if r["trend"] == "stijgend"]
    down = [r for r in rows if r["trend"] == "dalend"]
    out = [f"{len(up)} van de {n} grafieken staan in een stijgende trend, {len(down)} in een dalende, "
           f"{n - len(up) - len(down)} zonder duidelijke richting."]
    with_m = [r for r in rows if r["maand"] is not None]
    if with_m:
        best = max(with_m, key=lambda r: r["maand"])
        worst = min(with_m, key=lambda r: r["maand"])
        out.append(f"Sterkste van de laatste maand: {best['naam']} ({_pct(best['maand'])}); "
                   f"zwakste: {worst['naam']} ({_pct(worst['maand'])}).")
    with_w = [r for r in rows if r["week"] is not None]
    if with_w:
        avg = sum(r["week"] for r in with_w) / len(with_w)
        rising = sum(1 for r in with_w if r["week"] > 0)
        out.append(f"Afgelopen week: {rising} van de {len(with_w)} gestegen, gemiddeld {_pct(avg)}.")
    tops = [r["naam"] for r in rows if "3-maands top" in r["patronen"]]
    bottoms = [r["naam"] for r in rows if "3-maands bodem" in r["patronen"]]
    pull = [r["naam"] for r in rows if "terugval binnen een stijgende trend" in r["patronen"]]
    broke = [r["naam"] for r in rows if "net onder het 50-daags" in r["patronen"]]
    if tops:
        out.append("Op of vlak bij hun hoogste punt van 3 maanden: " + ", ".join(tops) + ".")
    if bottoms:
        out.append("Op of vlak bij hun laagste punt van 3 maanden: " + ", ".join(bottoms) + ".")
    if pull:
        out.append("Terugval binnen een stijgende trend: " + ", ".join(pull) + ".")
    if broke:
        out.append("Net onder het 50-daags gemiddelde gezakt (voor de trend-agent een verkoopsignaal): "
                   + ", ".join(broke) + ".")
    out.append("Dit beschrijft wat er gebeurd is; het voorspelt niet wat de koersen morgen doen.")
    return out


def latest_folder(reports_dir: Path) -> Path | None:
    root = reports_dir / "grafieken"
    folders = sorted(p for p in root.glob("*") if p.is_dir() and any(p.glob("*.json"))) if root.exists() else []
    return folders[-1] if folders else None
