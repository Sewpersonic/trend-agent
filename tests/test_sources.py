"""Tests voor koersen uit meerdere bronnen (zonder internet: nep-bronnen)."""

import tempfile
import unittest
from datetime import date
from pathlib import Path

from trendagent.agent import TrendAgent
from trendagent.core.config import Settings
from trendagent.data import Bar, DataError, SimulatedProvider
from trendagent.portfolio import Portfolio
from trendagent.sources import EcbFx, MultiSourceProvider, StooqSource, stooq_symbol
from trendagent.universe import BY_TICKER

END = date(2026, 10, 9)
UP = {"ASML.AS": 0.004, "NVDA": 0.004, "SAP.DE": 0.003, "SPY": 0.002}
FEW = ("ASML.AS", "NVDA", "SAP.DE", "SPY")


class Shifted:
    """Tweede bron die dezelfde koersen geeft, eventueel met een afwijking voor één ticker."""

    def __init__(self, base, factor=1.0, ticker=None, missing=()):
        self.base, self.factor, self.ticker, self.missing = base, factor, ticker, set(missing)

    def history(self, inst, days):
        if inst.ticker in self.missing:
            raise DataError("niet beschikbaar")
        bars = self.base.history(inst, days)
        if inst.ticker == self.ticker:
            bars = [Bar(b.day, b.open * self.factor, b.high * self.factor, b.low * self.factor,
                        b.close * self.factor, b.volume) for b in bars]
        return bars


class Fx:
    def __init__(self, value=None):
        self.value = value

    def usd_to_eur(self):
        if self.value is None:
            raise DataError("geen")
        return self.value


class StooqTests(unittest.TestCase):
    def test_symbols(self):
        self.assertEqual(stooq_symbol("AAPL"), "aapl.us")
        self.assertEqual(stooq_symbol("SAP.DE"), "sap.de")
        self.assertEqual(stooq_symbol("ASML.AS"), "asml.nl")
        self.assertEqual(stooq_symbol("BTC-USD"), "btcusd")

    def test_parse_csv(self):
        text = "Date,Open,High,Low,Close,Volume\n2026-10-08,10,11,9,10.5,1000\n2026-10-09,10.5,12,10,11.5,1200\n"
        src = StooqSource(fetch=lambda url: text, apikey="x")
        bars = src.history(BY_TICKER["AAPL"], 10)
        self.assertEqual(bars[-1].close, 11.5)

    def test_error_text_is_refused(self):
        src = StooqSource(fetch=lambda url: "Exceeded the daily hits limit", apikey="x")
        with self.assertRaises(DataError):
            src.history(BY_TICKER["AAPL"], 10)

    def test_ecb_parse(self):
        text = "KEY,TIME_PERIOD,OBS_VALUE\nX,2026-10-08,1.09\nX,2026-10-09,1.10\n"
        self.assertAlmostEqual(EcbFx(fetch=lambda url: text).usd_to_eur(), 1 / 1.10)


class MultiSourceTests(unittest.TestCase):
    def setUp(self):
        self.sim = SimulatedProvider(END, drifts=UP)

    def test_confirmed_when_sources_agree(self):
        p = MultiSourceProvider(self.sim, Shifted(self.sim, 1.005, "NVDA"), Fx(0.92))
        p.history(BY_TICKER["NVDA"], 260)
        self.assertEqual(p.checks["NVDA"]["status"], "bevestigd")
        self.assertEqual(p.source_issues("NVDA"), [])

    def test_disagreement_flagged(self):
        p = MultiSourceProvider(self.sim, Shifted(self.sim, 1.10, "NVDA"), Fx(0.92))
        p.history(BY_TICKER["NVDA"], 260)
        self.assertEqual(p.checks["NVDA"]["status"], "afwijking")
        self.assertTrue(p.source_issues("NVDA"))

    def test_fallback_to_second_source(self):
        class Broken:
            def history(self, inst, days):
                raise DataError("yahoo plat")

            def usd_to_eur(self):
                raise DataError("yahoo plat")

        p = MultiSourceProvider(Broken(), self.sim, Fx(0.91))
        self.assertTrue(p.history(BY_TICKER["SPY"], 260))
        self.assertEqual(p.checks["SPY"]["status"], "1 bron (stooq)")
        self.assertAlmostEqual(p.usd_to_eur(), 0.91)
        self.assertEqual(p.fx_status, "1 bron (ecb)")

    def test_circuit_breaker_stops_calling_slow_source(self):
        calls = []

        class Down:
            def history(self, inst, days):
                calls.append(inst.ticker)
                raise DataError("plat")

        p = MultiSourceProvider(self.sim, Down(), Fx(0.92))
        for t in ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "AVGO", "TSLA"]:
            p.history(BY_TICKER[t], 260)
        self.assertEqual(len(calls), 5)
        self.assertEqual(p.summary()["tweede_bron"], "overgeslagen na herhaalde fouten")

    def test_fx_disagreement_stops_trading(self):
        p = MultiSourceProvider(self.sim, self.sim, Fx(0.80))   # sim geeft 0.92: 15% verschil
        with self.assertRaises(DataError):
            p.usd_to_eur()

    def test_agent_skips_disputed_ticker(self):
        tmp = Path(tempfile.mkdtemp())
        s = Settings(state_dir=tmp / "s", reports_dir=tmp / "r", tickers_override=FEW)
        p = MultiSourceProvider(self.sim, Shifted(self.sim, 1.10, "NVDA", missing={"ASML.AS"}), Fx(0.92))
        rep = TrendAgent(s, p).run(END)
        pf = Portfolio.load(s.state_dir / "portfolio.json", 1)
        self.assertNotIn("NVDA", pf.positions)
        self.assertEqual(rep.health["bronnen"]["afwijkend"], ["NVDA"])
        self.assertEqual(rep.health["bronnen"]["koersen"].get("1 bron"), 1)
        self.assertIn("Koersbronnen", (s.state_dir / "report.md").read_text())


if __name__ == "__main__":
    unittest.main()


class IntradayFillTests(unittest.TestCase):
    def test_missing_day_built_from_hours(self):
        from datetime import date

        from trendagent.data import Bar, fill_from_intraday
        daily = [Bar(date(2026, 10, 12), 1, 2, 1, 1.5, 10), Bar(date(2026, 10, 13), 1.5, 2, 1, 1.8, 10)]
        hours = [(date(2026, 10, 13), 9, 9, 9, 9, 1),            # al in de dagkoersen: overslaan
                 (date(2026, 10, 14), 1.8, 2.0, 1.7, 1.9, 5), (date(2026, 10, 14), 1.9, 2.3, 1.85, 2.1, 7),
                 (date(2026, 10, 15), 2.1, 2.2, 2.0, 2.15, 3)]     # nog niet afgesloten: overslaan
        out = fill_from_intraday(daily, hours, date(2026, 10, 14))
        self.assertEqual(len(out), 3)
        b = out[-1]
        self.assertEqual((b.day, b.open, b.high, b.low, b.close, b.volume), (date(2026, 10, 14), 1.8, 2.3, 1.7, 2.1, 12))

    def test_nothing_missing(self):
        from datetime import date

        from trendagent.data import Bar, fill_from_intraday
        daily = [Bar(date(2026, 10, 14), 1, 2, 1, 1.5, 10)]
        self.assertEqual(fill_from_intraday(daily, [(date(2026, 10, 14), 1, 1, 1, 1, 1)], date(2026, 10, 14)), daily)


class UnfinishedDayTests(unittest.TestCase):
    def test_running_day_dropped(self):
        from datetime import date

        from trendagent.data import Bar, drop_unfinished
        bars = [Bar(date(2026, 10, 13), 1, 2, 1, 1.5, 10), Bar(date(2026, 10, 15), 1, 2, 1, 1.6, 3)]
        self.assertEqual([b.day for b in drop_unfinished(bars, date(2026, 10, 14))], [date(2026, 10, 13)])


class StooqSleutelTest(__import__("unittest").TestCase):
    def test_zonder_sleutel_geen_verzoek_en_duidelijke_status(self):
        from trendagent.sources import GeenSleutel, MultiSourceProvider, StooqSource
        from trendagent.universe import UNIVERSE
        gevraagd = []
        src = StooqSource(fetch=lambda url: gevraagd.append(url) or "", apikey="")
        with self.assertRaises(GeenSleutel):
            src.history(UNIVERSE[0], 10)
        self.assertEqual(gevraagd, [])
        met = StooqSource(fetch=lambda url: gevraagd.append(url) or "Date,Open,High,Low,Close,Volume\n", apikey="geheim")
        try:
            met.history(UNIVERSE[0], 10)
        except Exception:
            pass
        self.assertIn("apikey=geheim", gevraagd[-1])

        class Hoofd:
            def history(self, inst, days):
                from trendagent.data import SimulatedProvider
                from datetime import date
                return SimulatedProvider(end=date(2026, 10, 23)).history(inst, days)
        m = MultiSourceProvider(primary=Hoofd(), secondary=StooqSource(apikey=""), fx_check=None)
        m.history(UNIVERSE[0], 50)
        self.assertTrue(m.secondary_off)
        self.assertEqual(m.summary()["tweede_bron"], "geen sleutel")


class StooqUitTest(__import__("unittest").TestCase):
    def test_standaard_geen_tweede_bron(self):
        import os
        from datetime import date
        from unittest import mock

        from trendagent.data import SimulatedProvider
        from trendagent.sources import MultiSourceProvider
        from trendagent.universe import UNIVERSE
        with mock.patch.dict(os.environ, {"STOOQ_APIKEY": ""}):
            m = MultiSourceProvider(primary=SimulatedProvider(end=date(2026, 10, 23)), fx_check=None)
        self.assertIsNone(m.secondary)
        self.assertTrue(m.history(UNIVERSE[0], 50))
        self.assertEqual(m.summary()["tweede_bron"], "uit")
