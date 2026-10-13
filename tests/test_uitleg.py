"""Tests voor de uitleg van de analyse en de 'Klaar voor echt geld?'-lijst."""

import tempfile
import unittest
from dataclasses import replace
from datetime import date
from pathlib import Path

from trendagent import uitleg
from trendagent.agent import TrendAgent
from trendagent.core.config import Settings
from trendagent.data import SimulatedProvider

END = date(2026, 10, 9)
UP = {"ASML.AS": 0.004, "NVDA": 0.004, "SAP.DE": 0.003, "SPY": 0.002, "IWDA.AS": 0.001}
FEW = ("ASML.AS", "NVDA", "SAP.DE", "SPY", "IWDA.AS")


def history(days, bot_growth, etf_growth):
    h = [{"day": "start", "equity": 10000}]
    for i in range(days):
        h.append({"day": f"d{i}", "equity": 10000 * (1 + bot_growth) ** i, "bench": 100 * (1 + etf_growth) ** i})
    return h


class ReadinessTests(unittest.TestCase):
    def test_new_bot_is_not_ready(self):
        r = uitleg.readiness("trend", history(5, 0.001, 0.0), [])
        self.assertIn("Nog niet klaar", r["oordeel"])

    def test_good_long_record_is_ready_but_human_decides(self):
        r = uitleg.readiness("trend", history(70, 0.001, 0.0005), [0.5] * 25)
        self.assertTrue(all(state == "ok" for _, state, _ in r["eisen"]))
        self.assertIn("Jij beslist", r["oordeel"])

    def test_worse_than_etf_fails(self):
        r = uitleg.readiness("investeerder", history(70, 0.0, 0.001), [])
        self.assertIn("eis wordt niet gehaald", r["oordeel"])

    def test_losing_trades_fail(self):
        r = uitleg.readiness("trend", history(70, 0.001, 0.0), [-0.3] * 25)
        self.assertTrue(any(state == "nee" for _, state, _ in r["eisen"]))


class ConclusionTests(unittest.TestCase):
    def test_market_conclusions(self):
        m = {"trend": "dalend", "beweeglijkheid": "hoog", "breedte": {"totaal": [10, 50], "EU": [8, 20], "US": [2, 30]}}
        c = uitleg.market_conclusions(m)
        self.assertTrue(any("daalt" in x for x in c))
        self.assertTrue(any("Europa" in x for x in c))
        self.assertFalse(any("stop" in x for x in uitleg.market_conclusions(m, "investeerder")))

    def test_report_explains_analysis(self):
        tmp = Path(tempfile.mkdtemp())
        s = replace(Settings(state_dir=tmp / "s", reports_dir=tmp / "r", tickers_override=FEW))
        rep = TrendAgent(s, SimulatedProvider(END, drifts=UP)).run(END)
        self.assertEqual(rep.analyse["zeef"]["bekeken"], len(FEW))
        text = (s.state_dir / "report.md").read_text()
        for part in ("## Analyse van vandaag", "Wat de bot zag", "Wat de bot eruit haalt",
                     "## Wat de bot tot nu toe geleerd heeft", "## Klaar voor echt geld?", "Zo analyseert"):
            self.assertIn(part, text)


if __name__ == "__main__":
    unittest.main()
