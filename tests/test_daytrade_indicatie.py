import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from trendagent import daytrade_indicatie as di
from trendagent import daytrader as dt
from tests import test_daytrader as tdt


def ev(dag, r, tijd="10:15", rvol=2.0):
    return {"dag": dag, "ticker": "AAA", "tijd": tijd, "r": r, "reden": "x",
            "ctx": {"tijd": tijd, "rvol": rvol, "or_breedte": 0.01}}


class IndicatieTest(unittest.TestCase):
    def setUp(self):
        b = tdt.DaytraderTest()
        b.setUp()
        self.data, self.days = b.data, b.days

    def test_uitbraken_vindt_de_uitbraak_met_uitkomst(self):
        evs = di.uitbraken(self.data, dt.Params(rvol_days=10))
        self.assertTrue(evs)
        e = evs[0]
        self.assertEqual(e["ticker"], "AAA")
        self.assertEqual(e["dag"], self.days[-1].isoformat())
        self.assertGreater(e["r"], 0)
        self.assertIn("rvol", e["ctx"])

    def test_uitkomst_stop(self):
        bars = self.data["AAA"][-78:]
        t = datetime.combine(self.days[-1], dt.time(10, 0))
        o = (101.0, 99.0, 100.0)
        r, reden = di.uitkomst([dt.Bar5(b.t, b.o, b.h, 90.0, b.c, b.v) for b in bars], t, o, dt.Params())
        self.assertEqual(reden, "stop-loss")
        self.assertLess(r, -0.9)

    def test_tabel_en_indicatie(self):
        # vroeg (10:xx) goed, laat (11:xx) slecht
        evs = [ev(f"2026-08-{i % 28 + 1:02d}", 0.8, "10:15") for i in range(30)]
        evs += [ev(f"2026-08-{i % 28 + 1:02d}", -0.6, "11:30") for i in range(30)]
        t = di.tabel(evs)
        self.assertEqual(t["totaal"]["n"], 60)
        goed = di.indicatie({"tijd": "10:20", "rvol": 2.0, "or_breedte": 0.01}, t)
        slecht = di.indicatie({"tijd": "11:40", "rvol": 2.0, "or_breedte": 0.01}, t)
        self.assertEqual(goed["oordeel"], "gunstig", goed)
        self.assertEqual(slecht["oordeel"], "ongunstig", slecht)
        self.assertIn("%", goed["tekst"])
        self.assertEqual(di.indicatie({}, {})["oordeel"], "onbekend")

    def test_toets_alleen_op_latere_dagen(self):
        evs = []
        for d in range(1, 21):
            evs += [ev(f"2026-09-{d:02d}", 0.8, "10:15") for _ in range(3)]
            evs += [ev(f"2026-09-{d:02d}", -0.6, "11:30") for _ in range(3)]
        u = di.toets(evs)
        self.assertTrue(u["genoeg"])
        self.assertEqual(u["leer_dagen"] + u["test_dagen"], 20)
        self.assertTrue(u["werkt"], u)
        self.assertIn("verschil", di.zin(u))
        self.assertFalse(di.toets(evs[:6])["genoeg"])

    def test_live_beoordelaar_en_regel(self):
        from trendagent import daytrade_live as dl
        self.assertIn("indicatie_filter", dl.REGELS)
        with tempfile.TemporaryDirectory() as d:
            pad = Path(d) / "indicatie.json"
            self.assertIsNone(dl.beoordelaar(pad))
            evs = [ev("2026-08-01", 0.8, "10:15") for _ in range(30)] + [ev("2026-08-01", -0.6, "11:30") for _ in range(30)]
            pad.write_text(json.dumps({"tabel": di.tabel(evs)}))
            f = dl.beoordelaar(pad)
            self.assertEqual(f({"tijd": "11:45"})["oordeel"], "ongunstig")
        p = dl.params_from({"regels": {"indicatie_filter": True, "iets_anders": True}})
        self.assertTrue(p.indicatie_filter)

    def test_samenvoegen_bewaart_oude_dagen(self):
        oud = [ev("2026-07-01", 0.5), ev("2026-08-01", 0.1)]
        nieuw = [{**ev("2026-08-01", 0.9)}, ev("2026-08-02", -1.0)]
        uit = di.samenvoegen(oud, nieuw)
        self.assertEqual([e["dag"] for e in uit], ["2026-07-01", "2026-08-01", "2026-08-02"])
        self.assertEqual(uit[1]["r"], 0.9)

    def test_dashboard_rij(self):
        from trendagent.daytrade_overzicht import extra_rows
        evs = []
        for d in range(1, 21):
            evs += [ev(f"2026-09-{d:02d}", 0.8, "10:15") for _ in range(3)]
            evs += [ev(f"2026-09-{d:02d}", -0.6, "11:30") for _ in range(3)]
        ts = di.toets(evs)
        rows = extra_rows({}, {"indicatie": {"uitbraken": len(evs), "toets": ts, "zin": di.zin(ts)}},
                          {"regels": {"indicatie_filter": True}})
        r = next(x for x in rows if x["soort"] == "indicatie")
        self.assertTrue(r["werkt"] and r["aan"])
        self.assertIn("gunstig_r", r)
        self.assertTrue(all(not isinstance(v, (list, dict)) for v in r.values()))


if __name__ == "__main__":
    unittest.main()
