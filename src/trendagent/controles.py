"""Controles in gewone taal voor het dashboard (tabblad Controles).

Per bot een vaste lijst vragen ("Zijn alle koersen binnengekomen?") met een stand: goed, letop, fout of info.
Elke controle heeft een korte uitleg die iedereen snapt, en een technisch detail voor wie het precies wil weten.
Alleen beschrijvend: leest health.json en broker.json, verandert niets.
"""

from __future__ import annotations

import re

TREND = {"stijgend": "stijgt", "dalend": "daalt", "zijwaarts": "beweegt zijwaarts", "onbekend": "is onbekend"}
BEWEEG = {"laag": "rustig", "normaal": "normaal beweeglijk", "hoog": "erg beweeglijk", "onbekend": ""}


def _schoon(tekst: str) -> str:
    """Technische foutmelding zonder html-rommel."""
    t = re.sub(r"\('?<!DOCTYPE.*", "(gaf een webpagina in plaats van koersen)", str(tekst), flags=re.S | re.I)
    return t[:200]


def _bot_checks(name: str, key: str, h: dict) -> list[dict]:
    rows: list[dict] = []

    def add(cid: str, vraag: str, stand: str, uitleg: str, detail: str = "") -> None:
        rows.append({"id": f"{key}-{cid}", "bot": name, "vraag": vraag, "stand": stand, "uitleg": uitleg,
                     "detail": detail, "dag": h.get("day", ""), "tijd": h.get("vastgelegd_utc", "")})

    if not h:
        add("ronde", "Is de ronde gedraaid?", "fout", "Er zijn geen gegevens van de laatste ronde. Kijk op het tabblad GitHub.")
        return rows
    status = str(h.get("status", "?")).upper()
    if h.get("fout"):
        add("ronde", "Is de ronde goed gegaan?", "fout", "De bot liep vast en heeft niets gedaan. Je portefeuille is niet veranderd.",
            _schoon(h["fout"]))
    else:
        add("ronde", "Is de ronde goed gegaan?", "goed" if status == "OK" else "letop",
            "Ja, de bot heeft zijn ronde helemaal afgemaakt." if status == "OK" else
            "De ronde is gedraaid, maar met een waarschuwing (zie hieronder).", f"status {status}, versie {h.get('versie', '?')}")

    gevraagd, ok = int(h.get("gevraagd") or 0), int(h.get("ok") or 0)
    mis = gevraagd - ok
    if gevraagd and not mis:
        add("koersen", "Zijn alle koersen binnengekomen?", "goed", f"Ja, alle {gevraagd} koersen.")
    elif gevraagd and mis / gevraagd < 0.3:
        add("koersen", "Zijn alle koersen binnengekomen?", "letop",
            f"{ok} van de {gevraagd}. Met de ontbrekende aandelen heeft de bot vandaag niets gedaan.")
    else:
        add("koersen", "Zijn alle koersen binnengekomen?", "fout",
            f"Maar {ok} van de {gevraagd}. Te weinig om op te vertrouwen: de bot heeft niets gekocht.")

    src = h.get("bronnen") or {}
    k = src.get("koersen") or {}
    dubbel, een, afw = int(k.get("bevestigd", 0)), int(k.get("1 bron", 0)), int(k.get("afwijking", 0))
    tweede = src.get("tweede_bron", "actief")
    if afw:
        add("bronnen", "Kloppen de koersen met een tweede bron?", "letop",
            f"Bij {afw} aandelen gaven de twee bronnen een andere koers. Die heeft de bot vandaag niet gekocht of verkocht.",
            ", ".join(src.get("afwijkend") or [])[:200])
    elif tweede == "uit":
        add("bronnen", "Kloppen de koersen met een tweede bron?", "info",
            "Er is bewust geen tweede koersbron (jouw keuze). De koersen van Yahoo worden wel gecontroleerd op rare "
            "sprongen en of ze vers zijn, en de wisselkoers bij de ECB. Voor echt geld is een tweede bron verstandig.")
    elif tweede != "actief" and een:
        add("bronnen", "Kloppen de koersen met een tweede bron?", "letop",
            "Dit kon vandaag niet worden gecontroleerd: de tweede koersbron werkte niet. De bot gebruikte alleen "
            "Yahoo. Die koersen zijn wel gecontroleerd op rare sprongen en of ze vers zijn. Geen probleem, wel goed om te weten.",
            f"tweede bron {tweede}" + (f": {_schoon(src['fout_tweede_bron'])}" if src.get("fout_tweede_bron") else ""))
    elif dubbel:
        add("bronnen", "Kloppen de koersen met een tweede bron?", "goed",
            f"Ja, {dubbel} koersen zijn bevestigd door twee bronnen." + (f" {een} kwamen uit één bron." if een else ""))
    wk = src.get("wisselkoers") or h.get("wisselkoers")
    if wk:
        goed = wk in ("bevestigd", "ok")
        add("fx", "Klopt de wisselkoers dollar-euro?", "goed" if goed else "letop",
            "Ja, de wisselkoers is gecontroleerd." if goed else "De wisselkoers kon niet dubbel worden gecontroleerd.",
            f"wisselkoers: {wk}")

    oud = int(h.get("verouderd") or 0)
    add("vers", "Zijn de koersen van vandaag?", "goed" if not oud else "letop",
        "Ja, alle koersen zijn van de laatste handelsdag." if not oud else
        f"{oud} koersen waren nog niet bijgewerkt. Die aandelen heeft de bot vandaag niet gekocht.")

    verdacht = h.get("verdacht") or {}
    add("verdacht", "Zitten er rare koerssprongen in?", "goed" if not verdacht else "letop",
        "Nee, niets verdachts gevonden." if not verdacht else
        f"Ja, bij {', '.join(sorted(verdacht))}. Die heeft de bot voor de zekerheid niet gekocht.",
        "; ".join(f"{t}: {', '.join(v) if isinstance(v, list) else v}" for t, v in verdacht.items())[:200])

    for i, w in enumerate((h.get("waarschuwingen") or [])[:5]):
        ks = "Kill switch" in w
        add(f"w{i}", "Kill switch aan" if ks else "Waarschuwing van de bot", "fout" if ks else "letop", _schoon(w))

    reg = str(h.get("regime") or "onbekend-onbekend")
    trend, _, beweeg = reg.partition("-")
    zin = f"De markt {TREND.get(trend, trend)}" + (f" en is {BEWEEG.get(beweeg, beweeg)}" if BEWEEG.get(beweeg, beweeg) else "") + "."
    add("markt", "Hoe staat de markt ervoor?", "info", zin + " Dit is geen fout, alleen ter informatie.", f"marktregime {reg}")
    return rows


def _broker_checks(b: dict, gelijk: tuple[int, int, int] | None) -> list[dict]:
    rows: list[dict] = []
    if not b:
        return rows

    def add(cid: str, vraag: str, stand: str, uitleg: str, detail: str = "") -> None:
        rows.append({"id": f"broker-{cid}", "bot": "Oefenaccount", "vraag": vraag, "stand": stand, "uitleg": uitleg,
                     "detail": detail, "dag": str(b.get("tijd", ""))[:10], "tijd": b.get("tijd", "")})

    st = b.get("status", "")
    fout = st in ("fout", "deels mislukt")
    add("koppeling", "Werkt de koppeling met Trading 212?", "fout" if fout else "goed",
        ("Nee: " + (b.get("reden") or "er ging iets mis.") + " De bots zelf draaien gewoon door.") if fout else
        "Ja, de bot kon het oefenaccount lezen.", f"status {st}")
    if gelijk:
        g, onderweg, tot = gelijk
        if g == tot:
            add("gelijk", "Klopt het met de trend-agent?", "goed", f"Ja, alle {tot} aandelen staan gelijk.")
        elif g + onderweg == tot:
            add("gelijk", "Klopt het met de trend-agent?", "info",
                f"{g} van de {tot} staan al gelijk, {onderweg} zijn onderweg: die worden gekocht zodra de beurs opengaat.")
        else:
            add("gelijk", "Klopt het met de trend-agent?", "letop",
                f"{g} van de {tot} staan gelijk. De rest wordt bij de volgende ronde gelijkgezet.")
    if b.get("niet_gekoppeld"):
        add("niet", "Kan alles bij Trading 212 gekocht worden?", "info",
            "Niet alles: " + ", ".join(b["niet_gekoppeld"]) + " is daar niet te koop. Dat slaat het oefenaccount over.")
    return rows


def rows(health: dict, broker: dict, broker_pos: list[dict]) -> list[dict]:
    out = []
    for name, key in (("Trend-agent", "trend"), ("Investeerder", "investeerder")):
        out += _bot_checks(name, key, health.get(key, {}))
    pos = [r for r in broker_pos if r.get("soort") == "positie"]
    g = (sum(1 for p in pos if p.get("gelijk")), sum(1 for p in pos if not p.get("gelijk") and p.get("onderweg_gelijk")),
         len(pos)) if pos else None
    out += _broker_checks(broker, g)
    return out
