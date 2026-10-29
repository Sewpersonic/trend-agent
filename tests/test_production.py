"""Tests voor config/productie.json en het voorstel-mechanisme."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from trendagent.core.config import load_settings
from trendagent.core.production import ProductionConfigError, load_production


def write(tmp: Path, data) -> Path:
    p = tmp / "productie.json"
    p.write_text(json.dumps(data))
    return p


class ProductionConfigTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_real_file_is_valid(self):
        """Het echte productiebestand is geldig (alleen bekende instellingen binnen de grenzen).
        Het mag afwijkingen bevatten: die komen er alleen in via een voorstel dat een mens heeft overgenomen."""
        prod = load_production(Path("config/productie.json"))
        self.assertEqual(set(prod), {"trend", "investeerder"})

    def test_overrides_reach_settings(self):
        p = write(self.tmp, {"trend": {"max_consecutive_losses": 5, "regime_filter": True}})
        with mock.patch.dict(os.environ, {"PRODUCTION_CONFIG": str(p)}, clear=True):
            s = load_settings()
        self.assertEqual(s.max_consecutive_losses, 5)
        self.assertTrue(s.regime_filter)

    def test_unknown_key_refused(self):
        p = write(self.tmp, {"trend": {"paper_trading": False}})
        with self.assertRaises(ProductionConfigError):
            load_production(p)

    def test_out_of_bounds_refused(self):
        p = write(self.tmp, {"trend": {"risk_per_trade": 0.2}})
        with self.assertRaises(ProductionConfigError):
            load_production(p)

    def test_wrong_type_refused(self):
        p = write(self.tmp, {"investeerder": {"regime_filter": "ja"}})
        with self.assertRaises(ProductionConfigError):
            load_production(p)

    def test_investor_mix_from_config(self):
        from trendagent.strategies import production_mix
        p = write(self.tmp, {"investeerder": {"satellite_count": 3}})
        with mock.patch.dict(os.environ, {"PRODUCTION_CONFIG": str(p)}):
            self.assertEqual(production_mix().satellite_count, 3)

    def test_weights_over_100_refused(self):
        from trendagent.strategies import production_mix
        p = write(self.tmp, {"investeerder": {"core_weight": 0.9, "satellite_weight": 0.3}})
        with mock.patch.dict(os.environ, {"PRODUCTION_CONFIG": str(p)}):
            with self.assertRaises(ProductionConfigError):
                production_mix()


class ProposalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.cfg = write(self.tmp, {"trend": {}, "investeerder": {}})

    def _run(self, recs):
        from trendagent.__main__ import _proposal
        rec = self.tmp / "aanbeveling.json"
        rec.write_text(json.dumps(recs))
        with mock.patch.dict(os.environ, {"PRODUCTION_CONFIG": str(self.cfg)}):
            return _proposal(str(rec), str(self.tmp / "body.md"))

    def test_no_recommendation_does_nothing(self):
        self.assertEqual(self._run([]), 3)
        self.assertEqual(load_production(self.cfg)["trend"], {})

    def test_recommendation_applied(self):
        rec = [{"strategie": "trend", "variant": "regimefilter", "wijziging": {"regime_filter": True},
                "productieversie": "trend-1.1-x", "sharpe_holdout": 0.9, "sharpe_holdout_productie": 0.5,
                "max_daling": -0.04, "max_daling_productie": -0.05}]
        self.assertEqual(self._run(rec), 0)
        self.assertEqual(load_production(self.cfg)["trend"], {"regime_filter": True})
        self.assertIn("Merge", (self.tmp / "body.md").read_text())
        self.assertEqual(self._run(rec), 3)          # tweede keer: staat er al in

    def test_invalid_recommendation_refused(self):
        rec = [{"strategie": "trend", "variant": "x", "wijziging": {"risk_per_trade": 0.5},
                "productieversie": "", "sharpe_holdout": 1, "sharpe_holdout_productie": 0,
                "max_daling": 0, "max_daling_productie": 0}]
        with self.assertRaises(ProductionConfigError):
            self._run(rec)


if __name__ == "__main__":
    unittest.main()
