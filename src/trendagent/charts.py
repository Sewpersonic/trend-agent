"""Candlestick-grafieken voor de rapporten.

Per instrument: de laatste ~3 maanden dagkoersen als candles, met
- het 50- en 200-daags gemiddelde (de lijnen waarop de trend-agent beslist);
- de instapprijs en de stop-loss als stippellijnen (bij een open positie);
- het handelsvolume in een apart paneel eronder (aparte schaal, geen tweede y-as).

Candles: hol = slot hoger dan opening (stijgend), gevuld = slot lager (dalend).
De kleur (groen/rood) is extra; door hol/gevuld blijft het ook zonder kleur leesbaar.

Grafieken mogen de handel nooit beïnvloeden: fouten worden opgevangen door de aanroeper.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from .data import Bar

UP = "#008300"
DOWN = "#e34948"
SMA50_COLOR = "#2a78d6"
SMA200_COLOR = "#eb6834"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e6e5e1"
SURFACE = "#fcfcfb"
WINDOW = 65          # ongeveer 3 maanden handelsdagen
KEEP_DAYS = 20       # zoveel dagmappen met grafieken bewaren


def _sma_series(closes: list[float], n: int) -> list[float | None]:
    out, run = [], 0.0
    for i, c in enumerate(closes):
        run += c
        if i >= n:
            run -= closes[i - n]
        out.append(run / n if i >= n - 1 else None)
    return out


MONTHS = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
REFERENCE = "#8a8984"   # neutrale lijn voor de wereld-ETF (vergelijking, geen eigen reeks)


def _nl(x: float, digits: int = 2) -> str:
    return f"{x:,.{digits}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _day(d) -> str:
    return f"{d.day} {MONTHS[d.month - 1]}"


def _style(ax) -> None:
    ax.set_facecolor(SURFACE)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK_2, labelsize=10)


def _verdict(close: float, s50: float | None, s200: float | None) -> str:
    if s50 is None or s200 is None:
        return "Te weinig historie om de trend te beoordelen."
    if close > s50 > s200:
        return "Stijgende trend: de koers staat boven beide gemiddelden."
    if close < s50 < s200:
        return "Dalende trend: de koers staat onder beide gemiddelden."
    if close < s50:
        return "Trend verzwakt: de koers is onder het 50-daags gemiddelde gezakt."
    return "Geen duidelijke richting: de gemiddelden kruisen elkaar."


def describe(title: str, view: list[Bar], s50: float | None, s200: float | None, entry: float | None,
             stop: float | None, currency: str) -> tuple[str, list[str]]:
    """Kop en uitleg in gewone taal (dezelfde tekst in de afbeelding en in Excel)."""
    last = view[-1]
    cur = f" {currency}" if currency else ""
    change = last.close / view[0].close - 1
    head = f"{title}  ·  {_nl(last.close)}{cur}"
    lines = [f"{'Gestegen' if change >= 0 else 'Gedaald'}: {_nl(change * 100, 1)}% in de laatste 3 maanden. "
             + _verdict(last.close, s50, s200)]
    if entry:
        res = last.close / entry - 1
        if abs(res) < 0.0005:
            lines.append("Sinds de bot kocht: nog vrijwel gelijk.")
        else:
            lines.append(f"Sinds de bot kocht: {'+' if res >= 0 else ''}{_nl(res * 100, 1)}% "
                         f"({'winst' if res >= 0 else 'verlies'}).")
    if stop:
        lines[-1] += f" De bot verkoopt als de koers onder {_nl(stop)} zakt ({_nl((stop / last.close - 1) * 100, 1)}%)."
    return head, lines


def chart_data(bars: list[Bar], title: str, entry: float | None = None, stop: float | None = None,
               currency: str = "", opened: str | None = None, sold: tuple[str, float] | None = None) -> dict:
    """De cijfers achter een grafiek, zodat Excel er zelf een echte grafiek van kan maken."""
    closes = [b.close for b in bars]
    s50, s200 = _sma_series(closes, 50), _sma_series(closes, 200)
    view = bars[-WINDOW:]
    off = len(bars) - len(view)
    head, lines = describe(title, view, s50[-1], s200[-1], entry, stop, currency)
    r = lambda v: None if v is None else round(v, 4)  # noqa: E731
    return {"titel": title, "kop": head, "uitleg": lines, "valuta": currency,
            "datums": [_day(b.day) for b in view], "iso": [b.day.isoformat() for b in view],
            "koers": [r(b.close) for b in view], "sma50": [r(v) for v in s50[off:]],
            "sma200": [r(v) for v in s200[off:]], "instap": entry, "stop": stop, "gekocht": opened,
            "verkocht": sold[0] if sold else None}


def candle_chart(bars: list[Bar], title: str, path: Path, entry: float | None = None,
                 stop: float | None = None, currency: str = "", opened: str | None = None,
                 sold: tuple[str, float] | None = None) -> Path:
    """Candle-grafiek die je zonder beurskennis kunt lezen.

    Bovenaan in gewone taal: hoe het ervoor staat. Rechts prijslabels (koers nu, instap, stop-loss).
    Onder de stop-loss een lichtrode 'verkoopzone'. Driehoekjes bij de dag van kopen/verkopen.
    Onderaan: hoe je de grafiek leest.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    closes_all = [b.close for b in bars]
    sma50_all = _sma_series(closes_all, 50)
    sma200_all = _sma_series(closes_all, 200)
    view = bars[-WINDOW:]
    off = len(bars) - len(view)
    xs = list(range(len(view)))
    last = view[-1]
    cur = f" {currency}" if currency else ""

    fig = plt.figure(figsize=(12, 7.2), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax = fig.add_axes([0.07, 0.19, 0.74, 0.63])
    _style(ax)

    # Koptekst in gewone taal
    head, lines = describe(title, view, sma50_all[-1], sma200_all[-1], entry, stop, currency)
    fig.text(0.07, 0.95, head, fontsize=17, fontweight="bold", color=INK, va="top")
    fig.text(0.07, 0.905, "\n".join(lines), fontsize=11.5, color=INK_2, va="top", linespacing=1.5)

    base_lo = min([b.low for b in view] + [v for v in (stop, entry) if v])
    base_hi = max([b.high for b in view] + [v for v in (stop, entry) if v])
    # Gemiddelden die ver buiten beeld liggen niet meenemen, anders worden de candles platgedrukt.
    reach = (base_hi - base_lo) * 0.5
    smas = [v for v in sma50_all[off:] + sma200_all[off:]
            if v is not None and base_lo - reach <= v <= base_hi + reach]
    lows = [base_lo] + smas
    highs = [base_hi] + smas
    lo, hi = min(lows), max(highs)
    pad = (hi - lo) * 0.08 or 1
    ax.set_ylim(lo - pad, hi + pad)

    # Verkoopzone onder de stop-loss
    if stop:
        ax.axhspan(lo - pad, stop, color=DOWN, alpha=0.07, linewidth=0)
        ax.text(1, lo - pad * 0.6, "verkoopzone: onder de stop-loss verkoopt de bot", fontsize=9.5, color=DOWN,
                va="bottom", zorder=5, bbox={"boxstyle": "round,pad=0.2", "facecolor": SURFACE, "edgecolor": "none"})

    # Gemiddelden
    for series, color, label in ((sma50_all, SMA50_COLOR, "50-daags gemiddelde"),
                                 (sma200_all, SMA200_COLOR, "200-daags gemiddelde")):
        pts = [(x, y) for x, y in zip(xs, series[off:]) if y is not None]
        if pts:
            ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, linewidth=2.2, zorder=2)

    # Candles
    width = 0.66
    for x, b in zip(xs, view):
        up = b.close >= b.open
        color = UP if up else DOWN
        ax.vlines(x, b.low, b.high, color=color, linewidth=1.1, zorder=3)
        l, h = min(b.open, b.close), max(b.open, b.close)
        ax.add_patch(plt.Rectangle((x - width / 2, l), width, max(h - l, (hi - lo) * 0.002),
                                   facecolor=SURFACE if up else color, edgecolor=color, linewidth=1.1, zorder=3))

    # Lijnen voor instap en stop
    for level, color in ((entry, INK_2), (stop, DOWN)):
        if level:
            ax.axhline(level, color=color, linewidth=1.3, linestyle=(0, (5, 3)), zorder=1)

    # Kopen / verkopen markeren: verticale stippellijn met label bovenaan
    days = [b.day.isoformat() for b in view]
    for when, label in ((opened, "gekocht"), (sold[0] if sold else None, "verkocht")):
        if when and when in days:
            i = days.index(when)
            ax.axvline(i, color=INK, linewidth=1, linestyle=(0, (2, 3)), zorder=1)
            ax.text(i, hi + pad * 0.55, f"{label} {_day(view[i].day)}", ha="right" if i > len(xs) - 6 else "center", va="center", fontsize=10,
                    fontweight="bold", color=INK,
                    bbox={"boxstyle": "round,pad=0.25", "facecolor": SURFACE, "edgecolor": INK, "linewidth": 0.8})

    # Prijslabels rechts, uit elkaar geschoven zodat ze nooit overlappen
    tags = [(last.close, f"koers nu {_nl(last.close)}", INK, True)]
    if entry:
        tags.append((entry, f"instap {_nl(entry)}", INK_2, False))
    if stop:
        tags.append((stop, f"stop-loss {_nl(stop)}", DOWN, False))
    for series, color, label in ((sma50_all, SMA50_COLOR, "50-daags gem."), (sma200_all, SMA200_COLOR, "200-daags gem.")):
        v = series[-1]
        if v is None:
            continue
        if v < lo - pad:
            tags.append((lo - pad * 0.5, f"{label} {_nl(v)} \n(lager, buiten beeld)", color, False))
        elif v > hi + pad:
            tags.append((hi + pad * 0.5, f"{label} {_nl(v)} \n(hoger, buiten beeld)", color, False))
        else:
            tags.append((v, f"{label} {_nl(v)}", color, False))
    span = (hi + pad) - (lo - pad)
    min_gap = span * 0.065
    placed = []
    for y, text, color, bold in sorted(tags, key=lambda t: -t[0]):
        ty = y if not placed else min(y, placed[-1] - min_gap)
        placed.append(ty)
        ax.annotate(text, xy=(len(xs) - 1, y), xytext=(len(xs) + 1.5, ty), textcoords="data",
                    fontsize=10.5, color=INK if bold else INK_2, fontweight="bold" if bold else "normal", va="center",
                    arrowprops={"arrowstyle": "-", "color": color, "linewidth": 2, "shrinkA": 0, "shrinkB": 2},
                    annotation_clip=False)

    ticks = xs[::max(len(xs) // 6, 1)]
    ax.set_xticks(ticks)
    ax.set_xticklabels([_day(view[i].day) for i in ticks])
    ax.set_xlim(-1, len(xs))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: _nl(v, 0 if hi > 100 else 2)))
    ax.set_ylabel(f"koers{cur}", fontsize=10.5, color=INK_2)

    fig.text(0.07, 0.11,
             "Zo lees je deze grafiek:  elk staafje is één handelsdag.  Groen en hol = die dag gestegen, "
             "rood en gevuld = die dag gedaald.\n"
             "De blauwe lijn is de gemiddelde koers van de laatste 50 dagen, de oranje lijn van de laatste 200 dagen. "
             "Koers boven beide lijnen = stijgende trend.",
             fontsize=9.5, color=INK_2, va="top", linespacing=1.6)
    fig.text(0.07, 0.015, "Oefenportefeuille met nepgeld. Geen beleggingsadvies.", fontsize=8.5, color=INK_2)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)
    return path


def value_chart(series: dict[str, list[tuple[str, float]]], bench: list[tuple[str, float]], path: Path,
                start: float = 10000.0) -> Path | None:
    """Waarde van de bots per dag, met de wereld-ETF omgerekend naar dezelfde €10.000-start (één as)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    days = sorted({d for pts in series.values() for d, _ in pts})
    if len(days) < 2:
        return None
    fig = plt.figure(figsize=(12, 6), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax = fig.add_axes([0.08, 0.17, 0.72, 0.62])
    _style(ax)
    idx = {d: i for i, d in enumerate(days)}
    ax.axhline(start, color=INK_2, linewidth=1, zorder=1)
    ax.text(-0.25, start, f"start {_nl(start, 0)} euro", fontsize=9.5, color=INK_2, va="bottom", ha="left",
            bbox={"boxstyle": "round,pad=0.15", "facecolor": SURFACE, "edgecolor": "none"}, zorder=5)
    labels = []
    colors = {"Investeerder": SMA50_COLOR, "Trend-agent": SMA200_COLOR}
    for name, pts in series.items():
        if not pts:
            continue
        ax.plot([idx[d] for d, _ in pts], [v for _, v in pts], color=colors.get(name, INK), linewidth=2.4,
                marker="o", markersize=5, zorder=3)
        labels.append((pts[-1][1], f"{name} {_nl(pts[-1][1])}", colors.get(name, INK)))
    bpts = [(d, v) for d, v in bench if d in idx]
    if len(bpts) >= 2:
        base = bpts[0][1]
        # Zelfde startbedrag als de bot op de eerste dag met ETF-koers, zodat je eerlijk vergelijkt.
        first_bot = next((v for pts in series.values() for d, v in pts if d == bpts[0][0]), start)
        ys = [first_bot * v / base for _, v in bpts]
        ax.plot([idx[d] for d, _ in bpts], ys, color=REFERENCE, linewidth=2, linestyle=(0, (5, 3)), zorder=2)
        labels.append((ys[-1], f"wereld-ETF {_nl(ys[-1])}", REFERENCE))
    vals = [v for pts in series.values() for _, v in pts] + [l[0] for l in labels] + [start]
    lo, hi = min(vals), max(vals)
    pad = max((hi - lo) * 0.15, 20)
    ax.set_ylim(lo - pad, hi + pad)
    ax.axhspan(start, hi + pad, color=UP, alpha=0.05, linewidth=0, zorder=0)
    ax.axhspan(lo - pad, start, color=DOWN, alpha=0.05, linewidth=0, zorder=0)
    ax.text(len(days) - 1, hi + pad * 0.6, "winst", fontsize=10, color=INK_2, ha="right", va="center")
    ax.text(len(days) - 1, lo - pad * 0.6, "verlies", fontsize=10, color=INK_2, ha="right", va="center")
    placed = []
    for y, text, color in sorted(labels, key=lambda t: -t[0]):
        ty = y if not placed else min(y, placed[-1] - (hi - lo + 2 * pad) * 0.07)
        placed.append(ty)
        ax.annotate(text, xy=(len(days) - 1, y), xytext=(len(days) - 1 + max(len(days) * 0.04, 0.3), ty),
                    fontsize=11, color=INK, va="center", fontweight="bold", annotation_clip=False,
                    arrowprops={"arrowstyle": "-", "color": color, "linewidth": 2.4})
    from datetime import date as _d
    step = max(len(days) // 8, 1)
    ax.set_xticks(list(range(0, len(days), step)))
    ax.set_xticklabels([_day(_d.fromisoformat(d)) for d in days[::step]])
    ax.set_xlim(-0.3, len(days) - 1 + max(len(days) * 0.04, 0.3))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: _nl(v, 0)))
    ax.set_ylabel("waarde in euro", fontsize=10.5, color=INK_2)
    fig.text(0.08, 0.94, "Hoeveel zijn de bots waard?", fontsize=17, fontweight="bold", color=INK, va="top")
    sub = "Boven de startlijn = winst, eronder = verlies."
    if len(bpts) >= 2:
        sub += " De grijze stippellijn: wat je had gehad met gewoon de wereld-ETF kopen en vasthouden."
    fig.text(0.08, 0.885, sub, fontsize=11.5, color=INK_2, va="top")
    fig.text(0.08, 0.04, "Oefenportefeuilles met nepgeld. Geen beleggingsadvies.", fontsize=8.5, color=INK_2)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)
    return path


def chart_dir(reports_dir: Path, day: str) -> Path:
    return reports_dir / "grafieken" / day


def prune(reports_dir: Path, keep: int = KEEP_DAYS) -> None:
    root = reports_dir / "grafieken"
    if not root.exists():
        return
    days = sorted(p for p in root.iterdir() if p.is_dir())
    for old in days[:-keep]:
        shutil.rmtree(old, ignore_errors=True)


def markdown_section(paths: list[Path], reports_dir: Path) -> str:
    if not paths:
        return ""
    lines = ["", "## Grafieken (laatste 3 maanden)", ""]
    for p in paths:
        rel = p.relative_to(reports_dir).as_posix()
        lines += [f"![{p.stem}]({rel})", ""]
    lines.append(f"_Grafieken worden {KEEP_DAYS} handelsdagen bewaard._")
    return "\n".join(lines) + "\n"


EXCEL_IMAGE_WIDTH = 880        # pixels: ongeveer schermbreed in Excel
MAX_ROW_POINTS = 400           # Excel staat maximaal 409 punten rijhoogte toe


def place_image(ws, png: Path, row: int, column: str = "B", width: int = EXCEL_IMAGE_WIDTH) -> int:
    """Zet één grafiek in een eigen rij die precies zo hoog is als de grafiek. Zo kunnen grafieken
    nooit over elkaar of over tekst heen vallen. Geeft de eerstvolgende vrije rij terug."""
    from openpyxl.drawing.image import Image
    img = Image(str(png))
    scale = width / img.width
    w, h = img.width * scale, img.height * scale
    if h * 0.75 > MAX_ROW_POINTS:                 # te hoog voor één rij: kleiner maken
        f = MAX_ROW_POINTS / (h * 0.75)
        w, h = w * f, h * f
    img.width, img.height = w, h
    ws.row_dimensions[row].height = h * 0.75 + 6   # pixels -> punten, plus een beetje lucht
    ws.add_image(img, f"{column}{row}")
    return row + 1


def add_to_excel(xlsx: Path, paths: list[Path], titles: list[str] | None = None, position: int | None = 1) -> None:
    """Tabblad 'Grafieken': alle grafieken onder elkaar, elk met een kopje en een eigen rij."""
    if not paths or not xlsx.exists():
        return
    from openpyxl import load_workbook
    from openpyxl.styles import Font

    wb = load_workbook(xlsx)
    if "Grafieken" in wb.sheetnames:
        del wb["Grafieken"]
    ws = wb.create_sheet("Grafieken", position) if position is not None else wb.create_sheet("Grafieken")
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 100
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 128     # zo breed als de grafiek, zodat afdrukken/PDF niets afsnijdt
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws["B1"] = "Grafieken van vandaag"
    ws["B1"].font = Font(size=18, bold=True)
    ws.row_dimensions[1].height = 28
    ws["B2"] = ("Scroll naar beneden: alle grafieken staan onder elkaar. Elke grafiek legt bovenaan in gewone taal uit "
                "hoe het ervoor staat, en onderaan hoe je hem leest.")
    ws["B2"].font = Font(size=11, italic=True, color="52514E")
    row = 4
    for n, p in enumerate(paths, 1):
        title = titles[n - 1] if titles and n <= len(titles) else p.stem
        ws.cell(row=row, column=2, value=f"{n}. {title}").font = Font(size=14, bold=True)
        ws.row_dimensions[row].height = 26
        row = place_image(ws, p, row + 1)
        ws.row_dimensions[row].height = 30        # witregel tussen twee grafieken
        row += 1
    tmp = xlsx.with_suffix(".tmp.xlsx")
    wb.save(tmp)
    tmp.replace(xlsx)
