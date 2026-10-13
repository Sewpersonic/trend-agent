"""Eén Excel-bestand met alles van de dag: rapporten/dagrapport.xlsx.

Tabbladen:
  Overzicht            stand van beide bots en wat ze uit de analyse halen
  Analyse              wat elke bot zag (markt, breedte, zeef, momentum) en zijn conclusies
  Verlies en risico    resultaat per positie, afstand tot de stop, remmen, en winst/verlies per belegging
  Kansen               de sterkste trends met uitleg, instapmoment en het plan van de bot
  Klaar voor echt geld de eisen en de stand per bot
  Waarde per dag       beide bots en de wereld-ETF
  Trades               alle aan- en verkopen van beide bots
  Controles            koersbronnen en waarschuwingen
  Grafieken            de candle-grafieken van vandaag
  Uitleg               wat de begrippen betekenen

Wordt elke dag opnieuw opgebouwd uit de bestanden die de bots al schreven. Verandert niets aan de portefeuilles.
"""

from __future__ import annotations

import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

from . import insights
from .reports import EUR, PCT, _sheet
from .universe import BY_TICKER

WRAP = Alignment(wrap_text=True, vertical="top")
BOLD = Font(bold=True)
STATE = {"ok": "✅ gehaald", "bezig": "⏳ nog bezig", "nee": "❌ niet gehaald"}
BOTS = (("Investeerder", "investeerder", "investeerder.json"), ("Trend-agent", "trend", "portfolio.json"))


def _load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _plain(line: str) -> str:
    return line.removeprefix("- ").replace("**", "")


def _wrap_rows(ws, first: int = 2) -> None:
    for row in ws.iter_rows(min_row=first):
        for c in row:
            if isinstance(c.value, str):
                c.alignment = WRAP


def build(state_dir: Path, reports_dir: Path, day: str) -> Workbook:
    from .summary import _history_stats
    info = insights.load(state_dir)
    books = {key: _load(state_dir / fname) for _, key, fname in BOTS}
    health = _load(state_dir / "health.json")
    wb = Workbook()
    wb.remove(wb.active)

    # --- Overzicht
    ws = _sheet(wb, "Overzicht", ["Bot", "Waarde", "Vandaag", "Vandaag %", "Sinds start %", "Tegenover wereld-ETF",
                                  "Klaar voor echt geld?"], [16, 14, 13, 11, 13, 20, 60])
    for name, key, _ in BOTS:
        st = _history_stats(books[key].get("equity_history", []))
        ready = info.get(key, {}).get("klaar", {}).get("oordeel", "")
        ws.append([name, st.get("waarde"), st.get("vandaag"), st.get("vandaag_pct"), st.get("sinds_start"),
                   st.get("vs_etf"), ready])
        r = ws.max_row
        for col, fmt in ((2, EUR), (3, EUR), (4, PCT), (5, PCT), (6, PCT)):
            ws.cell(row=r, column=col).number_format = fmt
    ws.append([])
    ws.append([f"Handelsdag {day}. Twee oefenbots met elk €10.000 nepgeld. Geen beleggingsadvies."])
    ws.append([])
    for name, key, _ in BOTS:
        d = info.get(key, {})
        if d.get("conclusies"):
            ws.append([f"{name}: wat de bot eruit haalt"])
            ws.cell(row=ws.max_row, column=1).font = BOLD
            for c in d["conclusies"]:
                ws.append(["", c])
                ws.merge_cells(start_row=ws.max_row, start_column=2, end_row=ws.max_row, end_column=7)
                ws.cell(row=ws.max_row, column=2).alignment = WRAP
                ws.row_dimensions[ws.max_row].height = 30
            ws.append([])
    done = [(name, t) for name, key, _ in BOTS for t in books[key].get("trades", []) if t.get("day") == day]
    ws.append(["Vandaag gedaan"])
    ws.cell(row=ws.max_row, column=1).font = BOLD
    for name, t in done:
        ws.append(["", f"{name} {'kocht' if t['side'] == 'BUY' else 'verkocht'} {t['ticker']} voor "
                       f"€{t['value_eur']:,.2f} ({t['reason'][:90]})"])
    if not done:
        ws.append(["", "Niets gekocht of verkocht."])

    # --- Analyse
    ws = _sheet(wb, "Analyse", ["Bot", "Onderdeel", "Wat de bot zag of concludeert"], [16, 22, 110])
    for name, key, _ in BOTS:
        d = info.get(key, {})
        for line in d.get("zag", []):
            text = _plain(line)
            head, _, rest = text.partition(":")
            ws.append([name, head.strip(), rest.strip()])
        for c in d.get("conclusies", []):
            ws.append([name, "Conclusie", c])
    _wrap_rows(ws)

    # --- Verlies en risico
    ws = _sheet(wb, "Verlies en risico", ["Bot", "Ticker", "Instap", "Koers nu", "Stop", "Resultaat €", "Resultaat %",
                                          "Afstand tot stop", "Als de stop geraakt wordt €"],
                [14, 12, 11, 11, 11, 13, 12, 15, 24])
    tr = info.get("trend", {})
    for r in tr.get("posities", []):
        ws.append(["Trend-agent", r["ticker"], r["instap"], r["koers"], r["stop"], r["resultaat_eur"],
                   r["resultaat_pct"], r["afstand_stop_pct"], r["bij_stop_eur"]])
        row = ws.max_row
        for col, fmt in ((6, EUR), (7, PCT), (8, PCT), (9, EUR)):
            ws.cell(row=row, column=col).number_format = fmt
    b = tr.get("remmen")
    if b:
        ws.append([])
        ws.append(["Trend-agent remmen", "Nu", "Grens"])
        ws.cell(row=ws.max_row, column=1).font = BOLD
        for label, now, limit in (("Daling vanaf top", b["daling_vanaf_top"], -b["grens_daling"]),
                                  ("Vandaag", b["vandaag"], -b["grens_dag"])):
            ws.append([label, now, limit])
            ws.cell(row=ws.max_row, column=2).number_format = PCT
            ws.cell(row=ws.max_row, column=3).number_format = PCT
        ws.append(["Verliestrades op rij", b["verlies_op_rij"], b["grens_op_rij"]])
    inv = info.get("investeerder", {})
    if inv.get("posities"):
        ws.append([])
        ws.append(["Investeerder", "Instrument", "Waarde", "Ingelegd", "Resultaat €", "Resultaat %"])
        for c in range(1, 7):
            ws.cell(row=ws.max_row, column=c).font = BOLD
        for r in inv["posities"]:
            ws.append(["", r["ticker"], r["waarde_eur"], r["kosten_eur"], r["resultaat_eur"], r["resultaat_pct"]])
            row = ws.max_row
            for col, fmt in ((3, EUR), (4, EUR), (5, EUR), (6, PCT)):
                ws.cell(row=row, column=col).number_format = fmt

    # --- Kansen
    ws = _sheet(wb, "Kansen", ["#", "Ticker", "Naam", "Instapmoment", "Waarom sterk", "Uitleg instapmoment", "Status",
                               "Valuta", "Instap", "Stop", "Stop %", "Aantal", "Inzet €", "Max verlies €",
                               "2x risico (oriëntatie)"],
                [4, 10, 18, 13, 60, 45, 34, 7, 10, 10, 9, 8, 11, 13, 14])
    for i, k in enumerate(tr.get("kansen", []), 1):
        p = k["plan"]
        ws.append([i, k["ticker"], k["naam"], k["moment"], k["uitleg"], k["moment_uitleg"], k["status"], p["valuta"],
                   p["instap"], p["stop"], p["stop_pct"], p["aantal"], p["inzet_eur"], p["max_verlies_eur"], p["doel_2r"]])
        row = ws.max_row
        ws.cell(row=row, column=11).number_format = PCT
        ws.cell(row=row, column=13).number_format = EUR
        ws.cell(row=row, column=14).number_format = EUR
    ws.append([])
    ws.append(["", "Wat de oefenbot met nepgeld zou doen volgens zijn regels. Geen advies voor echt geld. "
                   "Het instapmoment is een ongeteste vuistregel en wordt door de bot niet gebruikt."])
    _wrap_rows(ws)

    # --- Klaar voor echt geld
    ws = _sheet(wb, "Klaar voor echt geld", ["Bot", "Eis", "Stand", "Nu"], [16, 36, 16, 50])
    for name, key, _ in BOTS:
        k = info.get(key, {}).get("klaar")
        if not k:
            continue
        for label, state, detail in k["eisen"]:
            ws.append([name, label, STATE.get(state, state), detail])
        ws.append([name, "Oordeel", "", k["oordeel"]])
        ws.cell(row=ws.max_row, column=4).font = BOLD
        ws.append([])
    ws.append(["", "Eerst bewijzen, dan een oefenaccount bij een echte broker, dan een klein bedrag met jouw "
                   "goedkeuring per order. Die beslissing neem jij, niet de bot."])
    _wrap_rows(ws)

    # --- Waarde per dag
    ws = _sheet(wb, "Waarde per dag", ["Datum", "Investeerder", "Trend-agent", "Wereld-ETF (koers in €)"], [14, 15, 15, 22])
    days: dict[str, list] = {}
    for col, (_, key, _) in enumerate(BOTS):
        for e in books[key].get("equity_history", []):
            row = days.setdefault(e["day"], [None, None, None])
            row[col] = e["equity"]
            if "bench" in e:
                row[2] = e["bench"]
    order = sorted(days, key=lambda d: (d != "start", d))
    for d in order:
        ws.append([d, *days[d]])
        ws.cell(row=ws.max_row, column=2).number_format = EUR
        ws.cell(row=ws.max_row, column=3).number_format = EUR

    # --- Trades
    ws = _sheet(wb, "Trades", ["Datum", "Bot", "Ticker", "Koop/verkoop", "Aantal", "Prijs", "Waarde €", "Kosten €",
                               "Resultaat €", "Reden"], [12, 14, 10, 13, 10, 11, 12, 10, 12, 70])
    rows = [(t["day"], name, t) for name, key, _ in BOTS for t in books[key].get("trades", [])]
    for d, name, t in sorted(rows, key=lambda x: x[0]):
        ws.append([d, name, t["ticker"], "koop" if t["side"] == "BUY" else "verkoop", t["qty"], t["price"],
                   t["value_eur"], t["costs_eur"], t.get("pnl_eur"), t["reason"]])
        for col in (7, 8, 9):
            ws.cell(row=ws.max_row, column=col).number_format = EUR

    # --- Controles
    ws = _sheet(wb, "Controles", ["Bot", "Controle"], [16, 120])
    from .summary import _plain_checks
    for name, key, _ in BOTS:
        for line in _plain_checks(name, health.get(key, {})):
            ws.append([name, line.replace("**", "")])
    _wrap_rows(ws)

    # --- Uitleg
    ws = _sheet(wb, "Uitleg", ["Begrip", "Betekenis"], [26, 110])
    for row in (
        ("Wereld-ETF", "Een fonds met ongeveer 1.500 grote bedrijven wereldwijd (IWDA). Dit is de maatstaf: doet de bot het beter dan dit simpelweg vasthouden?"),
        ("200-daags gemiddelde", "De gemiddelde slotkoers van de laatste 200 handelsdagen. Erboven = stijgende trend op lange termijn."),
        ("Breedte", "Hoeveel van de gevolgde aandelen boven hun 200-daags gemiddelde staan. Hoog = de stijging wordt breed gedragen."),
        ("Beweeglijkheid", "Hoe hard de koersen op en neer gaan, vergeleken met het afgelopen jaar."),
        ("ATR", "De gemiddelde dagbeweging van een aandeel. De stop-loss ligt 2x de ATR onder de instap."),
        ("RSI", "Maat voor hoe hard een koers recent is gestegen (0-100). Boven 70-75 = mogelijk te snel opgelopen."),
        ("MACD", "Laat zien of een stijging versnelt (positief) of vertraagt (negatief)."),
        ("Stop-loss", "De prijs waarop de bot automatisch verkoopt om het verlies te beperken. Schuift mee omhoog als het goed gaat."),
        ("R", "Resultaat van een trade gedeeld door het risico bij instap. +2 R = twee keer zoveel gewonnen als je riskeerde."),
        ("Instapmoment", "Ongeteste vuistregel: gunstig = sterk maar niet ver weggelopen; opgelopen = ver boven het 20-daags gemiddelde."),
        ("Momentum", "Stijging over 12 maanden zonder de laatste maand. De investeerder kiest de 5 hoogste."),
        ("Kill switch", "Noodstop. Bij te veel verlies koopt de bot niets meer tot jij hem weer aanzet."),
    ):
        ws.append(list(row))
    _wrap_rows(ws)
    return wb


def write(state_dir: Path, reports_dir: Path, day: str) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / "dagrapport.xlsx"
    tmp = path.with_suffix(".tmp.xlsx")
    build(state_dir, reports_dir, day).save(tmp)
    tmp.replace(path)
    try:   # grafieken van vandaag erbij; een fout hierin laat het bestand gewoon staan
        from . import charts
        folder = charts.chart_dir(reports_dir, day)
        pngs = sorted(folder.glob("*.png")) if folder.exists() else []
        charts.add_to_excel(path, pngs)
    except Exception:  # noqa: BLE001
        pass
    return path
