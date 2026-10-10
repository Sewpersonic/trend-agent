"""Koersdata.

Twee bronnen met dezelfde interface:
- YahooProvider: gratis dagkoersen via het pakket yfinance (voor echt oefenen);
- SimulatedProvider: verzonnen koersen, voor tests en voor draaien zonder internet.

Elke fout of ontbrekende reeks levert een DataError op. De agent handelt dan
niet in dat instrument (of helemaal niet, als de wisselkoers ontbreekt).
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Protocol

from .universe import Instrument


class DataError(RuntimeError):
    pass


@dataclass(frozen=True)
class Bar:
    day: date
    open: float
    high: float
    low: float
    close: float
    volume: float


class DataProvider(Protocol):
    name: str

    def history(self, instrument: Instrument, days: int) -> list[Bar]: ...

    def usd_to_eur(self) -> float: ...


def validate_bars(bars: list[Bar], ticker: str) -> list[Bar]:
    """Basiscontrole: oplopende datums, positieve prijzen, high >= low."""
    if not bars:
        raise DataError(f"{ticker}: geen koersdata")
    prev = None
    for b in bars:
        if not all(math.isfinite(x) for x in (b.open, b.high, b.low, b.close, b.volume)):
            raise DataError(f"{ticker}: ongeldige waarde op {b.day}")
        if min(b.open, b.high, b.low, b.close) <= 0 or b.high < b.low or b.volume < 0:
            raise DataError(f"{ticker}: onlogische koers op {b.day}")
        if prev and b.day <= prev:
            raise DataError(f"{ticker}: datums niet oplopend rond {b.day}")
        prev = b.day
    return bars


class YahooProvider:
    """Dagkoersen van Yahoo Finance. Gratis, maar onofficieel: kan haperen."""

    name = "yahoo"

    def __init__(self):
        try:
            import yfinance  # noqa: F401  (pas laden als deze bron echt wordt gebruikt)
        except ImportError as exc:
            raise DataError("Installeer eerst yfinance: pip install yfinance") from exc

    def history(self, instrument: Instrument, days: int) -> list[Bar]:
        import yfinance as yf

        try:
            df = yf.Ticker(instrument.ticker).history(
                period=f"{max(days * 2, 400)}d", interval="1d", auto_adjust=True)
        except Exception as exc:  # netwerk, rate limit, onbekende ticker
            raise DataError(f"{instrument.ticker}: ophalen mislukt ({type(exc).__name__})") from exc
        if df is None or df.empty:
            raise DataError(f"{instrument.ticker}: lege reeks")
        bars = [
            Bar(idx.date(), float(r["Open"]), float(r["High"]), float(r["Low"]),
                float(r["Close"]), float(r["Volume"]))
            for idx, r in df.iterrows()
            if r["Close"] == r["Close"]  # NaN-regels overslaan
        ]
        return validate_bars(bars[-days:], instrument.ticker)

    def usd_to_eur(self) -> float:
        import yfinance as yf

        try:
            df = yf.Ticker("EURUSD=X").history(period="10d", interval="1d")
        except Exception as exc:
            raise DataError("wisselkoers EUR/USD: ophalen mislukt") from exc
        if df is None or df.empty:
            raise DataError("wisselkoers EUR/USD ontbreekt")
        eurusd = float(df["Close"].iloc[-1])
        if not 0.5 < eurusd < 2.0:
            raise DataError(f"wisselkoers EUR/USD onwaarschijnlijk: {eurusd}")
        return 1.0 / eurusd


class SimulatedProvider:
    """Verzonnen maar reproduceerbare koersen (zelfde seed = zelfde koersen).

    `drifts` laat je per ticker een trend opgeven, handig in tests.
    """

    name = "simulated"

    def __init__(self, end: date, seed: int = 7, drifts: dict[str, float] | None = None,
                 usd_eur: float = 0.92, missing: set[str] | None = None):
        self.end = end
        self.seed = seed
        self.drifts = drifts or {}
        self._usd_eur = usd_eur
        self.missing = missing or set()

    def history(self, instrument: Instrument, days: int) -> list[Bar]:
        if instrument.ticker in self.missing:
            raise DataError(f"{instrument.ticker}: (gesimuleerd) geen data")
        rng = random.Random(f"{self.seed}-{instrument.ticker}")
        drift = self.drifts.get(instrument.ticker, rng.uniform(-0.0008, 0.0012))
        price = rng.uniform(40, 400)
        bars, day = [], self.end
        # Werkdagen terugtellen tot we genoeg dagen hebben.
        days_list = []
        while len(days_list) < days:
            if day.weekday() < 5:
                days_list.append(day)
            day -= timedelta(days=1)
        for d in reversed(days_list):
            ret = drift + rng.gauss(0, 0.012)
            open_ = price
            close = max(1.0, price * (1 + ret))
            high = max(open_, close) * (1 + abs(rng.gauss(0, 0.004)))
            low = min(open_, close) * (1 - abs(rng.gauss(0, 0.004)))
            volume = rng.uniform(2e6, 6e6)
            bars.append(Bar(d, open_, high, low, close, volume))
            price = close
        return validate_bars(bars, instrument.ticker)

    def usd_to_eur(self) -> float:
        return self._usd_eur
