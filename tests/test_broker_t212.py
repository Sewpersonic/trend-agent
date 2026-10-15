import io
import json
import os
import tempfile
import unittest
import urllib.error
from pathlib import Path

from trendagent import broker_t212 as b

INSTR = [{"ticker": "MSFT_US_EQ", "currencyCode": "USD", "shortName": "MSFT", "type": "STOCK"},
         {"ticker": "SAPd_EQ", "currencyCode": "EUR", "shortName": "SAP", "type": "STOCK"},
         {"ticker": "SHELLa_EQ", "currencyCode": "EUR", "shortName": "SHELL", "type": "STOCK"}]


class FakeResp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class FakeApi:
    def __init__(self, positions):
        self.positions = positions
        self.calls = []

    def __call__(self, req, timeout=30):
        self.calls.append((req.get_method(), req.full_url, req.data))
        assert req.full_url.startswith("https://demo.trading212.com/")
        path = req.full_url.split("/api/v0")[1]
        if path.startswith("/equity/account/summary"):
            body = {"cash": {"availableToTrade": 50000}, "currency": "EUR"}
        elif path.startswith("/equity/positions"):
            body = self.positions
        elif path.startswith("/equity/metadata/instruments"):
            body = INSTR
        elif path.startswith("/equity/orders/market"):
            body = {"id": 1, "status": "NEW"}
        else:
            raise urllib.error.HTTPError(req.full_url, 404, "nf", {}, None)
        return FakeResp(json.dumps(body).encode())


class BrokerTest(unittest.TestCase):
    def setUp(self):
        os.environ["PAPER_TRADING"] = "true"
        self.dir = Path(tempfile.mkdtemp())
        port = {"positions": {
            "MSFT": {"qty": 1, "currency": "USD", "highest_close": 540},
            "SAP.DE": {"qty": 2, "currency": "EUR", "highest_close": 197},
            "SHELL.AS": {"qty": 13, "currency": "EUR", "highest_close": 46}}}
        (self.dir / "portfolio.json").write_text(json.dumps(port))

    def test_refuses_live(self):
        with self.assertRaises(b.BrokerError):
            b.T212Demo("k", "s", base="https://live.trading212.com/api/v0")

    def test_needs_paper_trading(self):
        os.environ["PAPER_TRADING"] = "false"
        with self.assertRaises(b.BrokerError):
            b.T212Demo("k", "s")

    def test_map(self):
        self.assertEqual(b.map_ticker("MSFT", "USD", INSTR), "MSFT_US_EQ")
        self.assertEqual(b.map_ticker("SAP.DE", "EUR", INSTR), "SAPd_EQ")
        self.assertEqual(b.map_ticker("SHELL.AS", "EUR", INSTR), "SHELLa_EQ")
        self.assertIsNone(b.map_ticker("XYZ.AS", "EUR", INSTR))

    def test_check_places_nothing(self):
        api = FakeApi([])
        c = b.T212Demo("k", "s", opener=api)
        cfg = self.dir / "broker.json"; cfg.write_text(json.dumps({"orders_aan": True}))
        v = b.run(self.dir, cfg, check_only=True, client=c)
        self.assertEqual(v["status"], "alleen kijken")
        self.assertEqual(len(v["plan"]), 3)
        self.assertFalse(any(m == "POST" for m, *_ in api.calls))

    def test_sync_buys_difference_and_never_shorts(self):
        api = FakeApi([{"ticker": "SAPd_EQ", "quantity": 5}])
        c = b.T212Demo("k", "s", opener=api)
        cfg = self.dir / "broker.json"; cfg.write_text(json.dumps({"orders_aan": True}))
        v = b.run(self.dir, cfg, client=c)
        q = {o["ticker"]: o["quantity"] for o in v["orders"]}
        self.assertEqual(q["MSFT_US_EQ"], 1)
        self.assertEqual(q["SHELLa_EQ"], 13)
        self.assertEqual(q["SAPd_EQ"], -3)  # 5 -> 2, nooit onder nul
        self.assertTrue(all(o["uitkomst"] == "geplaatst" for o in v["orders"]))

    def test_kill_switch_blocks(self):
        api = FakeApi([])
        c = b.T212Demo("k", "s", opener=api)
        (self.dir / "kill_switch.json").write_text(json.dumps({"active": True, "reason": "test"}))
        cfg = self.dir / "broker.json"; cfg.write_text(json.dumps({"orders_aan": True}))
        v = b.run(self.dir, cfg, client=c)
        self.assertEqual(v["status"], "alleen kijken")
        self.assertFalse(any(m == "POST" for m, *_ in api.calls))

    def test_missing_key_is_reported(self):
        os.environ.pop("T212_DEMO_KEY", None)
        v = b.run(self.dir, self.dir / "nope.json")
        self.assertEqual(v["status"], "fout")
        self.assertIn("T212_DEMO_KEY", v["reden"])
