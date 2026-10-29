import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from tests import test_daytrader as tdt
from trendagent import daytrader as dt
from trendagent.daytrade_sessie import momenten, sessie


class SessieTest(unittest.TestCase):
    def setUp(self):
        base = tdt.LiveTest()
        base.setUp()
        self.base, self.days = base, base.days

    def _draai(self, start_ny, deel="koop", sd=None):
        """Sessie met een verzonnen klok: slaap() zet de klok vooruit, de ronde krijgt alleen bestaande koersen."""
        from trendagent import daytrade_live as dl
        klok = [start_ny.replace(tzinfo=dt.NY).astimezone(timezone.utc)]
        rondes = []

        def nu():
            return klok[0]

        def slaap(sec):
            klok[0] += timedelta(seconds=sec)

        def ronde(sd, cp, now):
            ny = now.astimezone(dt.NY).replace(tzinfo=None)
            rondes.append(ny)
            st = dl.run(sd, cp, now=now, provider=self.base.provider_at(ny))
            klok[0] += timedelta(seconds=20)   # een ronde duurt even
            return st

        sd = sd or Path(tempfile.mkdtemp())
        cfg = sd / "cfg.json"
        cfg.write_text("{}")
        regels = sessie(sd, cfg, deel=deel, nu=nu, slaap=slaap, ronde=ronde, p=dt.Params(rvol_days=10))
        return sd, cfg, rondes, regels

    def test_rondes_op_elk_kijkmoment_en_koopt_op_tijd(self):
        last = self.days[-1]
        sd, cfg, rondes, regels = self._draai(datetime.combine(last, dt.time(9, 40)))
        verwacht = momenten(last, dt.Params(rvol_days=10))
        self.assertEqual(len(rondes), len(verwacht))
        self.assertTrue(all(abs((a - b).total_seconds()) < 5 for a, b in zip(rondes, verwacht)))
        self.assertLessEqual(rondes[-1].time(), dt.time(12, 33))
        import json
        st = json.loads((sd / "daytrader.json").read_text())
        gekocht = [t["ticker"] for t in (st["vandaag"].get("trades") or [])] + list((st["vandaag"].get("open") or {}))
        self.assertIn("AAA", gekocht)
        # zelfde aankoopmoment als de test op oude koersen
        bt = dt.backtest(self.base.data, dt.Params(rvol_days=10))
        t_in = (st["vandaag"].get("open") or {}).get("AAA", {}).get("t_in") or st["vandaag"]["trades"][0]["t_in"]
        self.assertIn(bt["trades"][0]["t_in"], str(t_in))

    def test_te_laat_gestart_doet_een_ronde(self):
        last = self.days[-1]
        sd, cfg, rondes, regels = self._draai(datetime.combine(last, dt.time(14, 0)))
        self.assertEqual(len(rondes), 1)
        self.assertIn("Na het koopdeel", regels[0])

    def test_halverwege_gestart_slaat_voorbije_momenten_over(self):
        last = self.days[-1]
        sd, cfg, rondes, regels = self._draai(datetime.combine(last, dt.time(11, 5)))
        self.assertTrue(rondes)
        self.assertGreaterEqual(rondes[0], datetime.combine(last, dt.time(11, 0)))

    def test_hele_beursdag_koop_en_middag(self):
        """Koopdeel vroeg gestart (07:30), daarna het middagdeel: elk kwartier, en om 15:45 is alles verkocht."""
        last = self.days[-1]
        sd, cfg, rondes, regels = self._draai(datetime.combine(last, dt.time(7, 30)))
        self.assertEqual(rondes[0].strftime("%H:%M"), "10:01")
        sd, cfg, rondes2, regels2 = self._draai(datetime.combine(last, dt.time(12, 33)), deel="middag", sd=sd)
        self.assertEqual(rondes2[0].strftime("%H:%M"), "12:46")
        self.assertEqual(rondes2[-1].strftime("%H:%M"), "15:46")
        self.assertTrue(all((b - a).total_seconds() <= 15 * 60 + 30 for a, b in zip(rondes2, rondes2[1:])))
        import json
        st = json.loads((sd / "daytrader.json").read_text())
        self.assertTrue(st["vandaag"]["klaar"])
        self.assertEqual(st["vandaag"]["open"], {})
        # een tweede start op dezelfde dag doet niets
        sd, cfg, rondes3, regels3 = self._draai(datetime.combine(last, dt.time(13, 0)), deel="middag", sd=sd)
        self.assertEqual(rondes3, [])
        self.assertIn("al gedaan", regels3[0])

    def test_te_vroeg_gestart_doet_niets(self):
        last = self.days[-1]
        sd, cfg, rondes, regels = self._draai(datetime.combine(last, dt.time(6, 0)))
        self.assertEqual(rondes, [])
        self.assertIn("Te vroeg", regels[0])

    def test_kopen_tot_11_verkort_het_koopdeel(self):
        from trendagent.daytrade_live import params_from
        p = params_from({"regels": {"kopen_tot_11": True}}, dt.Params(rvol_days=10))
        last = self.days[-1]
        self.assertEqual(momenten(last, p, "koop")[-1].strftime("%H:%M"), "11:01")
        self.assertEqual(momenten(last, p, "middag")[0].strftime("%H:%M"), "11:16")
        self.assertEqual(params_from({"regels": {"kopen_tot_11": "ja"}}).entry_until, dt.Params().entry_until)


if __name__ == "__main__":
    unittest.main()
