"""Productie-instellingen uit config/productie.json.

Dit bestand bevat alleen afwijkingen van de standaard in de code. Het wordt
gewijzigd door een mens, normaal door een voorstel van het wekelijkse onderzoek
samen te voegen op GitHub.

Veiligheid: alleen bekende instellingen binnen vaste grenzen zijn toegestaan.
Klopt er iets niet, dan weigert de bot te starten (liever niet handelen dan
met een onbedoelde instelling).
"""

from __future__ import annotations

import json
import os
from pathlib import Path


class ProductionConfigError(ValueError):
    pass


# naam -> (type, minimum, maximum). bool en tuple hebben geen grenzen.
TREND_ALLOWED = {
    "risk_per_trade": (float, 0.0005, 0.01),
    "max_open_risk": (float, 0.001, 0.05),
    "max_drawdown": (float, 0.03, 0.15),
    "max_positions": (int, 1, 10),
    "max_per_sector": (int, 0, 5),
    "max_consecutive_losses": (int, 2, 10),
    "stop_atr_multiple": (float, 1.0, 5.0),
    "trail_atr_multiple": (float, 1.0, 6.0),
    "regime_filter": (bool, None, None),
    "max_rsi_entry": (float, 50.0, 100.0),
    "entry_filter": (str, ("geen", "terugval", "uitbraak"), None),
    "ha_exit": (bool, None, None),
}

INVESTOR_ALLOWED = {
    "core_weight": (float, 0.3, 1.0),
    "satellite_weight": (float, 0.0, 0.5),
    "satellite_count": (int, 1, 10),
    "crypto_weight": (float, 0.0, 0.15),
    "regime_filter": (bool, None, None),
}


def config_path() -> Path:
    return Path(os.environ.get("PRODUCTION_CONFIG", "config/productie.json"))


def _check(section: str, values: dict, allowed: dict) -> dict:
    if not isinstance(values, dict):
        raise ProductionConfigError(f"'{section}' moet een object zijn")
    out = {}
    for key, value in values.items():
        if key not in allowed:
            raise ProductionConfigError(f"onbekende instelling '{section}.{key}'")
        typ, lo, hi = allowed[key]
        if typ is bool:
            if not isinstance(value, bool):
                raise ProductionConfigError(f"'{section}.{key}' moet true of false zijn")
        elif typ is str:
            if value not in lo:
                raise ProductionConfigError(f"'{section}.{key}' moet een van {list(lo)} zijn")
        else:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ProductionConfigError(f"'{section}.{key}' moet een getal zijn")
            if typ is int and int(value) != value:
                raise ProductionConfigError(f"'{section}.{key}' moet een geheel getal zijn")
            value = typ(value)
            if not lo <= value <= hi:
                raise ProductionConfigError(f"'{section}.{key}' moet tussen {lo} en {hi} liggen")
        out[key] = value
    return out


def load_production(path: Path | None = None) -> dict:
    """Geeft {"trend": {...}, "investeerder": {...}} met gecontroleerde waarden."""
    path = path or config_path()
    if not path.exists():
        return {"trend": {}, "investeerder": {}}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise ProductionConfigError(f"{path} is geen geldige JSON") from exc
    unknown = set(raw) - {"_uitleg", "trend", "investeerder"}
    if unknown:
        raise ProductionConfigError(f"onbekende onderdelen in {path}: {sorted(unknown)}")
    trend = _check("trend", raw.get("trend", {}), TREND_ALLOWED)
    inv = _check("investeerder", raw.get("investeerder", {}), INVESTOR_ALLOWED)
    return {"trend": trend, "investeerder": inv}


def save_production(data: dict, path: Path | None = None) -> None:
    path = path or config_path()
    _check("trend", data.get("trend", {}), TREND_ALLOWED)
    _check("investeerder", data.get("investeerder", {}), INVESTOR_ALLOWED)
    out = {"_uitleg": "Productie-instellingen die afwijken van de standaard in de code. Alleen een mens wijzigt "
                      "dit bestand (via een samengevoegd voorstel). Leeg = de standaard uit de code.",
           "trend": data.get("trend", {}), "investeerder": data.get("investeerder", {})}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
