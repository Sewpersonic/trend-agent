import unittest
from datetime import date, datetime, timedelta

from trendagent import daytrader as dt
from trendagent.daytrade_test import baselines, drop_unfinished_day, run


def day_bars(d: date, prices, vols=None):
    """78 blokken van 5 minuten vanaf 9:30; prices = lijst slotkoersen (wordt aangevuld met de laatste)."""
    prices = list(prices) + [prices[-1]] * (78 - len(prices))
    vols = list(vols or [1000] * 78) + [1000] * (78 - len(vols or [1000] * 78))
    out, prev = [], prices[0]
    for i, c in enumerate(prices[:78]):
        t = datetime.combine(d, dt.OPEN) + timedelta(minutes=5 * i)
        o = prev
        out.append(dt.Bar5(t, o, max(o, c) * 1.001, min(o, c) * 0.999, c, vols[i]))
        prev = c
    return out


def flat_days(start: date, n: int, price=100.0):
    days, d = [], start
    while len(days) < n:
        if d.weekday() < 5:
            days.append(d)
        d += timedelta(days=1)
    return days


class DaytraderTest(unittest.TestCase):
    def setUp(self):
        self.days = flat_days(date(2026, 8, 3), 12)
        self.data = {"SPY": [], "AAA": []}
        for d in self.days[:-1]:
            self.data["SPY"] += day_bars(d, [500.0] * 78)
            self.data["AAA"] += day_bars(d, [100.0] * 78)
        last = self.days[-1]
        # markt stijgt licht; AAA: rustige range rond 100, dan uitbraak met veel volume en verder omhoog
        self.data["SPY"] += day_bars(last, [500 + 0.05 * i for i in range(78)])
        aaa = [100.0, 100.4, 99.8, 100.2, 100.1, 100.3] + [100.6 + 0.08 * i for i in range(72)]
        self.data["AAA"] += day_bars(last, aaa, [5000] * 6 + [3000] * 72)

    def test_breakout_trade_and_flat_at_close(self):
        r = dt.backtest(self.data, dt.Params(rvol_days=10))
        trades = r["trades"]
        self.assertTrue(trades, "verwacht minstens één trade op de uitbraakdag")
        t = trades[0]
        self.assertEqual(t["ticker"], "AAA")
        self.assertGreaterEqual(t["t_in"], "10:00")
        self.assertLessEqual(t["t_in"], "12:30")
        # nooit iets mee de nacht in: elke trade is dezelfde dag gesloten
        self.assertTrue(all(x["t_uit"] <= "16:00" for x in trades))
        self.assertIn(t["reden"], ("winstdoel", "einde van de dag"))
        self.assertGreater(t["resultaat"], 0)

    def test_no_trade_when_market_down(self):
        last = self.days[-1]
        self.data["SPY"] = [b for b in self.data["SPY"] if b.t.date() != last] + day_bars(last, [500 - 0.1 * i for i in range(78)])
        r = dt.backtest(self.data, dt.Params(rvol_days=10))
        self.assertEqual(r["trades"], [])
        r2 = dt.backtest(self.data, dt.Params(rvol_days=10, market_filter=False))
        self.assertTrue(r2["trades"])

    def test_stop_loss_hit(self):
        last = self.days[-1]
        aaa = [100.0, 100.4, 99.8, 100.2, 100.1, 100.3, 100.6, 100.7, 100.8] + [98.0] * 69
        self.data["AAA"] = [b for b in self.data["AAA"] if b.t.date() != last] + day_bars(last, aaa, [5000] * 6 + [3000] * 72)
        r = dt.backtest(self.data, dt.Params(rvol_days=10))
        t = r["trades"][0]
        self.assertEqual(t["reden"], "stop-loss")
        self.assertAlmostEqual(t["r"], -1.0, delta=0.15)

    def test_sizing_limits(self):
        p = dt.Params()
        q = dt.size(10_000, 100.0, 99.0, p)   # risico 50 / 1 = 50, maar max 25% = 25 stuks
        self.assertEqual(q, 25)
        self.assertEqual(dt.size(10_000, 100.0, 100.0, p), 0)

    def test_unfinished_day_dropped_and_report(self):
        bs = self.data["SPY"][:-10]
        self.assertNotEqual(drop_unfinished_day(bs)[-1].t.date(), bs[-1].t.date())
        with __import__("tempfile").TemporaryDirectory() as d:
            from pathlib import Path
            s = run(Path(d), data=self.data)
            self.assertIn("basis", s["varianten"])
            self.assertIn("Test daytrade-bot", (Path(d) / "RAPPORT.md").read_text())
        self.assertIn("spy_vasthouden", baselines(self.data, self.days[0].isoformat()))


class LiveTest(unittest.TestCase):
    """Het echte oefenen (elk kwartier een ronde) moet hetzelfde doen als de test op oude koersen."""

    def setUp(self):
        base = DaytraderTest()
        base.setUp()
        self.data, self.days = base.data, base.days

    def provider_at(self, now_ny):
        def prov(tks, period):
            out = {}
            for tk, bs in self.data.items():
                # alleen blokken die op dit moment bestaan (het lopende blok telt mee, zoals bij Yahoo)
                out[tk] = [b for b in bs if b.t <= now_ny - timedelta(minutes=1)]
            return out
        return prov

    def test_live_matches_backtest(self):
        import tempfile
        from pathlib import Path

        from trendagent import daytrade_live as dl
        last = self.days[-1]
        with tempfile.TemporaryDirectory() as d:
            sd = Path(d)
            cfg = sd / "cfg.json"
            cfg.write_text('{"aan": true}')
            t = datetime.combine(last, dt.OPEN) - timedelta(minutes=10)
            while t <= datetime.combine(last, dt.CLOSE) + timedelta(minutes=20):
                now_utc = t.replace(tzinfo=dt.NY).astimezone(__import__("datetime").timezone.utc)
                st = dl.run(sd, cfg, now=now_utc, provider=self.provider_at(t))
                self.assertNotEqual(st["laatste_ronde"]["status"], "fout", st["laatste_ronde"])
                t += timedelta(minutes=15)
            live = [(x["ticker"], x["t_in"], x["reden"]) for x in st["trades"]]
            self.assertTrue(live)
            self.assertTrue(st["vandaag"]["klaar"])
            self.assertEqual(st["vandaag"]["open"], {})
            from trendagent.dashboard_data import daytrader_rows
            rows = daytrader_rows(sd)
            stand = rows[0]
            self.assertEqual(stand["soort"], "stand")
            self.assertAlmostEqual(stand["waarde"], 10000 + sum(x["resultaat"] for x in st["trades"]), places=1)
            self.assertTrue(any(r["soort"] == "trade" for r in rows))
            self.assertTrue(any(r["soort"] == "dag" for r in rows))
        bt = dt.backtest(self.data, dt.Params(rvol_days=10))
        self.assertEqual(live, [(x["ticker"], x["t_in"], x["reden"]) for x in bt["trades"]])

    def test_kill_switch_blocks_buying(self):
        import json
        import tempfile
        from pathlib import Path

        from trendagent import daytrade_live as dl
        last = self.days[-1]
        with tempfile.TemporaryDirectory() as d:
            sd = Path(d)
            (sd / "kill_switch.json").write_text(json.dumps({"active": True, "by": "human", "reason": "test"}))
            cfg = sd / "cfg.json"
            cfg.write_text("{}")
            t = datetime.combine(last, dt.OPEN) + timedelta(minutes=33)
            while t <= datetime.combine(last, dt.CLOSE):
                st = dl.run(sd, cfg, now=t.replace(tzinfo=dt.NY), provider=self.provider_at(t))
                t += timedelta(minutes=15)
            self.assertEqual(st["trades"], [])

    def test_early_close_sells_everything(self):
        import tempfile
        from pathlib import Path

        from trendagent import daytrade_live as dl
        last = self.days[-1]
        stop = datetime.combine(last, dt.time(13, 0))
        self.data = {tk: [b for b in bs if b.t.date() != last or b.t < stop] for tk, bs in self.data.items()}
        with tempfile.TemporaryDirectory() as d:
            sd = Path(d)
            cfg = sd / "cfg.json"
            cfg.write_text("{}")
            t = datetime.combine(last, dt.OPEN) + timedelta(minutes=33)
            while t <= datetime.combine(last, dt.CLOSE):
                st = dl.run(sd, cfg, now=t.replace(tzinfo=dt.NY), provider=self.provider_at(t))
                t += timedelta(minutes=15)
            self.assertTrue(st["trades"])
            self.assertTrue(st["vandaag"]["klaar"])
            self.assertEqual(st["vandaag"]["open"], {})
            self.assertTrue(all(x["t_uit"] < "14:00" for x in st["trades"]), st["trades"])

    def test_late_last_round_closes_same_day(self):
        """Laatste ronde om 15:37 (positie open), daarna pas weer om 19:05: de dag moet dan dicht."""
        import tempfile
        from pathlib import Path

        from trendagent import daytrade_live as dl
        last = self.days[-1]
        with tempfile.TemporaryDirectory() as d:
            sd = Path(d)
            cfg = sd / "cfg.json"
            cfg.write_text("{}")
            for hm in ((10, 33), (15, 37), (19, 5)):
                t = datetime.combine(last, dt.time(*hm))
                st = dl.run(sd, cfg, now=t.replace(tzinfo=dt.NY), provider=self.provider_at(t))
            self.assertTrue(st["vandaag"]["klaar"])
            self.assertEqual(st["vandaag"]["open"], {})
            self.assertTrue(st["trades"])
            self.assertLessEqual(st["trades"][-1]["t_uit"], "15:45")
            self.assertEqual(len(st["dagen"]), 1)


if __name__ == "__main__":
    unittest.main()
