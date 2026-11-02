import tempfile
import unittest
from datetime import date, datetime, time, timedelta
from pathlib import Path

from trendagent import daytrade_eu as eu
from trendagent import daytrader as dt


def dag(d, prices, vols, start=time(9, 0), n=102):
    prices = list(prices) + [prices[-1]] * (n - len(prices))
    vols = list(vols) + [vols[-1]] * (n - len(vols))
    out, prev = [], prices[0]
    for i in range(n):
        t = datetime.combine(d, start) + timedelta(minutes=5 * i)
        c = prices[i]
        out.append(dt.Bar5(t, prev, max(prev, c) * 1.001, min(prev, c) * 0.999, c, vols[i]))
        prev = c
    return out


class EuTest(unittest.TestCase):
    def test_europese_beurstijden_en_uitbraak(self):
        days, d = [], date(2026, 9, 1)
        while len(days) < 12:
            if d.weekday() < 5:
                days.append(d)
            d += timedelta(days=1)
        data = {eu.MARKT: [], "ASML.AS": []}
        for x in days[:-1]:
            data[eu.MARKT] += dag(x, [50.0], [1000])
            data["ASML.AS"] += dag(x, [600.0], [1000])
        last = days[-1]
        data[eu.MARKT] += dag(last, [50 + 0.01 * i for i in range(102)], [1000])
        asml = [600.0, 602, 599, 601, 600, 601.5] + [603 + 0.5 * i for i in range(96)]
        data["ASML.AS"] += dag(last, asml, [5000] * 6 + [3000] * 96)
        # de dag hoort bij de Europese uren 09:00-17:30
        self.assertEqual(len(dt.split_days(data["ASML.AS"], eu.PARAMS.open_t, eu.PARAMS.close_t)[last]), 102)
        with tempfile.TemporaryDirectory() as tmp:
            s = eu.run(Path(tmp), data=data)
            b = s["varianten"]["basis (kopen tot 10:30)"]["stats"]
            self.assertGreaterEqual(b["trades"], 1)
            self.assertTrue((Path(tmp) / "RAPPORT.md").read_text().startswith("# Daytrader op de Europese beurs"))
        # de Amerikaanse daytrader verandert niet
        self.assertEqual(dt.Params().open_t, time(9, 30))
