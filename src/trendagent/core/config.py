"""Instellingen van de agent.

Alles heeft een veilige standaardwaarde en kan via een environment variable
worden aangepast. API-sleutels staan hier bewust niet: deze versie handelt
alleen met een nep-portefeuille en heeft geen broker nodig.

Live trading bestaat niet in deze versie. Staat PAPER_TRADING op iets anders
dan "true", dan weigert de agent te starten.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


class LiveTradingNotAllowedError(RuntimeError):
    pass


def _num(name: str, default: float, lo: float, hi: float) -> float:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"{name} moet een getal zijn, kreeg {raw!r}") from exc
    if not lo <= value <= hi:
        raise ValueError(f"{name} moet tussen {lo} en {hi} liggen, kreeg {value}")
    return value


@dataclass(frozen=True)
class Settings:
    # --- algemeen
    paper_trading: bool = True
    state_dir: Path = Path("state")
    reports_dir: Path = Path("rapporten")   # dagnotities en Excel-bestand
    write_reports: bool = True              # uit in de backtest (scheelt tijd)
    starting_cash_eur: float = 10_000.0

    # --- risico (percentages als fractie: 0.0025 = 0,25%)
    risk_per_trade: float = 0.0025        # max verlies per trade als de stop wordt geraakt
    max_open_risk: float = 0.01           # max opgeteld risico van alle open posities
    max_positions: int = 3
    max_position_weight: float = 0.25     # max 25% van het vermogen in één positie
    daily_loss_limit: float = 0.01        # -1% op één dag  -> kill switch
    max_drawdown: float = 0.05            # -5% vanaf de top -> kill switch
    max_consecutive_losses: int = 3       # daarna geen nieuwe aankopen

    # --- strategie
    stop_atr_multiple: float = 2.0        # beginstop = instap - 2 x ATR
    trail_atr_multiple: float = 3.0       # meeschuivende stop = hoogste slot - 3 x ATR
    min_avg_traded_value: float = 20_000_000  # min gem. dagomzet (in lokale valuta)
    max_daily_jump: float = 0.25          # dagsprong > 25% in 20 dagen = verdacht, overslaan
    max_bar_age_days: int = 4             # laatste koers ouder dan 4 dagen = data te oud

    # --- simulatie van kosten
    slippage: float = 0.0005              # 0,05% slechter dan de slotkoers
    commission_pct: float = 0.0005        # 0,05% van het orderbedrag
    commission_min_eur: float = 1.0

    tickers_override: tuple[str, ...] = field(default_factory=tuple)


def load_settings() -> Settings:
    paper = os.environ.get("PAPER_TRADING", "true").strip().lower()
    if paper != "true":
        raise LiveTradingNotAllowedError(
            "PAPER_TRADING moet 'true' zijn. Deze agent kan alleen oefenen met nepgeld."
        )
    tickers = os.environ.get("TICKERS", "")
    return Settings(
        state_dir=Path(os.environ.get("STATE_DIR", "state")),
        reports_dir=Path(os.environ.get("REPORTS_DIR", "rapporten")),
        starting_cash_eur=_num("STARTING_CASH_EUR", 10_000.0, 1_000, 10_000_000),
        risk_per_trade=_num("RISK_PER_TRADE", 0.0025, 0.0005, 0.01),
        max_open_risk=_num("MAX_OPEN_RISK", 0.01, 0.001, 0.03),
        max_positions=int(_num("MAX_POSITIONS", 3, 1, 10)),
        tickers_override=tuple(t.strip() for t in tickers.split(",") if t.strip()),
    )
