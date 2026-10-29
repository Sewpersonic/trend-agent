"""De daytrade-bot op het dashboard: lessen, onderzochte regels, klaar voor echt geld, controles en weekoverzicht.

Alleen beschrijvend: leest state/daytrader.json en backtest/daytrade/resultaat.json, verandert niets.
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path

from .daytrade_leren import leer, les_tekst, samenvatting

MIN_DAGEN = 40          # ongeveer 2 maanden oefenen
MIN_TRADES = 30
MAX_DALING = -0.05

REGEL_NAMEN = {"dagtrend_filter": "alleen als de daggrafiek van het aandeel stijgt",
               "markt_trend_filter": "niet als de daggrafiek van de markt daalt",
               "indicatie_filter": "geen kansen met een ongunstige indicatie",
               "kopen_tot_11": "alleen kopen tot 11:00"}


def _load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def alle_trades(st: dict) -> list[dict]:
    v = st.get("vandaag") or {}
    out = list(st.get("trades", []))
    if v and not v.get("klaar"):
        out += v.get("trades", [])
    return out


def max_daling(st: dict) -> float:
    peak, mdd = float(st.get("start", 10000.0)), 0.0
    for d in st.get("dagen", []):
        peak = max(peak, d["eind"])
        mdd = min(mdd, d["eind"] / peak - 1)
    return round(mdd, 4)


def actieve_regels(cfg: dict) -> list[str]:
    return [REGEL_NAMEN[k] for k, v in (cfg.get("regels") or {}).items() if k in REGEL_NAMEN and v is True]


def extra_rows(st: dict, test: dict, cfg: dict) -> list[dict]:
    """Lessen (oefenen en test), groepen per kenmerk, onderzochte regels en een eventueel voorstel."""
    rows: list[dict] = []
    oefen = leer(alle_trades(st))
    for i, z in enumerate(samenvatting(oefen, "Oefenen met echte koersen")):
        rows.append({"id": f"les-oefenen-{i}", "soort": "les", "bron": "oefenen", "tekst": z})
    leren = test.get("leren") or {}
    for les in leren.get("lessen") or []:   # tekst opnieuw maken, zodat oude onderzoeken ook de nieuwe korte zinnen tonen
        if {"kenmerk", "groep", "n", "gem_r", "verschil_r"} <= set(les):
            les["tekst"] = les_tekst(les["kenmerk"], les["groep"], les, les["verschil_r"])
    if leren.get("lessen"):   # de belangrijkste les los, voor 'In het kort'
        k = leren["lessen"][0]
        rows.append({"id": "kernles", "soort": "kernles", "kenmerk": k["kenmerk"], "groep": k["groep"],
                     "beter": k.get("soort") == "beter", "n": k["n"], "tekst": k["tekst"]})
    for i, z in enumerate(samenvatting(leren, "Test op oude koersen") if leren else test.get("lessen") or []):
        rows.append({"id": f"les-test-{i}", "soort": "les", "bron": "test", "tekst": z})
    for bron, uit in (("oefenen", oefen), ("test", test.get("leren") or {})):
        for kenmerk, groepen in (uit.get("groepen") or {}).items():
            for g in groepen:
                rows.append({"id": f"g-{bron}-{kenmerk}-{g['groep']}", "soort": "groep", "bron": bron, "kenmerk": kenmerk,
                             "groep": g["groep"], "n": g["n"], "winst_pct": g.get("winst_pct"), "gem_r": g.get("gem_r"),
                             "resultaat": g.get("resultaat")})
    aan = set(actieve_regels(cfg))
    for naam, x in (test.get("varianten") or {}).items():
        s = x.get("stats") or {}
        rows.append({"id": "v-" + naam, "soort": "variant", "naam": naam, "rendement": s.get("rendement"),
                     "trades": s.get("trades"), "winst_pct": s.get("winst_pct"), "gem_r": s.get("gem_r"),
                     "max_daling": s.get("max_daling"),
                     "huidig": (naam == "basis" and not aan) or naam in aan,
                     "uit_grafiek": naam in (REGEL_NAMEN["dagtrend_filter"], REGEL_NAMEN["markt_trend_filter"])})
    if test.get("voorstel"):
        v = test["voorstel"]
        rows.append({"id": "voorstel", "soort": "voorstel", "naam": v["naam"], "tekst": v["tekst"],
                     "aan": v["naam"] in aan})
    ind = test.get("indicatie") or {}
    if ind:
        ts = ind.get("toets") or {}
        rij = {"id": "indicatie", "soort": "indicatie", "uitbraken": ind.get("uitbraken", 0), "zin": ind.get("zin", ""),
               "werkt": bool(ts.get("werkt")), "test_dagen": ts.get("test_dagen"), "aan": "indicatie_filter" in
               {k for k, v in (cfg.get("regels") or {}).items() if v is True}}
        for k, x in (ts.get("per_oordeel") or {}).items():
            rij[f"{k}_n"], rij[f"{k}_r"], rij[f"{k}_winst"] = x["n"], x["gem_r"], x["winst_pct"]
        rows.append(rij)
    if test:
        rows.append({"id": "onderzoek", "soort": "onderzoek", "van": test.get("van", ""), "tot": test.get("tot", ""),
                     "gemaakt": test.get("gemaakt", "")})
    return rows


def gereed_row(st: dict, today: date | None = None) -> dict | None:
    """Klaar voor echt geld? Zelfde opbouw als bij de andere bots."""
    if not st:
        return None
    from .weekoverzicht import _add_trading_days
    today = today or date.today()
    dagen = len(st.get("dagen", []))
    trades = [t for t in st.get("trades", [])]
    n = len(trades)
    gem = sum(t["r"] for t in trades) / n if n else None
    mdd = max_daling(st)
    eisen = [("Oefentijd", "ok" if dagen >= MIN_DAGEN else "bezig"),
             ("Genoeg trades", "ok" if n >= MIN_TRADES else "bezig"),
             ("Gemiddeld winst per trade", "bezig" if n < MIN_TRADES else "ok" if gem and gem > 0 else "nee"),
             ("Grootste daling kleiner dan 5%", "ok" if mdd > MAX_DALING else "nee")]
    ok = sum(1 for e in eisen if e[1] == "ok")
    rest = max(MIN_DAGEN - dagen, 0)
    if ok == len(eisen):
        status, kort = "klaar", "Klaar: alle eisen gehaald. Volgende stap: oefenen bij een broker (Alpaca paper trading)."
    elif any(e[1] == "nee" for e in eisen):
        status, kort = "nee", "Nog niet klaar: een eis wordt niet gehaald."
    else:
        status, kort = "bezig", f"Nog niet klaar: nog {rest} beursdagen oefenen en {max(MIN_TRADES - n, 0)} trades."
    return {"id": "daytrader", "bot": "Daytrader", "status": status, "ok": ok, "totaal": len(eisen), "dagen": dagen,
            "nodig": MIN_DAGEN, "voortgang": round(min(dagen / MIN_DAGEN, 1.0), 4),
            "vroegst": (_add_trading_days(today, rest) if rest else today).isoformat(), "kort": kort,
            "oordeel": "; ".join(f"{a}: {b}" for a, b in eisen)}


def klaar_rows(st: dict) -> list[dict]:
    """De eisen los, voor het tabblad Risico (zelfde vorm als klaar.json)."""
    if not st:
        return []
    dagen = len(st.get("dagen", []))
    trades = st.get("trades", [])
    n = len(trades)
    gem = sum(t["r"] for t in trades) / n if n else None
    mdd = max_daling(st)
    r = lambda v: f"{v:+.2f}".replace(".", ",") + " R"  # noqa: E731
    return [
        {"id": "daytrader-Oefentijd", "bot": "Daytrader", "eis": "Oefentijd", "stand": "ok" if dagen >= MIN_DAGEN else "bezig",
         "nu": f"{dagen} van {MIN_DAGEN} beursdagen (ongeveer 2 maanden)"},
        {"id": "daytrader-Trades", "bot": "Daytrader", "eis": "Genoeg trades", "stand": "ok" if n >= MIN_TRADES else "bezig",
         "nu": f"{n} van {MIN_TRADES}"},
        {"id": "daytrader-Gemiddeld", "bot": "Daytrader", "eis": "Gemiddeld winst per trade",
         "stand": "bezig" if n < MIN_TRADES else "ok" if gem and gem > 0 else "nee",
         "nu": "nog geen trades" if gem is None else f"gemiddeld {r(gem)}"},
        {"id": "daytrader-Daling", "bot": "Daytrader", "eis": "Grootste daling kleiner dan 5%",
         "stand": "ok" if mdd > MAX_DALING else "nee", "nu": f"{mdd * 100:+.2f}%".replace(".", ",")},
    ]


def doel_row(st: dict) -> dict:
    n = len(st.get("trades", [])) if st else 0
    return {"id": "doel-daytrader", "soort": "doel", "week": "", "titel": "Daytrader: leren van zijn trades",
            "waarom": "Bij elke trade legt hij vast hoe de daggrafiek en de markt eruitzagen. Pas met genoeg trades "
                      "zie je in welke situaties daytraden werkt en wanneer niet.",
            "nu": f"{n} van {MIN_TRADES} trades afgesloten", "voortgang": round(min(n / MIN_TRADES, 1.0), 4),
            "status": "klaar" if n >= MIN_TRADES else "bezig", "extra": ""}


def week_zin(st: dict, iso_week: str) -> str | None:
    """Eén zin voor het weekoverzicht: wat deed de daytrader deze week?"""
    ts = [t for t in alle_trades(st) if date.fromisoformat(t["dag"]).isocalendar()[:2] == _wk(iso_week)]
    if not ts:
        return None
    w = sum(1 for t in ts if t["resultaat"] > 0)
    tot = sum(t["resultaat"] for t in ts)
    bedrag = f"{abs(tot):.2f}".replace(".", ",")
    return f"Daytrader: {len(ts)} trades op de Amerikaanse beurs, {w} met winst, samen {'+' if tot >= 0 else '−'}${bedrag}."


def _wk(iso_week: str) -> tuple[int, int]:
    y, w = iso_week.split("-W")
    return int(y), int(w)


def checks(st: dict, now: datetime | None = None) -> list[dict]:
    """Controles in gewone taal, zelfde vorm als controles.rows()."""
    if not st:
        return []
    lr = st.get("laatste_ronde") or {}
    rows: list[dict] = []

    def add(cid: str, vraag: str, stand: str, uitleg: str, detail: str = "") -> None:
        rows.append({"id": "daytrader-" + cid, "bot": "Daytrader", "vraag": vraag, "stand": stand, "uitleg": uitleg,
                     "detail": detail, "dag": str(lr.get("tijd", ""))[:10], "tijd": lr.get("tijd", "")})

    status = lr.get("status", "")
    fout = status == "fout"
    add("ronde", "Is de laatste ronde goed gegaan?", "fout" if fout else "goed",
        "Nee: de ronde liep vast. Hij heeft daarom niets gekocht; de volgende ronde probeert het opnieuw." if fout
        else "Ja, de laatste ronde is goed afgerond.", f"status {status}, {lr.get('ny', '')} New York")
    now = now or datetime.now(timezone.utc)
    try:
        oud = (now - datetime.fromisoformat(lr["tijd"])).total_seconds() / 3600
    except (KeyError, ValueError, TypeError):
        oud = None
    if oud is not None and oud > 80:
        add("bijgewerkt", "Draait hij nog?", "letop",
            f"De laatste ronde is {oud / 24:.0f} dagen geleden. Op beursdagen hoort hij elk uur te draaien.")
    uit = st.get("uitgesloten") or {}
    if uit:
        add("verdacht", "Zitten er rare koerssprongen in?", "letop",
            f"Ja, bij {', '.join(sorted(uit))}. Die koopt hij vandaag voor de zekerheid niet.",
            "; ".join(f"{k}: {v}" for k, v in uit.items())[:200])
    else:
        add("verdacht", "Zitten er rare koerssprongen in?", "goed", "Nee, niets verdachts gevonden.")
    ctx = st.get("dagcontext")
    if ctx is not None:
        add("grafiek", "Zijn de daggrafieken opgehaald?", "goed" if ctx else "letop",
            f"Ja, van {len(ctx)} aandelen. Daarmee legt hij vast hoe de grafiek eruitzag bij elke trade." if ctx
            else "Nee. Hij handelt gewoon, maar kan vandaag minder leren van de grafieken.")
    v = st.get("vandaag") or {}
    if "daglimiet" in (v.get("notities") or []):
        add("daglimiet", "Is de daglimiet geraakt?", "info", "Ja: vandaag 1,5% verlies, dus hij koopt vandaag niets meer.")
    return rows


def load_all(state_dir: Path) -> tuple[dict, dict, dict]:
    return (_load(state_dir / "daytrader.json"), _load(Path("backtest/daytrade/resultaat.json")),
            _load(Path("config/daytrader.json")))
