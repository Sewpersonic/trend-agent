"""Koersen uit meerdere bronnen, met controle of ze overeenkomen.

Bronnen
- Yahoo Finance (hoofdbron): dagkoersen van alle aandelen, ETF's en crypto.
- Stooq (tweede bron): gratis dagkoersen, zonder account. Dekt niet alle
  instrumenten; wat Stooq niet heeft, krijgt de status "1 bron".
- Europese Centrale Bank (ECB): de officiële wisselkoers euro/dollar.

Regels per instrument (op de laatste dag die beide bronnen hebben)
- verschil slotkoers ≤ 2%      -> "bevestigd"
- verschil groter              -> "afwijking": niet nieuw kopen (wel beheren)
- alleen Yahoo                 -> "1 bron (yahoo)"
- Yahoo mislukt, Stooq werkt   -> Stooq-koersen gebruiken, "1 bron (stooq)"
- beide mislukt                -> geen koersen (de bot handelt dat instrument niet)

Wisselkoers
- Yahoo en ECB verschillen ≤ 1% -> Yahoo gebruiken, "bevestigd"
- één van beide ontbreekt       -> de andere gebruiken
- groter verschil               -> fout: die dag geen handel (bij twijfel niet handelen)

Er wordt nooit een gemiddelde van bronnen gemaakt: we gebruiken één bron en
controleren hem met de andere. Zo blijven de koersen eerlijk naar één bron
herleidbaar.
"""

from __future__ import annotations

import csv
import io
import time
import urllib.request
from datetime import date

from .data import Bar, DataError, YahooProvider, validate_bars
from .universe import Instrument

PRICE_TOLERANCE = 0.02
FX_TOLERANCE = 0.01
MAX_SECONDARY_FAILURES = 5
USER_AGENT = "trend-agent/1.0 (paper trading; github.com)"


def http_get(url: str, timeout: float = 20.0, tries: int = 2) -> str:
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001  (netwerkfout, time-out, HTTP-fout)
            last = exc
            time.sleep(1.5 * (i + 1))
    raise DataError(f"ophalen mislukt: {type(last).__name__}")


# ------------------------------------------------------------------ Stooq

def stooq_symbol(ticker: str) -> str | None:
    """Yahoo-ticker omzetten naar Stooq. None = bij Stooq niet beschikbaar."""
    t = ticker.lower()
    if t.endswith("-usd"):                       # crypto: BTC-USD -> btcusd
        return t.replace("-", "")
    if "." not in t:                             # VS: aapl -> aapl.us
        return f"{t}.us"
    base, market = t.rsplit(".", 1)
    return {"de": f"{base}.de", "as": f"{base}.nl", "pa": f"{base}.fr"}.get(market)


class GeenSleutel(DataError):
    """De controlebron heeft een (gratis) sleutel nodig die nog niet in GitHub staat."""


class StooqSource:
    """Stooq vraagt sinds maart 2026 een gratis sleutel (apikey). Die staat als GitHub-secret STOOQ_APIKEY,
    nooit in de code of de chat. Zonder sleutel wordt Stooq overgeslagen (geen nutteloze verzoeken)."""
    name = "stooq"
    URL = "https://stooq.com/q/d/l/?s={symbol}&i=d"

    def __init__(self, fetch=None, apikey: str | None = None):
        import os
        # Controlebron: kort wachten en niet herhalen, zodat een trage Stooq de ronde niet ophoudt.
        self.fetch = fetch or (lambda url: http_get(url, timeout=10.0, tries=1))
        self.apikey = (apikey if apikey is not None else os.environ.get("STOOQ_APIKEY", "")).strip()

    def history(self, instrument: Instrument, days: int) -> list[Bar]:
        if not self.apikey:
            raise GeenSleutel("Stooq heeft een sleutel nodig (GitHub-secret STOOQ_APIKEY ontbreekt)")
        symbol = stooq_symbol(instrument.ticker)
        if symbol is None:
            raise DataError(f"{instrument.ticker}: niet bij Stooq")
        from urllib.parse import quote
        text = self.fetch(self.URL.format(symbol=symbol) + "&apikey=" + quote(self.apikey))
        return self.parse(text, instrument.ticker)[-days:]

    @staticmethod
    def parse(text: str, ticker: str) -> list[Bar]:
        if not text.lstrip().lower().startswith("date"):
            raise DataError(f"{ticker}: Stooq gaf geen koersen ({text.strip()[:40]!r})")
        bars = []
        for row in csv.DictReader(io.StringIO(text)):
            try:
                bars.append(Bar(date.fromisoformat(row["Date"]), float(row["Open"]), float(row["High"]),
                                float(row["Low"]), float(row["Close"]), float(row.get("Volume") or 0)))
            except (KeyError, ValueError):
                continue
        return validate_bars(bars, ticker)


# -------------------------------------------------------------------- ECB

class EcbFx:
    name = "ecb"
    URL = "https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?lastNObservations=5&format=csvdata"

    def __init__(self, fetch=http_get):
        self.fetch = fetch

    def usd_to_eur(self) -> float:
        text = self.fetch(self.URL)
        rows = [r for r in csv.DictReader(io.StringIO(text)) if r.get("OBS_VALUE")]
        if not rows:
            raise DataError("ECB gaf geen wisselkoers")
        eurusd = float(rows[-1]["OBS_VALUE"])     # dollars per euro
        if not 0.5 < eurusd < 2.0:
            raise DataError(f"ECB-wisselkoers onwaarschijnlijk: {eurusd}")
        return 1.0 / eurusd


# ---------------------------------------------------------- samenvoegen

def _compare(primary: list[Bar], secondary: list[Bar]) -> tuple[str, float | None]:
    """Vergelijkt de slotkoers op de laatste dag die beide bronnen hebben."""
    sec = {b.day: b.close for b in secondary}
    for b in reversed(primary[-5:]):
        if b.day in sec:
            diff = abs(sec[b.day] / b.close - 1)
            return ("bevestigd" if diff <= PRICE_TOLERANCE else "afwijking"), diff
    return "1 bron (geen gemeenschappelijke dag)", None


class MultiSourceProvider:
    """Hoofdbron + controlebron. Zelfde interface als de andere providers."""

    name = "yahoo+stooq+ecb"

    def __init__(self, primary=None, secondary=None, fx_check=None):
        self.primary = primary or YahooProvider()
        self.secondary = secondary if secondary is not None else StooqSource()
        self.fx_check = fx_check if fx_check is not None else EcbFx()
        self.checks: dict[str, dict] = {}
        self.fx_status = "onbekend"
        # Zekering: na zoveel mislukte pogingen op rij wordt de controlebron deze ronde overgeslagen.
        self.secondary_failures = 0
        self.secondary_off = False
        self.secondary_error = ""
        self.secondary_geen_sleutel = False

    def history(self, instrument: Instrument, days: int) -> list[Bar]:
        t = instrument.ticker
        try:
            main = self.primary.history(instrument, days)
        except DataError:
            main = None
        second = None
        if not self.secondary_off:
            try:
                second = self.secondary.history(instrument, days)
                self.secondary_failures = 0
            except GeenSleutel as exc:
                self.secondary_error = str(exc)[:160]
                self.secondary_off = True
                self.secondary_geen_sleutel = True
            except DataError as exc:
                self.secondary_error = str(exc).replace(getattr(self.secondary, "apikey", "") or "\0", "***")[:160]
                self.secondary_failures += 1
                if self.secondary_failures >= MAX_SECONDARY_FAILURES:
                    self.secondary_off = True
        if main and second:
            status, diff = _compare(main, second)
            self.checks[t] = {"status": status, "verschil": None if diff is None else round(diff, 4)}
            return main
        if main:
            self.checks[t] = {"status": "1 bron (yahoo)"}
            return main
        if second:
            self.checks[t] = {"status": "1 bron (stooq)"}
            return second
        self.checks[t] = {"status": "geen bron"}
        raise DataError(f"{t}: geen enkele bron had koersen")

    def source_issues(self, ticker: str) -> list[str]:
        c = self.checks.get(ticker, {})
        if c.get("status") == "afwijking":
            return [f"bronnen spreken elkaar tegen ({c['verschil']:.1%} verschil Yahoo/Stooq)"]
        return []

    def usd_to_eur(self) -> float:
        try:
            main = self.primary.usd_to_eur()
        except DataError:
            main = None
        try:
            check = self.fx_check.usd_to_eur()
        except DataError:
            check = None
        if main and check:
            if abs(main / check - 1) > FX_TOLERANCE:
                self.fx_status = "afwijking"
                raise DataError(f"wisselkoers Yahoo en ECB verschillen {abs(main / check - 1):.1%}")
            self.fx_status = "bevestigd"
            return main
        if main or check:
            self.fx_status = "1 bron (yahoo)" if main else "1 bron (ecb)"
            return main or check
        self.fx_status = "geen bron"
        raise DataError("geen wisselkoers bij Yahoo of ECB")

    def summary(self) -> dict:
        counts: dict[str, int] = {}
        for c in self.checks.values():
            key = c["status"].split(" (")[0] if c["status"].startswith("1 bron") else c["status"]
            counts[key] = counts.get(key, 0) + 1
        return {"koersen": counts, "wisselkoers": self.fx_status,
                "tweede_bron": ("geen sleutel" if self.secondary_geen_sleutel else
                                "overgeslagen na herhaalde fouten" if self.secondary_off else "actief"),
                "fout_tweede_bron": self.secondary_error,
                "afwijkend": sorted(t for t, c in self.checks.items() if c["status"] == "afwijking")}
