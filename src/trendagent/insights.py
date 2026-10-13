"""Verlies, risico en kansen in gewone taal, voor de dagrapporten.

Alles hier is ALLEEN uitleg: deze module koopt of verkoopt niets en verandert geen portefeuille.
De "plannen" laten zien wat de oefenbot met zijn nepgeld volgens zijn eigen regels zou doen
(instap, stop-loss, aantal, inzet, maximaal verlies). Het is geen advies voor echt geld.

Het "instapmoment" is een eenvoudige, NIET geteste vuistregel (hoe ver de koers al is opgelopen).
De bot gebruikt hem niet om te beslissen; hij staat er alleen ter uitleg.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

FILE = "inzicht.json"
TOP_N = 5


def _eur(x: float) -> str:
    s = f"€{abs(x):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-" if x < 0 else "") + s


def _pct(x: float, digits: int = 1) -> str:
    return f"{x:+.{digits}%}".replace(".", ",")


def _n(x: float, digits: int = 1, sign: bool = False) -> str:
    return (f"{x:+.{digits}f}" if sign else f"{x:.{digits}f}").replace(".", ",")


# ------------------------------------------------------------------ verlies en risico

def trend_positions(pf, prices: dict, fx: dict, costs) -> list[dict]:
    """Per open positie: resultaat nu, afstand tot de stop en wat er gebeurt als de stop wordt geraakt."""
    rows = []
    for p in pf.positions.values():
        price = prices.get(p.ticker)
        rate = fx.get(p.currency)
        if price is None or rate is None:
            continue
        cost = p.qty * p.entry_price * p.entry_fx
        now = p.qty * price * rate
        at_stop = p.qty * p.stop * rate
        rows.append({"ticker": p.ticker, "aantal": p.qty, "valuta": p.currency,
                     "instap": round(p.entry_price, 4), "koers": round(price, 4), "stop": round(p.stop, 4),
                     "resultaat_eur": round(now - cost, 2), "resultaat_pct": round(price / p.entry_price - 1, 4),
                     "afstand_stop_pct": round(price / p.stop - 1, 4) if p.stop > 0 else None,
                     "bij_stop_eur": round(at_stop - cost - costs(at_stop), 2)})
    return rows


def trend_brakes(pf, equity: float, day: str, s) -> dict:
    """Hoe dicht de bot bij zijn risicoremmen zit (die zetten de kill switch aan)."""
    pts = [e for e in pf.equity_history if e.get("day") not in ("start", day)]
    prev = pts[-1]["equity"] if pts else (pf.equity_history[0]["equity"] if pf.equity_history else equity)
    peak = pf.peak_equity() or equity
    if pf.peak_from_index == 0:
        peak = max(peak, s.starting_cash_eur)
    peak = max(peak, equity)
    return {"waarde": round(equity, 2), "top": round(peak, 2),
            "daling_vanaf_top": round(equity / peak - 1, 4) if peak else 0.0,
            "grens_daling": s.max_drawdown,
            "vandaag": round(equity / prev - 1, 4) if prev else 0.0,
            "grens_dag": s.daily_loss_limit,
            "verlies_op_rij": pf.consecutive_losses, "grens_op_rij": s.max_consecutive_losses}


def investor_holdings(book, prices_eur: dict) -> list[dict]:
    rows = []
    for t, q in book.qty.items():
        if t not in prices_eur:
            continue
        cost = book.cost_eur.get(t, 0.0)
        now = q * prices_eur[t]
        rows.append({"ticker": t, "waarde_eur": round(now, 2), "kosten_eur": round(cost, 2),
                     "resultaat_eur": round(now - cost, 2),
                     "resultaat_pct": round(now / cost - 1, 4) if cost else 0.0})
    return sorted(rows, key=lambda r: r["resultaat_eur"])


def drawdown(history: list[dict]) -> dict:
    vals = [e["equity"] for e in history]
    if not vals:
        return {}
    peak = max(vals)
    return {"top": round(peak, 2), "daling_vanaf_top": round(vals[-1] / peak - 1, 4) if peak else 0.0}


# ------------------------------------------------------------------ kansen

def moment(snap: dict) -> tuple[str, str]:
    """Vuistregel: is de koers al ver opgelopen? Niet getest, alleen ter uitleg."""
    rsi = snap.get("rsi14")
    dist = snap.get("ema20_afstand_pct")
    atr = snap.get("atr_pct")
    if rsi is None or dist is None or not atr:
        return "onbekend", "te weinig historie om het instapmoment te beoordelen"
    stretch = dist / atr
    if rsi > 75 or stretch > 3:
        return "opgelopen", (f"de koers staat {_n(dist, sign=True)}% van het 20-daags gemiddelde ({_n(stretch)}x de normale "
                             f"dagbeweging) en RSI is {rsi:.0f}; na zo'n sprint volgt vaak eerst een terugval")
    if rsi <= 65 and stretch <= 1.5:
        return "gunstig", (f"de trend is sterk maar de koers is niet ver weggelopen ({_n(dist, sign=True)}% van het "
                           f"20-daags gemiddelde, RSI {rsi:.0f})")
    return "neutraal", f"de koers staat {_n(dist, sign=True)}% van het 20-daags gemiddelde, RSI {rsi:.0f}"


def explain(a, snap: dict, name: str) -> str:
    bits = [f"{name} steeg {_pct(a.ret63)} in 3 maanden en {_pct(a.ret21)} in 1 maand",
            "koers boven het 50-daags en dat boven het 200-daags gemiddelde"]
    h = snap.get("macd_hist_pct")
    if h is not None:
        bits.append("MACD " + ("positief (de stijging versnelt)" if h > 0 else "negatief (de stijging vertraagt)"))
    if a.rel_volume:
        bits.append(f"handel {_n(a.rel_volume)}x het normale volume")
    if snap.get("atr_pct"):
        bits.append(f"beweegt gemiddeld {_n(snap['atr_pct'])}% per dag")
    return "; ".join(bits)


def plan(a, snap: dict, s, pf, equity: float, fx: dict, currency: str, costs) -> dict:
    """Wat de oefenbot volgens zijn regels zou doen bij dit instrument (zelfde rekensom als bij kopen)."""
    rate = fx.get(currency) or 1.0
    entry = a.close * (1 + s.slippage)
    stop = entry - s.stop_atr_multiple * a.atr14
    risk_share = (entry - stop) * rate
    out = {"instap": round(entry, 4), "stop": round(stop, 4), "valuta": currency,
           "doel_2r": round(entry + 2 * (entry - stop), 4), "aantal": 0, "inzet_eur": 0.0, "max_verlies_eur": 0.0,
           "stop_pct": round(stop / entry - 1, 4) if entry else 0.0}
    if stop <= 0 or risk_share <= 0:
        return out
    budget = equity * s.risk_per_trade                 # vol budget: alsof er een plek vrij is
    qty = math.floor(budget / risk_share)
    qty = min(qty, math.floor(equity * s.max_position_weight / (entry * rate)))
    qty = max(qty, 0)
    value = qty * entry * rate
    out.update(aantal=qty, inzet_eur=round(value, 2),
               max_verlies_eur=round(qty * risk_share + (2 * costs(value) if qty else 0), 2),
               budget_eur=round(budget, 2))
    return out


def opportunities(rep, pf, snaps: dict, s, equity: float, fx: dict, by_ticker: dict, costs,
                  buys_blocked_reason: str | None) -> list[dict]:
    out = []
    bought_today = {t.ticker for t in pf.trades if t.day == rep.day and t.side == "BUY"}
    free = s.max_positions - len(pf.positions)
    for a in rep.ranking[:TOP_N]:
        inst = by_ticker[a.ticker]
        snap = snaps.get(a.ticker, {})
        label, why = moment(snap)
        p = plan(a, snap, s, pf, equity, fx, inst.currency, costs)
        rsi = snap.get("rsi14")
        if a.ticker in bought_today:
            status = "vandaag gekocht door de bot"
        elif a.ticker in pf.positions:
            status = "al in bezit"
        elif buys_blocked_reason:
            status = f"niet gekocht: {buys_blocked_reason}"
        elif rsi is not None and rsi > s.max_rsi_entry:
            status = f"niet gekocht: RSI {rsi:.0f} boven de grens {s.max_rsi_entry:.0f}"
        elif p["aantal"] < 1:
            status = "niet gekocht: één stuk is te duur voor het risicobudget van deze kleine oefenrekening"
        elif free <= 0:
            status = f"niet gekocht: alle {s.max_positions} plekken zijn bezet"
        else:
            status = "niet gekocht: risicobudget of kas was op"
        out.append({"ticker": a.ticker, "naam": inst.name, "score": round(a.score, 3),
                    "uitleg": explain(a, snap, inst.name), "moment": label, "moment_uitleg": why,
                    "status": status, "plan": p})
    return out


# ------------------------------------------------------------------ opslaan en tonen

def save(state_dir: Path, bot: str, data: dict) -> None:
    path = state_dir / FILE
    try:
        allp = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        allp = {}
    allp[bot] = data
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(allp, indent=1, ensure_ascii=False), encoding="utf-8")


def load(state_dir: Path) -> dict:
    try:
        return json.loads((state_dir / FILE).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def render_trend_risk(rows: list[dict], brakes: dict) -> list[str]:
    lines = ["## Verlies en risico", ""]
    if rows:
        lines += ["| Ticker | Instap | Koers nu | Resultaat | Stop | Afstand tot stop | Als de stop geraakt wordt |",
                  "| --- | --- | --- | --- | --- | --- | --- |"]
        for r in rows:
            st = r["bij_stop_eur"]
            at_stop = f"{_eur(st)} {'verlies' if st < 0 else 'winst vastgezet'}"
            dist = _pct(r["afstand_stop_pct"]) if r["afstand_stop_pct"] is not None else "–"
            lines.append(f"| {r['ticker']} | {r['instap']:.2f} {r['valuta']} | {r['koers']:.2f} | "
                         f"{_eur(r['resultaat_eur'])} ({_pct(r['resultaat_pct'])}) | {r['stop']:.2f} | {dist} | {at_stop} |")
        worst = sum(min(r["bij_stop_eur"], 0) for r in rows)
        lines += ["", f"Raken alle stops tegelijk, dan is het verlies hooguit ongeveer {_eur(-worst if worst else 0)}"
                      " (bij een koersgat 's ochtends kan het meer zijn)."]
    else:
        lines.append("Geen open posities, dus nu geen verlies mogelijk.")
    if brakes:
        lines += ["", "**Remmen** (bij overschrijden gaat de kill switch aan en koopt de bot niets meer):", "",
                  f"- Daling vanaf de top: {_pct(brakes['daling_vanaf_top'], 2)} (grens -{brakes['grens_daling']:.0%}; "
                  f"top was {_eur(brakes['top'])})",
                  f"- Vandaag: {_pct(brakes['vandaag'], 2)} (grens -{brakes['grens_dag']:.0%})",
                  f"- Verliestrades op rij: {brakes['verlies_op_rij']} van {brakes['grens_op_rij']}"]
    return lines


def render_opportunities(items: list[dict]) -> list[str]:
    if not items:
        return []
    lines = ["## Kansen: wat de bot vandaag het sterkst vond", "",
             "_Dit is wat de oefenbot met zijn nepgeld volgens zijn eigen regels zou doen. Geen advies voor echt geld; "
             "het instapmoment is een ongeteste vuistregel en wordt door de bot niet gebruikt._", ""]
    for i, k in enumerate(items, 1):
        p = k["plan"]
        cur = p["valuta"]
        lines += [f"### {i}. {k['naam']} ({k['ticker']}): instapmoment **{k['moment']}**", "",
                  f"- **Waarom sterk:** {k['uitleg']}.",
                  f"- **Instapmoment:** {k['moment_uitleg']}.",
                  f"- **Status:** {k['status']}."]
        if p["aantal"] >= 1:
            lines.append(f"- **Plan van de bot:** koop {p['aantal']:g} {'stuk' if p['aantal'] == 1 else 'stuks'} rond {p['instap']:.2f} {cur} "
                         f"(inzet {_eur(p['inzet_eur'])}), stop-loss {p['stop']:.2f} {cur} ({_pct(p['stop_pct'])}). "
                         f"Maximaal verlies als de stop wordt geraakt: ongeveer {_eur(p['max_verlies_eur'])}. "
                         f"Ter oriëntatie: 2x het risico winst ligt bij {p['doel_2r']:.2f} {cur}; de bot verkoopt daar "
                         "niet vanzelf, hij laat de stop meeschuiven.")
        else:
            lines.append(f"- **Plan van de bot:** instap rond {p['instap']:.2f} {cur}, stop {p['stop']:.2f} {cur} "
                         f"({_pct(p['stop_pct'])}). Met een risicobudget van {_eur(p.get('budget_eur', 0))} past er "
                         "geen heel stuk in.")
        lines.append("")
    return lines


def render_investor_risk(rows: list[dict], dd: dict) -> list[str]:
    if not rows:
        return []
    total = sum(r["resultaat_eur"] for r in rows)
    lines = ["## Verlies en winst per belegging", "",
             "| Instrument | Waarde | Ingelegd | Resultaat |", "| --- | --- | --- | --- |"]
    for r in rows:
        lines.append(f"| {r['ticker']} | {_eur(r['waarde_eur'])} | {_eur(r['kosten_eur'])} | "
                     f"{_eur(r['resultaat_eur'])} ({_pct(r['resultaat_pct'])}) |")
    lines += ["", f"Totaal op de beleggingen: {_eur(total)} (inclusief aankoopkosten)."]
    if dd:
        lines.append(f"Daling vanaf de hoogste waarde ooit: {_pct(dd['daling_vanaf_top'], 2)} (top {_eur(dd['top'])}). "
                     "De investeerder heeft geen stop-loss: hij houdt een spreiding vast en herverdeelt maandelijks.")
    return lines
