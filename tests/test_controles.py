import unittest

from trendagent import controles


class ControlesTest(unittest.TestCase):
    def test_plain_rows(self):
        h = {"trend": {"day": "2026-10-14", "status": "OK", "gevraagd": 50, "ok": 50, "regime": "stijgend-laag", "verouderd": 0,
                       "bronnen": {"koersen": {"1 bron": 50}, "wisselkoers": "bevestigd", "tweede_bron": "overgeslagen",
                                   "fout_tweede_bron": "GOOGL: Stooq gaf geen koersen ('<!DOCTYPE html><html>')"}}}
        rows = controles.rows(h, {"status": "ok"}, [{"soort": "positie", "gelijk": True}, {"soort": "positie", "gelijk": False, "onderweg_gelijk": True}])
        by = {r["id"]: r for r in rows}
        self.assertEqual(by["trend-ronde"]["stand"], "goed")
        self.assertEqual(by["trend-bronnen"]["stand"], "letop")
        self.assertNotIn("DOCTYPE", by["trend-bronnen"]["detail"])
        self.assertEqual(by["trend-markt"]["stand"], "info")
        self.assertIn("stijgt en is rustig", by["trend-markt"]["uitleg"])
        self.assertEqual(by["investeerder-ronde"]["stand"], "fout")  # geen gegevens
        self.assertEqual(by["broker-gelijk"]["stand"], "info")

    def test_errors(self):
        h = {"trend": {"status": "FOUT", "fout": "ValueError: x", "gevraagd": 50, "ok": 10, "verdacht": {"ABC": ["sprong"]},
                       "waarschuwingen": ["Kill switch staat aan (test)."]}}
        by = {r["id"]: r for r in controles.rows(h, {"status": "fout", "reden": "geen sleutel"}, [])}
        self.assertEqual(by["trend-ronde"]["stand"], "fout")
        self.assertEqual(by["trend-koersen"]["stand"], "fout")
        self.assertEqual(by["trend-verdacht"]["stand"], "letop")
        self.assertEqual(by["trend-w0"]["stand"], "fout")
        self.assertEqual(by["broker-koppeling"]["stand"], "fout")


if __name__ == "__main__":
    unittest.main()
