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


def candle_chart(bars: list[Bar], title: str, path: Path, entry: float | None = None,
                 stop: float | None = None, currency: str = "") -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    closes_all = [b.close for b in bars]
    sma50_all = _sma_series(closes_all, 50)
    sma200_all = _sma_series(closes_all, 200)
    view = bars[-WINDOW:]
    off = len(bars) - len(view)
    xs = list(range(len(view)))

    fig, (ax, axv) = plt.subplots(2, 1, figsize=(9, 5.2), dpi=85, sharex=True,
                                  gridspec_kw={"height_ratios": [3.2, 1], "hspace": 0.06})
    fig.patch.set_facecolor(SURFACE)
    for a in (ax, axv):
        a.set_facecolor(SURFACE)
        a.grid(axis="y", color=GRID, linewidth=0.8)
        for side in ("top", "right"):
            a.spines[side].set_visible(False)
        a.spines["left"].set_color(GRID)
        a.spines["bottom"].set_color(GRID)
        a.tick_params(colors=INK_2, labelsize=8)

    width = 0.62
    for x, b in zip(xs, view):
        up = b.close >= b.open
        color = UP if up else DOWN
        ax.vlines(x, b.low, b.high, color=color, linewidth=1)
        lo, hi = min(b.open, b.close), max(b.open, b.close)
        h = max(hi - lo, (b.high - b.low) * 0.01 or 1e-9)
        ax.add_patch(plt.Rectangle((x - width / 2, lo), width, h, facecolor=SURFACE if up else color,
                                   edgecolor=color, linewidth=1))
        axv.bar(x, b.volume, width=width, color=color, alpha=0.35, linewidth=0)

    for series, color, label in ((sma50_all, SMA50_COLOR, "50-daags gem."), (sma200_all, SMA200_COLOR, "200-daags gem.")):
        ys = series[off:]
        pts = [(x, y) for x, y in zip(xs, ys) if y is not None]
        if pts:
            ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, linewidth=2, label=label)
            ax.annotate(label, (pts[-1][0], pts[-1][1]), xytext=(4, 0), textcoords="offset points",
                        fontsize=8, color=INK_2, va="center")

    for level, label in ((entry, "instap"), (stop, "stop-loss")):
        if level:
            ax.axhline(level, color=INK_2, linewidth=1, linestyle=(0, (4, 3)))
            ax.annotate(f"{label} {level:,.2f}", (xs[0], level), xytext=(2, 3), textcoords="offset points",
                        fontsize=8, color=INK_2)

    ticks = xs[::max(len(xs) // 6, 1)]
    axv.set_xticks(ticks)
    axv.set_xticklabels([view[i].day.strftime("%d %b") for i in ticks])
    ax.set_xlim(-1, len(xs) + 7)   # ruimte rechts voor de lijnlabels
    ax.set_ylabel(f"koers {currency}".strip(), fontsize=9, color=INK_2)
    axv.set_ylabel("volume", fontsize=9, color=INK_2)
    axv.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
        lambda v, _: f"{v / 1e6:.0f} mln" if v >= 1e6 else f"{v / 1e3:.0f}k"))
    last = view[-1]
    change = last.close / view[0].close - 1
    ax.set_title(f"{title}   slot {last.close:,.2f} {currency}  ({change:+.1%} in 3 mnd)",
                 loc="left", fontsize=11, color=INK, pad=18)
    ax.legend(loc="lower right", bbox_to_anchor=(1.0, 1.0), ncol=2, frameon=False, fontsize=8,
              labelcolor=INK_2, borderaxespad=0.2)
    fig.text(0.01, 0.005, "Hol = dag gestegen, gevuld = dag gedaald. Nepgeld-oefenportefeuille; geen advies.",
             fontsize=7, color=INK_2)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor=SURFACE, bbox_inches="tight")
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


def add_to_excel(xlsx: Path, paths: list[Path]) -> None:
    """Zet de grafieken in een tabblad 'Grafieken' van een bestaand Excel-bestand."""
    if not paths or not xlsx.exists():
        return
    from openpyxl import load_workbook
    from openpyxl.drawing.image import Image

    wb = load_workbook(xlsx)
    if "Grafieken" in wb.sheetnames:
        del wb["Grafieken"]
    ws = wb.create_sheet("Grafieken", 1)
    row = 1
    for p in paths:
        img = Image(str(p))
        img.width, img.height = img.width * 0.8, img.height * 0.8
        ws.add_image(img, f"A{row}")
        row += int(img.height / 20) + 2
    tmp = xlsx.with_suffix(".tmp.xlsx")
    wb.save(tmp)
    tmp.replace(xlsx)
