"""Tests voor de backtest en voor de kill-switchregels die de backtest gebruikt."""

import tempfile
import unittest
from dataclasses import replace
from datetime import date, timedelta
from pathlib import Path

from trendagent.agent import TrendAgent
from trendagent.backtest import (HistoricalProvider, max_drawdown, run_backtest, window_stats,
                                 windows)
from trendagent.backtest_report import write_all
from trendagent.core.config import Settings
from trendagent.core.kill_switch import KillSwitch
from trendagent.data import Bar, SimulatedProvider
from trendagent.portfolio import Portfolio
from trendagent.universe import BY_TICKER

END = date(2026, 10, 9)
FEW = ("ASML.AS", "NVDA", "SAP.DE", "SPY", "IWDA.AS")


def provider(years=2, drifts=None):
    sim = SimulatedProvider(END, drifts=drifts or {"NVDA": 0.003, "ASML.AS": 0.002})
    bars = {t: sim.history(BY_TICKER[t], (years + 1) * 260) for t in FEW}
    fx = {b.day: 0.92 for b in bars["SPY"]}
    return HistoricalProvider(bars, fx)


def settings():
    tmp = Path(tempfile.mkdtemp())
    return Settings(state_dir=tmp / "s", reports_dir=tmp / "r", tickers_override=FEW, write_reports=False)


class ProviderTests(unittest.TestCase):
    def test_no_look_ahead(self):
        p = provider()
        d = date(2025, 6, 2)
        p.set_day(d)
        bars = p.history(BY_TICKER["NVDA"], 260)
        self.assertTrue(all(b.day <= d for b in bars))
        self.assertEqual(len(bars), 260)

    def test_fx_missing_far_back(self):
        p = provider()
        p.set_day(date(2000, 1, 3))
        with self.assertRaises(Exception):
            p.usd_to_eur()


class MetricTests(unittest.TestCase):
    def test_max_drawdown(self):
        s = [(date(2026, 1, i), v) for i, v in enumerate([100, 120, 90, 130], start=1)]
        self.assertAlmostEqual(max_drawdown(s), -0.25)

    def test_windows(self):
        s = [(date(2026, 1, 1) + timedelta(days=i), 100 + i) for i in range(30)]
        w = windows(s, 20)
        self.assertEqual(len(w), 10)
        self.assertEqual(window_stats(w)["positive_share"], 1.0)


class BacktestTests(unittest.TestCase):
    def test_runs_and_writes_reports(self):
        p = provider()
        r = run_backtest(settings(), p, END - timedelta(days=365), END)
        self.assertGreater(len(r.equity), 200)
        self.assertIn("IWDA.AS", r.benchmarks)
        out = Path(tempfile.mkdtemp())
        write_all(r, out, 1)
        self.assertTrue((out / "RAPPORT.md").exists())
        self.assertTrue((out / "backtest.xlsx").exists())


class KillSwitchExitTests(unittest.TestCase):
    def test_stop_loss_still_sells_while_halted(self):
        s = replace(settings(), tickers_override=("NVDA", "ASML.AS", "SAP.DE", "SPY"))
        up = {"ASML.AS": 0.004, "NVDA": 0.004, "SAP.DE": 0.003, "SPY": 0.002}
        TrendAgent(s, SimulatedProvider(END, drifts=up)).run(END)
        path = s.state_dir / "portfolio.json"
        pf = Portfolio.load(path, s.starting_cash_eur)
        ticker = next(iter(pf.positions))
        stop = pf.positions[ticker].stop
        KillSwitch(s.state_dir / "kill_switch.json").activate("test", by="human")

        class Crash(SimulatedProvider):
            def history(self, inst, days):
                bars = super().history(inst, days)
                if inst.ticker == ticker:
                    last = bars[-1]
                    bars = bars[:-1] + [Bar(last.day, stop * 0.98, stop * 0.99, stop * 0.95, stop * 0.96, last.volume)]
                return bars

        nxt = END + timedelta(days=3)
        rep = TrendAgent(s, Crash(nxt, drifts=up)).run(nxt)
        pf = Portfolio.load(path, s.starting_cash_eur)
        self.assertEqual(rep.status, "GESTOPT")
        self.assertNotIn(ticker, pf.positions)
        self.assertFalse(any(t.side == "BUY" and t.day == nxt.isoformat() for t in pf.trades))

    def test_resume_resets_drawdown_baseline(self):
        pf = Portfolio(cash_eur=9_000.0, equity_history=[{"day": "start", "equity": 10_000.0},
                                                         {"day": "2026-10-09", "equity": 9_000.0}])
        self.assertEqual(pf.peak_equity(), 10_000.0)
        pf.reset_risk_baseline()
        self.assertEqual(pf.peak_equity(), 9_000.0)


if __name__ == "__main__":
    unittest.main()


class InvestorTests(unittest.TestCase):
    def _bars(self):
        from trendagent.universe import CRYPTO, UNIVERSE
        sim = SimulatedProvider(END, drifts={"NVDA": 0.003, "SAP.DE": 0.002, "BTC-USD": 0.002, "ETH-USD": -0.002})
        return {i.ticker: sim.history(i, 300) for i in UNIVERSE + CRYPTO}

    def test_weights_add_up_and_respect_limits(self):
        from trendagent.investor import Mix, target_weights
        w, _ = target_weights(self._bars(), Mix())
        self.assertLessEqual(sum(w.values()), 1.0 + 1e-9)
        self.assertGreaterEqual(w["IWDA.AS"], 0.60 - 1e-9)
        self.assertLessEqual(sum(v for t, v in w.items() if t.endswith("-USD")), 0.10 + 1e-9)
        self.assertNotIn("ETH-USD", w)          # dalende trend: niet kopen
        self.assertLessEqual(len([t for t in w if t not in ("IWDA.AS", "BTC-USD", "ETH-USD")]), 5)

    def test_rebalances_once_per_month(self):
        from trendagent.investor import Book, Investor
        s = settings()
        sim = SimulatedProvider(END, drifts={"NVDA": 0.003})
        inv = Investor(s, sim)
        inv.run(END)
        n = len(Book.load(inv.path, 1).trades)
        self.assertGreater(n, 0)
        inv.run(END)                             # zelfde maand: niets doen
        self.assertEqual(len(Book.load(inv.path, 1).trades), n)

    def test_kill_switch_blocks_buys(self):
        from trendagent.investor import Book, Investor
        s = settings()
        KillSwitch(s.state_dir / "kill_switch.json").activate("test", by="human")
        Investor(s, SimulatedProvider(END)).run(END)
        self.assertEqual([t for t in Book.load(s.state_dir / "investeerder.json", 1).trades if t.side == "BUY"], [])

    def test_investor_backtest_runs(self):
        from trendagent.backtest import run_investor_backtest
        from trendagent.universe import CRYPTO, UNIVERSE
        sim = SimulatedProvider(END)
        bars = {i.ticker: sim.history(i, 600) for i in UNIVERSE + CRYPTO}
        p = HistoricalProvider(bars, {b.day: 0.92 for b in bars["SPY"]})
        r = run_investor_backtest(settings(), p, END - timedelta(days=200), END)
        self.assertGreater(len(r.equity), 100)
        self.assertTrue(all(d.weekday() < 5 for d, _ in r.equity))
