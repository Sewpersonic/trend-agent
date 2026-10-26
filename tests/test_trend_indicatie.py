import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from trendagent import trend_indicatie as ti
from trendagent.core.config import load_settings
from trendagent.data import Bar, SimulatedProvider
from trendagent.universe import UNIVERSE


def bars_from(closes, start=date(2024, 1, 1)):
    out, d = [], start
    for c in closes:
        while d.weekday() >= 5:
            d += timedelta(days=1)
        out.append(Bar(d, c, c * 1.005, c * 0.995, c, 1_000_000))
        d += timedelta(days=1)
    return out


class TrendIndicatieTest(unittest.TestCase):
    def setUp(self):
        self.s = load_settings()

    def test_signalen_op_verzonnen_koersen(self):
        sim = SimulatedProvider(end=date(2026, 10, 23))
        tickers = [i.ticker for i in UNIVERSE[:8]] + ["SPY"]
        bars = {i.ticker: sim.history(i, 3 * 260) for i in UNIVERSE if i.ticker in tickers}
        evs = ti.signalen(bars, self.s, tickers[:8])
        self.assertTrue(evs)
        e = evs[0]
        self.assertIn(e["reden"], ("stop-loss", "trend gebroken", "na een jaar"))
        self.assertIn("moment", e["ctx"])
        self.assertIn("rsi14", e["ctx"])
        self.assertTrue(any(x["ctx"].get("trend_regime") not in (None, "onbekend") for x in evs), "markttrend moet bekend zijn")
        # nooit twee signalen van hetzelfde aandeel vlak na elkaar
        per = {}
        for x in evs:
            per.setdefault(x["ticker"], []).append(date.fromisoformat(x["dag"]))
        for ds in per.values():
            self.assertTrue(all((b - a).days >= ti.RUST for a, b in zip(ds, ds[1:])))

    def test_uitkomst_stop_en_trendbreuk(self):
        stijg = [100 * 1.004 ** i for i in range(260)]
        bars = bars_from(stijg + [stijg[-1] * 0.80] * 5)
        from trendagent.signals import analyse
        i = 259
        a = analyse("X", bars[:i + 1], bars[i].day, self.s)
        r, reden, dagen = ti.uitkomst(bars, i, a, self.s)
        self.assertEqual(reden, "stop-loss")
        self.assertLess(r, -0.9)
        self.assertEqual(dagen, 1)
        # loopt nog (geen uitstap en nog geen jaar verder): geen uitkomst
        bars2 = bars_from(stijg + [stijg[-1] * 1.004 ** k for k in range(1, 6)])
        self.assertIsNone(ti.uitkomst(bars2, i, a, self.s))

    def test_maak_beoordeel_en_dashboard(self):
        evs = []
        for d in range(1, 29):
            dag = (date(2025, 1, 1) + timedelta(days=d * 7)).isoformat()
            evs += [{"dag": dag, "ticker": "A", "r": 1.0, "ctx": {"moment": "gunstig", "rsi14": 55}} for _ in range(2)]
            evs += [{"dag": dag, "ticker": "B", "r": -0.8, "ctx": {"moment": "opgelopen", "rsi14": 85}} for _ in range(2)]
        from trendagent.daytrade_indicatie import tabel, toets, zin
        ts = toets(evs, kenmerken=ti.KENMERKEN)
        uit = {"tabel": tabel(evs, ti.KENMERKEN), "toets": ts, "zin": zin(ts, ti.WOORD), "signalen": len(evs)}
        self.assertTrue(ts["werkt"], ts)
        self.assertEqual(ti.beoordeel({"moment": "gunstig", "rsi14": 50}, uit)["oordeel"], "gunstig")
        self.assertEqual(ti.beoordeel({"moment": "opgelopen", "rsi14": 82}, uit)["oordeel"], "ongunstig")
        self.assertIn("koopsignalen", ti.beoordeel({"moment": "gunstig"}, uit)["tekst"])
        self.assertEqual(ti.beoordeel({}, {})["oordeel"], "onbekend")
        from trendagent.dashboard_data import ti_rows
        r = ti_rows(uit)[0]
        self.assertEqual(r["soort"], "indicatie")
        self.assertTrue(r["werkt"])
        self.assertTrue(all(not isinstance(v, (list, dict)) for v in r.values()))
        with tempfile.TemporaryDirectory() as d:
            sim = SimulatedProvider(end=date(2026, 10, 23))
            bars = {i.ticker: sim.history(i, 2 * 260) for i in UNIVERSE[:5]}
            out = ti.maak(bars, self.s, Path(d))
            self.assertEqual(json.loads((Path(d) / ti.BESTAND).read_text())["signalen"], out["signalen"])


if __name__ == "__main__":
    unittest.main()
