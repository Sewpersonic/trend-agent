"""Bepaalt wat 'trending' is. Alles is gewone rekenkunde: geen AI, geen gokwerk.

Een instrument is een kandidaat als ALLE regels kloppen:
1. genoeg historie (minimaal 210 handelsdagen);
2. laatste koers is vers (niet ouder dan max_bar_age_days);
3. slotkoers > 50-daags gemiddelde > 200-daags gemiddelde (stijgende trend);
4. rendement over 3 maanden en over 1 maand allebei positief;
5. genoeg handel: gemiddelde dagomzet boven de drempel;
6. geen verdachte dagsprong (> 25%) in de laatste 20 dagen.

De kandidaten worden gerangschikt op een trendscore:
  (0,6 x rendement 3 mnd + 0,4 x rendement 1 mnd) / volatiliteit
Zo wint een rustige, stevige stijger van een wilde stuiterbal.
Een bonus voor volume (meer handel dan normaal) telt mee, maar is begrensd.

Er wordt alleen data gebruikt tot en met de laatste slotkoers: geen
toekomstige informatie (geen look-ahead).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date

from .core.config import Settings
from .data import Bar

MIN_BARS = 210


def sma(values: list[float], n: int) -> float:
    if len(values) < n:
        raise ValueError(f"te weinig waarden voor SMA{n}")
    return sum(values[-n:]) / n


def atr(bars: list[Bar], n: int = 14) -> float:
    """Average True Range: hoe ver de koers gemiddeld per dag beweegt."""
    if len(bars) < n + 1:
        raise ValueError("te weinig koersen voor ATR")
    trs = []
    for prev, cur in zip(bars[-n - 1:-1], bars[-n:]):
        trs.append(max(cur.high - cur.low, abs(cur.high - prev.close), abs(cur.low - prev.close)))
    return sum(trs) / n


def pct_return(closes: list[float], n: int) -> float:
    return closes[-1] / closes[-n - 1] - 1


def volatility(closes: list[float], n: int = 63) -> float:
    rets = [closes[i] / closes[i - 1] - 1 for i in range(len(closes) - n, len(closes))]
    mean = sum(rets) / n
    return math.sqrt(sum((r - mean) ** 2 for r in rets) / (n - 1))


@dataclass(frozen=True)
class Analysis:
    ticker: str
    last_day: date
    close: float
    sma50: float
    sma200: float
    atr14: float
    ret21: float
    ret63: float
    vol63: float
    rel_volume: float
    avg_traded_value: float
    is_candidate: bool
    score: float
    reasons: tuple[str, ...]      # waarom wel of niet


def analyse(ticker: str, bars: list[Bar], today: date, s: Settings) -> Analysis:
    reasons: list[str] = []
    if len(bars) < MIN_BARS:
        return Analysis(ticker, bars[-1].day if bars else today, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        False, 0.0, (f"te weinig historie ({len(bars)} dagen)",))

    closes = [b.close for b in bars]
    vols = [b.volume for b in bars]
    close = closes[-1]
    s50, s200 = sma(closes, 50), sma(closes, 200)
    a14 = atr(bars)
    r21, r63 = pct_return(closes, 21), pct_return(closes, 63)
    v63 = volatility(closes)
    rel_vol = (sum(vols[-20:]) / 20) / max(sum(vols[-60:]) / 60, 1e-9)
    traded = sum(b.close * b.volume for b in bars[-20:]) / 20
    jumps = max(abs(closes[i] / closes[i - 1] - 1) for i in range(len(closes) - 20, len(closes)))
    age = (today - bars[-1].day).days

    ok = True
    if age > s.max_bar_age_days:
        ok = False; reasons.append(f"data te oud ({age} dagen)")
    if not close > s50 > s200:
        ok = False; reasons.append("geen stijgende trend (slot > SMA50 > SMA200 klopt niet)")
    if r63 <= 0 or r21 <= 0:
        ok = False; reasons.append("rendement 1 of 3 maanden niet positief")
    if traded < s.min_avg_traded_value:
        ok = False; reasons.append("te weinig handel")
    if jumps > s.max_daily_jump:
        ok = False; reasons.append(f"verdachte dagsprong ({jumps:.0%})")

    score = 0.0
    if ok:
        volume_bonus = min(max(rel_vol - 1.0, 0.0), 0.5) * 0.1   # max +0,05
        score = (0.6 * r63 + 0.4 * r21) / max(v63, 1e-6) / 100 + volume_bonus
        reasons.append(f"trend OK: 3m {r63:+.1%}, 1m {r21:+.1%}, volume x{rel_vol:.2f}")

    return Analysis(ticker, bars[-1].day, close, s50, s200, a14, r21, r63, v63,
                    rel_vol, traded, ok, round(score, 6), tuple(reasons))


def trend_broken(a: Analysis) -> bool:
    """Verkoopsignaal: slotkoers onder het 50-daags gemiddelde."""
    return a.close < a.sma50
