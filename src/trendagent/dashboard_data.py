"""Cijfers voor het online dashboard: één JSON-bestand per onderwerp in de map dashboard/.

Leest alleen wat de bots al schreven (state/ en de grafiekgegevens in rapporten/grafieken/<dag>/).
Verandert niets aan de portefeuilles. Elk bestand is een lijst rijen (een tabel), zodat het
dashboard elk getal kan herleiden naar een rij.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import insights
from .universe import BY_TICKER

BOTS = (("Investeerder", "investeerder", "investeerder.json"), ("Trend-agent", "trend", "portfolio.json"))


def _load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _name(ticker: str) -> str:
    inst = BY_TICKER.get(ticker)
    return inst.name if inst else ticker


def build(state_dir: Path, reports_dir: Path) -> dict[str, list[dict]]:
    from .summary import _history_stats, _plain_checks
    info = insights.load(state_dir)
    books = {key: _load(state_dir / fname) for _, key, fname in BOTS}
    health = _load(state_dir / "health.json")
    out: dict[str, list[dict]] = {}

    # Stand per bot
    rows = []
    for name, key, _ in BOTS:
        hist = books[key].get("equity_history", [])
        st = _history_stats(hist)
        if not st:
            continue
        start = hist[0]["equity"]
        rows.append({
            "bot": name, "dag": next((e["day"] for e in reversed(hist) if e["day"] != "start"), ""),
            "waarde": round(st["waarde"], 2), "sinds_start_eur": round(st["waarde"] - start, 2),
            "sinds_start_pct": round(st["sinds_start"], 5),
            "vandaag_eur": round(st["vandaag"], 2) if "vandaag" in st else None,
            "vandaag_pct": round(st["vandaag_pct"], 5) if "vandaag_pct" in st else None,
            "vs_etf_pct": round(st["vs_etf"], 5) if "vs_etf" in st else None,
            "vastgezet_eur": round(sum(t.get("pnl_eur") or 0 for t in books[key].get("trades", [])
                                       if t.get("side") == "SELL"), 2),
            "status": health.get(key, {}).get("status", ""),
            "klaar": info.get(key, {}).get("klaar", {}).get("oordeel", ""),
        })
    out["stand"] = rows

    # Waarde per dag, met de wereld-ETF omgerekend naar hetzelfde startbedrag
    rows = []
    for name, key, _ in BOTS:
        pts = [e for e in books[key].get("equity_history", []) if e["day"] != "start"]
        bench = [e for e in pts if "bench" in e]
        base = (bench[0]["equity"], bench[0]["bench"]) if bench else None
        for e in pts:
            rows.append({"dag": e["day"], "bot": name, "waarde": round(e["equity"], 2),
                         "etf_waarde": round(base[0] * e["bench"] / base[1], 2) if base and "bench" in e else None})
    out["waarde"] = rows

    # Posities met risico
    rows = []
    tr, inv = info.get("trend", {}), info.get("investeerder", {})
    for r in tr.get("posities", []):
        rows.append({"bot": "Trend-agent", "ticker": r["ticker"], "naam": _name(r["ticker"]), "instap": r["instap"],
                     "koers": r["koers"], "stop": r["stop"], "resultaat_eur": r["resultaat_eur"],
                     "resultaat_pct": r["resultaat_pct"], "afstand_stop_pct": r["afstand_stop_pct"],
                     "bij_stop_eur": r["bij_stop_eur"], "waarde_eur": None})
    for r in inv.get("posities", []):
        rows.append({"bot": "Investeerder", "ticker": r["ticker"], "naam": _name(r["ticker"]), "instap": None,
                     "koers": None, "stop": None, "resultaat_eur": r["resultaat_eur"],
                     "resultaat_pct": r["resultaat_pct"], "afstand_stop_pct": None, "bij_stop_eur": None,
                     "waarde_eur": r["waarde_eur"]})
    out["posities"] = rows

    # Remmen van de trend-agent
    b = tr.get("remmen") or {}
    out["remmen"] = [{"rem": "Daling vanaf de top", "nu": b.get("daling_vanaf_top"), "grens": -b["grens_daling"],
                      "eenheid": "pct"},
                     {"rem": "Vandaag", "nu": b.get("vandaag"), "grens": -b["grens_dag"], "eenheid": "pct"},
                     {"rem": "Verliestrades op rij", "nu": b.get("verlies_op_rij"), "grens": b["grens_op_rij"],
                      "eenheid": "aantal"}] if b else []

    # Wat de bots zagen en concludeerden
    rows = []
    for name, key, _ in BOTS:
        d = info.get(key, {})
        for i, line in enumerate(d.get("zag", [])):
            text = line.removeprefix("- ").replace("**", "")
            head, _, rest = text.partition(":")
            rows.append({"id": f"{key}-zag-{i}", "bot": name, "soort": "zag", "onderdeel": head.strip(),
                         "tekst": rest.strip()})
        for i, c in enumerate(d.get("conclusies", [])):
            rows.append({"id": f"{key}-conclusie-{i}", "bot": name, "soort": "conclusie", "onderdeel": "",
                         "tekst": c})
    out["analyse"] = rows

    # Kansen
    rows = []
    for i, k in enumerate(tr.get("kansen", []), 1):
        p = k["plan"]
        rows.append({"nr": i, "ticker": k["ticker"], "naam": k["naam"], "moment": k["moment"],
                     "moment_uitleg": k["moment_uitleg"], "waarom": k["uitleg"], "status": k["status"],
                     "valuta": p["valuta"], "instap": p["instap"], "stop": p["stop"], "stop_pct": p["stop_pct"],
                     "aantal": p["aantal"], "inzet_eur": p["inzet_eur"], "max_verlies_eur": p["max_verlies_eur"]})
    out["kansen"] = rows

    # Klaar voor echt geld
    rows = []
    for name, key, _ in BOTS:
        k = info.get(key, {}).get("klaar")
        if not k:
            continue
        for label, state, detail in k["eisen"]:
            rows.append({"id": f"{key}-{label}", "bot": name, "eis": label, "stand": state, "nu": detail})
    out["klaar"] = rows

    # Koersen voor de kaarsgrafieken (laatste ~3 maanden per positie)
    rows = []
    folders = sorted(p for p in (reports_dir / "grafieken").glob("*") if p.is_dir()) \
        if (reports_dir / "grafieken").exists() else []
    if folders:
        for f in sorted(folders[-1].glob("*.json"), key=lambda p: (not p.name.startswith("trend"), p.name)):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except ValueError:
                continue
            bot = "Trend-agent" if f.name.startswith("trend") else "Investeerder"
            ticker = f.stem.split("-", 1)[1]
            for i, day in enumerate(d.get("iso", [])):
                rows.append({"bot": bot, "ticker": ticker, "naam": _name(ticker), "valuta": d.get("valuta", ""),
                             "dag": day, "open": (d.get("open") or d["koers"])[i],
                             "hoog": (d.get("hoog") or d["koers"])[i], "laag": (d.get("laag") or d["koers"])[i],
                             "slot": d["koers"][i], "sma50": d["sma50"][i], "sma200": d["sma200"][i],
                             "instap": d.get("instap"), "stop": d.get("stop"), "uitleg": " ".join(d.get("uitleg", []))})
    out["koersen"] = rows

    # Trades
    rows = []
    for name, key, _ in BOTS:
        for i, t in enumerate(books[key].get("trades", [])):
            rows.append({"id": f"{key}-{i}", "dag": t["day"], "bot": name, "ticker": t["ticker"],
                         "naam": _name(t["ticker"]), "soort": "koop" if t["side"] == "BUY" else "verkoop",
                         "aantal": round(t["qty"], 4), "waarde_eur": t["value_eur"], "kosten_eur": t["costs_eur"],
                         "resultaat_eur": t.get("pnl_eur"), "reden": t["reason"]})
    out["trades"] = sorted(rows, key=lambda r: r["dag"], reverse=True)

    # Controles
    rows = []
    for name, key, _ in BOTS:
        for i, line in enumerate(_plain_checks(name, health.get(key, {}))[:8]):
            rows.append({"id": f"{key}-{i}", "bot": name, "tekst": line.replace("**", "")})
    out["controles"] = rows
    return out


def write(state_dir: Path, reports_dir: Path, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, rows in build(state_dir, reports_dir).items():
        p = out_dir / f"{name}.json"
        p.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
        paths.append(p)
    return paths
