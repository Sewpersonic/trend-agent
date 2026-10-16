"""Tests voor de patronen in de grafieken."""

import unittest

from trendagent import patronen


def item(closes, sma50=None, sma200=None):
    n = len(closes)
    return {"titel": "Test (TST)", "iso": [f"2026-{7 + i // 28:02d}-{1 + i % 28:02d}" for i in range(n)],
            "koers": closes, "open": [c * 0.999 for c in closes], "hoog": [c * 1.005 for c in closes],
            "laag": [c * 0.995 for c in closes], "sma50": sma50 or [None] * n, "sma200": sma200 or [None] * n}


class PatronenTests(unittest.TestCase):
    def test_rising_series_new_top_and_streak(self):
        closes = [100 + i for i in range(65)]
        r = patronen.analyse(item(closes, [c - 5 for c in closes], [c - 15 for c in closes]))
        self.assertEqual(r["trend"], "stijgend")
        self.assertIn("nieuwe 3-maands top", r["patronen"])
        self.assertIn("dagen op rij gestegen", r["patronen"])
        self.assertGreater(r["drie_mnd"], 0.5)

    def test_falling_series(self):
        closes = [200 - i for i in range(65)]
        r = patronen.analyse(item(closes, [c + 5 for c in closes], [c + 15 for c in closes]))
        self.assertEqual(r["trend"], "dalend")
        self.assertIn("3-maands bodem", r["patronen"])

    def test_too_short(self):
        self.assertIsNone(patronen.analyse(item([100] * 5)))

    def test_summary_never_predicts(self):
        rows = [dict(patronen.analyse(item([100 + i for i in range(65)])), ticker="A", bot="x")]
        text = " ".join(patronen.samenvatting(rows))
        self.assertIn("voorspelt niet", text)


if __name__ == "__main__":
    unittest.main()


class PatternRuleTests(unittest.TestCase):
    def test_heikin_ashi_red(self):
        from datetime import date, timedelta

        from trendagent.agent import heikin_ashi_red
        from trendagent.data import Bar
        up = [Bar(date(2026, 1, 1) + timedelta(days=i), 100 + i, 101 + i, 99 + i, 100.5 + i, 1) for i in range(20)]
        down = [Bar(date(2026, 2, 1) + timedelta(days=i), 120 - i, 121 - i, 118 - i, 119 - i, 1) for i in range(6)]
        self.assertFalse(heikin_ashi_red(up, 2))
        self.assertTrue(heikin_ashi_red(up + down, 2))

    def test_production_accepts_pattern_settings(self):
        import json
        import tempfile
        from pathlib import Path

        from trendagent.core.production import ProductionConfigError, load_production
        p = Path(tempfile.mkdtemp()) / "p.json"
        p.write_text(json.dumps({"trend": {"entry_filter": "terugval", "ha_exit": True}}))
        self.assertEqual(load_production(p)["trend"]["entry_filter"], "terugval")
        p.write_text(json.dumps({"trend": {"entry_filter": "gokken"}}))
        with self.assertRaises(ProductionConfigError):
            load_production(p)

    def test_version_unchanged_with_defaults(self):
        from dataclasses import replace

        from trendagent.core.config import Settings
        from trendagent.strategies import trend_version
        s = Settings()
        self.assertNotEqual(trend_version(s), trend_version(replace(s, ha_exit=True)))
        self.assertNotIn("ha_exit", __import__("trendagent.strategies", fromlist=["x"]).trend_params(s))
