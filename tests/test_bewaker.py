import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from trendagent import bewaker


class FakeClient:
    def __init__(self, posities, orders=()):
        self.pos = posities
        self.orders = list(orders)
        self.geplaatst = []

    def positions(self):
        return [{"instrument": {"ticker": t}, "quantity": q, "currentPrice": k} for t, (q, k) in self.pos.items()]

    def open_orders(self):
        return [{"ticker": t, "quantity": -1} for t in self.orders]

    def market_order(self, ticker, quantity):
        self.geplaatst.append((ticker, quantity))
        return {"id": 1}


class BewakerTest(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        (self.d / "portfolio.json").write_text(json.dumps({"positions": {
            "SHELL.AS": {"qty": 13, "stop": 45.0, "currency": "EUR"},
            "MSFT": {"qty": 1, "stop": 500.0, "currency": "USD"}}}))
        (self.d / "broker.json").write_text(json.dumps({"koppeling": {"SHELL.AS": "SHELLa_EQ", "MSFT": "MSFT_US_EQ"}}))
        self.cfg = self.d / "broker_cfg.json"
        self.cfg.write_text(json.dumps({"orders_aan": True}))

    def test_verkoopt_alleen_onder_de_stop_met_twee_bronnen(self):
        c = FakeClient({"SHELLa_EQ": (13, 44.5), "MSFT_US_EQ": (1, 520.0)})
        v = bewaker.ronde(self.d, self.cfg, client=c, yahoo={"SHELL.AS": 44.6, "MSFT": 521.0}.get)
        self.assertEqual(c.geplaatst, [("SHELLa_EQ", -13)])
        self.assertEqual(v["verkocht"][0]["ticker"], "SHELL.AS")
        self.assertTrue((self.d / "bewaker.json").exists())

    def test_bronnen_oneens_of_geen_tweede_koers_doet_niets(self):
        c = FakeClient({"SHELLa_EQ": (13, 44.5), "MSFT_US_EQ": (1, 480.0)})
        v = bewaker.ronde(self.d, self.cfg, client=c, yahoo={"SHELL.AS": 47.0}.get)   # 5% verschil; MSFT geen Yahoo
        self.assertEqual(c.geplaatst, [])
        acties = {r["ticker"]: r["actie"] for r in v["posities"]}
        self.assertIn("verschillen", acties["SHELL.AS"])
        self.assertIn("geen tweede koers", acties["MSFT"])

    def test_orders_uit_kill_switch_of_open_order(self):
        c = FakeClient({"SHELLa_EQ": (13, 44.0), "MSFT_US_EQ": (1, 480.0)}, orders=["MSFT_US_EQ"])
        self.cfg.write_text(json.dumps({"orders_aan": False}))
        bewaker.ronde(self.d, self.cfg, client=c, yahoo={"SHELL.AS": 44.0, "MSFT": 480.0}.get)
        self.assertEqual(c.geplaatst, [])
        self.cfg.write_text(json.dumps({"orders_aan": True}))
        (self.d / "kill_switch.json").write_text(json.dumps({"active": True, "by": "human", "reason": "test"}))
        bewaker.ronde(self.d, self.cfg, client=c, yahoo={"SHELL.AS": 44.0, "MSFT": 480.0}.get)
        self.assertEqual(c.geplaatst, [])
        (self.d / "kill_switch.json").unlink()
        bewaker.ronde(self.d, self.cfg, client=c, yahoo={"SHELL.AS": 44.0, "MSFT": 480.0}.get)
        self.assertEqual(c.geplaatst, [("SHELLa_EQ", -13)])     # MSFT heeft al een open order

    def test_sessie_elk_kwartier_tot_22_en_overdracht(self):
        klok = [datetime(2026, 10, 30, 7, 50, tzinfo=timezone.utc)]   # 08:50 NL (wintertijd)
        rondes = []

        def nu():
            return klok[0]

        def slaap(s):
            klok[0] += timedelta(seconds=s)

        def r():
            rondes.append(klok[0])
            return {"status": "ok", "log": []}
        regels, verder = bewaker.sessie(self.d, nu=nu, slaap=slaap, ronde_fn=r, max_duur_min=330)
        self.assertTrue(verder)                                     # na ~5,5 uur stopt deze run
        self.assertEqual(rondes[0].astimezone(bewaker_nl()).strftime("%H:%M"), "09:00")
        self.assertTrue(all(abs((b - a).total_seconds() - 900) < 60 for a, b in zip(rondes, rondes[1:])))
        regels, verder = bewaker.sessie(self.d, nu=nu, slaap=slaap, ronde_fn=r, max_duur_min=600)
        self.assertFalse(verder)
        self.assertLess(rondes[-1].astimezone(bewaker_nl()).hour, 22)


def bewaker_nl():
    from zoneinfo import ZoneInfo
    return ZoneInfo("Europe/Amsterdam")


if __name__ == "__main__":
    unittest.main()
