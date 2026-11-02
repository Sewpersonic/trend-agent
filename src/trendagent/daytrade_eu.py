"""Daytrade-onderzoek op de Europese beurs (Amsterdam, Frankfurt, Parijs): alleen kijken en testen, nog niet handelen.

Zelfde regels als de daytrader in Amerika (uitbraak uit de openingsrange), maar met de Europese beurstijden
(09:00-17:30 Nederlandse tijd). De 5-minutenkoersen worden elke beursdag bewaard (backtest/daytrade/koersen_eu),
zodat de test steeds verder terug kan kijken. Pas als de test laat zien dat het werkt, kan de eigenaar via een
voorstel besluiten om de daytrader ook hier te laten oefenen. Verandert niets aan de bots.
"""

from __future__ import annotations

import json
from datetime import datetime, time, timezone
from pathlib import Path

from .daytrader import Bar5, Params, backtest, variant

try:
    from zoneinfo import ZoneInfo
    AMS = ZoneInfo("Europe/Amsterdam")
except Exception:  # pragma: no cover
    AMS = None

MARKT = "EXW1.DE"   # iShares Core EURO STOXX 50 (Xetra): de 'markt' voor de marktfilter, zoals SPY in Amerika
TICKERS = [
    MARKT,
    "ASML.AS", "SHELL.AS", "INGA.AS", "ADYEN.AS", "PRX.AS", "UNA.AS", "AD.AS", "PHIA.AS", "BESI.AS", "ASM.AS",
    "HEIA.AS", "WKL.AS", "ABN.AS", "KPN.AS", "MT.AS",
    "SAP.DE", "SIE.DE", "ALV.DE", "DTE.DE", "RHM.DE", "IFX.DE", "MBG.DE",
    "MC.PA", "TTE.PA", "AIR.PA", "BNP.PA", "SU.PA", "OR.PA",
]
MAP = Path("backtest/daytrade/koersen_eu")
PARAMS = Params(open_t=time(9, 0), close_t=time(17, 30), entry_until=time(10, 30), exit_at=time(17, 15), market=MARKT)

VARIANTEN = {
    "basis (kopen tot 10:30)": {},
    "kopen tot 11:30": {"entry_until": time(11, 30)},
    "kopen tot 13:00": {"entry_until": time(13, 0)},
    "zonder marktfilter": {"market_filter": False},
    "minder streng op volume (1,0x)": {"min_rvol": 1.0},
}


def download(period: str = "60d") -> dict[str, list[Bar5]]:
    from .daytrade_test import download as _dl
    return _dl(TICKERS, period=period, tz=AMS, einde="17:25")


def archiveer(period: str = "5d") -> list[Path]:
    from .daytrade_archief import bewaar
    return bewaar(download(period), MAP, tz=AMS)


def run(out_dir: Path = Path("backtest/daytrade/eu"), data: dict[str, list[Bar5]] | None = None) -> dict:
    from .daytrade_archief import laad, samen
    if data is None:
        nieuw = download()
        from .daytrade_archief import bewaar
        bewaar(nieuw, MAP, tz=AMS)
        data = samen(laad(MAP, tz=AMS), nieuw)
    out_dir.mkdir(parents=True, exist_ok=True)
    res = {naam: backtest(data, variant(PARAMS, **kw)) for naam, kw in VARIANTEN.items()}
    b = res["basis (kopen tot 10:30)"]
    summary = {"gemaakt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "van": b["curve"][0][0] if b["curve"] else "", "tot": b["curve"][-1][0] if b["curve"] else "",
               "aandelen": sorted(data), "varianten": {k: {"stats": v["stats"], "eind": v["eind"]} for k, v in res.items()}}
    (out_dir / "resultaat.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    (out_dir / "RAPPORT.md").write_text(rapport(summary), encoding="utf-8")
    return summary


def _p(x) -> str:
    return "–" if x is None else f"{x * 100:+.2f}%".replace(".", ",")


def rapport(s: dict) -> str:
    regels = [
        "# Daytrader op de Europese beurs (alleen test, nog niet handelen)", "",
        f"Koersen per 5 minuten van {s['van']} t/m {s['tot']}, {len(s['aandelen'])} beleggingen (Amsterdam, Frankfurt, "
        "Parijs). Zelfde regels als in Amerika, met Europese beurstijden (09:00-17:30). $10.000 nepgeld, na kosten.", "",
        "| Variant | Resultaat | Trades | Met winst | Grootste daling |", "| --- | --- | --- | --- | --- |",
    ]
    for naam, v in s["varianten"].items():
        st = v["stats"]
        winst = "–" if st["winst_pct"] is None else f"{st['winst_pct'] * 100:.0f}%"
        regels.append(f"| {naam} | {_p(st['rendement'])} | {st['trades']} | {winst} | {_p(st['max_daling'])} |")
    regels += ["", "Een korte periode bewijst weinig. De daytrader handelt hier pas als de eigenaar dat via een voorstel besluit."]
    return "\n".join(regels) + "\n"
