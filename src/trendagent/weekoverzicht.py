"""Per week: wat de bots deden (orders) en wat ze leerden. En per bot: klaar voor echt geld of nog niet.

Alleen beschrijvend, uit wat de bots al opsloegen. Verandert niets en beslist niets.
"""

from __future__ import annotations

import csv
import re
from datetime import date, timedelta
from pathlib import Path

from .uitleg import MIN_CLOSED_TRADES, MIN_LIVE_DAYS

MAAND = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
BOTS = (("Trend-agent", "trend"), ("Investeerder", "investeerder"))


def _eur(x: float) -> str:
    s = f"{abs(x):,.0f}".replace(",", ".")
    return ("-" if x < 0 else "+" if x > 0 else "") + "€" + s


def _pct(x: float) -> str:
    return (f"{x * 100:+.1f}%").replace(".", ",")


def _day(s: str) -> date | None:
    try:
        return date.fromisoformat(str(s)[:10])
    except ValueError:
        return None


def week_of(d: date) -> tuple[str, date, date]:
    y, w, _ = d.isocalendar()
    mon = d - timedelta(days=d.weekday())
    return f"{y}-W{w:02d}", mon, mon + timedelta(days=4)


def _label(mon: date, fri: date) -> str:
    w = mon.isocalendar()[1]
    if mon.month == fri.month:
        return f"Week {w} · {mon.day}–{fri.day} {MAAND[fri.month - 1]}"
    return f"Week {w} · {mon.day} {MAAND[mon.month - 1]} – {fri.day} {MAAND[fri.month - 1]}"


def _week_result(hist: list[dict], mon: date, fri: date) -> dict | None:
    """Waarde-verandering in de week: laatste stand in de week t.o.v. de laatste stand ervoor."""
    pts = [(_day(e.get("day")), e) for e in hist]
    before = [e for d, e in pts if d and d < mon] or [e for d, e in pts if e.get("day") == "start"]
    inside = [e for d, e in pts if d and mon <= d <= fri + timedelta(days=2)]
    if not inside:
        return None
    a = before[-1] if before else inside[0]
    b = inside[-1]
    out = {"eur": round(b["equity"] - a["equity"], 2), "pct": round(b["equity"] / a["equity"] - 1, 5)}
    if "bench" in a and "bench" in b and a["bench"]:
        out["etf_pct"] = round(b["bench"] / a["bench"] - 1, 5)
    return out


def _onderzoek_rows(onderzoek_dir: Path) -> list[dict]:
    try:
        with (onderzoek_dir / "historie.csv").open(encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except OSError:
        return []


def weken(books: dict, trades: list[dict], broker: dict, onderzoek: dict, onderzoek_dir: Path,
          today: date | None = None, max_weeks: int = 12) -> list[dict]:
    """Rijen voor het dashboard. soort = week (samenvatting + geleerde zinnen), order (wat er gekocht/verkocht is)."""
    today = today or date.today()
    weeks: dict[str, dict] = {}

    def wk(d: date) -> dict:
        key, mon, fri = week_of(d)
        return weeks.setdefault(key, {"key": key, "mon": mon, "fri": fri, "orders": [], "broker": [], "onderzoek": []})

    for t in trades:
        d = _day(t.get("dag"))
        if d:
            wk(d)["orders"].append(t)
    for h in (broker or {}).get("geschiedenis") or []:
        d = _day(h.get("tijd"))
        if d:
            for o in h.get("orders") or []:
                wk(d)["broker"].append(dict(o, tijd=h.get("tijd", "")))
    for r in _onderzoek_rows(onderzoek_dir):
        d = _day(r.get("datum"))
        if d:
            wk(d)["onderzoek"].append(r)
    for _, key in BOTS:
        for e in books.get(key, {}).get("equity_history", []):
            d = _day(e.get("day"))
            if d:
                wk(d)
    if not weeks:
        return leerplan(books, trades, broker, onderzoek, onderzoek_dir)

    from .universe import BY_TICKER
    naam_t212 = {v: (BY_TICKER[k].name if k in BY_TICKER else k) for k, v in ((broker or {}).get("koppeling") or {}).items()}
    sells_total = {name: 0 for name, _ in BOTS}
    rows: list[dict] = []
    for key in sorted(weeks):
        w = weeks[key]
        mon, fri = w["mon"], w["fri"]
        lessen: list[str] = []
        per_bot = {}
        for name, bk in BOTS:
            o = [t for t in w["orders"] if t["bot"] == name]
            buys = [t for t in o if t["soort"] == "koop"]
            sells = [t for t in o if t["soort"] == "verkoop"]
            sells_total[name] += len(sells)
            res = _week_result(books.get(bk, {}).get("equity_history", []), mon, fri)
            closed = [t for t in sells if t.get("resultaat_eur") is not None]
            wins = [t for t in closed if t["resultaat_eur"] > 0]
            per_bot[name] = {"kopen": len(buys), "verkopen": len(sells), "resultaat": res,
                             "vastgezet_eur": round(sum(t["resultaat_eur"] for t in closed), 2)}
            if buys:
                namen = ", ".join(sorted({t["naam"] for t in buys}))
                lessen.append(f"{name} kocht {len(buys)}× ({namen}).")
            if closed:
                best = max(closed, key=lambda t: t["resultaat_eur"])
                lessen.append(f"{name} sloot {len(closed)} trade{'s' if len(closed) != 1 else ''} af: {len(wins)} met winst, "
                              f"samen {_eur(sum(t['resultaat_eur'] for t in closed))}. Beste: {best['naam']} "
                              f"{_eur(best['resultaat_eur'])}.")
            if res and "etf_pct" in res:
                beter = res["pct"] - res["etf_pct"]
                lessen.append(f"{name} {_pct(res['pct'])} deze week, de wereld-ETF {_pct(res['etf_pct'])}: "
                              f"{'beter' if beter > 0.0005 else 'slechter' if beter < -0.0005 else 'gelijk'} dan de markt.")
        n_closed = sells_total["Trend-agent"]
        if n_closed < MIN_CLOSED_TRADES:
            lessen.append(f"Trend-agent heeft nu {n_closed} van de {MIN_CLOSED_TRADES} afgesloten trades die nodig zijn "
                          "om echte conclusies te trekken. Tot die tijd is winst of verlies vooral toeval.")
        b = w["broker"]
        if b:
            ok = [o for o in b if o.get("uitkomst") in ("geplaatst", "uitgevoerd", "ingetrokken")]
            mis = [o for o in b if o.get("uitkomst") not in ("geplaatst", "uitgevoerd", "ingetrokken", "geweigerd")]
            weg = [o for o in b if o.get("uitkomst") == "geweigerd"]
            zin = f"Oefenaccount Trading 212: {len(ok)} order{'s' if len(ok) != 1 else ''} geplaatst"
            if mis:
                zin += f", {len(mis)} mislukt"
            if weg:
                zin += f", {len(weg)} geweigerd door de veiligheidsregels"
            lessen.append(zin + ".")
        if w["onderzoek"]:
            dag = max(r["datum"] for r in w["onderzoek"])
            r_dag = [r for r in w["onderzoek"] if r["datum"] == dag]
            getest = [r for r in r_dag if r.get("oordeel") != "productie"]
            goed = [r for r in getest if r.get("oordeel") == "aanbevolen"]
            lessen.append(f"Onderzoek ({dag}): {len(getest)} andere regels getest op 10 jaar koersen. " +
                          (f"{len(goed)} werkte bewezen beter; dat staat als voorstel klaar en jij beslist."
                           if goed else "Geen enkele was bewezen beter, dus de huidige regels blijven."))
            if onderzoek.get("datum") and week_of(_day(onderzoek["datum"]) or mon)[0] == key:
                for les in (onderzoek.get("lessen") or [])[:3]:
                    lessen.append(_les(str(les.get("tekst", ""))))
        if not w["orders"] and not b:
            lessen.insert(0, "Geen orders deze week: de bots vonden niets dat aan hun regels voldeed, of hielden vast.")
        trend = per_bot["Trend-agent"]
        inv = per_bot["Investeerder"]
        rows.append({
            "id": key, "soort": "week", "week": key, "label": _label(mon, fri),
            "van": mon.isoformat(), "tot": fri.isoformat(), "lopend": mon <= today <= fri + timedelta(days=2),
            "trend_eur": (trend["resultaat"] or {}).get("eur"), "trend_pct": (trend["resultaat"] or {}).get("pct"),
            "inv_eur": (inv["resultaat"] or {}).get("eur"), "inv_pct": (inv["resultaat"] or {}).get("pct"),
            "etf_pct": (trend["resultaat"] or inv["resultaat"] or {}).get("etf_pct"),
            "kopen": trend["kopen"] + inv["kopen"], "verkopen": trend["verkopen"] + inv["verkopen"],
            "oefen_orders": len(b), "geleerd": "\n".join(lessen),
        })
        for i, t in enumerate(sorted(w["orders"], key=lambda t: t["dag"])):
            rows.append({"id": f"{key}-o{i}", "soort": "order", "week": key, "dag": t["dag"], "bot": t["bot"],
                         "ticker": t["ticker"], "naam": t["naam"], "actie": t["soort"], "waarde_eur": t["waarde_eur"],
                         "resultaat_eur": t.get("resultaat_eur"), "reden": _reden(t)})
        for i, o in enumerate(b):
            q = float(o.get("quantity") or 0)
            rows.append({"id": f"{key}-b{i}", "soort": "order", "week": key, "dag": str(o.get("tijd", ""))[:10],
                         "bot": "Oefenaccount", "ticker": o.get("ticker"), "naam": naam_t212.get(o.get("ticker"), o.get("ticker")),
                         "actie": o.get("actie") or ("koop" if q > 0 else "verkoop" if q < 0 else "intrekken"),
                         "waarde_eur": o.get("waarde_eur"), "resultaat_eur": None,
                         "reden": f"{o.get('uitkomst', '')}{': ' + o['reden'] if o.get('reden') else ''}"})
    # Nieuwste week eerst; alleen de laatste weken.
    keep = sorted({r["week"] for r in rows}, reverse=True)[:max_weeks]
    rows = [r for r in rows if r["week"] in keep]
    rows = sorted(rows, key=lambda r: (r["week"], r["soort"] == "week", r.get("dag", "")), reverse=True)
    return rows + leerplan(books, trades, broker, onderzoek, onderzoek_dir)


def leerplan(books: dict, trades: list[dict], broker: dict, onderzoek: dict, onderzoek_dir: Path) -> list[dict]:
    """Wat de bots nog moeten leren of bewijzen, met hoe ver ze zijn. Rijen met soort = doel."""
    out: list[dict] = []

    def add(did: str, titel: str, waarom: str, nu: str, voortgang: float | None, status: str, extra: str = "") -> None:
        out.append({"id": "doel-" + did, "soort": "doel", "week": "", "titel": titel, "waarom": waarom, "nu": nu,
                    "voortgang": None if voortgang is None else round(max(0.0, min(voortgang, 1.0)), 4),
                    "status": status, "extra": extra})

    th = books.get("trend", {}).get("equity_history", [])
    dagen = len([e for e in th if e.get("day") != "start"])
    add("oefentijd", "Lang genoeg oefenen",
        "Een paar goede of slechte dagen zeggen niets. Pas na ongeveer 3 maanden is het meer dan toeval.",
        f"{dagen} van {MIN_LIVE_DAYS} handelsdagen", dagen / MIN_LIVE_DAYS, "klaar" if dagen >= MIN_LIVE_DAYS else "bezig")

    closed = [t for t in trades if t.get("bot") == "Trend-agent" and t.get("soort") == "verkoop" and t.get("resultaat_eur") is not None]
    wins = sum(1 for t in closed if t["resultaat_eur"] > 0)
    add("trades", "Leren van afgesloten trades",
        "Pas als een aandeel weer verkocht is, weet de bot of het kopen een goed idee was. Vanaf 20 trades zoekt hij "
        "uit wanneer kopen goed uitpakt en wanneer niet (bijvoorbeeld bij een rustige of onrustige markt).",
        f"{len(closed)} van {MIN_CLOSED_TRADES} trades afgesloten" + (f", {wins} met winst" if closed else ""),
        len(closed) / MIN_CLOSED_TRADES, "klaar" if len(closed) >= MIN_CLOSED_TRADES else "bezig")

    bench = [e for e in th if e.get("day") != "start" and "bench" in e]
    if len(bench) >= 2:
        diff = (bench[-1]["equity"] / bench[0]["equity"] - 1) - (bench[-1]["bench"] / bench[0]["bench"] - 1)
        nu = f"Trend-agent tot nu toe {_pct(diff)} tegenover de wereld-ETF"
    else:
        diff, nu = None, "nog te weinig dagen om te vergelijken"
    add("etf", "Beter doen dan gewoon de wereld-ETF",
        "Als de bot het niet beter doet dan simpelweg een wereldwijd beursfonds kopen en vasthouden, heeft hij geen zin.",
        nu, None, "bezig")

    datums = sorted({r.get("datum") for r in _onderzoek_rows(onderzoek_dir) if r.get("datum")})
    goed = [r for r in _onderzoek_rows(onderzoek_dir) if r.get("oordeel") == "aanbevolen"]
    add("onderzoek", "Uitzoeken welke regels beter werken",
        "Elke zaterdag test de bot andere regels op 10 jaar koersen, ook patronen uit de grafieken. Alleen een regel die "
        "alle toetsen haalt wordt voorgesteld; jij beslist.",
        f"{len(datums)} keer onderzocht, {len(goed)} betere regel{'s' if len(goed) != 1 else ''} gevonden",
        len(datums) / 12, "bezig", "Doel: 12 weken onderzoek")

    vragen = []
    for les in (onderzoek.get("lessen") or [])[:4]:
        m = re.match(r"(Sterkte|Zwakte): (.+?) = (.+?):", str(les.get("tekst", "")))
        if m:
            wat = m.group(2).replace(" bij instap", "")
            beter = "beter" if m.group(1) == "Sterkte" else "slechter"
            if wat.upper().startswith("RSI"):
                zin = f"Werkt kopen bij RSI {m.group(3)} (hoe snel het aandeel net steeg) echt {beter}?"
            else:
                zin = f"Werkt kopen als de {wat[0].lower() + wat[1:]} {m.group(3)} is echt {beter}?"
            vragen.append(zin + " In oude trades (testperiode) leek dat zo.")
    if vragen:
        add("vragen", "Vragen die hij nog moet beantwoorden",
            "Het onderzoek zag patronen in oude trades. Of die echt kloppen, moet blijken uit nieuwe trades.",
            f"{len(vragen)} open vragen", None, "bezig", "\n".join(vragen))

    ords = [o for h in (broker or {}).get("geschiedenis") or [] for o in h.get("orders") or [] if o.get("quantity") is not None]
    ok = [o for o in ords if o.get("uitkomst") in ("geplaatst", "uitgevoerd", "ingetrokken")]
    add("oefenaccount", "Foutloos handelen bij een echte broker",
        "Het oefenaccount bij Trading 212 bewijst dat de orders in de praktijk goed gaan (juiste aandelen, juiste aantallen).",
        f"{len(ok)} van {len(ords)} orders goed geplaatst" if ords else "nog geen orders", min(len(ok), 20) / 20,
        "klaar" if len(ok) >= 20 and len(ok) == len(ords) else "bezig", "Doel: 20 orders zonder fout")
    return out


def _les(tekst: str) -> str:
    """'Sterkte: RSI bij instap = 70-80: gemiddeld +0.58 R over 54 trades (...)' -> gewone taal."""
    m = re.match(r"(Sterkte|Zwakte): (.+?) = (.+?): gemiddeld ([+-]?[\d.]+) R over (\d+) trades", tekst)
    if not m:
        return "Uit oude trades: " + tekst.split(" Te testen via")[0]
    soort, wat, waarde, r, n = m.groups()
    r = r.replace(".", ",")
    wat = wat.replace(" bij instap", "").strip()
    if not wat[:2].isupper():
        wat = wat[0].lower() + wat[1:]
    return (f"Uit {n} oude trades (testperiode): instappen bij {wat} {waarde} werkte "
            f"{'beter' if soort == 'Sterkte' else 'slechter'} (gemiddeld {r} R per trade). Het onderzoek blijft dit toetsen.")


def _reden(t: dict) -> str:
    r = str(t.get("reden") or "")
    if r.startswith("trend OK"):
        return "Stijgende trend: " + r.split(":", 1)[1].strip().replace("3m", "3 mnd").replace("1m", "1 mnd")
    if r.startswith("doelgewicht"):
        return "Herverdelen naar " + r
    return r


def _add_trading_days(d: date, n: int) -> date:
    while n > 0:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d


def gereed(books: dict, info: dict, today: date | None = None) -> list[dict]:
    """Per bot één rij: klaar voor echt geld ja/nee, hoeveel eisen gehaald, en vanaf wanneer het op zijn vroegst kan."""
    today = today or date.today()
    rows = []
    for name, key in BOTS:
        k = info.get(key, {}).get("klaar")
        if not k:
            continue
        eisen = k["eisen"]
        ok = sum(1 for e in eisen if e[1] == "ok")
        nee = sum(1 for e in eisen if e[1] == "nee")
        days = len([e for e in books.get(key, {}).get("equity_history", []) if e.get("day") != "start"])
        rest = max(MIN_LIVE_DAYS - days, 0)
        vroegst = _add_trading_days(today, rest) if rest else today
        if ok == len(eisen):
            status, kort = "klaar", "Klaar: alle eisen gehaald. Jij beslist of en wanneer."
        elif nee:
            status, kort = "nee", "Nog niet klaar: een eis wordt niet gehaald."
        else:
            status, kort = "bezig", f"Nog niet klaar: nog {rest} handelsdagen oefenen" + (
                f" en {MIN_CLOSED_TRADES} afgesloten trades." if key == "trend" else ".")
        rows.append({"id": key, "bot": name, "status": status, "ok": ok, "totaal": len(eisen), "dagen": days,
                     "nodig": MIN_LIVE_DAYS, "voortgang": round(min(days / MIN_LIVE_DAYS, 1.0), 4),
                     "vroegst": vroegst.isoformat(), "kort": kort, "oordeel": k.get("oordeel", "")})
    t = next((r for r in rows if r["id"] == "trend"), None)
    if t:
        rows.append({**t, "id": "oefenaccount", "bot": "Oefenaccount",
                     "kort": "Volgt de trend-agent, dus dezelfde eisen. " + t["kort"]})
    return rows
