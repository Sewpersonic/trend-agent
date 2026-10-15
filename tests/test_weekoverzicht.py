import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from trendagent import volglijst, weekoverzicht
from trendagent.broker_t212 import find_instrument
from trendagent.core.config import Settings
from trendagent.data import SimulatedProvider


def _trade(dag, bot, soort, naam, res=None):
    return {"dag": dag, "bot": bot, "ticker": naam[:4].upper(), "naam": naam, "soort": soort, "waarde_eur": 500.0,
            "resultaat_eur": res, "reden": "trend OK: 3m +20.0%, 1m +5.0%, volume x1.00"}


class WekenTest(unittest.TestCase):
    def test_week_rows_orders_and_lessons(self):
        books = {"trend": {"equity_history": [{"day": "start", "equity": 10000}, {"day": "2026-10-09", "equity": 10000, "bench": 100},
                                              {"day": "2026-10-16", "equity": 10100, "bench": 100.5}]},
                 "investeerder": {"equity_history": []}}
        trades = [_trade("2026-10-13", "Trend-agent", "koop", "Shell"),
                  _trade("2026-10-15", "Trend-agent", "verkoop", "SAP", 42.0)]
        broker = {"koppeling": {"SHELL.AS": "SHELLa_EQ"},
                  "geschiedenis": [{"tijd": "2026-10-14T20:00:00+00:00", "orders": [
                      {"ticker": "SHELLa_EQ", "quantity": 13, "waarde_eur": 600, "uitkomst": "geplaatst"},
                      {"ticker": "BTC", "quantity": None, "uitkomst": "geweigerd", "reden": "crypto"}]}]}
        rows = weekoverzicht.weken(books, trades, broker, {}, Path("/nonexistent"), today=date(2026, 10, 15))
        week = [r for r in rows if r["soort"] == "week"]
        self.assertEqual(len(week), 2)  # week 41 (alleen een waarde) en week 42
        w = next(r for r in week if r["week"] == "2026-W42")
        self.assertTrue(w["lopend"])
        self.assertEqual(w["kopen"], 1)
        self.assertEqual(w["verkopen"], 1)
        self.assertAlmostEqual(w["trend_eur"], 100.0)
        tekst = " ".join(w["geleerd"])
        self.assertIn("kocht 1×", tekst)
        self.assertIn("1 met winst", tekst)
        self.assertIn("1 order geplaatst", tekst)
        self.assertIn("1 geweigerd", tekst)
        self.assertIn("beter dan de markt", tekst)
        orders = [r for r in rows if r["soort"] == "order" and r["week"] == "2026-W42"]
        self.assertEqual(len(orders), 4)
        self.assertIn("Shell", {o["naam"] for o in orders if o["bot"] == "Oefenaccount"})
        self.assertEqual(rows[0]["soort"], "week")  # nieuwste week bovenaan, samenvatting eerst

    def test_lesson_plain_language(self):
        z = weekoverzicht._les("Zwakte: RSI bij instap = 60-70: gemiddeld -0.21 R over 55 trades (x). Te testen via y.")
        self.assertIn("RSI 60-70", z)
        self.assertIn("slechter", z)
        self.assertIn("-0,21 R", z)

    def test_empty(self):
        self.assertEqual(weekoverzicht.weken({}, [], {}, {}, Path("/nonexistent")), [])


class GereedTest(unittest.TestCase):
    def test_not_ready_with_date(self):
        books = {"trend": {"equity_history": [{"day": "start", "equity": 1}] + [{"day": f"d{i}", "equity": 1} for i in range(3)]}}
        info = {"trend": {"klaar": {"eisen": [("Oefentijd", "bezig", ""), ("Daling", "ok", "")], "oordeel": "x"}}}
        rows = weekoverzicht.gereed(books, info, today=date(2026, 10, 15))
        t = rows[0]
        self.assertEqual((t["status"], t["ok"], t["totaal"], t["dagen"]), ("bezig", 1, 2, 3))
        self.assertEqual(t["vroegst"], "2027-01-07")  # 60 handelsdagen na 15 okt
        self.assertEqual(rows[-1]["id"], "oefenaccount")

    def test_ready(self):
        info = {"investeerder": {"klaar": {"eisen": [("A", "ok", ""), ("B", "ok", "")], "oordeel": "x"}}}
        rows = weekoverzicht.gereed({"investeerder": {"equity_history": []}}, info)
        self.assertEqual(rows[0]["status"], "klaar")


class VolglijstTest(unittest.TestCase):
    def test_build_and_t212(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            cfg = d / "v.json"
            cfg.write_text(json.dumps({"items": [{"ticker": "WMT", "naam": "Walmart"}, {"ticker": "MSFT"},
                                                  {"ticker": "PHIA.AS", "naam": "Philips"}]}))
            (d / "t212_instrumenten.json").write_text(json.dumps({"dag": "x", "items": [
                {"ticker": "WMT_US_EQ", "currencyCode": "USD", "shortName": "WMT", "type": "STOCK"}]}))
            insts = volglijst.load(cfg)
            self.assertEqual([i.ticker for i in insts], ["WMT", "PHIA.AS"])  # MSFT zit al bij de bots
            self.assertEqual(insts[1].currency, "EUR")
            today = date(2026, 10, 15)
            rows = volglijst.build(cfg, d, SimulatedProvider(end=today), Settings(), today)
            by = {r["ticker"]: r for r in rows}
            self.assertTrue(by["WMT"]["bij_t212"])
            self.assertEqual(by["WMT"]["t212"], "WMT_US_EQ")
            self.assertFalse(by["PHIA.AS"]["bij_t212"])
            for r in rows:
                self.assertIn(r["trend"], ("stijgend", "dalend", "zijwaarts", "onbekend"))
                self.assertLessEqual(len(r["lijn"]), 60)
            # zonder instrumentenlijst: onbekend in plaats van nee
            (d / "t212_instrumenten.json").unlink()
            rows = volglijst.build(cfg, d, SimulatedProvider(end=today), Settings(), today)
            self.assertIsNone(rows[0]["bij_t212"])

    def test_manual_order_can_find_watchlist_item(self):
        i = find_instrument("Philips")
        self.assertIsNotNone(i)
        self.assertEqual(i.ticker, "PHIA.AS")
        self.assertEqual(find_instrument("ASML").ticker, "ASML.AS")


if __name__ == "__main__":
    unittest.main()
