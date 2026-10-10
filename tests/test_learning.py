"""Tests voor indicatoren, regime, datakwaliteit, journaal, leeranalyse, evaluatie en health."""

import json
import tempfile
import unittest
from dataclasses import replace
from datetime import date, timedelta
from pathlib import Path

from trendagent import evaluation, learning
from trendagent.agent import TrendAgent
from trendagent.core.config import Settings
from trendagent.data import Bar, SimulatedProvider
from trendagent.features import data_issues, ema, macd, market_regime, rsi, snapshot
from trendagent.portfolio import Portfolio, Trade
from trendagent.strategies import trend_version
from trendagent.universe import BY_TICKER

END = date(2026, 10, 9)
UP = {"ASML.AS": 0.004, "NVDA": 0.004, "SAP.DE": 0.003, "SPY": 0.002, "IWDA.AS": 0.001}
FEW = ("ASML.AS", "NVDA", "SAP.DE", "SPY", "IWDA.AS")


def settings(**kw):
    tmp = Path(tempfile.mkdtemp())
    return replace(Settings(state_dir=tmp / "s", reports_dir=tmp / "r", tickers_override=FEW), **kw)


def bars_from(closes, start=date(2025, 1, 1), volume=1e6):
    out, d = [], start
    for c in closes:
        out.append(Bar(d, c, c * 1.01, c * 0.99, c, volume))
        d += timedelta(days=1)
    return out


class IndicatorTests(unittest.TestCase):
    def test_rsi_extremes(self):
        self.assertEqual(rsi([float(i) for i in range(1, 40)]), 100.0)
        self.assertAlmostEqual(rsi([10.0, 11.0] * 20), 50.0, delta=3)
        self.assertLess(rsi([float(i) for i in range(60, 20, -1)]), 1.0)

    def test_macd_constant_is_zero(self):
        m, sig, h = macd([100.0] * 60)
        self.assertAlmostEqual(m, 0.0)
        self.assertAlmostEqual(h, 0.0)

    def test_ema_constant(self):
        self.assertAlmostEqual(ema([5.0] * 30, 10), 5.0)

    def test_snapshot_uses_only_given_bars(self):
        b = bars_from([100 + i * 0.5 for i in range(260)])
        self.assertEqual(snapshot(b), snapshot(b + []))   # deterministisch
        self.assertGreater(snapshot(b)["rsi14"], 70)

    def test_regime_up_and_down(self):
        up = bars_from([100 * 1.002 ** i for i in range(300)])
        down = bars_from([100 * 0.998 ** i for i in range(300)])
        self.assertEqual(market_regime({"SPY": up}).trend, "stijgend")
        self.assertEqual(market_regime({"SPY": down}).trend, "dalend")
        self.assertEqual(market_regime({"SPY": up[:100]}).trend, "onbekend")


class DataQualityTests(unittest.TestCase):
    def test_frozen_price(self):
        self.assertTrue(data_issues(bars_from([100.0] * 10)))

    def test_jump(self):
        self.assertTrue(any("sprong" in i for i in data_issues(bars_from([100, 101, 102, 160, 161, 162]))))

    def test_normal_series_ok(self):
        self.assertEqual(data_issues(bars_from([100 + i for i in range(20)])), [])

    def test_suspicious_ticker_not_bought(self):
        class Frozen(SimulatedProvider):
            def history(self, inst, days):
                b = super().history(inst, days)
                if inst.ticker == "NVDA":
                    last = b[-1]
                    b = b[:-5] + [Bar(x.day, last.close, last.close, last.close, last.close, x.volume) for x in b[-5:]]
                return b
        s = settings()
        rep = TrendAgent(s, Frozen(END, drifts=UP)).run(END)
        pf = Portfolio.load(s.state_dir / "portfolio.json", 1)
        self.assertNotIn("NVDA", pf.positions)
        self.assertIn("NVDA", rep.health["verdacht"])


class JournalTests(unittest.TestCase):
    def test_trades_carry_context_version_and_r(self):
        s = settings()
        TrendAgent(s, SimulatedProvider(END, drifts=UP)).run(END)
        path = s.state_dir / "portfolio.json"
        pf = Portfolio.load(path, 1)
        buy = next(t for t in pf.trades if t.side == "BUY")
        self.assertEqual(buy.version, trend_version(s))
        self.assertIn("rsi14", buy.context)
        self.assertTrue(buy.regime)
        t = buy.ticker
        sell = pf.sell("2026-10-20", t, pf.positions[t].stop, 1.0, 1.0, "test", exit_context={"rsi14": 40})
        self.assertIsNotNone(sell.r_multiple)
        self.assertLess(sell.r_multiple, 0)
        self.assertEqual(sell.hold_days, 11)
        self.assertIn("rsi14", sell.context["instap"])

    def test_old_portfolio_files_still_load(self):
        s = settings()
        s.state_dir.mkdir(parents=True)
        old = {"cash_eur": 100.0, "positions": {}, "trades": [
            {"day": "2026-10-01", "ticker": "SPY", "side": "BUY", "qty": 1, "price": 1, "fx": 1,
             "value_eur": 1, "costs_eur": 1, "reason": "x", "pnl_eur": None}], "equity_history": []}
        (s.state_dir / "portfolio.json").write_text(json.dumps(old))
        pf = Portfolio.load(s.state_dir / "portfolio.json", 1)
        self.assertEqual(pf.trades[0].version, "")

    def test_regime_filter_blocks_buys_in_down_market(self):
        down = {t: -0.002 for t in FEW}
        down["NVDA"] = 0.004
        s = settings(regime_filter=True)
        rep = TrendAgent(s, SimulatedProvider(END, drifts=down)).run(END)
        self.assertTrue(rep.regime.startswith("dalend"))
        self.assertEqual([t for t in Portfolio.load(s.state_dir / "portfolio.json", 1).trades if t.side == "BUY"], [])


def fake_trade(r, rsi_val, trend="stijgend"):
    return Trade("2026-01-01", "X", "SELL", 1, 1, 1, 1, 1, "stop-loss geraakt", pnl_eur=r * 10,
                 context={"instap": {"rsi14": rsi_val, "trend_regime": trend}}, r_multiple=r, hold_days=10)


class LearningTests(unittest.TestCase):
    def test_finds_real_difference(self):
        trades = [fake_trade(1.0 + (i % 3) * 0.1, 55) for i in range(30)]
        trades += [fake_trade(-0.8 - (i % 3) * 0.1, 85) for i in range(30)]
        _, _, findings = learning.analyse(trades)
        self.assertTrue(any(f.dimension == "RSI bij instap" and f.kind == "zwakte" for f in findings))

    def test_outcomes_are_not_findings(self):
        trades = [replace(fake_trade(1.5, 55), hold_days=60) for _ in range(30)]
        trades += [replace(fake_trade(-1.0, 55), hold_days=3) for _ in range(30)]
        _, tables, findings = learning.analyse(trades)
        self.assertIn("Houdduur", tables)
        self.assertFalse(any(f.dimension in learning.OUTCOME_DIMENSIONS for f in findings))

    def test_ignores_small_groups(self):
        trades = [fake_trade(1.0, 55) for _ in range(5)] + [fake_trade(-1.0, 85) for _ in range(5)]
        _, _, findings = learning.analyse(trades)
        self.assertEqual(findings, [])

    def test_no_finding_for_noise(self):
        import random
        rng = random.Random(1)
        trades = [fake_trade(rng.gauss(0.1, 1.0), rng.choice([55, 85])) for _ in range(200)]
        _, _, findings = learning.analyse(trades)
        self.assertFalse(any(f.dimension == "RSI bij instap" for f in findings))

    def test_drift_warning(self):
        ref = [fake_trade(0.5 + (i % 5) * 0.1, 55) for i in range(100)]
        live = [fake_trade(-1.0 + (i % 5) * 0.05, 55) for i in range(25)]
        self.assertIn("LET OP", learning.drift(live, ref))

    def test_vs_benchmark(self):
        eh = [{"day": "start", "equity": 10000}, {"day": "2026-10-01", "equity": 10000, "bench": 100},
              {"day": "2026-10-02", "equity": 10200, "bench": 101}]
        vb = learning.vs_benchmark(eh)
        self.assertAlmostEqual(vb["verschil"], 0.01)


class EvaluationTests(unittest.TestCase):
    def _series(self, daily, n=500, noise=0.0):
        import random
        rng = random.Random(3)
        v, out, d = 10000.0, [], date(2024, 1, 1)
        for _ in range(n):
            v *= 1 + daily + rng.gauss(0, noise)
            out.append((d, v))
            d += timedelta(days=1)
        return out

    def test_better_candidate_accepted_worse_rejected(self):
        prod = evaluation.VariantResult("productie", {}, self._series(0.0002, noise=0.01), [],
                                        self._series(0.0001, noise=0.01))
        good = evaluation.VariantResult("goed", {}, self._series(0.0012, noise=0.01), [],
                                        self._series(0.0011, noise=0.01))
        bad = evaluation.VariantResult("slecht", {}, self._series(-0.0005, noise=0.01), [],
                                       self._series(-0.0006, noise=0.01))
        days = [d for d, _ in prod.equity]
        self.assertTrue(evaluation.judge(prod, good, days, "investeerder").accepted)
        self.assertFalse(evaluation.judge(prod, bad, days, "investeerder").accepted)

    def test_trend_needs_enough_trades(self):
        prod = evaluation.VariantResult("productie", {}, self._series(0.0002, noise=0.01), [],
                                        self._series(0.0001, noise=0.01))
        good = evaluation.VariantResult("goed", {}, self._series(0.0012, noise=0.01), [],
                                        self._series(0.0011, noise=0.01))
        v = evaluation.judge(prod, good, [d for d, _ in prod.equity], "trend")
        self.assertFalse(v.accepted)            # 0 trades: te weinig bewijs

    def test_periods_do_not_overlap_holdout(self):
        days = [date(2024, 1, 1) + timedelta(days=i) for i in range(100)]
        dev, hold, folds = evaluation.periods(days)
        self.assertLess(dev[1], hold[0])
        self.assertEqual(len(folds), evaluation.FOLDS)


class HealthTests(unittest.TestCase):
    def test_problems(self):
        from trendagent.__main__ import health_problems
        ok = {"trend": {"status": "OK", "gevraagd": 50, "mislukt": 2},
              "investeerder": {"status": "OK", "gevraagd": 52, "mislukt": 0}}
        self.assertEqual(health_problems(ok), [])
        bad = {"trend": {"status": "FOUT", "fout": "x"}, "investeerder": {"status": "OK", "gevraagd": 50, "mislukt": 30}}
        self.assertEqual(len(health_problems(bad)), 2)

    def test_run_writes_health(self):
        from trendagent.__main__ import main
        import os
        from unittest import mock
        tmp = Path(tempfile.mkdtemp())
        env = {"STATE_DIR": str(tmp / "s"), "REPORTS_DIR": str(tmp / "r"), "TICKERS": ",".join(FEW)}
        with mock.patch.dict(os.environ, env):
            main(["run", "--simulated"])
            main(["invest", "--simulated"])
            self.assertEqual(main(["health", "--check"]), 0)
        data = json.loads((tmp / "s" / "health.json").read_text())
        self.assertEqual(set(data), {"trend", "investeerder"})


if __name__ == "__main__":
    unittest.main()
