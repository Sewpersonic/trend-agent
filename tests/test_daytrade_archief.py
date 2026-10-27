import tempfile
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path

from tests.test_daytrader import day_bars
from trendagent import daytrade_archief as da


class ArchiefTest(unittest.TestCase):
    def test_bewaren_laden_en_groeien(self):
        d1, d2, d3 = date(2026, 10, 19), date(2026, 10, 20), date(2026, 10, 26)
        oud = {"AAA": day_bars(d1, [100.0] * 78) + day_bars(d2, [101.0] * 78)}
        nieuw = {"AAA": day_bars(d2, [102.0] * 78) + day_bars(d3, [103.0] * 78), "BBB": day_bars(d3, [50.0] * 78)}
        with tempfile.TemporaryDirectory() as t:
            m = Path(t)
            self.assertEqual(len(da.bewaar(oud, m)), 1)          # één week
            self.assertEqual(da.bewaar(oud, m), [])              # zelfde inhoud: niets gewijzigd
            da.bewaar(nieuw, m)
            self.assertEqual(sorted(p.name for p in m.iterdir()), ["2026-W43.csv.gz", "2026-W44.csv.gz"])
            alles = da.laad(m)
            dagen = sorted({b.t.date() for b in alles["AAA"]})
            self.assertEqual(dagen, [d1, d2, d3])                 # de oude dag blijft bewaard
            d2_bars = [b for b in alles["AAA"] if b.t.date() == d2]
            self.assertEqual(len(d2_bars), 78)
            self.assertAlmostEqual(d2_bars[-1].c, 102.0)          # de nieuwe koers wint
            self.assertIn("BBB", alles)

    def test_samen_houdt_laatste_dagen(self):
        bars = []
        d = date(2026, 1, 5)
        for _ in range(12):
            bars += day_bars(d, [10.0] * 78)
            d += timedelta(days=1)
        uit = da.samen({"X": bars}, {}, max_dagen=5)
        self.assertEqual(len({b.t.date() for b in uit["X"]}), 5)
        self.assertIsInstance(uit["X"][0].t, datetime)


if __name__ == "__main__":
    unittest.main()
