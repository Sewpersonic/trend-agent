"""Leren van de daytrade-bot: wat zegt de daggrafiek, en in welke situaties werkte daytraden wel of niet?

1. dag_context(): per aandeel de daggrafiek van de dagen vóór de handelsdag, met dezelfde regels als de patronen
   van de trend-agent: trend (slot boven of onder het 50- en 200-daags gemiddelde), plek in het bereik van
   3 maanden (bij de top, midden, onderaan), een terugval binnen een stijgende trend, en het vorige slot.
2. Bij elke aankoop legt de bot die situatie vast (daytrader.entry_context): de daggrafiek, de markt,
   het tijdstip, hoeveel extra handel er was, hoe breed de openingsrange was, of het aandeel met een gat opende.
3. leer(): groepeert alle afgesloten trades per kenmerk en zoekt groepen die duidelijk beter of slechter waren
   dan de rest (genoeg trades én een duidelijk verschil). Dat is een LES, geen regel: de bot past zijn eigen
   regels nooit zelf aan. Het onderzoek (daytrade_test) test een regel op oude koersen; aanzetten doe jij.
"""

from __future__ import annotations

import math
from datetime import date

MIN_GROEP = 10        # minstens zoveel trades in een groep voordat er een les uit mag komen
MIN_VERSCHIL_R = 0.15
T_GRENS = 2.0


# ---------------------------------------------------------------- daggrafiek

def _sma(x: list[float], n: int) -> float | None:
    return sum(x[-n:]) / n if len(x) >= n else None


def chart_view(bars) -> dict:
    """Daggrafiek van één aandeel (bars: dagkoersen tot en met de vorige handelsdag)."""
    c = [b.close for b in bars]
    if len(c) < 30:
        return {}
    s50, s200 = _sma(c, 50), _sma(c, 200)
    last = c[-1]
    if s50 and s200 and last > s50 > s200:
        trend = "stijgend"
    elif s50 and s200 and last < s50 < s200:
        trend = "dalend"
    elif s50 and s200:
        trend = "zijwaarts"
    else:
        trend = "onbekend"
    hi = max(b.high for b in bars[-63:])
    lo = min(b.low for b in bars[-63:])
    plek = (last - lo) / (hi - lo) if hi > lo else 0.5
    d5 = last / c[-6] - 1 if len(c) > 5 else None
    return {"dagtrend": trend,
            "plek": "bij de 3-maands top" if plek >= 0.9 else "onderaan het bereik" if plek <= 0.2 else "midden in het bereik",
            "terugval": bool(trend == "stijgend" and d5 is not None and d5 < -0.02),
            "boven_sma50": bool(s50 and last > s50),
            "vorig_slot": last}


def dag_context(daily: dict | None, day: date) -> dict:
    """Per aandeel de daggrafiek zoals die er de ochtend van 'day' uitzag (alleen eerdere dagen)."""
    out = {}
    for tk, bars in (daily or {}).items():
        before = [b for b in bars if b.day < day]
        v = chart_view(before[-260:])
        if v:
            out[tk] = v
    return out


# ---------------------------------------------------------------- leren van trades

def _pct_bucket(v, edges, labels):
    if v is None:
        return "onbekend"
    for e, lab in zip(edges, labels):
        if v < e:
            return lab
    return labels[-1]


KENMERKEN = {
    "Daggrafiek van het aandeel": lambda c: {"stijgend": "stijgende trend", "dalend": "dalende trend",
                                             "zijwaarts": "geen duidelijke richting"}.get(c.get("dagtrend"), "onbekend"),
    "Plek in het bereik van 3 maanden": lambda c: c.get("plek", "onbekend"),
    "Daggrafiek van de markt (SPY)": lambda c: {"stijgend": "markt in stijgende trend", "dalend": "markt in dalende trend",
                                               "zijwaarts": "markt zonder richting"}.get(c.get("markt_dagtrend"), "onbekend"),
    "Tijdstip van kopen (New York)": lambda c: "onbekend" if not c.get("tijd") else
        "10:00-10:59" if c["tijd"] < "11:00" else "11:00-11:59" if c["tijd"] < "12:00" else "12:00-12:30",
    "Extra handel in het eerste half uur": lambda c: _pct_bucket(c.get("rvol"), [1.5, 2.5], ["1,2-1,5x", "1,5-2,5x", "meer dan 2,5x"]),
    "Breedte van de openingsrange": lambda c: _pct_bucket(c.get("or_breedte"), [0.01, 0.02], ["smal (<1%)", "normaal (1-2%)", "breed (>2%)"]),
    "Opening t.o.v. gisteren": lambda c: _pct_bucket(c.get("gap"), [-0.005, 0.005, 0.02],
                                                    ["lager geopend", "rond gisteren", "hoger geopend", "veel hoger geopend (>2%)"]),
    "Markt op het moment van kopen": lambda c: _pct_bucket(c.get("markt_vandaag"), [0.003, 0.008],
                                                          ["licht hoger (<0,3%)", "hoger (0,3-0,8%)", "sterk hoger (>0,8%)"]),
}


def _stats(rs: list[float], pnl: list[float]) -> dict:
    n = len(rs)
    if not n:
        return {"n": 0}
    gem = sum(rs) / n
    sd = math.sqrt(sum((r - gem) ** 2 for r in rs) / (n - 1)) if n > 1 else 0.0
    return {"n": n, "gem_r": round(gem, 3), "winst_pct": round(sum(1 for r in rs if r > 0) / n, 3),
            "resultaat": round(sum(pnl), 2), "se": sd / math.sqrt(n) if n > 1 else 0.0}


def leer(trades: list[dict]) -> dict:
    """trades: afgesloten daytrades (dicts met r, resultaat en ctx). Geeft totaal, groepen per kenmerk en lessen."""
    done = [t for t in trades if t.get("r") is not None]
    totaal = _stats([t["r"] for t in done], [t["resultaat"] for t in done])
    groepen, lessen = {}, []
    for naam, fn in KENMERKEN.items():
        g: dict[str, list[dict]] = {}
        for t in done:
            g.setdefault(fn(t.get("ctx") or {}), []).append(t)
        rows = []
        for k, ts in g.items():
            st = _stats([t["r"] for t in ts], [t["resultaat"] for t in ts])
            rows.append({"groep": k, **{x: y for x, y in st.items() if x != "se"}})
            if k == "onbekend" or len(ts) < MIN_GROEP:
                continue
            rest = [t for t in done if fn(t.get("ctx") or {}) != k]
            if len(rest) < MIN_GROEP:
                continue
            b = _stats([t["r"] for t in rest], [t["resultaat"] for t in rest])
            se = math.sqrt(st["se"] ** 2 + b["se"] ** 2)
            diff = st["gem_r"] - b["gem_r"]
            tv = diff / se if se > 0 else 0.0
            if abs(diff) >= MIN_VERSCHIL_R and abs(tv) >= T_GRENS:
                lessen.append({"kenmerk": naam, "groep": k, "soort": "beter" if diff > 0 else "slechter",
                               "n": st["n"], "gem_r": st["gem_r"], "verschil_r": round(diff, 3), "t": round(tv, 1),
                               "tekst": les_tekst(naam, k, st, diff)})
        groepen[naam] = sorted(rows, key=lambda r: -r["n"])
    lessen.sort(key=lambda x: -abs(x["t"]))
    return {"totaal": {k: v for k, v in totaal.items() if k != "se"}, "groepen": groepen, "lessen": lessen}


def _r(v: float) -> str:
    return f"{v:+.2f}".replace(".", ",").replace("-", "−") + " R"


def les_tekst(kenmerk: str, groep: str, st: dict, diff: float) -> str:
    beter = diff > 0
    # Kort en gewoon: eerst de situatie, dan beter/slechter, cijfers tussen haakjes.
    return (f"{'Beter' if beter else 'Slechter'}: {kenmerk[:1].lower() + kenmerk[1:]} {groep} "
            f"({st['n']} trades, gemiddeld {_r(st['gem_r'])} per trade).")


def samenvatting(leer_uit: dict, bron: str) -> list[str]:
    """Korte zinnen voor het dashboard."""
    t = leer_uit.get("totaal") or {}
    if not t.get("n"):
        return [f"{bron}: nog geen afgesloten trades om van te leren."]
    zinnen = [f"{bron}: {t['n']} trades, {round(t['winst_pct'] * 100)}% met winst, gemiddeld {_r(t['gem_r'])} per trade."]
    if leer_uit.get("lessen"):
        zinnen += [x["tekst"] for x in leer_uit["lessen"][:4]]
    elif t["n"] < 2 * MIN_GROEP:
        zinnen.append(f"Nog te weinig trades om iets te leren: per situatie zijn er minstens {MIN_GROEP} nodig.")
    else:
        zinnen.append("Geen situatie die duidelijk beter of slechter was dan de rest.")
    return zinnen
