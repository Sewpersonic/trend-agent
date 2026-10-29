"""Systeemkaart voor het dashboard: hoe de bots samenwerken en waar het nu knelt.

Elk blok van de kaart krijgt een stand (goed / let op / fout) en een korte regel, berekend uit de echte bestanden
van de bots. Klopt er iets niet, dan wordt dat vanzelf een knelpunt met uitleg en een mogelijke oplossing.
Alleen lezen: dit verandert niets aan de bots.

Wordt gemaakt na elke GitHub-run (workflow status) en in de nachtronde. Alleen de standaardbibliotheek,
zodat het ook zonder installatie draait:  PYTHONPATH=src python -m trendagent.systeem
"""

from __future__ import annotations

import csv
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
    NL, NY = ZoneInfo("Europe/Amsterdam"), ZoneInfo("America/New_York")
except Exception:  # noqa: BLE001
    NL = NY = timezone.utc


def _load(p: Path, default=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _tijd(iso: str | None) -> datetime | None:
    if not iso:
        return None
    try:
        t = datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
        return t if t.tzinfo else t.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _eur(v: float) -> str:
    return "€" + f"{v:,.0f}".replace(",", ".")


def _usd(v: float) -> str:
    return "$" + f"{v:,.0f}".replace(",", ".")


def _uur(t: datetime) -> str:
    return t.astimezone(NL).strftime("%d-%m %H:%M")


class Kaart:
    def __init__(self):
        self.nodes: dict[str, dict] = {}
        self.knel: list[dict] = []

    def node(self, nid: str, stand: str, sub: str, uitleg: str = "") -> None:
        self.nodes[nid] = {"id": "n-" + nid, "soort": "node", "node": nid, "stand": stand, "sub": sub, "uitleg": uitleg}

    def knelpunt(self, nid: str, ernst: str, titel: str, wat: str, oplos: str) -> None:
        self.knel.append({"id": f"k-{nid}-{len(self.knel)}", "soort": "knel", "node": nid, "ernst": ernst,
                          "titel": titel, "wat": wat, "oplos": oplos})
        n = self.nodes.get(nid)
        if n and ernst in ("fout", "letop") and n["stand"] == "goed":
            n["stand"] = ernst


def rows(state: Path = Path("state"), dash: Path = Path("dashboard"), root: Path = Path("."),
         nu: datetime | None = None) -> list[dict]:
    nu = nu or datetime.now(timezone.utc)
    nl, ny = nu.astimezone(NL), nu.astimezone(NY)
    werkdag = ny.weekday() < 5
    k = Kaart()

    # ---------- bronnen
    health = _load(state / "health.json", {}) or {}
    tr = health.get("trend") or {}
    br = (tr.get("bronnen") or {})
    if not tr:
        k.node("yahoo", "letop", "nog geen ronde")
    else:
        ok, gevraagd = tr.get("ok", 0), tr.get("gevraagd", 0)
        k.node("yahoo", "goed", f"{ok} van {gevraagd} koersen · {tr.get('day', '')}")
        if tr.get("status") not in ("OK", None) or tr.get("mislukt"):
            k.knelpunt("yahoo", "fout", "Koersen kwamen niet goed binnen",
                       f"Bij de laatste nachtronde kwamen {tr.get('mislukt', 0)} van de {gevraagd} koersen niet binnen "
                       f"(status {tr.get('status')}). De bot koopt dan niets met die aandelen.",
                       "Meestal tijdelijk bij Yahoo. Blijft het, laat Claude de koersbron nakijken (workflow diagnose).")
        if br.get("tweede_bron") == "uit":
            k.nodes["yahoo"]["sub"] = f"{ok} van {gevraagd} · alleen Yahoo"
        elif br.get("tweede_bron") == "geen sleutel":
            k.knelpunt("yahoo", "letop", "De controlebron voor koersen heeft een sleutel nodig",
                       "Stooq controleert de koersen van Yahoo, maar vraagt sinds maart 2026 een gratis sleutel. Zonder die "
                       "sleutel komt alles uit één bron; de andere controles (sprongen, oude koersen, wisselkoers bij de ECB) "
                       "werken wel.",
                       "Vraag een gratis sleutel aan op stooq.com (bij het downloaden van koersen, 'get apikey') en zet hem in "
                       "GitHub als secret STOOQ_APIKEY (Settings → Secrets and variables → Actions). Nooit in de chat.")
        elif "overgeslagen" in str(br.get("tweede_bron", "")) or (br.get("koersen") or {}).get("1 bron") == gevraagd:
            k.knelpunt("yahoo", "letop", "De controlebron voor koersen werkt niet",
                       "De koersen van Yahoo worden normaal gecontroleerd bij Stooq. Stooq gaf geen koersen terug, dus nu "
                       "komt alles uit één bron. Een fout in Yahoo zou dan minder snel opvallen.",
                       "Een andere tweede bron kiezen of Stooq anders aanspreken. Tot die tijd blijven de andere "
                       "controles (sprongen, oude koersen, wisselkoers bij de ECB) gewoon werken.")

    arch = sorted((root / "backtest/daytrade/koersen").glob("*.csv.gz"))
    if arch:
        y, w = arch[-1].name[:8].split("-W")
        laatste = date.fromisocalendar(int(y), int(w), 5)
        k.node("vijfmin", "goed", f"{len(arch)} weken bewaard")
        if (nu.date() - laatste).days > 12:
            k.knelpunt("vijfmin", "letop", "Het archief van 5-minutenkoersen groeit niet",
                       f"De nieuwste bewaarde week is {arch[-1].name[:8]}. Normaal komt er elke zaterdag een week bij.",
                       "Kijk of het zaterdagonderzoek van de daytrader goed liep (tabblad GitHub).")
    else:
        k.node("vijfmin", "letop", "nog niets bewaard")

    bst = next((r for r in (_load(dash / "broker.json", []) or []) if r.get("soort") == "stand"), None)
    if bst:
        t = _tijd(bst.get("tijd"))
        k.node("t212", "fout" if bst.get("status") == "fout" else "goed",
               f"{_eur(bst['waarde'])} · {bst.get('status', '')}" if bst.get("waarde") is not None else bst.get("status", ""))
        if bst.get("status") == "fout":
            k.knelpunt("t212", "fout", "De koppeling met Trading 212 geeft een fout",
                       f"Laatste melding: {bst.get('reden', '')[:160]}", "Zie het tabblad Oefenaccount; vaak is het tijdelijk.")
        elif t and werkdag and 11 <= nl.hour <= 23 and nu - t > timedelta(hours=3):
            k.knelpunt("t212", "letop", "Het oefenaccount is al uren niet bekeken",
                       f"De laatste stand is van {_uur(t)}. Op werkdagen hoort dat elk uur.",
                       "Waarschijnlijk liep de uurlijkse taak van Claude niet. De nachtronde zet het oefenaccount wel gelijk.")
    else:
        k.node("t212", "letop", "nog niet gekoppeld")

    # ---------- starters (GitHub en de taken van Claude)
    gh = [r for r in (_load(dash / "github.json", []) or []) if r.get("workflow") and r.get("soort") != "voorstel"]
    fout = [r for r in gh if r.get("uitkomst") == "fout" and not r.get("opgelost")]
    goed = sum(1 for r in gh if r.get("uitkomst") == "goed")
    k.node("cron", "fout" if fout else "goed", f"{goed} van {len(gh)} runs goed")
    for r in fout[:3]:
        k.knelpunt("cron", "fout", f"{r.get('wat', r['workflow'])} ging mis",
                   f"Run van {_uur(_tijd(r['start']))}: {r.get('uitleg', '')}",
                   "Op het tabblad GitHub staat de run met een link. Gaat een volgende run goed, dan is het vanzelf opgelost.")
    hand = [_tijd(r["start"]) for r in gh if r.get("workflow") == "broker" and r.get("aanleiding") == "met de hand gestart"]
    hand = [t for t in hand if t]
    laatst_uur = max(hand) if hand else None
    k.node("uur", "goed", f"laatst {_uur(laatst_uur)}" if laatst_uur else "werkdagen 09:25–22:25")
    if werkdag and 11 <= nl.hour <= 23 and (not laatst_uur or nu - laatst_uur > timedelta(hours=3)):
        k.knelpunt("uur", "letop", "De uurlijkse taak van Claude liep niet",
                   ("Laatste keer: " + _uur(laatst_uur) + ". " if laatst_uur else "") +
                   "Zonder die taak ververst het oefenaccount niet elk uur en mist de daytrader zijn reserve-start.",
                   "De koopuren van de daytrader starten ook via GitHub zelf. Blijft het uit, vraag Claude de geplande taak na te lopen.")
    k.node("ochtend", "goed", "di–za 07:41")

    # ---------- bots
    pf = _load(state / "portfolio.json", {}) or {}
    stand = {r.get("bot"): r for r in (_load(dash / "stand.json", []) or []) if not r.get("leeg")}
    prod = (_load(root / "config/productie.json", {}) or {}).get("trend") or {}
    max_pos = int(prod.get("max_positions", 3))
    ta = stand.get("Trend-agent") or {}
    if pf and ta.get("waarde"):
        npos = len(pf.get("positions") or {})
        cash = float(pf.get("cash_eur", 0))
        deel = cash / ta["waarde"] if ta["waarde"] else 0
        dicht = sum(1 for t in pf.get("trades", []) if t.get("side") == "SELL")
        k.node("trend", "goed", f"{_eur(ta['waarde'])} · {npos} van {max_pos} plekken")
        if npos >= max_pos and deel > 0.6:
            k.knelpunt("trend", "letop", "De trend-agent staat grotendeels stil",
                       f"Alle {max_pos} plekken zijn bezet en {round(deel * 100)}% van het geld staat op de rekening. "
                       f"Afgesloten trades tot nu toe: {dicht}. Het oefenaccount volgt hem, dus dat staat ook stil.",
                       "Hij koopt pas weer als een stop-loss of trendbreuk een plek vrijmaakt. Meer plekken kan alleen via "
                       "een voorstel van het onderzoek dat jij overneemt.")
    else:
        k.node("trend", "letop", "nog geen stand")
    iv = stand.get("Investeerder") or {}
    k.node("invest", "goed", f"{_eur(iv['waarde'])} · 1× per maand" if iv.get("waarde") else "nog geen stand")
    if iv.get("vs_etf_pct") is not None and iv["vs_etf_pct"] < -0.05:
        k.knelpunt("invest", "letop", "De investeerder blijft achter bij de wereld-ETF",
                   f"Hij doet het {abs(iv['vs_etf_pct']) * 100:.1f}% slechter dan gewoon de wereld-ETF vasthouden.",
                   "Het weekonderzoek test andere verdelingen; een bewezen betere komt als voorstel.")
    pos = [r for r in (_load(dash / "broker.json", []) or []) if r.get("soort") == "positie"]
    if pos:
        gelijk = sum(1 for p in pos if p.get("gelijk"))
        onderweg = sum(1 for p in pos if not p.get("gelijk") and p.get("onderweg_gelijk"))
        k.node("oefen", "goed", f"{gelijk} van {len(pos)} gelijk" + (f" · {onderweg} onderweg" if onderweg else ""))
        if gelijk + onderweg < len(pos):
            k.knelpunt("oefen", "letop", "Het oefenaccount loopt niet gelijk met de trend-agent",
                       f"{len(pos) - gelijk - onderweg} aandeel/aandelen wijken af en er staat geen order onderweg.",
                       "De nachtronde zet het normaal gelijk. Blijft het, kijk op het tabblad Oefenaccount (soms weigert "
                       "Trading 212 een order, bijvoorbeeld als een aandeel daar niet te koop is).")
    else:
        k.node("oefen", "goed", "volgt de trend-agent")

    dts = _load(state / "daytrader.json", {}) or {}
    if dts:
        vandaag = ny.date().isoformat()
        koop = [r for r in dts.get("rondes", []) if str(r.get("ny", "")).startswith(vandaag)
                and "10:00" <= str(r.get("ny", ""))[11:16] <= "12:35"]
        trades = dts.get("trades", [])
        winst = sum(1 for t in trades if t.get("resultaat", 0) > 0)
        k.node("day", "goed", f"{_usd(float(dts.get('equity', 10000)))} · {len(trades)} trades, {winst} winst")
        na_koopuren = werkdag and (ny.hour, ny.minute) >= (12, 45)
        if na_koopuren and len(koop) < 8 and not (dts.get("laatste_ronde") or {}).get("status", "").startswith("beurs dicht"):
            k.knelpunt("day", "letop", "De koopuren van de daytrader liepen niet goed",
                       f"Vandaag {len(koop)} rondes tussen 10:00 en 12:30 New York (verwacht 11). Hij heeft dan "
                       f"uitbraken kunnen missen.",
                       "De beursdag start via drie vroege GitHub-starts en de uurtaak van Claude. Kijk op het tabblad GitHub.")
        middag = [r for r in dts.get("rondes", []) if str(r.get("ny", "")).startswith(vandaag)
                  and "12:45" <= str(r.get("ny", ""))[11:16] <= "15:50"]
        if werkdag and (ny.hour, ny.minute) >= (15, 55) and len(koop) >= 8 and len(middag) < 8 \
                and not (dts.get("vandaag") or {}).get("dag") != vandaag:
            k.knelpunt("day", "letop", "De middag van de daytrader werd niet elk kwartier bewaakt",
                       f"Vandaag {len(middag)} rondes tussen 12:45 en 15:45 New York (verwacht 13). Verkopen gaat wel goed "
                       "(gemiste momenten worden nagespeeld), maar het dashboard liep achter.",
                       "Het koopdeel start het middagdeel zelf; kijk op het tabblad GitHub of dat lukte.")
        if any(r.get("status") == "fout" for r in dts.get("rondes", [])[-6:]):
            k.knelpunt("day", "fout", "Een ronde van de daytrader liep vast",
                       "Een van de laatste rondes eindigde met een fout. Hij heeft dan niets gekocht.",
                       "De volgende ronde probeert het opnieuw; zie het tabblad Daytrader, Laatste ronde.")
    else:
        k.node("day", "letop", "nog geen ronde")

    kill = _load(state / "kill_switch.json", {}) or {}
    if kill.get("active"):
        k.node("rem", "fout", "kill switch staat aan")
        k.knelpunt("rem", "fout", "De noodrem staat aan",
                   f"Reden: {kill.get('reason', 'onbekend')}. De trend-agent koopt niets nieuws; stop-losses blijven werken.",
                   "Lees de reden. Als jij vindt dat het weer kan: workflow practice met 'resume' (alleen jij).")
    else:
        k.node("rem", "goed", "kill switch uit")

    # ---------- onderzoek
    hist = root / "onderzoek/historie.csv"
    laatst_o = None
    try:
        with hist.open(encoding="utf-8") as f:
            ds = [r.get("datum") or r.get("dag") or "" for r in csv.DictReader(f)]
        laatst_o = max(d for d in ds if d) if ds else None
    except (OSError, ValueError):
        pass
    k.node("onderz", "goed", f"laatst {laatst_o}" if laatst_o else "za 07:17")
    if laatst_o and (nu.date() - date.fromisoformat(laatst_o[:10])).days > 8:
        k.knelpunt("onderz", "letop", "Het weekonderzoek liep niet",
                   f"Het laatste onderzoek is van {laatst_o}. Normaal draait het elke zaterdag.",
                   "Kijk op het tabblad GitHub of de run van zaterdag misging.")
    ti = _load(root / "onderzoek/trend_indicatie.json", {}) or {}
    k.node("labelT", "goed", f"{ti.get('signalen', 0)} signalen · " + ("werkt" if (ti.get("toets") or {}).get("werkt")
                                                                       else "nog onbewezen") if ti else "nog geen onderzoek")
    dtr = _load(root / "backtest/daytrade/resultaat.json", {}) or {}
    gem = _tijd(dtr.get("gemaakt"))
    k.node("onderzD", "goed", f"laatst {_uur(gem)[:5]}" if gem else "za 07:41")
    if gem and nu - gem > timedelta(days=8):
        k.knelpunt("onderzD", "letop", "Het daytrade-onderzoek liep niet",
                   f"Het laatste onderzoek is van {_uur(gem)[:5]}. Normaal elke zaterdag.",
                   "Kijk op het tabblad GitHub (workflow daytrade, actie test).")
    di = _load(root / "backtest/daytrade/indicatie.json", {}) or {}
    k.node("labelD", "goed", f"{di.get('uitbraken', 0)} uitbraken · " + ("werkt" if (di.get("toets") or {}).get("werkt")
                                                                        else "nog onbewezen") if di else "nog geen onderzoek")

    # ---------- opslag en jij
    k.node("repo", "goed", "stand en rapporten")
    k.node("dash", "goed", "alle onderdelen")
    vs = [r for r in (_load(dash / "github.json", []) or []) if r.get("soort") == "voorstel"]
    k.node("jij", "goed", f"{len(vs)} voorstel wacht" if vs else "niets wacht op jou")
    for v in vs:
        k.knelpunt("jij", "mens", "Er wacht een voorstel op jou",
                   f"{v.get('titel', 'Voorstel')}. Het gaat pas aan als jij het overneemt.",
                   "Open het voorstel op GitHub en kies Merge (overnemen) of Close (niet).")

    meta = {"id": "meta", "soort": "meta", "gemaakt": nu.isoformat(timespec="seconds"),
            "fout": sum(1 for x in k.knel if x["ernst"] == "fout"), "letop": sum(1 for x in k.knel if x["ernst"] == "letop"),
            "mens": sum(1 for x in k.knel if x["ernst"] == "mens")}
    orde = {"fout": 0, "letop": 1, "mens": 2}
    return [meta] + list(k.nodes.values()) + sorted(k.knel, key=lambda x: orde.get(x["ernst"], 3))


def write(path: Path = Path("dashboard/systeem.json"), **kw) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows(**kw), ensure_ascii=False), encoding="utf-8")
    return path


if __name__ == "__main__":
    p = write()
    data = json.loads(p.read_text(encoding="utf-8"))
    print(f"{p}: {data[0]['fout']} fout, {data[0]['letop']} let op, {data[0]['mens']} wacht op jou")
    for r in data:
        if r["soort"] == "knel":
            print(f"  [{r['ernst']}] {r['titel']}")
