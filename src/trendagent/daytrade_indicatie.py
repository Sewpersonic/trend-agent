"""Indicatie per kans voor de daytrader: hoe liepen vergelijkbare uitbraken in het verleden af?

Geen voorspelling. Het is een ervaringsgetal uit de koersgeschiedenis, zoals een handelaar zegt: "dit soort uitbraken
liep meestal goed af" of "dit soort zakte vaak terug". Zo werkt het:

1. uitbraken(): speelt de 5-minutenkoersen van alle aandelen na en noteert ELKE uitbraak die aan de koopregels voldeed,
   ook die de bot zelf niet kocht (hij koopt er hooguit 3 per dag). Per uitbraak: de situatie (tijdstip, extra handel,
   daggrafiek, markt, gat bij de opening, ...) en de uitkomst als je hem had gekocht (in R, na kosten).
   Zo zijn er honderden voorbeelden in plaats van een handvol eigen trades: dat is hoe 'de markt' zulke situaties
   behandelde, dus ook hoe andere handelaren erop reageerden.
2. tabel(): per kenmerk en groep hoe vaak het goed afliep en het gemiddelde in R.
3. indicatie(): voor een nieuwe kans de groepen die erbij passen (alleen groepen met genoeg voorbeelden) en daaruit
   gunstig / gemiddeld / ongunstig, met de cijfers erbij.
4. toets(): eerlijk testen: de tabel maken van de eerste dagen en kijken of de indicatie klopte op de latere dagen.

De bot verandert hierdoor niets aan zijn regels. Je kunt hem wel laten overslaan wat ongunstig is
(config/daytrader.json "regels": {"indicatie_filter": true}); dat doe jij, na het onderzoek.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from .daytrade_leren import KENMERKEN, dag_context
from .daytrader import (Bar5, Params, avg_or_volumes, check_times, entry_context, entry_signal, or_stats,
                        split_days)

MIN_N = 20          # minstens zoveel voorbeelden in een groep, anders telt die groep niet mee
DREMPEL_R = 0.10    # zoveel beter/slechter dan gemiddeld = gunstig/ongunstig


def uitkomst(bars: list[Bar5], t: datetime, o: tuple[float, float, float], p: Params) -> tuple[float, str] | None:
    """Wat was het resultaat (in R, na slippage) als je op kijkmoment t had gekocht, met de gewone stop, het
    winstdoel en verkopen om exit_at?"""
    idx = {b.t.replace(tzinfo=None): b for b in bars}
    nb = idx.get(t)
    if not nb:
        return None
    entry = nb.o * (1 + p.slippage)
    stop = max(o[1], entry * (1 - p.max_risk_pct))
    if stop >= entry:
        return None
    risk = entry - stop
    target = entry + p.target_r * risk if p.use_target else None
    exit_t = datetime.combine(t.date(), p.exit_at)
    m = t
    while m < exit_t:
        b = idx.get(m)
        m += timedelta(minutes=5)
        if not b:
            continue
        if b.l <= stop:
            return (min(b.o, stop) * (1 - p.slippage) - entry) / risk, "stop-loss"
        if target and b.h >= target:
            return (max(b.o, target) * (1 - p.slippage) - entry) / risk, "winstdoel"
    eb = idx.get(exit_t)
    last = eb.o if eb else next((b.c for b in reversed(bars) if b.t.replace(tzinfo=None) < exit_t), None)
    if last is None:
        return None
    return (last * (1 - p.slippage) - entry) / risk, "einde van de dag"


def uitbraken(data: dict[str, list[Bar5]], p: Params = Params(), daily: dict | None = None) -> list[dict]:
    """Alle uitbraken die aan de koopregels voldeden (per aandeel de eerste per dag), met situatie en uitkomst."""
    per = {tk: split_days(bs) for tk, bs in data.items()}
    days = sorted({d for x in per.values() for d in x})
    out = []
    for d in days[p.rvol_days:]:
        day_bars = {tk: x[d] for tk, x in per.items() if d in x and len(x[d]) >= 70}
        mkt = day_bars.get(p.market)
        if not mkt:
            continue
        avg = avg_or_volumes(per, d, p)
        ctx_dag = dag_context(daily, d) if daily else {}
        gezien: set[str] = set()
        for t in check_times(d, p):
            if t.time() > p.entry_until:
                break
            m_done = [b for b in mkt if b.t.replace(tzinfo=None) < t]
            market_ok = (not p.market_filter) or (bool(m_done) and m_done[-1].c > mkt[0].o)
            for tk, bs in day_bars.items():
                if tk in gezien:
                    continue
                o = or_stats(bs, p)
                done = [b for b in bs if b.t.replace(tzinfo=None) < t]
                if not o or not done:
                    continue
                ok, _, _ = entry_signal(tk, done, o, avg.get(tk), market_ok, p)
                if not ok:
                    continue
                gezien.add(tk)
                u = uitkomst(bs, t, o, p)
                if u is None:
                    continue
                out.append({"dag": d.isoformat(), "ticker": tk, "tijd": t.strftime("%H:%M"), "r": round(u[0], 3),
                            "reden": u[1], "ctx": entry_context(tk, day_bars, t, o, avg.get(tk), ctx_dag, p)})
    return out


def samenvoegen(oud: list[dict], nieuw: list[dict]) -> list[dict]:
    """Bewaarde uitbraken plus de nieuwe (dezelfde dag en aandeel: de nieuwe telt), gesorteerd op dag."""
    alles = {(e["dag"], e["ticker"]): e for e in oud if isinstance(e, dict) and "dag" in e and "r" in e}
    alles.update({(e["dag"], e["ticker"]): e for e in nieuw})
    return [alles[k] for k in sorted(alles)]


def _gem(rs: list[float]) -> float:
    return sum(rs) / len(rs) if rs else 0.0


def tabel(events: list[dict], kenmerken: dict | None = None) -> dict:
    """Per kenmerk per groep: aantal, % goed afgelopen, gemiddelde R. Plus het gemiddelde van alles.
    kenmerken: naam -> functie(ctx) -> groep (standaard die van de daytrader; de trend-agent geeft zijn eigen)."""
    kenmerken = KENMERKEN if kenmerken is None else kenmerken
    rs = [e["r"] for e in events]
    t = {"totaal": {"n": len(rs), "winst_pct": round(sum(1 for r in rs if r > 0) / len(rs), 3) if rs else None,
                    "gem_r": round(_gem(rs), 3)}, "kenmerken": {}}
    for naam, fn in kenmerken.items():
        g: dict[str, list[float]] = {}
        for e in events:
            g.setdefault(fn(e.get("ctx") or {}), []).append(e["r"])
        t["kenmerken"][naam] = {k: {"n": len(v), "winst_pct": round(sum(1 for r in v if r > 0) / len(v), 3),
                                    "gem_r": round(_gem(v), 3)} for k, v in g.items()}
    return t


def indicatie(ctx: dict, t: dict, kenmerken: dict | None = None, woord: str = "uitbraken") -> dict:
    """Indicatie voor één kans: gunstig / gemiddeld / ongunstig, met de groepen die meetellen."""
    kenmerken = KENMERKEN if kenmerken is None else kenmerken
    tot = (t or {}).get("totaal") or {}
    if not tot.get("n"):
        return {"oordeel": "onbekend", "tekst": "Nog geen ervaringscijfers.", "score": None}
    passend = []
    for naam, fn in kenmerken.items():
        groep = fn(ctx or {})
        g = ((t.get("kenmerken") or {}).get(naam) or {}).get(groep)
        if groep != "onbekend" and g and g["n"] >= MIN_N:
            passend.append((naam, groep, g))
    if not passend:
        return {"oordeel": "onbekend", "tekst": f"Te weinig vergelijkbare {woord} om iets te zeggen.", "score": None}
    score = sum(g["gem_r"] for _, _, g in passend) / len(passend)
    winst = sum(g["winst_pct"] for _, _, g in passend) / len(passend)
    verschil = score - tot["gem_r"]
    oordeel = "gunstig" if verschil >= DREMPEL_R else "ongunstig" if verschil <= -DREMPEL_R else "gemiddeld"
    beste = max(passend, key=lambda x: x[2]["gem_r"])
    slechtste = min(passend, key=lambda x: x[2]["gem_r"])
    tekst = (f"{oordeel.capitalize()}: vergelijkbare {woord} liepen in {round(winst * 100)}% van de gevallen goed af "
             f"(gemiddeld {_r(score)}; alle {woord} samen {_r(tot['gem_r'])}).")
    if oordeel != "gemiddeld":
        x = beste if oordeel == "gunstig" else slechtste
        tekst += f" Vooral: {x[0].lower()} '{x[1]}'."
    return {"oordeel": oordeel, "score": round(score, 3), "winst_pct": round(winst, 3), "tekst": tekst,
            "groepen": len(passend)}


def toets(events: list[dict], deel: float = 0.6, kenmerken: dict | None = None) -> dict:
    """Eerlijk testen: tabel uit de eerste dagen, indicatie beoordelen op de latere dagen (die de tabel nooit zag)."""
    dagen = sorted({e["dag"] for e in events})
    if len(dagen) < 10:
        return {"genoeg": False}
    grens = dagen[int(len(dagen) * deel)]
    leer = [e for e in events if e["dag"] < grens]
    test = [e for e in events if e["dag"] >= grens]
    t = tabel(leer, kenmerken)
    per: dict[str, list[float]] = {}
    for e in test:
        per.setdefault(indicatie(e.get("ctx") or {}, t, kenmerken)["oordeel"], []).append(e["r"])
    uit = {k: {"n": len(v), "gem_r": round(_gem(v), 3), "winst_pct": round(sum(1 for r in v if r > 0) / len(v), 3)}
           for k, v in per.items()}
    g, o = uit.get("gunstig"), uit.get("ongunstig")
    werkt = bool(g and o and g["n"] >= 10 and o["n"] >= 10 and g["gem_r"] > o["gem_r"] + 0.1)
    return {"genoeg": True, "leer_dagen": len({e["dag"] for e in leer}), "test_dagen": len({e["dag"] for e in test}),
            "vanaf": grens, "per_oordeel": uit, "werkt": werkt}


def zin(toetsuitslag: dict, woord: str = "uitbraken") -> str:
    if not toetsuitslag.get("genoeg"):
        return "Nog te weinig dagen om de indicatie eerlijk te toetsen."
    u = toetsuitslag["per_oordeel"]
    f = lambda k: "–" if k not in u else f"{_r(u[k]['gem_r'])} ({u[k]['n']} {woord})"  # noqa: E731
    basis = (f"Toets op {toetsuitslag['test_dagen']} latere dagen die de indicatie nooit zag: "
             f"gunstig {f('gunstig')}, gemiddeld {f('gemiddeld')}, ongunstig {f('ongunstig')}.")
    return basis + (" De indicatie maakte dus echt verschil." if toetsuitslag["werkt"] else
                    " Nog geen duidelijk verschil: gebruik de indicatie voorlopig alleen als informatie.")


def _r(v: float) -> str:
    return f"{v:+.2f}".replace(".", ",").replace("-", "−") + " R"
