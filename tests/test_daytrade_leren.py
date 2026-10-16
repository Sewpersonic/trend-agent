import json
import tempfile
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path

from trendagent import daytrade_leren as dl
from trendagent import daytrade_live as live
from trendagent import daytrader as dt
from trendagent.data import Bar
from tests import test_daytrader as tdt


def daily(start: date, n: int, step: float, base: float = 100.0):
    out, d, p = [], start, base
    while len(out) < n:
        if d.weekday() < 5:
            out.append(Bar(d, p, p * 1.01, p * 0.99, p, 1e6))
            p *= 1 + step
        d += timedelta(days=1)
    return out


class ChartViewTest(unittest.TestCase):
    def test_trend_and_place(self):
        up = dl.chart_view(daily(date(2025, 6, 2), 260, 0.002))
        self.assertEqual(up["dagtrend"], "stijgend")
        self.assertEqual(up["plek"], "bij de 3-maands top")
        self.assertTrue(up["boven_sma50"])
        down = dl.chart_view(daily(date(2025, 6, 2), 260, -0.002))
        self.assertEqual(down["dagtrend"], "dalend")
        self.assertEqual(down["plek"], "onderaan het bereik")
        self.assertEqual(dl.chart_view(daily(date(2025, 6, 2), 10, 0.0)), {})

    def test_context_uses_only_earlier_days(self):
        bars = daily(date(2025, 6, 2), 260, 0.002)
        day = bars[200].day
        ctx = dl.dag_context({"AAA": bars}, day)
        self.assertAlmostEqual(ctx["AAA"]["vorig_slot"], bars[199].close)


class LeerTest(unittest.TestCase):
    def test_lesson_when_clear_difference(self):
        trades = ([{"r": 1.0 + i * 0.01, "resultaat": 10, "ctx": {"dagtrend": "stijgend"}} for i in range(12)]
                  + [{"r": -1.0 - i * 0.01, "resultaat": -10, "ctx": {"dagtrend": "dalend"}} for i in range(12)])
        uit = dl.leer(trades)
        self.assertEqual(uit["totaal"]["n"], 24)
        les = [x for x in uit["lessen"] if x["kenmerk"] == "Daggrafiek van het aandeel"]
        self.assertTrue(les)
        self.assertIn("stijgende trend", {x["groep"] for x in les if x["soort"] == "beter"})
        self.assertTrue(any("R" in z for z in dl.samenvatting(uit, "Test")))

    def test_too_few_trades_no_lesson(self):
        uit = dl.leer([{"r": 1, "resultaat": 1, "ctx": {"dagtrend": "stijgend"}}] * 3)
        self.assertEqual(uit["lessen"], [])
        self.assertIn("te weinig", " ".join(dl.samenvatting(uit, "Oefenen")))


class LiveLerenTest(unittest.TestCase):
    def setUp(self):
        b = tdt.DaytraderTest()
        b.setUp()
        self.data, self.days = b.data, b.days

    def _run_day(self, sd, cfg, daily_bars):
        last = self.days[-1]
        t = datetime.combine(last, dt.OPEN) + timedelta(minutes=33)
        while t <= datetime.combine(last, dt.CLOSE):
            prov = lambda tks, period, t=t: {tk: [b for b in bs if b.t <= t - timedelta(minutes=1)] for tk, bs in self.data.items()}
            st = live.run(sd, cfg, now=t.replace(tzinfo=dt.NY), provider=prov, daily_provider=lambda _t: daily_bars)
            t += timedelta(minutes=15)
        return st

    def test_trade_remembers_chart_and_filter_from_config(self):
        start = self.days[-1] - timedelta(days=400)
        dalend = {"AAA": daily(start, 270, -0.002), "SPY": daily(start, 270, 0.001, 500)}
        with tempfile.TemporaryDirectory() as d:
            sd = Path(d)
            cfg = sd / "cfg.json"
            cfg.write_text("{}")
            st = self._run_day(sd, cfg, dalend)
            self.assertTrue(st["trades"])
            ctx = st["trades"][0]["ctx"]
            self.assertEqual(ctx["dagtrend"], "dalend")
            self.assertEqual(ctx["markt_dagtrend"], "stijgend")
            self.assertIn("rvol", ctx)
        with tempfile.TemporaryDirectory() as d:
            sd = Path(d)
            cfg = sd / "cfg.json"
            cfg.write_text(json.dumps({"regels": {"dagtrend_filter": True, "risk_per_trade": 0.5}}))
            st = self._run_day(sd, cfg, dalend)
            self.assertEqual(st["trades"], [])   # daggrafiek daalt: met de regel aan koopt hij niet

    def test_params_whitelist(self):
        p = live.params_from({"regels": {"dagtrend_filter": True, "risk_per_trade": 0.9, "max_trades": 50}})
        self.assertTrue(p.dagtrend_filter)
        self.assertEqual(p.risk_per_trade, dt.Params().risk_per_trade)
        self.assertEqual(p.max_trades, dt.Params().max_trades)


if __name__ == "__main__":
    unittest.main()
