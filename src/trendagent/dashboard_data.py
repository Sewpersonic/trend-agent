"""Cijfers voor het online dashboard: één JSON-bestand per onderwerp in de map dashboard/.

Leest alleen wat de bots al schreven (state/ en de grafiekgegevens in rapporten/grafieken/<dag>/).
Verandert niets aan de portefeuilles. Elk bestand is een lijst rijen (een tabel), zodat het
dashboard elk getal kan herleiden naar een rij.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import insights, uitleg
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
    for r in rows:
        if r["soort"] == "conclusie":
            r["kleur"] = uitleg.kleur_van(r["tekst"])
    out["analyse"] = rows

    # In één oogopslag: tegels per bot
    rows = []
    for name, key, _ in BOTS:
        for i, t in enumerate(uitleg.oogopslag(key, info.get(key, {}))):
            rows.append(dict(t, id=f"{key}-{i}", bot=name))
    out["oogopslag"] = rows

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
                             "slot": d["koers"][i], "volume": (d.get("volume") or [None] * len(d["iso"]))[i],
                             "sma50": d["sma50"][i], "sma200": d["sma200"][i],
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

    # Wekelijks onderzoek (zaterdag): getoetste varianten en wat de bot leerde
    onderzoek = _load(state_dir.parent / "onderzoek" / "dashboard.json") if state_dir.name == "state" else {}
    if not onderzoek:
        onderzoek = _load(Path("onderzoek") / "dashboard.json")
    out["onderzoek"] = onderzoek.get("varianten", [])
    out["onderzoek_samenvatting"] = [{"id": f"o{i}", "nr": i, "tekst": t}
                                     for i, t in enumerate(onderzoek_zinnen(onderzoek, books), 1)]

    # Patronen in de grafieken (beschrijvend, voorspelt niets)
    from . import patronen
    folder = patronen.latest_folder(reports_dir)
    prow = patronen.per_ticker(folder) if folder else []
    out["patronen"] = [dict(r, id=r["ticker"]) for r in prow]
    out["patronen_samenvatting"] = [{"id": f"s{i}", "nr": i, "tekst": t}
                                    for i, t in enumerate(patronen.samenvatting(prow), 1)]
    out["broker"] = broker_rows(state_dir)

    # Per week: orders en wat de bots leerden; per bot: klaar voor echt geld of nog niet
    from . import weekoverzicht
    odir = state_dir.parent / "onderzoek" if state_dir.name == "state" else Path("onderzoek")
    out["weken"] = weekoverzicht.weken(books, out["trades"], _load(state_dir / "broker.json"), onderzoek, odir)
    out["gereed"] = weekoverzicht.gereed(books, info)

    # Controles in gewone taal (vraag, stand, uitleg, technisch detail)
    from . import controles
    bv = _load(state_dir / "broker.json")
    live = _load(state_dir / "broker_live.json")
    if live and live.get("tijd", "") > bv.get("tijd", ""):
        bv = live
    out["checks"] = controles.rows(health, bv, out["broker"])

    # Wanneer is wat ververst (voor de tijd bovenaan het dashboard)
    from datetime import datetime, timezone
    bots = max((str(h.get("vastgelegd_utc") or "") for h in health.values() if isinstance(h, dict)), default="")
    vl = _load_list(Path("dashboard") / "volglijst.json") if state_dir.name == "state" else []
    out["ververst"] = [
        {"id": "cijfers", "wat": "Cijfers van het dashboard", "tijd": datetime.now(timezone.utc).isoformat(timespec="seconds")},
        {"id": "bots", "wat": "Laatste ronde van de bots", "tijd": bots},
        {"id": "oefenaccount", "wat": "Stand oefenaccount", "tijd": str(bv.get("tijd") or "")},
        {"id": "handelsdag", "wat": "Laatste handelsdag", "tijd": max((r["dag"] for r in out["stand"] if r.get("dag")), default="")},
    ] + ([{"id": "volglijst", "wat": "Volglijst", "tijd": vl[0].get("gemaakt", "")}] if vl and vl[0].get("gemaakt") else [])
    return out


def _load_list(path: Path) -> list:
    try:
        v = json.loads(path.read_text(encoding="utf-8"))
        return v if isinstance(v, list) else []
    except (OSError, ValueError):
        return []


def broker_rows(state_dir: Path) -> list[dict]:
    """Oefenaccount Trading 212: stand, posities naast die van de trend-agent, en de laatste orders."""
    v = _load(state_dir / "broker.json")
    live = _load(state_dir / "broker_live.json")
    if live and live.get("status") != "fout" and live.get("tijd", "") > (v or {}).get("tijd", ""):
        # Nieuwere stand van de uurlijkse controle tonen; de ordergeschiedenis komt uit broker.json.
        v = {**live, "geschiedenis": (v or {}).get("geschiedenis", []), "managed": (v or {}).get("managed", [])}
    if not v:
        return []
    acc = v.get("account") or {}
    cash = (acc.get("cash") or {}).get("availableToTrade")
    inv = acc.get("investments") or {}
    rows = [{"id": "stand", "soort": "stand", "status": v.get("status", ""), "reden": v.get("reden", ""),
             "tijd": v.get("tijd", ""), "valuta": acc.get("currency", "EUR"), "waarde": acc.get("totalValue"),
             "cash": cash, "belegd": inv.get("currentValue"), "gereserveerd": (acc.get("cash") or {}).get("reservedForOrders"),
             "winst": (inv.get("unrealizedProfitLoss") or 0) + (inv.get("realizedProfitLoss") or 0) if inv else None,
             "orders_aan": bool(_load(Path("config/broker.json")).get("orders_aan"))}]
    port = _load(state_dir / "portfolio.json").get("positions", {})
    have: dict[str, float] = {}
    info: dict[str, dict] = {}
    for p in v.get("posities") or []:
        t = p.get("ticker") or (p.get("instrument") or {}).get("ticker")
        if t:
            have[t] = float(p.get("quantity") or 0)
            wi = p.get("walletImpact") or {}
            info[t] = {"waarde_eur": wi.get("currentValue"), "winst_eur": wi.get("unrealizedProfitLoss"),
                       "koers": p.get("currentPrice"), "gem_prijs": p.get("averagePricePaid") or p.get("averagePrice"),
                       "valuta": (p.get("instrument") or {}).get("currency")}
    onderweg: dict[str, float] = {}
    for o in v.get("open_orders") or []:
        if o.get("ticker"):
            onderweg[o["ticker"]] = onderweg.get(o["ticker"], 0.0) + float(o.get("quantity") or 0)
    bekend = set(have) | set(onderweg) | {o.get("ticker") for h in v.get("geschiedenis") or [] for o in h.get("orders") or []}
    koppeling = dict(v.get("koppeling") or {})
    for y in port:
        if y not in koppeling:  # oudere verslagen: zelfde naam zoeken onder de bekende Trading 212-tickers
            base = y.split(".")[0]
            for t in bekend:
                if t and (t == f"{base}_US_EQ" or (t.startswith(base) and t.endswith("_EQ") and len(t) == len(base) + 4)):
                    koppeling[y] = t
    hand = v.get("handmatig") or {}
    port = dict(port)
    for t, h in hand.items():   # handmatig gekocht en niet bij de trend-agent: ook tonen
        if h.get("yahoo") and h["yahoo"] not in port and float(h.get("qty", 0)) > 0:
            port[h["yahoo"]] = {"qty": 0}
            koppeling[h["yahoo"]] = t
    gezien = set()
    for y, p in port.items():
        t = koppeling.get(y)
        if not t:
            continue
        gezien.add(t)
        hq, oq = have.get(t, 0.0), onderweg.get(t, 0.0)
        bq = max(0.0, float(p.get("qty") or 0) + float(hand.get(t, {}).get("qty", 0)))
        rows.append({"id": "pos-" + t, "soort": "positie", "ticker": t, "yahoo": y, "naam": _name(y), "oefenaccount": hq,
                     "onderweg": oq, "trend_agent": bq, "gelijk": abs(hq - bq) < 1e-6, "onderweg_gelijk": abs(hq + oq - bq) < 1e-6,
                     **info.get(t, {})})
    for t in set(have) | set(onderweg):
        if t not in gezien:
            hq, oq = have.get(t, 0.0), onderweg.get(t, 0.0)
            rows.append({"id": "pos-" + t, "soort": "positie", "ticker": t, "naam": t, "oefenaccount": hq, "onderweg": oq,
                         "trend_agent": 0.0, "gelijk": abs(hq) < 1e-6, "onderweg_gelijk": abs(hq + oq) < 1e-6})
    for i, h in enumerate(reversed(v.get("geschiedenis") or [])):
        for j, o in enumerate(h.get("orders") or []):
            rows.append({"id": f"order-{i}-{j}", "soort": "order", "tijd": h.get("tijd", ""), "ticker": o.get("ticker"),
                         "aantal": o.get("quantity"), "actie": o.get("actie", ""), "waarde_eur": o.get("waarde_eur"), "uitkomst": o.get("uitkomst"),
                         "reden": o.get("reden") or ""})
    return rows


def _p(x: float) -> str:
    return f"{x:+.1%}".replace(".", ",")


def onderzoek_zinnen(onderzoek: dict, books: dict) -> list[str]:
    """Het onderzoek in gewone taal: is er bewijs dat de bots winst maken, en leerde de bot iets nieuws?"""
    rows = onderzoek.get("varianten", [])
    if not rows:
        return []
    out = []
    datum = onderzoek.get("datum", "")
    for bot in ("Trend-agent", "Investeerder"):
        prod = next((r for r in rows if r["bot"] == bot and r["variant"] == "productie"), None)
        if not prod:
            continue
        etf = prod.get("etf_totaal")
        line = (f"{bot}: in de test over 5 jaar werd €10.000 ongeveer €{prod['eindwaarde']:,.0f} "
                f"({_p(prod['totaal'])}, {_p(prod['per_jaar'])} per jaar)").replace(",", ".", 1)
        if etf is not None:
            line += f"; de wereld-ETF deed {_p(etf)}" + (", de bot deed het dus beter." if prod["totaal"] > etf
                                                          else ", gewoon de ETF kopen was dus beter.")
        else:
            line += "."
        out.append(line)
    tested = [r for r in rows if r["variant"] != "productie"]
    good = [r for r in tested if r["oordeel"] == "aanbevolen"]
    pat = [r for r in tested if r.get("patroon")]
    out.append(f"Getest op {datum}: {len(tested)} andere regels, waarvan {len(pat)} op basis van patronen uit de "
               f"grafieken. " + (f"Aanbevolen: {', '.join(r['variant'] for r in good)}. Er staat een voorstel "
                                 "voor je klaar op GitHub; jij beslist." if good else
                                 "Geen enkele was aantoonbaar beter op de ongeziene laatste 30% van de jaren, "
                                 "dus de bot blijft bij zijn huidige regels."))
    for r in pat:
        prod = next((p for p in rows if p["bot"] == r["bot"] and p["variant"] == "productie"), None)
        if prod:
            beter = r["totaal"] > prod["totaal"]
            out.append(f"Patroon '{r['uitleg'].split(': ', 1)[-1].rstrip('.')}' leverde {_p(r['totaal'])} op, "
                       f"tegen {_p(prod['totaal'])} met de huidige regels: "
                       + ("beter, en het haalde alle toetsen." if beter and r["oordeel"] == "aanbevolen" else
                          "op het geheel beter, maar het haalde niet alle toetsen, dus niet overgenomen." if beter else
                          "slechter, dus niet overgenomen."))
    for name, key in (("Trend-agent", "trend"), ("Investeerder", "investeerder")):
        pts = [e for e in books.get(key, {}).get("equity_history", []) if "bench" in e]
        if len(pts) >= 2:
            bot = pts[-1]["equity"] / pts[0]["equity"] - 1
            etf = pts[-1]["bench"] / pts[0]["bench"] - 1
            out.append(f"Live met nepgeld ({len(pts)} handelsdagen): {name} {_p(bot)}, wereld-ETF {_p(etf)}. "
                       "Nog te kort om iets te bewijzen; daar zijn ongeveer 3 maanden voor nodig.")
    out.append("Winst in het verleden is geen garantie voor later. De aandelenlijst is achteraf gekozen, "
               "dus de echte uitkomst zou waarschijnlijk lager zijn geweest.")
    return out


EMPTY = {
    "kansen": "Bij de laatste ronde vond de trend-agent geen koopbare trends, of waren de koersen niet bijgewerkt.",
    "posities": "Geen open posities.",
    "trades": "Nog geen aan- of verkopen.",
    "remmen": "Nog geen gegevens over de remmen.",
    "analyse": "Nog geen analyse.",
    "klaar": "Nog geen gegevens.",
    "koersen": "Nog geen koersen voor grafieken.",
    "controles": "Nog geen controles.",
    "waarde": "Nog geen waarde per dag.",
    "oogopslag": "De samenvatting verschijnt na de volgende ronde van de bots.",
    "onderzoek": "Het wekelijkse onderzoek draait elke zaterdag; de uitkomst verschijnt daarna hier.",
    "onderzoek_samenvatting": "Het wekelijkse onderzoek draait elke zaterdag; de uitkomst verschijnt daarna hier.",
    "patronen": "Nog geen grafieken om patronen in te zoeken.",
    "patronen_samenvatting": "Nog geen grafieken om samen te vatten.",
    "stand": "Nog geen stand.",
    "checks": "Nog geen controles: de bots hebben nog geen ronde gedraaid.",
    "weken": "Nog geen week met gegevens.",
    "gereed": "Nog geen gegevens over klaar voor echt geld.",
    "volglijst": "De volglijst is nog niet bekeken; dat gebeurt elke werkdag in de oefenronde.",
    "broker": "Het oefenaccount van Trading 212 is nog niet gekoppeld.",
}


def write(state_dir: Path, reports_dir: Path, out_dir: Path) -> list[Path]:
    """Een leeg onderdeel krijgt één rij met leeg=true en de reden, zodat het dashboard laat zien
    waarom er niets is (een helemaal leeg bestand kan het dashboard niet lezen)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, rows in build(state_dir, reports_dir).items():
        if not rows:
            rows = [{"id": "leeg", "leeg": True, "reden": EMPTY.get(name, "Nog geen gegevens.")}]
        p = out_dir / f"{name}.json"
        p.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
        paths.append(p)
    return paths
