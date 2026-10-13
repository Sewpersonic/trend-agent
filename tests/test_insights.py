"""Tests voor de uitleg over verlies, risico en kansen in de rapporten."""

import os
import tempfile
import unittest
from dataclasses import replace
from datetime import date
from pathlib import Path
from unittest import mock

from trendagent import insights
from trendagent.agent import TrendAgent
from trendagent.core.config import Settings
from trendagent.data import SimulatedProvider
from trendagent.portfolio import Portfolio

END = date(2026, 10, 9)
UP = {"ASML.AS": 0.004, "NVDA": 0.004, "SAP.DE": 0.003, "SPY": 0.002, "IWDA.AS": 0.001}
FEW = ("ASML.AS", "NVDA", "SAP.DE", "SPY", "IWDA.AS")


def settings(**kw):
    tmp = Path(tempfile.mkdtemp())
    return replace(Settings(state_dir=tmp / "s", reports_dir=tmp / "r", tickers_override=FEW), **kw)


class MomentTests(unittest.TestCase):
    def test_labels(self):
        self.assertEqual(insights.moment({"rsi14": 60, "ema20_afstand_pct": 1.0, "atr_pct": 2.0})[0], "gunstig")
        self.assertEqual(insights.moment({"rsi14": 80, "ema20_afstand_pct": 1.0, "atr_pct": 2.0})[0], "opgelopen")
        self.assertEqual(insights.moment({"rsi14": 60, "ema20_afstand_pct": 8.0, "atr_pct": 2.0})[0], "opgelopen")
        self.assertEqual(insights.moment({"rsi14": 70, "ema20_afstand_pct": 4.0, "atr_pct": 2.0})[0], "neutraal")
        self.assertEqual(insights.moment({})[0], "onbekend")


class ReportTests(unittest.TestCase):
    def test_trend_report_has_risk_and_plans(self):
        s = settings()
        rep = TrendAgent(s, SimulatedProvider(END, drifts=UP)).run(END)
        pf = Portfolio.load(s.state_dir / "portfolio.json", 1)
        self.assertTrue(rep.kansen)
        for k in rep.kansen:
            p = k["plan"]
            self.assertLess(p["stop"], p["instap"])
            if p["aantal"] >= 1:
                # Maximaal verlies blijft rond het risicobudget per trade (plus kosten).
                self.assertLessEqual(p["max_verlies_eur"], 10000 * s.risk_per_trade + 5)
            if k["ticker"] in pf.positions:
                self.assertIn(k["status"], ("vandaag gekocht door de bot", "al in bezit"))
        self.assertEqual(len(rep.risk_rows), len(pf.positions))
        for r in rep.risk_rows:
            self.assertLess(r["bij_stop_eur"], 0)        # net gekocht: stop onder instap = verlies
        text = (s.state_dir / "report.md").read_text()
        self.assertIn("## Verlies en risico", text)
        self.assertIn("## Kansen", text)
        self.assertIn("Geen advies", text)

    def test_overview_shows_chances(self):
        from trendagent.__main__ import main
        tmp = Path(tempfile.mkdtemp())
        env = {"STATE_DIR": str(tmp / "s"), "REPORTS_DIR": str(tmp / "r"), "TICKERS": ",".join(FEW)}
        with mock.patch.dict(os.environ, env):
            main(["run", "--simulated"])
            main(["invest", "--simulated"])
            main(["overzicht", "--simulated"])
        text = (tmp / "r" / "OVERZICHT.md").read_text()
        self.assertIn("## Verlies en risico", text)
        self.assertIn("Beste kansen", text)
        inv = next((tmp / "r").glob("*-investeerder.md")).read_text()
        self.assertIn("Verlies en winst per belegging", inv)


if __name__ == "__main__":
    unittest.main()
