"""Echte Excel-grafieken (geen plaatjes): Excel tekent ze zelf, dus ze blijven scherp bij elke zoom
en je kunt met de muis over een lijn gaan om de waarde te zien.

Tabblad 'Grafieken': alle grafieken onder elkaar. Boven elke grafiek een kop en uitleg in gewone taal.
Tabblad 'Grafiekdata': de cijfers waar de grafieken op gebaseerd zijn (verborgen; zichtbaar te maken
via rechtsklik op een tabblad -> Zichtbaar maken).
"""

from __future__ import annotations

from pathlib import Path

from openpyxl import load_workbook
from openpyxl.chart import LineChart, Reference, StockChart
from openpyxl.chart.axis import ChartLines
from openpyxl.chart.data_source import NumData, NumVal
from openpyxl.chart.updown_bars import UpDownBars
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
from openpyxl.styles import Alignment, Font

INK = "0B0B0B"
INK_2 = "52514E"
BLUE = "2A78D6"
ORANGE = "EB6834"
RED = "E34948"
GREEN = "008300"
GREY = "8A8984"
CHART_W_CM, CHART_H_CM = 15.5, 9      # één grafiek in het raster (twee naast elkaar)
WIDE_W_CM, WIDE_H_CM = 31.5, 10       # de waardegrafiek over de volle breedte
ROW_PX = 20                            # standaard rijhoogte (15 punten) in pixels


def _rows_for(height_cm: float) -> int:
    return int(height_cm / 2.54 * 96 / ROW_PX) + 1


def _line(series, color: str, width_pt: float, dash: str | None = None) -> None:
    series.graphicalProperties = GraphicalProperties(ln=LineProperties(solidFill=color, w=int(width_pt * 12700),
                                                                       prstDash=dash))
    series.smooth = False
    series.marker.symbol = "none"


def _nice(lo: float, hi: float) -> tuple[float, float, float]:
    """Ronde asgrenzen en stapgrootte (bijv. 280-390 in stappen van 20) zodat de getallen makkelijk lezen."""
    import math
    raw = (hi - lo) / 6 or 1
    mag = 10 ** math.floor(math.log10(raw))
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    return math.floor(lo / step) * step, math.ceil(hi / step) * step, step


def _base_chart(y_title: str, lo: float, hi: float, n: int) -> LineChart:
    lo, hi, step = _nice(lo, hi)
    ch = LineChart()
    ch.y_axis.majorUnit = step
    ch.width, ch.height = CHART_W_CM, CHART_H_CM
    ch.legend.position = "b"
    ch.y_axis.title = y_title
    ch.y_axis.scaling.min = lo
    ch.y_axis.scaling.max = hi
    ch.y_axis.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill="E6E5E1"))
    ch.y_axis.number_format = "#,##0.00" if hi < 100 else "#,##0"
    ch.x_axis.number_format = "@"
    ch.x_axis.tickLblSkip = max(n // 7, 1)
    ch.x_axis.tickMarkSkip = max(n // 7, 1)
    # openpyxl 3.1 verbergt de assen standaard in nieuwe Excel-versies; expliciet tonen.
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.layout = Layout(manualLayout=ManualLayout(x=0.02, y=0.03, w=0.96, h=0.8))
    return ch


def _range(values: list[float | None], pad_share: float = 0.06) -> tuple[float, float]:
    vals = [v for v in values if v is not None]
    lo, hi = min(vals), max(vals)
    pad = (hi - lo) * pad_share or max(abs(hi) * 0.01, 1)
    return lo - pad, hi + pad


def _price_chart(data_ws, item: dict, col: int, size: tuple[float, float] = (CHART_W_CM, CHART_H_CM)):
    """Kaarsgrafiek (candles) met de gemiddelden, de instap en de stop-loss als lijnen erover.

    Groene kaars = die dag gestegen, rode kaars = die dag gedaald. De dunne streep door een kaars is
    de hoogste en laagste koers van die dag. Geeft (grafiek, volgende vrije kolom) terug.
    """
    n = len(item["datums"])
    has_ohlc = all(item.get(k) for k in ("open", "hoog", "laag"))
    if not has_ohlc:                                   # oude gegevens zonder open/hoog/laag: alleen lijnen
        item = dict(item, open=item["koers"], hoog=item["koers"], laag=item["koers"])
    lines = [("50-daags gemiddelde", item["sma50"], BLUE, 2, None),
             ("200-daags gemiddelde", item["sma200"], ORANGE, 2, None)]
    if item.get("instap"):
        lines.append(("Instap", [item["instap"]] * n, INK_2, 1.5, "dash"))
    if item.get("stop"):
        lines.append(("Stop-loss (hier verkoopt de bot)", [item["stop"]] * n, RED, 1.75, "dash"))
    cols = [("Datum", item["datums"]), ("Opening", item["open"]), ("Hoogste", item["hoog"]),
            ("Laagste", item["laag"]), ("Slot", item["koers"])] + [(name, vals) for name, vals, *_ in lines]
    for j, (name, values) in enumerate(cols):
        data_ws.cell(row=1, column=col + j, value=f"{item['titel']}: {name}" if j == 0 else name)
        for i, v in enumerate(values, start=2):
            data_ws.cell(row=i, column=col + j, value=v)

    # Schaal: kaarsen, instap en stop altijd in beeld; gemiddelden alleen als ze niet ver weg liggen,
    # anders worden de kaarsen platgedrukt.
    core = item["laag"] + item["hoog"] + [v for v in (item.get("instap"), item.get("stop")) if v]
    lo, hi = _range(core, 0.0)
    reach = (hi - lo) * 0.5
    extra = [v for v in item["sma50"] + item["sma200"] if v is not None and lo - reach <= v <= hi + reach]
    lo, hi, step = _nice(*_range(core + extra))

    cats = Reference(data_ws, min_col=col, min_row=2, max_row=n + 1)
    stock = StockChart()
    stock.width, stock.height = size
    stock.add_data(Reference(data_ws, min_col=col + 1, max_col=col + 4, min_row=1, max_row=n + 1),
                   titles_from_data=True)
    stock.set_categories(cats)
    for s in stock.series:
        s.graphicalProperties = GraphicalProperties(ln=LineProperties(noFill=True))
        s.marker.symbol = "none"
    stock.hiLowLines = ChartLines(spPr=GraphicalProperties(ln=LineProperties(solidFill=INK_2, w=12700)))
    up = UpDownBars(gapWidth=60)
    up.upBars = ChartLines(spPr=GraphicalProperties(solidFill=GREEN, ln=LineProperties(solidFill=GREEN)))
    up.downBars = ChartLines(spPr=GraphicalProperties(solidFill=RED, ln=LineProperties(solidFill=RED)))
    stock.upDownBars = up
    # Excel toont de kaarsen pas als er een (lege) cache is.
    stock.series[-1].val.numRef.numCache = NumData(pt=[NumVal(idx=i) for i in range(n)])

    stock.y_axis.title = f"koers {item.get('valuta', '')}".strip()
    stock.y_axis.scaling.min, stock.y_axis.scaling.max = lo, hi
    stock.y_axis.majorUnit = step
    stock.y_axis.number_format = "#,##0.00" if hi < 100 else "#,##0"
    stock.y_axis.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill="E6E5E1"))
    stock.x_axis.number_format = "@"
    stock.x_axis.tickLblSkip = max(n // 5, 1)
    stock.x_axis.tickMarkSkip = max(n // 5, 1)
    stock.x_axis.delete = False
    stock.y_axis.delete = False

    over = LineChart()
    over.add_data(Reference(data_ws, min_col=col + 5, max_col=col + 4 + len(lines), min_row=1, max_row=n + 1),
                  titles_from_data=True)
    over.set_categories(cats)
    for s, (_, _, color, w, dash) in zip(over.series, lines):
        _line(s, color, w, dash)
    over.x_axis = stock.x_axis
    over.y_axis = stock.y_axis
    stock += over
    # Geen legenda in de grafiek (die toont ook opening/hoog/laag/slot en verschilt per Excel-versie);
    # de uitleg in kleur staat in een vaste regel direct boven de grafiek.
    stock.legend = None
    stock.layout = Layout(manualLayout=ManualLayout(x=0.02, y=0.03, w=0.96, h=0.8))
    return stock, col + len(cols) + 1


def value_chart(data_ws, series: dict[str, list[tuple[str, float]]], bench: list[tuple[str, float]],
                col: int, labels: dict[str, str], start: float = 10000.0) -> tuple[LineChart | None, int]:
    days = sorted({d for pts in series.values() for d, _ in pts})
    if len(days) < 2:
        return None, col
    by = {name: dict(pts) for name, pts in series.items()}
    bpts = dict(bench)
    bdays = [d for d in days if d in bpts]
    etf = {}
    if len(bdays) >= 2:
        base = bpts[bdays[0]]
        first = next((by[n][bdays[0]] for n in by if bdays[0] in by[n]), start)
        etf = {d: round(first * bpts[d] / base, 2) for d in bdays}
    names = list(series) + (["Wereld-ETF (zelfde startbedrag)"] if etf else []) + ["Start €10.000"]
    data_ws.cell(row=1, column=col, value="Waarde: Datum")
    for j, name in enumerate(names, start=1):
        data_ws.cell(row=1, column=col + j, value=name)
    for i, d in enumerate(days, start=2):
        data_ws.cell(row=i, column=col, value=labels.get(d, d))
        for j, name in enumerate(names, start=1):
            if name in by:
                v = by[name].get(d)
            elif name.startswith("Wereld"):
                v = etf.get(d)
            else:
                v = start
            data_ws.cell(row=i, column=col + j, value=v)
    vals = [v for pts in series.values() for _, v in pts] + list(etf.values()) + [start]
    lo, hi = _range(vals, 0.15)
    ch = _base_chart("waarde in euro", lo, hi, len(days))
    ch.add_data(Reference(data_ws, min_col=col + 1, max_col=col + len(names), min_row=1, max_row=len(days) + 1),
                titles_from_data=True)
    ch.set_categories(Reference(data_ws, min_col=col, min_row=2, max_row=len(days) + 1))
    styles = {"Investeerder": (BLUE, 2.75, None), "Trend-agent": (ORANGE, 2.75, None)}
    for s, name in zip(ch.series, names):
        color, w, dash = styles.get(name, (GREY, 2, "dash") if name.startswith("Wereld") else (INK_2, 1, None))
        _line(s, color, w, dash)
        if name in styles:
            s.marker.symbol = "circle"
            s.marker.size = 6
            s.marker.graphicalProperties = GraphicalProperties(solidFill=color, ln=LineProperties(solidFill=color))
    return ch, col + len(names) + 2


def _key() -> CellRichText:
    """Gekleurde legenda-regel: elk woord in de kleur van zijn lijn of kaars. Geldt voor alle grafieken."""
    parts = [("▮ groen", GREEN, " = dag gestegen    "), ("▮ rood", RED, " = dag gedaald    "),
             ("━ blauw", BLUE, " = gemiddelde 50 dagen    "), ("━ oranje", ORANGE, " = gemiddelde 200 dagen    "),
             ("╌ grijs", INK_2, " = instap    "), ("╌ rood", RED, " = stop-loss, hier verkoopt de bot")]
    out = []
    for word, color, rest in parts:
        out.append(TextBlock(InlineFont(b=True, color=color, sz=12), word))
        out.append(TextBlock(InlineFont(color=INK_2, sz=12), rest))
    return CellRichText(*out)


def _section(ws, row: int, title: str) -> int:
    c = ws.cell(row=row, column=2, value=title)
    c.font = Font(size=15, bold=True, color=INK)
    ws.row_dimensions[row].height = 26
    return row + 1


def _title_cells(ws, row: int, column: int, title: str, lines: list[str], wrap: bool = True) -> None:
    t = ws.cell(row=row, column=column, value=title)
    t.font = Font(size=13, bold=True, color=INK)
    t.alignment = Alignment(vertical="bottom")
    u = ws.cell(row=row + 1, column=column, value=" ".join(lines))
    u.font = Font(size=10.5, color=INK_2)
    u.alignment = Alignment(wrap_text=wrap, vertical="top")


def add(xlsx: Path, items: list[dict], value: dict | None = None, position: int | None = 1) -> None:
    """Tabblad 'Grafieken' als dashboard: bovenaan de waarde van de bots over de volle breedte,
    daaronder per bot de kaarsgrafieken, twee naast elkaar.

    value (optioneel): {"series": {naam: [(dag, waarde)]}, "bench": [(dag, koers)], "labels": {dag: label}}
    items: grafiekgegevens per instrument; item["bot"] ("trend"/"investeerder") bepaalt het blok.
    """
    if not xlsx.exists() or (not items and not value):
        return
    wb = load_workbook(xlsx)
    for name in ("Grafieken", "Grafiekdata"):
        if name in wb.sheetnames:
            del wb[name]
    ws = wb.create_sheet("Grafieken", position) if position is not None else wb.create_sheet("Grafieken")
    data_ws = wb.create_sheet("Grafiekdata")
    data_ws.sheet_state = "hidden"
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 90
    ws.column_dimensions["A"].width = 2
    ws.column_dimensions["B"].width = 84
    ws.column_dimensions["C"].width = 3
    ws.column_dimensions["D"].width = 84
    ws["B1"] = "Grafieken van vandaag"
    ws["B1"].font = Font(size=20, bold=True)
    ws.row_dimensions[1].height = 30
    ws["B2"] = _key()
    ws.row_dimensions[2].height = 20
    ws["B3"] = ("Elke kaars is één handelsdag; het dunne streepje loopt van de laagste naar de hoogste koers van die dag. "
                "Ga met de muis over een kaars of lijn om de waarde te zien.")
    ws["B3"].font = Font(size=10.5, italic=True, color=INK_2)
    row, col = 5, 1
    if value:
        vchart, _ = value_chart(data_ws, value["series"], value.get("bench", []), 300, value.get("labels", {}))
        if vchart:
            vchart.width, vchart.height = WIDE_W_CM, WIDE_H_CM
            _title_cells(ws, row, 2, "Hoeveel zijn de bots waard?",
                         ["Boven €10.000 = winst, eronder = verlies. De grijze stippellijn is wat je had gehad met "
                          "gewoon de wereld-ETF kopen en vasthouden."], wrap=False)
            ws.row_dimensions[row].height = 22
            ws.row_dimensions[row + 1].height = 20
            ws.add_chart(vchart, f"B{row + 2}")
            row += 2 + _rows_for(WIDE_H_CM) + 2

    groups: dict[str, list[dict]] = {}
    for item in items:
        groups.setdefault(item.get("bot", ""), []).append(item)
    names = {"trend": "Trend-agent: open posities", "investeerder": "Investeerder: beleggingen"}
    for bot, group in groups.items():
        if names.get(bot):
            row = _section(ws, row, names[bot])
        for i in range(0, len(group), 2):
            pair = group[i:i + 2]
            ws.row_dimensions[row].height = 22
            ws.row_dimensions[row + 1].height = 30
            for item, column, letter in zip(pair, (2, 4), ("B", "D")):
                ch, col = _price_chart(data_ws, item, col)
                _title_cells(ws, row, column, item["kop"], item["uitleg"])
                ws.add_chart(ch, f"{letter}{row + 2}")
            row += 2 + _rows_for(CHART_H_CM) + 1
        row += 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.orientation = "landscape"
    tmp = xlsx.with_suffix(".tmp.xlsx")
    wb.save(tmp)
    tmp.replace(xlsx)
