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
    def __init__(self, positions, pending=None):
        self.positions = positions
        self.pending = pending or []
        self.calls = []

    def __call__(self, req, timeout=30):
        self.calls.append((req.get_method(), req.full_url, req.data))
        assert req.full_url.startswith("https://demo.trading212.com/")
        path = req.full_url.split("/api/v0")[1]
        if path.startswith("/equity/account/summary"):
            body = {"cash": {"availableToTrade": 50000}, "currency": "EUR"}
        elif path == "/equity/orders":
            body = self.pending
        elif path.startswith("/equity/positions"):
            body = self.positions
        elif path.startswith("/equity/metadata/instruments"):
            body = INSTR
        elif path.startswith("/equity/orders/market"):
            body = {"id": 1, "status": "NEW"}
        elif req.get_method() == "DELETE":
            body = None
            return FakeResp(b"")
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


class PendingTest(BrokerTest):
    def test_pending_orders_prevent_double_buy(self):
        api = FakeApi([{"ticker": "MSFT_US_EQ", "quantity": 1}],
                      pending=[{"ticker": "SHELLa_EQ", "quantity": 13, "filledQuantity": 0, "status": "NEW"},
                               {"ticker": "SAPd_EQ", "quantity": 2, "filledQuantity": 0, "status": "NEW"}])
        c = b.T212Demo("k", "s", opener=api)
        cfg = self.dir / "broker.json"; cfg.write_text(json.dumps({"orders_aan": True}))
        v = b.run(self.dir, cfg, client=c)
        self.assertEqual(v["plan"], [])
        self.assertFalse(any(m == "POST" for m, *_ in api.calls))


class HardeningTest(BrokerTest):
    def _cfg(self):
        cfg = self.dir / "cfg.json"; cfg.write_text(json.dumps({"orders_aan": True})); return cfg

    def test_nested_shape_counts_positions(self):
        api = FakeApi([{"instrument": {"ticker": "MSFT_US_EQ"}, "quantity": 1},
                       {"instrument": {"ticker": "SAPd_EQ"}, "quantity": 2},
                       {"instrument": {"ticker": "SHELLa_EQ"}, "quantity": 13}])
        v = b.run(self.dir, self._cfg(), client=b.T212Demo("k", "s", opener=api))
        self.assertEqual(v["plan"], [])

    def test_bad_shape_means_no_orders(self):
        api = FakeApi({"weird": True})
        v = b.run(self.dir, self._cfg(), client=b.T212Demo("k", "s", opener=api))
        self.assertEqual(v["status"], "fout")
        self.assertFalse(any(m == "POST" for m, *_ in api.calls))

    def test_missing_quantity_means_no_orders(self):
        api = FakeApi([{"ticker": "MSFT_US_EQ"}])
        v = b.run(self.dir, self._cfg(), client=b.T212Demo("k", "s", opener=api))
        self.assertEqual(v["status"], "fout")

    def test_never_sell_pending_and_cancel_unwanted_buy(self):
        (self.dir / "portfolio.json").write_text(json.dumps({"positions": {}}))
        (self.dir / "broker.json").write_text(json.dumps({"managed": ["MSFT_US_EQ"]}))
        api = FakeApi([], pending=[{"id": 77, "ticker": "MSFT_US_EQ", "quantity": 1, "filledQuantity": 0}])
        cfg = self.dir / "cfg.json"; cfg.write_text(json.dumps({"orders_aan": True}))
        v = b.run(self.dir, cfg, client=b.T212Demo("k", "s", opener=api))
        self.assertEqual([o["actie"] for o in v["orders"]], ["intrekken"])
        self.assertTrue(any(m == "DELETE" for m, *_ in api.calls))
        self.assertFalse(any(m == "POST" for m, *_ in api.calls))

    def test_timeout_on_post_stops_and_keeps_managed(self):
        api = FakeApi([])
        orig = api.__call__
        def boom(req, timeout=30):
            if req.get_method() == "POST":
                raise TimeoutError("read timeout")
            return orig(req, timeout)
        v = b.run(self.dir, self._cfg(), client=b.T212Demo("k", "s", opener=boom))
        self.assertEqual(len(v["orders"]), 1)
        self.assertEqual(v["orders"][0]["uitkomst"], "onzeker")
        self.assertIn(v["orders"][0]["ticker"], v["managed"])
        saved = json.loads((self.dir / "broker.json").read_text())
        self.assertIn(v["orders"][0]["ticker"], saved["managed"])

    def test_sells_first(self):
        (self.dir / "broker.json").write_text(json.dumps({"managed": ["XYZa_EQ"]}))
        api = FakeApi([{"ticker": "XYZa_EQ", "quantity": 3}])
        v = b.run(self.dir, self._cfg(), client=b.T212Demo("k", "s", opener=api))
        self.assertEqual(v["orders"][0]["actie"], "verkoop")
        self.assertEqual(v["orders"][0]["quantity"], -3)


class SecondRoundTest(BrokerTest):
    def test_incomplete_read_keeps_managed_and_orders(self):
        import http.client
        api = FakeApi([])
        orig = api.__call__
        n = {"post": 0}
        def flaky(req, timeout=30):
            if req.get_method() == "POST":
                n["post"] += 1
                if n["post"] == 2:
                    raise http.client.IncompleteRead(b"")
            return orig(req, timeout)
        cfg = self.dir / "cfg.json"; cfg.write_text(json.dumps({"orders_aan": True}))
        v = b.run(self.dir, cfg, client=b.T212Demo("k", "s", opener=flaky))
        self.assertEqual([o["uitkomst"] for o in v["orders"]], ["geplaatst", "onzeker"])
        self.assertEqual(len(v["managed"]), 2)

    def test_gateway_error_on_order_is_uncertain(self):
        api = FakeApi([])
        orig = api.__call__
        def gw(req, timeout=30):
            if req.get_method() == "POST":
                raise urllib.error.HTTPError(req.full_url, 504, "gw", {}, None)
            return orig(req, timeout)
        cfg = self.dir / "cfg.json"; cfg.write_text(json.dumps({"orders_aan": True}))
        v = b.run(self.dir, cfg, client=b.T212Demo("k", "s", opener=gw))
        self.assertEqual([o["uitkomst"] for o in v["orders"]], ["onzeker"])

    def test_crash_mid_run_keeps_placed_orders(self):
        api = FakeApi([])
        orig = api.__call__
        n = {"post": 0}
        def crash(req, timeout=30):
            if req.get_method() == "POST":
                n["post"] += 1
                if n["post"] == 2:
                    raise KeyError("onverwacht")
            return orig(req, timeout)
        cfg = self.dir / "cfg.json"; cfg.write_text(json.dumps({"orders_aan": True}))
        v = b.run(self.dir, cfg, client=b.T212Demo("k", "s", opener=crash))
        self.assertEqual(v["status"], "fout")
        self.assertEqual(v["orders"][0]["uitkomst"], "geplaatst")
        self.assertIn(v["orders"][0]["ticker"], v["managed"])


class ManualTest(BrokerTest):
    def test_manual_buy_is_kept_by_sync(self):
        api = FakeApi([{"ticker": "MSFT_US_EQ", "quantity": 1}, {"ticker": "SAPd_EQ", "quantity": 2}, {"ticker": "SHELLa_EQ", "quantity": 13}])
        c = b.T212Demo("k", "s", opener=api)
        e = b.manual(self.dir, "koop", "SAP", "3", client=c, price_eur=190.0)
        self.assertEqual(e["status"], "ok")
        self.assertEqual(e["orders"][0]["quantity"], 3)
        api.positions = [{"ticker": "MSFT_US_EQ", "quantity": 1}, {"ticker": "SAPd_EQ", "quantity": 5}, {"ticker": "SHELLa_EQ", "quantity": 13}]
        cfg = self.dir / "cfg.json"; cfg.write_text(json.dumps({"orders_aan": True}))
        v = b.run(self.dir, cfg, client=c)
        self.assertEqual(v["plan"], [])

    def test_manual_never_short_and_cap(self):
        api = FakeApi([{"ticker": "SAPd_EQ", "quantity": 2}])
        c = b.T212Demo("k", "s", opener=api)
        e = b.manual(self.dir, "verkoop", "SAP.DE", "10", client=c, price_eur=190.0)
        self.assertEqual(e["orders"][0]["quantity"], -2)
        e = b.manual(self.dir, "koop", "SAP", "100", client=c, price_eur=190.0)
        self.assertEqual(e["status"], "fout")
        e = b.manual(self.dir, "koop", "Bitcoin", "1", client=c, price_eur=1.0)
        self.assertEqual(e["status"], "fout")
        e = b.manual(self.dir, "koop", "onbekend aandeel", "1", client=c, price_eur=1.0)
        self.assertEqual(e["status"], "fout")
