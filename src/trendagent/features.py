"""Marktanalyse: indicatoren, marktregime en datakwaliteit.

Alles is gewone, deterministische rekenkunde op koersen t/m de laatste
slotkoers (geen blik in de toekomst). Deze module verandert zelf geen
beslissingen: hij levert meetwaarden die
- bij elke trade worden vastgelegd (zodat we later kunnen meten wat werkt), en
- door strategieën als filter gebruikt KUNNEN worden, maar alleen als een
  instelling dat aanzet en de evaluatie heeft laten zien dat het helpt.

Indicatoren
  EMA      exponentieel voortschrijdend gemiddelde
  RSI(14)  kracht van recente stijgingen t.o.v. dalingen (0-100; >70 = sterk/overgekocht)
  MACD     EMA12 - EMA26, met signaallijn EMA9; histogram > 0 = momentum neemt toe
  ATR%     gemiddelde dagbeweging als percentage van de koers (beweeglijkheid)

Marktregime (op basis van de brede markt, standaard de MSCI World-ETF)
  trend:       "stijgend"  slot > SMA200 en SMA50 > SMA200
               "dalend"    slot < SMA200 en SMA50 < SMA200
               "zijwaarts" anders
  beweeglijkheid: beweeglijkheid van de laatste 20 dagen vergeleken met het
               afgelopen jaar: "laag" (onderste kwart), "hoog" (bovenste kwart), anders "normaal"
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .data import Bar

REGIME_BENCHMARKS = ("IWDA.AS", "SPY")


# ------------------------------------------------------------- indicatoren

def ema_series(values: list[float], n: int) -> list[float]:
    if len(values) < n:
        raise ValueError(f"te weinig waarden voor EMA{n}")
    k = 2 / (n + 1)
    out = [sum(values[:n]) / n]           # start met een gewoon gemiddelde
    for v in values[n:]:
        out.append(v * k + out[-1] * (1 - k))
    return out


def ema(values: list[float], n: int) -> float:
    return ema_series(values, n)[-1]


def rsi(closes: list[float], n: int = 14) -> float:
    """RSI volgens Wilder. 50 = neutraal."""
    if len(closes) < n + 1:
        raise ValueError("te weinig koersen voor RSI")
    gains, losses = 0.0, 0.0
    for i in range(1, n + 1):
        d = closes[i] - closes[i - 1]
        gains += max(d, 0.0)
        losses += max(-d, 0.0)
    avg_g, avg_l = gains / n, losses / n
    for i in range(n + 1, len(closes)):
        d = closes[i] - closes[i - 1]
        avg_g = (avg_g * (n - 1) + max(d, 0.0)) / n
        avg_l = (avg_l * (n - 1) + max(-d, 0.0)) / n
    if avg_l == 0:
        return 100.0 if avg_g > 0 else 50.0
    return 100 - 100 / (1 + avg_g / avg_l)


def macd(closes: list[float], fast: int = 12, slow: int = 26, signal: int = 9) -> tuple[float, float, float]:
    """Geeft (macd, signaal, histogram)."""
    if len(closes) < slow + signal:
        raise ValueError("te weinig koersen voor MACD")
    f = ema_series(closes, fast)
    s = ema_series(closes, slow)
    line = [a - b for a, b in zip(f[len(f) - len(s):], s)]
    sig = ema_series(line, signal)
    return line[-1], sig[-1], line[-1] - sig[-1]


def realized_vol(closes: list[float], n: int) -> float:
    rets = [closes[i] / closes[i - 1] - 1 for i in range(len(closes) - n, len(closes))]
    m = sum(rets) / n
    return math.sqrt(sum((r - m) ** 2 for r in rets) / max(n - 1, 1)) * math.sqrt(252)


def snapshot(bars: list[Bar]) -> dict:
    """Meetwaarden van één instrument op de laatste dag. Leeg als er te weinig historie is."""
    if len(bars) < 60:
        return {}
    closes = [b.close for b in bars]
    out: dict = {}
    try:
        out["rsi14"] = round(rsi(closes[-200:]), 1)
        m, s, h = macd(closes[-200:])
        out["macd_hist_pct"] = round(h / closes[-1] * 100, 3)    # als % van de koers, vergelijkbaar
        out["ema20_afstand_pct"] = round((closes[-1] / ema(closes[-200:], 20) - 1) * 100, 2)
        trs = [max(c.high - c.low, abs(c.high - p.close), abs(c.low - p.close)) for p, c in zip(bars[-15:-1], bars[-14:])]
        out["atr_pct"] = round(sum(trs) / len(trs) / closes[-1] * 100, 2)
        out["vol20_jaar"] = round(realized_vol(closes, 20), 3)
    except ValueError:
        pass
    if len(closes) >= 200:
        sma200 = sum(closes[-200:]) / 200
        out["afstand_sma200_pct"] = round((closes[-1] / sma200 - 1) * 100, 2)
    return out


# ------------------------------------------------------------------ regime

@dataclass(frozen=True)
class Regime:
    trend: str             # stijgend / dalend / zijwaarts / onbekend
    beweeglijkheid: str    # laag / normaal / hoog / onbekend
    bron: str

    @property
    def label(self) -> str:
        return f"{self.trend}-{self.beweeglijkheid}"

    @property
    def onzeker(self) -> bool:
        """Omstandigheden waarin nieuwe posities extra riskant zijn: dalende trend of hoge beweeglijkheid."""
        return self.trend == "dalend" or self.beweeglijkheid == "hoog"


UNKNOWN = Regime("onbekend", "onbekend", "")


def market_regime(bars_by_ticker: dict[str, list[Bar]]) -> Regime:
    for t in REGIME_BENCHMARKS:
        bars = bars_by_ticker.get(t)
        if bars and len(bars) >= 260:
            return _regime_from(bars, t)
    return UNKNOWN


def _regime_from(bars: list[Bar], source: str) -> Regime:
    closes = [b.close for b in bars]
    sma50 = sum(closes[-50:]) / 50
    sma200 = sum(closes[-200:]) / 200
    c = closes[-1]
    if c > sma200 and sma50 > sma200:
        trend = "stijgend"
    elif c < sma200 and sma50 < sma200:
        trend = "dalend"
    else:
        trend = "zijwaarts"
    # Beweeglijkheid nu vs. de verdeling over het afgelopen jaar (20-daagse vensters).
    vols = [realized_vol(closes[:i], 20) for i in range(len(closes) - 230, len(closes) + 1, 5)]
    now = vols[-1]
    srt = sorted(vols)
    low, high = srt[len(srt) // 4], srt[(3 * len(srt)) // 4]
    level = "hoog" if now > high else "laag" if now < low else "normaal"
    return Regime(trend, level, source)


# ----------------------------------------------------------- datakwaliteit

def data_issues(bars: list[Bar], max_jump: float = 0.40) -> list[str]:
    """Signalen dat een koersreeks onbetrouwbaar is. Leeg = geen bijzonderheden.

    - bevroren koers: de laatste 5 slotkoersen exact gelijk (feed hangt of handel stilgelegd);
    - geen handel: volume 0 op de laatste dag (bij aandelen/ETF's verdacht);
    - extreme sprong: meer dan 40% op één dag in de laatste 5 dagen (vaak een datafout of split).
    """
    issues = []
    if len(bars) >= 5 and len({round(b.close, 6) for b in bars[-5:]}) == 1:
        issues.append("koers 5 dagen exact gelijk (bevroren?)")
    if bars and bars[-1].volume == 0:
        issues.append("geen handelsvolume op de laatste dag")
    for p, c in zip(bars[-6:-1], bars[-5:]):
        if p.close > 0 and abs(c.close / p.close - 1) > max_jump:
            issues.append(f"sprong van {c.close / p.close - 1:+.0%} op {c.day}")
            break
    return issues


# ------------------------------------------------------- achterlopende koersen

def expected_market_day(now_utc) -> "date":
    """De handelsdag waarvan de slotkoersen er nu zouden moeten zijn.

    Na 21:00 UTC zijn zowel Europa als Amerika gesloten: dan is het vandaag.
    Daarvoor (bijv. een run die door GitHub pas na middernacht start): de vorige werkdag.
    """
    from datetime import timedelta
    d = now_utc.date() if now_utc.hour >= 21 else now_utc.date() - timedelta(days=1)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


def stale_issues(bars_by_ticker: dict, expected_day, regions: dict) -> tuple[dict, list[str]]:
    """Welke koersreeksen lopen achter op de verwachte handelsdag?

    Geeft (problemen per ticker, waarschuwingen per regio). Crypto wordt overgeslagen.
    regions: ticker -> regio ("US", "EU", "CRYPTO").
    """
    issues: dict[str, list[str]] = {}
    per_region: dict[str, list] = {}
    for t, bars in bars_by_ticker.items():
        region = regions.get(t, "?")
        if region == "CRYPTO" or not bars:
            continue
        last = bars[-1].day
        per_region.setdefault(region, []).append(last)
        if last < expected_day:
            issues[t] = [f"koers niet bijgewerkt (laatste {last:%d-%m}, verwacht {expected_day:%d-%m})"]
    warnings = []
    for region, lasts in per_region.items():
        if lasts and max(lasts) < expected_day:
            warnings.append(f"Alle koersen uit {region} lopen achter (nieuwste {max(lasts):%d-%m}): mogelijk een "
                            f"beursvakantie of een storing bij de bron. Daar vandaag niets gekocht.")
    return issues, warnings
