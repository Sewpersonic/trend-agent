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

    def _draai(self, start_ny):
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

        d = tempfile.mkdtemp()
        sd = Path(d)
        cfg = sd / "cfg.json"
        cfg.write_text("{}")
        regels = sessie(sd, cfg, nu=nu, slaap=slaap, ronde=ronde, p=dt.Params(rvol_days=10))
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
        self.assertIn("Na de koopuren", regels[0])

    def test_halverwege_gestart_slaat_voorbije_momenten_over(self):
        last = self.days[-1]
        sd, cfg, rondes, regels = self._draai(datetime.combine(last, dt.time(11, 5)))
        self.assertTrue(rondes)
        self.assertGreaterEqual(rondes[0], datetime.combine(last, dt.time(11, 0)))


if __name__ == "__main__":
    unittest.main()
