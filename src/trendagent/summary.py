"""Dagoverzicht: beide bots op één pagina, in gewone taal.

Schrijft rapporten/<handelsdag>-overzicht.md en rapporten/OVERZICHT.md (altijd de nieuwste):
- stand van beide bots: waarde, resultaat vandaag, sinds de start, en tegenover de wereld-ETF;
- wat er vandaag gekocht en verkocht is;
- wat de controles vonden: koersbronnen, achterlopende koersen, wisselkoers, waarschuwingen;
- of GitHub de ronde op tijd startte.
Leest alleen bestanden die de bots al hebben geschreven; verandert niets aan de portefeuilles.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

PLANNED_UTC = (22, 17)       # geplande start van de dagelijkse ronde (zie practice.yml)


def _eur(x: float) -> str:
    return f"€{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _pct(x: float) -> str:
    return f"{x:+.2%}".replace(".", ",")


def _history_stats(history: list[dict]) -> dict:
    pts = [e for e in history if e.get("day") != "start"]
    if not history:
        return {}
    start = history[0]["equity"]
    now = history[-1]["equity"]
    out = {"waarde": now, "sinds_start": now / start - 1 if start else 0.0}
    if len(pts) >= 2:
        out["vandaag"] = now - pts[-2]["equity"]
        out["vandaag_pct"] = now / pts[-2]["equity"] - 1
    bench = [e for e in pts if "bench" in e]
    if len(bench) >= 2:
        b = bench[-1]["bench"] / bench[0]["bench"] - 1
        bot = bench[-1]["equity"] / bench[0]["equity"] - 1
        out["vs_etf"] = bot - b
        out["etf"] = b
        out["sinds"] = bench[0]["day"]
    return out


def _load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _plain_checks(name: str, h: dict) -> list[str]:
    lines = []
    if not h:
        return [f"{name}: geen gegevens (ronde niet gedraaid?)"]
    status = h.get("status", "?")
    lines.append(f"{name}: status **{status}**, {h.get('ok', '?')} van {h.get('gevraagd', '?')} koersen opgehaald, "
                 f"marktregime {h.get('regime', '?')}.")
    src = h.get("bronnen") or {}
    if src:
        k = src.get("koersen", {})
        line = (f"Koersbronnen: {k.get('bevestigd', 0)} bevestigd door twee bronnen, {k.get('1 bron', 0)} uit één bron, "
                f"{k.get('afwijking', 0)} afwijkend. Wisselkoers: {src.get('wisselkoers', '?')}.")
        if src.get("tweede_bron") and src["tweede_bron"] != "actief":
            line += f" Tweede bron {src['tweede_bron']}"
            if src.get("fout_tweede_bron"):
                line += f" ({src['fout_tweede_bron']})"
            line += "."
        lines.append(line)
    if h.get("verouderd"):
        lines.append(f"{h['verouderd']} koersen waren niet bijgewerkt; die instrumenten zijn vandaag niet gekocht.")
    if h.get("verdacht"):
        lines.append("Niet gekocht door verdachte data: " + ", ".join(sorted(h["verdacht"])) + ".")
    for w in h.get("waarschuwingen", [])[:6]:
        lines.append(w)
    if h.get("fout"):
        lines.append(f"Fout: {h['fout']}")
    return lines


def build(state_dir: Path, reports_dir: Path, day: str, now_utc: datetime | None = None) -> str:
    now_utc = now_utc or datetime.now(timezone.utc)
    trend = _load(state_dir / "portfolio.json")
    inv = _load(state_dir / "investeerder.json")
    health = _load(state_dir / "health.json")

    rows = []
    for name, data in (("Investeerder", inv), ("Trend-agent", trend)):
        st = _history_stats(data.get("equity_history", []))
        if not st:
            rows.append(f"| {name} | – | – | – | – |")
            continue
        today = f"{_eur(st['vandaag'])} ({_pct(st['vandaag_pct'])})" if "vandaag" in st else "–"
        vs = f"{_pct(st['vs_etf'])} (ETF {_pct(st['etf'])} sinds {st['sinds']})" if "vs_etf" in st else "nog te kort"
        rows.append(f"| {name} | {_eur(st['waarde'])} | {today} | {_pct(st['sinds_start'])} | {vs} |")

    done = []
    for name, data in (("Investeerder", inv), ("Trend-agent", trend)):
        for t in data.get("trades", []):
            if t.get("day") == day:
                verb = "kocht" if t["side"] == "BUY" else "verkocht"
                res = f", resultaat {_eur(t['pnl_eur'])}" if t.get("pnl_eur") is not None else ""
                done.append(f"{name} {verb} {t['ticker']} voor {_eur(t['value_eur'])} ({t['reason'][:90]}{res})")

    lines = [f"# Dagoverzicht {day}", "",
             "_Twee oefenbots met elk €10.000 nepgeld. Geen beleggingsadvies._", "",
             "## Stand", "",
             "| Bot | Waarde | Vandaag | Sinds start | Tegenover wereld-ETF |",
             "| --- | --- | --- | --- | --- |", *rows, "",
             "## Vandaag gedaan", ""]
    lines += [f"- {d}" for d in done] or ["- Niets gekocht of verkocht."]
    lines += ["", "## Controles", ""]
    for bot, label in (("investeerder", "Investeerder"), ("trend", "Trend-agent")):
        lines += [f"- {c}" for c in _plain_checks(label, health.get(bot, {}))]

    try:
        d = datetime.fromisoformat(day).replace(tzinfo=timezone.utc)
        planned = d.replace(hour=PLANNED_UTC[0], minute=PLANNED_UTC[1])
        delay = now_utc - planned
        if delay > timedelta(hours=2):
            lines += ["", f"_GitHub startte deze ronde {delay.total_seconds() / 3600:.0f} uur later dan gepland. "
                          "De koersen zijn die van de slotkoers van deze handelsdag; de vertraging verandert daar niets aan._"]
    except ValueError:
        pass

    lines += ["", "## Details", "",
              f"- Investeerder: [{day}-investeerder.md]({day}-investeerder.md)",
              f"- Trend-agent: [{day}.md]({day}.md)",
              "- Excel: `investeerder.xlsx` en `trend-agent.xlsx` (met tabblad Grafieken)"]
    return "\n".join(lines) + "\n"


def write(state_dir: Path, reports_dir: Path, day: str) -> Path:
    text = build(state_dir, reports_dir, day)
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / f"{day}-overzicht.md"
    path.write_text(text, encoding="utf-8")
    (reports_dir / "OVERZICHT.md").write_text(text, encoding="utf-8")
    return path
