"""Uitleg van de analyse: HOE de bot kijkt, WAT hij ziet en WAT hij eruit haalt.

Alleen uitleg voor de mens. Deze module beslist niets en verandert geen portefeuille.
Ook de "Klaar voor echt geld?"-lijst beslist niets: hij laat zien hoe ver de bot is
met bewijzen dat hij werkt. De beslissing om ooit echt geld te gebruiken neem jij.
"""

from __future__ import annotations

from .features import realized_vol
from .insights import _eur, _n, _pct
from .signals import sma

# Eisen voordat de volgende stap (oefenaccount bij een echte broker) zinvol is.
MIN_LIVE_DAYS = 63          # ongeveer 3 maanden handelsdagen
MIN_CLOSED_TRADES = 20
MAX_EXTRA_DRAWDOWN = 0.05   # investeerder: niet meer dan 5 procentpunt diepere daling dan de ETF

TREND_METHOD = """<details><summary>Zo analyseert de trend-agent (klik om te openen)</summary>

1. **Data controleren.** Koersen van Yahoo, gecontroleerd bij een tweede bron en de wisselkoers bij de ECB.
   Bevroren koersen, rare sprongen of achterlopende markten: dat instrument wordt die dag niet gekocht.
2. **De markt als geheel.** Aan de hand van de wereld-ETF (IWDA) of de S&P 500: staat de koers boven het
   200-daags gemiddelde (stijgend), eronder (dalend) of ertussenin (zijwaarts)? En beweegt de markt meer of
   minder dan normaal vergeleken met het afgelopen jaar? Plus: hoeveel aandelen staan boven hun 200-daags gemiddelde (de breedte).
3. **Elk instrument door de zeef.** Een trend telt alleen als ALLES klopt: koers boven het 50-daags gemiddelde en
   dat boven het 200-daags, plus over 1 en 3 maanden gestegen, genoeg handel en geen verdachte sprong.
4. **Rangschikken.** Score = stijging (60% 3 maanden, 40% 1 maand) gedeeld door de beweeglijkheid. Een rustige,
   stevige stijger wint van een wilde.
5. **Risico bepalen.** Stop-loss op 2x de gemiddelde dagbeweging (ATR) onder de instap. Het aantal stuks wordt zo
   gekozen dat de stop hooguit 0,25% van het vermogen kost.
6. **Beheren.** De stop schuift mee omhoog (3x ATR onder de hoogste slotkoers). Verkopen bij stop of als de koers
   onder het 50-daags gemiddelde sluit.

</details>"""

INVESTOR_METHOD = """<details><summary>Zo analyseert de investeerder (klik om te openen)</summary>

1. **Kern (60%):** de wereld-ETF (IWDA), altijd.
2. **Satelliet (30%):** de 5 aandelen of ETF's met de grootste stijging over 12 maanden (de laatste maand niet
   meegeteld, omdat die vaak terugveert), alleen als ze boven hun 200-daags gemiddelde staan en genoeg verhandeld worden.
3. **Crypto (10%):** Bitcoin en Ethereum, alleen als ze boven hun 200-daags gemiddelde staan; anders kas.
4. **Eén keer per maand** wordt alles teruggezet naar deze verdeling. Tussendoor kijkt hij elke dag mee, maar handelt niet.

</details>"""


# ------------------------------------------------------------------ de markt

def market_view(bars: dict, regime, region_of: dict) -> dict:
    """Cijfers achter het marktregime, plus de breedte: hoeveel instrumenten in een stijgende trend staan."""
    out = {"regime": regime.label, "trend": regime.trend, "beweeglijkheid": regime.beweeglijkheid,
           "bron": regime.bron}
    b = bars.get(regime.bron)
    if b and len(b) >= 260:
        closes = [x.close for x in b]
        vols = [realized_vol(closes[:i], 20) for i in range(len(closes) - 230, len(closes) + 1, 5)]
        out.update(koers=round(closes[-1], 2), sma50=round(sma(closes, 50), 2), sma200=round(sma(closes, 200), 2),
                   afstand_sma200=round(closes[-1] / sma(closes, 200) - 1, 4),
                   maand=round(closes[-1] / closes[-22] - 1, 4),
                   vol_nu=round(vols[-1], 3), vol_mediaan=round(sorted(vols)[len(vols) // 2], 3))
    above = {"EU": [0, 0], "US": [0, 0]}
    for t, bb in bars.items():
        reg = region_of.get(t)
        if reg not in above or len(bb) < 200:
            continue
        closes = [x.close for x in bb]
        above[reg][1] += 1
        above[reg][0] += closes[-1] > sma(closes, 200)
    tot = [above["EU"][0] + above["US"][0], above["EU"][1] + above["US"][1]]
    out["breedte"] = {k: v for k, v in (("totaal", tot), ("EU", above["EU"]), ("US", above["US"])) if v[1]}
    return out


def _share(v) -> float:
    return v[0] / v[1] if v and v[1] else 0.0


def market_lines(m: dict) -> list[str]:
    lines = []
    if "koers" in m:
        pos = "boven" if m["afstand_sma200"] > 0 else "onder"
        lines.append(f"- **Markt ({m['bron']}):** koers {_n(m['koers'], 2)}, {_pct(abs(m['afstand_sma200']))[1:]} {pos} "
                     f"het 200-daags gemiddelde ({_n(m['sma200'], 2)}); de afgelopen maand {_pct(m['maand'])}. "
                     f"Trend: **{m['trend']}**.")
        lines.append(f"- **Beweeglijkheid:** {_n(m['vol_nu'] * 100, 0)}% op jaarbasis, tegen normaal "
                     f"{_n(m['vol_mediaan'] * 100, 0)}% het afgelopen jaar: **{m['beweeglijkheid']}**.")
    else:
        lines.append(f"- **Markt:** {m.get('regime', 'onbekend')} (te weinig historie voor details).")
    br = m.get("breedte", {})
    if br.get("totaal"):
        parts = [f"{k} {v[0]} van {v[1]}" for k, v in br.items() if k != "totaal"]
        lines.append(f"- **Breedte:** {br['totaal'][0]} van de {br['totaal'][1]} instrumenten staan boven hun 200-daags "
                     f"gemiddelde ({_share(br['totaal']):.0%}; " + ", ".join(parts) + ").")
    return lines


def market_conclusions(m: dict, bot: str = "trend") -> list[str]:
    if bot == "investeerder":
        return _investor_market(m)
    out = []
    breadth = _share(m.get("breedte", {}).get("totaal"))
    if m.get("trend") == "stijgend" and breadth >= 0.6:
        out.append("De markt stijgt breed: goede omstandigheden voor trendvolgen.")
    elif m.get("trend") == "stijgend":
        out.append("De markt stijgt, maar gedragen door een minderheid van de aandelen: kwetsbaarder dan het lijkt.")
    elif m.get("trend") == "dalend":
        out.append("De markt daalt: weinig echte trends, meer kans dat nieuwe posities op de stop uitkomen.")
    elif m.get("trend") == "zijwaarts":
        out.append("De markt beweegt zijwaarts: trends houden vaak kort stand, verwacht meer kleine verliezen.")
    if m.get("beweeglijkheid") == "hoog":
        out.append("De markt beweegt meer dan normaal: stops worden sneller geraakt. Het risico per trade blijft gelijk, "
                   "dus de posities worden vanzelf kleiner.")
    elif m.get("beweeglijkheid") == "laag":
        out.append("De markt is rustig: stops liggen dichterbij, posities kunnen iets groter.")
    br = m.get("breedte", {})
    if br.get("EU") and br.get("US"):
        eu, us = _share(br["EU"]), _share(br["US"])
        if abs(eu - us) >= 0.2:
            lead, lag = ("Europa", "Amerika") if eu > us else ("Amerika", "Europa")
            out.append(f"{lead} staat er duidelijk beter voor dan {lag} ({max(eu, us):.0%} tegen {min(eu, us):.0%} in een stijgende trend).")
    return out


def _investor_market(m: dict) -> list[str]:
    out = []
    t = m.get("trend")
    if t == "stijgend":
        out.append("De markt stijgt: de kern (wereld-ETF) doet zijn werk, de sterkste aandelen lopen mee.")
    elif t == "dalend":
        out.append("De markt daalt: de investeerder verkoopt daar niet op, hij blijft gespreid. Bij de herverdeling "
                   "vallen aandelen onder hun 200-daags gemiddelde vanzelf af.")
    elif t == "zijwaarts":
        out.append("De markt beweegt zijwaarts: geen reden om iets aan de verdeling te veranderen.")
    if m.get("beweeglijkheid") == "hoog":
        out.append("De markt beweegt meer dan normaal: grotere schommelingen in de waarde zijn te verwachten; "
                   "de spreiding over 60% wereld-ETF dempt dat.")
    return out


# ------------------------------------------------------------------ de zeef (trend-agent)

RULES = (("te weinig historie", "te weinig koersgeschiedenis"),
         ("data te oud", "koers te oud"),
         ("geen stijgende trend", "geen stijgende trend (koers niet boven 50- en 200-daags gemiddelde)"),
         ("rendement", "niet gestegen over 1 of 3 maanden"),
         ("te weinig handel", "te weinig handel"),
         ("verdachte dagsprong", "verdachte dagsprong"))


def funnel(analyses: dict, suspicious: dict) -> dict:
    counts = {label: 0 for _, label in RULES}
    for a in analyses.values():
        for key, label in RULES:
            if any(r.startswith(key) for r in a.reasons):
                counts[label] += 1
    passed = [t for t, a in analyses.items() if a.is_candidate]
    return {"bekeken": len(analyses), "afgevallen": {k: v for k, v in counts.items() if v},
            "door_zeef": len(passed), "verdacht": len([t for t in passed if t in suspicious]),
            "kandidaten": len([t for t in passed if t not in suspicious])}


def funnel_lines(f: dict) -> list[str]:
    lines = [f"- **Bekeken:** {f['bekeken']} instrumenten."]
    if f["afgevallen"]:
        lines.append("- **Afgevallen** (een instrument kan op meer regels afvallen): "
                     + "; ".join(f"{k}: {v}" for k, v in f["afgevallen"].items()) + ".")
    extra = f", waarvan {f['verdacht']} met verdachte data (niet koopbaar)" if f["verdacht"] else ""
    lines.append(f"- **Door de zeef:** {f['door_zeef']}{extra}. Koopbare trends: **{f['kandidaten']}**.")
    return lines


def trend_conclusions(f: dict, kansen: list[dict], free_slots: int, bought: list[str], region_of: dict) -> list[str]:
    out = []
    if f["bekeken"]:
        share = f["kandidaten"] / f["bekeken"]
        if share < 0.1:
            out.append(f"Maar {f['kandidaten']} van de {f['bekeken']} instrumenten zijn een koopbare trend: weinig keus, "
                       "de bot is daardoor vanzelf voorzichtig.")
        elif share > 0.4:
            out.append(f"{f['kandidaten']} van de {f['bekeken']} instrumenten zijn een koopbare trend: veel keus, "
                       "de bot neemt alleen de rustigste, sterkste.")
    if kansen:
        regions = [region_of.get(k["ticker"]) for k in kansen]
        for reg, name in (("US", "Amerikaanse"), ("EU", "Europese")):
            if regions.count(reg) >= 4:
                out.append(f"De sterkste trends zijn vooral {name} instrumenten.")
        hot = [k["ticker"] for k in kansen if k["moment"] == "opgelopen"]
        if len(hot) >= 3:
            out.append(f"{len(hot)} van de {len(kansen)} sterkste staan al ver boven hun gemiddelde ({', '.join(hot)}): "
                       "de trend is sterk, maar instappen op zo'n moment kost vaker een terugval.")
        calm = [k["ticker"] for k in kansen if k["moment"] == "gunstig"]
        if calm:
            out.append("Sterk zonder ver weggelopen te zijn: " + ", ".join(calm) + ".")
    if bought:
        out.append("Gekocht vandaag: " + ", ".join(bought) + ".")
    elif free_slots <= 0:
        out.append("Alle plekken zijn bezet, dus de bot koopt niets bij, hoe sterk een trend ook is.")
    elif f["kandidaten"]:
        out.append("Er waren trends, maar geen enkele paste binnen de risicoregels (zie Kansen voor de reden per ticker).")
    return out


# ------------------------------------------------------------------ investeerder

def investor_view(bars: dict, momentum: dict, held: set, picks: list[str], crypto: list[str]) -> dict:
    top = sorted(((m, t) for t, m in momentum.items() if t in picks), reverse=True)
    cr = {}
    for t in crypto:
        b = bars.get(t)
        if b and len(b) >= 200:
            closes = [x.close for x in b]
            cr[t] = {"boven_sma200": closes[-1] > sma(closes, 200), "afstand": round(closes[-1] / sma(closes, 200) - 1, 4)}
    sat_held = sorted(t for t in held if t not in crypto and t not in ("IWDA.AS", "SPY"))
    return {"keuze_nu": [{"ticker": t, "momentum": m} for m, t in top],
            "satelliet_bezit": sat_held,
            "uit_top": [t for t in sat_held if t not in picks],
            "nieuw_in_top": [t for t in picks if t not in held],
            "crypto": cr}


def investor_lines(v: dict, names: dict) -> list[str]:
    lines = []
    if v["keuze_nu"]:
        lines.append("- **Sterkste momentum nu (12 maanden, zonder laatste maand):** "
                     + ", ".join(f"{names.get(x['ticker'], x['ticker'])} {_pct(x['momentum'], 0)}" for x in v["keuze_nu"]) + ".")
    for t, c in v["crypto"].items():
        state = "boven" if c["boven_sma200"] else "onder"
        lines.append(f"- **{t}:** {_pct(abs(c['afstand']))[1:]} {state} het 200-daags gemiddelde"
                     f" ({'mag in de mix' if c['boven_sma200'] else 'blijft in kas'}).")
    return lines


def investor_conclusions(v: dict, next_rebalance: str) -> list[str]:
    out = []
    if v["satelliet_bezit"] and not v["uit_top"]:
        out.append("Alle satellietposities horen nog bij de sterkste 5: de keuze van deze maand houdt stand.")
    if v["uit_top"]:
        out.append(f"Uit de top gevallen: {', '.join(v['uit_top'])}. Blijft dat zo, dan worden ze bij de volgende "
                   f"herverdeling ({next_rebalance}) vervangen door {', '.join(v['nieuw_in_top']) or 'iets anders'}.")
    off = [t for t, c in v["crypto"].items() if not c["boven_sma200"]]
    if off:
        out.append(f"{', '.join(off)} staat onder het 200-daags gemiddelde: bij de volgende herverdeling gaat dat deel naar kas.")
    return out


# ------------------------------------------------------------------ leren en klaar voor echt geld

def _max_drawdown(values: list[float]) -> float:
    peak, worst = 0.0, 0.0
    for v in values:
        peak = max(peak, v)
        if peak:
            worst = min(worst, v / peak - 1)
    return worst


def readiness(bot: str, equity_history: list[dict], r_values: list[float]) -> dict:
    """Hoe ver de bot is met bewijzen dat hij werkt. Beslist niets."""
    pts = [e for e in equity_history if e.get("day") != "start"]
    days = len(pts)
    checks = []
    checks.append(("Oefentijd", "ok" if days >= MIN_LIVE_DAYS else "bezig",
                   f"{days} van {MIN_LIVE_DAYS} handelsdagen (ongeveer 3 maanden)"))
    bench = [e for e in pts if "bench" in e]
    if len(bench) >= 2:
        diff = (bench[-1]["equity"] / bench[0]["equity"] - 1) - (bench[-1]["bench"] / bench[0]["bench"] - 1)
        state = ("ok" if diff >= 0 else "nee") if days >= MIN_LIVE_DAYS else "bezig"
        checks.append(("Minstens zo goed als de wereld-ETF", state, f"verschil tot nu toe {_pct(diff, 2)}"))
    else:
        checks.append(("Minstens zo goed als de wereld-ETF", "bezig", "nog te weinig dagen"))
    dd = _max_drawdown([e["equity"] for e in equity_history])
    if bot == "trend":
        checks.append(("Grootste daling onder 5%", "ok" if dd > -0.05 else "nee", f"grootste daling tot nu toe {_pct(dd, 2)}"))
        n = len(r_values)
        if n >= MIN_CLOSED_TRADES:
            avg = sum(r_values) / n
            checks.append(("Genoeg afgesloten trades", "ok", f"{n} trades"))
            checks.append(("Gemiddeld winst per trade", "ok" if avg > 0 else "nee", f"gemiddeld {_n(avg, 2, True)} R"))
        else:
            checks.append(("Genoeg afgesloten trades", "bezig", f"{n} van {MIN_CLOSED_TRADES}"))
    else:
        bdd = _max_drawdown([e["bench"] for e in bench]) if bench else 0.0
        checks.append(("Daling niet veel dieper dan de ETF", "ok" if dd >= bdd - MAX_EXTRA_DRAWDOWN else "nee",
                       f"bot {_pct(dd, 2)}, ETF {_pct(bdd, 2)}"))
    if all(c[1] == "ok" for c in checks):
        verdict = "Alle eisen gehaald. Volgende stap kan: een oefenaccount bij een echte broker. Jij beslist."
    elif any(c[1] == "nee" for c in checks):
        verdict = "Nog niet klaar: een eis wordt niet gehaald. Blijven oefenen en kijken waarom."
    else:
        verdict = "Nog niet klaar: de bot is nog bezig met bewijzen. Blijven oefenen."
    return {"eisen": checks, "oordeel": verdict}


ICON = {"ok": "✅", "bezig": "⏳", "nee": "❌"}


def readiness_lines(name: str, r: dict) -> list[str]:
    lines = [f"**{name}:** {r['oordeel']}", "", "| Eis | Stand | Nu |", "| --- | --- | --- |"]
    lines += [f"| {label} | {ICON[state]} | {detail} |" for label, state, detail in r["eisen"]]
    return lines


def learning_lines(r_values: list[float], pnl: float) -> list[str]:
    n = len(r_values)
    if not n:
        return ["- Nog geen afgesloten trades. Leren begint pas als trades zijn afgesloten: dan weet de bot of een "
                "instap goed of slecht uitpakte, en onder welke omstandigheden."]
    wins = sum(r > 0 for r in r_values)
    avg = sum(r_values) / n
    lines = [f"- {n} afgesloten trades: {wins} met winst ({wins / n:.0%}), gemiddeld {_n(avg, 2, True)} R per trade "
             f"(R = winst of verlies gedeeld door het risico bij instap), totaal {_eur(pnl)}."]
    if n < MIN_CLOSED_TRADES:
        lines.append(f"- Pas vanaf {MIN_CLOSED_TRADES} trades trekt de bot conclusies over welke omstandigheden goed of "
                     "slecht uitpakken; met minder is het vooral toeval. Het wekelijkse onderzoek (zaterdag) doet dat.")
    else:
        lines.append("- Het wekelijkse onderzoek (zaterdag) zoekt in deze trades naar patronen. Zie `onderzoek/LAATSTE.md`.")
    return lines


# ------------------------------------------------------------------ in één oogopslag (dashboard)

MAANDEN = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober",
           "november", "december"]


def oogopslag(bot: str, d: dict) -> list[dict]:
    """Eenvoudige tegels per bot: onderwerp, waarde, kleur (goed/letop/slecht/neutraal) en uitleg in gewone taal.
    Plus één regel 'kort gezegd'. Alleen uit cijfers die de bot al berekende."""
    m = d.get("markt") or {}
    if not m:
        return []
    rows = []
    trend = m.get("trend", "onbekend")
    afst = m.get("afstand_sma200")
    t_kleur = {"stijgend": "goed", "dalend": "slecht", "zijwaarts": "letop"}.get(trend, "neutraal")
    t_uitleg = "De wereldwijde beurs (wereld-ETF) "
    if afst is not None:
        t_uitleg += (f"staat {abs(afst) * 100:.1f}% {'boven' if afst > 0 else 'onder'} zijn gemiddelde van de "
                     f"laatste 200 dagen.").replace(".", ",", 1)
    else:
        t_uitleg += "heeft te weinig historie."
    rows.append({"tegel": "Markt", "waarde": {"stijgend": "Stijgt", "dalend": "Daalt", "zijwaarts": "Zijwaarts"}
                 .get(trend, "Onbekend"), "kleur": t_kleur, "uitleg": t_uitleg})

    bw = m.get("beweeglijkheid", "onbekend")
    rows.append({"tegel": "Onrust", "waarde": {"laag": "Rustig", "normaal": "Normaal", "hoog": "Onrustig"}.get(bw, "Onbekend"),
                 "kleur": {"laag": "goed", "normaal": "neutraal", "hoog": "letop"}.get(bw, "neutraal"),
                 "uitleg": {"laag": "Koersen bewegen minder dan normaal. Minder kans op plotselinge dalingen.",
                            "normaal": "Koersen bewegen zoals gewoonlijk.",
                            "hoog": "Koersen schieten meer op en neer dan normaal. " + (
                                "Grotere kans dat een stop-loss wordt geraakt." if bot == "trend"
                                else "De waarde schommelt dan ook meer.")}
                 .get(bw, "Te weinig gegevens.")})

    br = (m.get("breedte") or {})
    tot = br.get("totaal")
    if tot and tot[1]:
        share = tot[0] / tot[1]
        extra = ""
        if br.get("EU") and br.get("US") and br["EU"][1] and br["US"][1]:
            extra = f" Amerika {br['US'][0] / br['US'][1]:.0%}, Europa {br['EU'][0] / br['EU'][1]:.0%}."
        rows.append({"tegel": "Hoeveel stijgt er?", "waarde": f"{share:.0%}",
                     "kleur": "goed" if share >= 0.6 else "letop" if share >= 0.4 else "slecht",
                     "uitleg": f"{tot[0]} van de {tot[1]} aandelen zitten in een stijgende trend.{extra}"})

    if bot == "trend":
        z = d.get("zeef") or {}
        n = z.get("kandidaten", 0)
        free = d.get("vrije_plekken", 0)
        gek = d.get("gekocht") or []
        if gek:
            act = "Gekocht vandaag: " + ", ".join(gek) + "."
        elif free <= 0:
            act = "Alle 3 plekken zijn bezet, dus de bot koopt nu niets bij."
        elif n:
            act = "Er waren kansen, maar geen paste binnen de risicoregels."
        else:
            act = "Niets dat aan alle regels voldoet, dus de bot wacht."
        rows.append({"tegel": "Koopbare trends", "waarde": str(n), "kleur": "goed" if n >= 5 else "letop" if n else "slecht",
                     "uitleg": f"{n} van de {z.get('bekeken', '?')} aandelen voldoen aan alle regels. {act}"})
        if t_kleur == "goed" and tot and tot[0] / tot[1] >= 0.6:
            kort = "Goede omstandigheden: de markt stijgt breed."
        elif trend == "dalend":
            kort = "Lastige markt: de beurs daalt, de bot is voorzichtig."
        elif trend == "zijwaarts":
            kort = "Geen duidelijke richting: trends houden vaak kort stand."
        else:
            kort = "De markt stijgt, maar niet breed: wat kwetsbaarder."
        rows.insert(0, {"tegel": "kort", "waarde": "", "kleur": t_kleur, "uitleg": kort + " " + act})
    else:
        b = d.get("beeld") or {}
        uit = b.get("uit_top") or []
        nxt = d.get("volgende_herverdeling", "")
        when = ""
        if nxt:
            y, mo, _ = nxt.split("-")
            when = f"begin {MAANDEN[int(mo) - 1]}"
        rows.append({"tegel": "Keuzes nog goed?", "waarde": "Ja" if not uit else f"{len(uit)} wankelen",
                     "kleur": "goed" if not uit else "letop",
                     "uitleg": ("Alle aandelen die hij koos horen nog bij de sterkste 5." if not uit else
                                "Uit de top 5 gevallen: " + ", ".join(uit) + f". Blijft dat zo, dan wisselt hij ze {when}.")})
        kort = ("De investeerder houdt zijn verdeling vast en herverdeelt " + (when or "volgende maand") + ".")
        if trend == "dalend":
            kort = "De beurs daalt; de investeerder verkoopt daar niet op en blijft gespreid. " + kort
        rows.insert(0, {"tegel": "kort", "waarde": "", "kleur": t_kleur, "uitleg": kort})
    return rows


def kleur_van(tekst: str) -> str:
    """Grove indeling van een conclusie: goed nieuws, aandachtspunt of neutraal (voor een gekleurd bolletje)."""
    t = tekst.lower()
    if any(w in t for w in ("daalt", "kwetsbaar", "onder het", "terugval", "opgelopen", "te weinig", "verlies",
                            "meer dan normaal", "sneller geraakt", "uit de top", "lastig", "naar kas")):
        return "letop"
    if any(w in t for w in ("stijgt breed", "goede omstandigheden", "rustig", "houdt stand", "gekocht vandaag",
                            "sterk zonder", "doet zijn werk", "beter voor")):
        return "goed"
    return "neutraal"
