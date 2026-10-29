import unittest

from trendagent.universe import BY_TICKER, DAYTRADE, SECTOR, UNIVERSE


class UniverseTest(unittest.TestCase):
    def test_ruim_honderd_unieke_beleggingen_in_usd_of_eur(self):
        tickers = [i.ticker for i in UNIVERSE]
        self.assertGreaterEqual(len(tickers), 120)
        self.assertEqual(len(tickers), len(set(tickers)))
        self.assertTrue(all(i.currency in ("USD", "EUR") for i in UNIVERSE))

    def test_elke_belegging_heeft_een_sector(self):
        self.assertEqual([i.ticker for i in UNIVERSE if i.ticker not in SECTOR], [])

    def test_daytrader_houdt_zijn_vaste_amerikaanse_lijst(self):
        self.assertEqual(len(DAYTRADE), 27)
        self.assertTrue(all(BY_TICKER[t].region == "US" for t in DAYTRADE))


if __name__ == "__main__":
    unittest.main()
