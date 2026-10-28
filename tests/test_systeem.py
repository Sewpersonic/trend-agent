import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from trendagent import systeem


def schrijf(p: Path, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data), encoding="utf-8")


class SysteemTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        r = Path(self.tmp.name)
        self.state, self.dash, self.root = r / "state", r / "dashboard", r
        schrijf(self.state / "health.json", {"trend": {"day": "2026-10-27", "status": "OK", "ok": 50, "gevraagd": 50,
                                                       "bronnen": {"koersen": {"2 bronnen": 50}, "tweede_bron": "ok"}}})
        schrijf(self.state / "portfolio.json", {"cash_eur": 2000, "positions": {"A": {}, "B": {}}, "trades": []})
        schrijf(self.dash / "stand.json", [{"bot": "Trend-agent", "waarde": 10000}, {"bot": "Investeerder", "waarde": 9900}])
        schrijf(self.dash / "github.json", [])
        schrijf(self.dash / "broker.json", [{"soort": "stand", "status": "ok", "waarde": 5000,
                                             "tijd": "2026-10-28T13:30:00+00:00"}])
        schrijf(self.state / "daytrader.json", {"equity": 10000, "trades": [], "rondes": []})
        # woensdag 28 oktober 14:00 NL (09:00 New York): werkuur, nog voor de koopuren
        self.nu = datetime(2026, 10, 28, 13, 40, tzinfo=timezone.utc)

    def tearDown(self):
        self.tmp.cleanup()

    def rows(self, nu=None):
        return systeem.rows(self.state, self.dash, self.root, nu=nu or self.nu)

    def knel(self, rows):
        return {r["node"]: r for r in rows if r["soort"] == "knel"}

    def test_alles_goed(self):
        rows = self.rows()
        self.assertEqual(rows[0]["soort"], "meta")
        self.assertEqual(rows[0]["fout"], 0)
        nodes = {r["node"]: r for r in rows if r["soort"] == "node"}
        self.assertEqual(nodes["trend"]["stand"], "goed")
        self.assertIn("2 van 3", nodes["trend"]["sub"])
        self.assertTrue(all(not isinstance(v, (list, dict)) for r in rows for v in r.values()))

    def test_knelpunten_worden_gevonden(self):
        schrijf(self.state / "portfolio.json", {"cash_eur": 8000, "positions": {"A": {}, "B": {}, "C": {}}, "trades": []})
        schrijf(self.state / "kill_switch.json", {"active": True, "reason": "daling"})
        h = json.loads((self.state / "health.json").read_text())
        h["trend"]["bronnen"] = {"koersen": {"1 bron": 50}, "tweede_bron": "overgeslagen na herhaalde fouten"}
        schrijf(self.state / "health.json", h)
        schrijf(self.dash / "github.json", [{"soort": "voorstel", "titel": "Voorstel X"},
                                            {"workflow": "practice", "wat": "Dagelijkse ronde", "uitkomst": "fout",
                                             "opgelost": False, "start": "2026-10-28T01:00:00Z", "uitleg": "liep vast"}])
        k = self.knel(self.rows())
        self.assertEqual(k["trend"]["ernst"], "letop")
        self.assertEqual(k["rem"]["ernst"], "fout")
        self.assertEqual(k["yahoo"]["ernst"], "letop")
        self.assertEqual(k["jij"]["ernst"], "mens")
        self.assertEqual(k["cron"]["ernst"], "fout")
        self.assertIn("uur", k)    # geen uurlijkse run van de taak gezien tijdens werkuren
        rows = self.rows()
        self.assertEqual(rows[1]["soort"], "node")
        self.assertEqual([r["ernst"] for r in rows if r["soort"] == "knel"][0], "fout")   # ernstigste eerst

    def test_koopuren_gemist(self):
        laat = datetime(2026, 10, 28, 18, 0, tzinfo=timezone.utc)   # 14:00 New York
        rondes = [{"ny": "2026-10-28 10:01", "status": "ok"}, {"ny": "2026-10-28 13:26", "status": "ok"}]
        schrijf(self.state / "daytrader.json", {"equity": 10000, "trades": [], "rondes": rondes,
                                                "laatste_ronde": {"status": "ok"}})
        self.assertIn("day", self.knel(self.rows(laat)))
        rondes = [{"ny": f"2026-10-28 {h:02d}:{m:02d}", "status": "ok"} for h in (10, 11, 12) for m in (1, 16, 31, 46)]
        schrijf(self.state / "daytrader.json", {"equity": 10000, "trades": [], "rondes": rondes,
                                                "laatste_ronde": {"status": "ok"}})
        self.assertNotIn("day", self.knel(self.rows(laat)))


if __name__ == "__main__":
    unittest.main()
