"""Versiebeheer van strategieën.

Elke trade en elk rapport krijgt een versie mee, bijvoorbeeld "trend-1.1-3fa2c1".
- Het eerste deel ("trend-1.1") is een label dat een mens ophoogt bij een bewuste wijziging.
- Het laatste deel is een vingerafdruk van alle instellingen die de beslissingen
  bepalen. Verandert er één instelling, dan verandert de vingerafdruk vanzelf.

Zo kun je resultaten altijd toeschrijven aan precies de regels die ze opleverden,
en zie je in de leerrapporten per versie hoe het ging.

Productie-instellingen veranderen gebeurt ALLEEN door een mens (wijziging in de
code via GitHub). Het wekelijkse onderzoek doet aanbevelingen maar past nooit
zelf iets aan.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, fields

TREND_LABEL = "trend-1.1"
INVESTOR_LABEL = "investeerder-1.0"

# Instellingen die de beslissingen van de trend-agent bepalen.
TREND_PARAMS = (
    "risk_per_trade", "max_open_risk", "max_positions", "max_position_weight",
    "daily_loss_limit", "max_drawdown", "max_consecutive_losses",
    "stop_atr_multiple", "trail_atr_multiple", "min_avg_traded_value",
    "max_daily_jump", "max_bar_age_days", "regime_filter", "max_rsi_entry",
)


def _fingerprint(params: dict) -> str:
    raw = json.dumps(params, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode()).hexdigest()[:6]


def trend_params(settings) -> dict:
    return {k: getattr(settings, k) for k in TREND_PARAMS}


def trend_version(settings) -> str:
    return f"{TREND_LABEL}-{_fingerprint(trend_params(settings))}"


def investor_params(mix) -> dict:
    return {f.name: getattr(mix, f.name) for f in fields(mix)}


def investor_version(mix) -> str:
    return f"{INVESTOR_LABEL}-{_fingerprint(investor_params(mix))}"


def production_mix():
    """De investeerder-instellingen zoals goedgekeurd in config/productie.json."""
    from .core.production import load_production
    from .investor import Mix

    mix = Mix(**load_production()["investeerder"])
    if mix.core_weight + mix.satellite_weight + mix.crypto_weight > 1.0 + 1e-9:
        from .core.production import ProductionConfigError
        raise ProductionConfigError("kern + satelliet + crypto mag samen niet boven 100% uitkomen")
    return mix
