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
from dataclasses import fields

TREND_LABEL = "trend-1.1"
INVESTOR_LABEL = "investeerder-1.0"
RUSTIG_LABEL = "rustig-1.0"

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


# Later toegevoegde instellingen tellen alleen mee als ze afwijken van de standaard,
# zodat de versie van bestaande productie-instellingen niet verandert.
TREND_OPTIONAL = {"entry_filter": "geen", "ha_exit": False}


def trend_params(settings) -> dict:
    out = {k: getattr(settings, k) for k in TREND_PARAMS}
    out.update({k: getattr(settings, k) for k, d in TREND_OPTIONAL.items() if getattr(settings, k, d) != d})
    return out


def trend_version(settings) -> str:
    return f"{TREND_LABEL}-{_fingerprint(trend_params(settings))}"


def investor_params(mix) -> dict:
    # 'vast' telt alleen mee als het gebruikt wordt: zo blijft de versie van de gewone investeerder gelijk.
    return {f.name: getattr(mix, f.name) for f in fields(mix) if not (f.name == "vast" and not mix.vast)}


def investor_version(mix, naam: str = "investeerder") -> str:
    label = RUSTIG_LABEL if naam == "rustig" else INVESTOR_LABEL
    return f"{label}-{_fingerprint(investor_params(mix))}"


def production_mix():
    """De investeerder-instellingen zoals goedgekeurd in config/productie.json."""
    from .core.production import load_production
    from .investor import Mix

    mix = Mix(**load_production()["investeerder"])
    if mix.totaal() > 1.0 + 1e-9:
        from .core.production import ProductionConfigError
        raise ProductionConfigError("kern + satelliet + crypto mag samen niet boven 100% uitkomen")
    return mix


# ------------------------------------------------------------ rustige investeerder
# Kandidaten voor de rustige investeerder (nov 2026, op verzoek van de eigenaar). Geen crypto; een vast deel
# obligaties en goud dat in slechte beursjaren de klap moet dempen. De backtest (--strategie rustig) vergelijkt ze.
RUSTIG_VARIANTEN: dict[str, dict] = {
    "70-20-10": {"core_weight": 0.70, "satellite_weight": 0.0, "crypto_weight": 0.0,
                 "vast": (("IEAG.AS", 0.20), ("4GLD.DE", 0.10))},
    "60-20-10-10": {"core_weight": 0.60, "satellite_weight": 0.10, "satellite_count": 2, "max_per_sector": 1,
                    "crypto_weight": 0.0, "vast": (("IEAG.AS", 0.20), ("4GLD.DE", 0.10))},
    "60-20kort-10-10": {"core_weight": 0.60, "satellite_weight": 0.10, "satellite_count": 2, "max_per_sector": 1,
                        "crypto_weight": 0.0, "vast": (("IBGS.AS", 0.20), ("4GLD.DE", 0.10))},
    "50-25-15-10": {"core_weight": 0.50, "satellite_weight": 0.10, "satellite_count": 2, "max_per_sector": 1,
                    "crypto_weight": 0.0, "vast": (("IEAG.AS", 0.25), ("4GLD.DE", 0.15))},
    "60-0-20-20": {"core_weight": 0.60, "satellite_weight": 0.20, "satellite_count": 4, "max_per_sector": 1,
                   "crypto_weight": 0.0, "vast": (("4GLD.DE", 0.20),)},
}
RUSTIG_UITLEG = {
    "70-20-10": "70% wereld-ETF, 20% euro-obligaties, 10% goud. Geen losse aandelen, geen crypto.",
    "60-20-10-10": "60% wereld-ETF, 20% euro-obligaties, 10% goud, 10% in de 2 sterkste aandelen (andere sectoren).",
    "60-20kort-10-10": "Als hierboven, maar met kortlopende staatsobligaties (1-3 jaar) in plaats van alle looptijden.",
    "50-25-15-10": "50% wereld-ETF, 25% euro-obligaties, 15% goud, 10% in de 2 sterkste aandelen.",
    "60-0-20-20": "60% wereld-ETF, 20% goud, 20% in de 4 sterkste aandelen (andere sectoren). Geen obligaties.",
}
# De mix waarmee de rustige investeerder draait. Gekozen op basis van de backtest; veranderen alleen via een
# wijziging die de eigenaar goedkeurt.
RUSTIG_KEUZE = "60-20-10-10"


def rustig_mix(variant: str | None = None):
    from .investor import Mix
    return Mix(**RUSTIG_VARIANTEN[variant or RUSTIG_KEUZE])
