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
