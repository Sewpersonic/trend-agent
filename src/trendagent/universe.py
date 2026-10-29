"""De lijst met instrumenten waaruit de agent mag kiezen.

Alleen grote, liquide aandelen en ETF's uit de VS en de eurozone. Kleine,
onbekende of zeer beweeglijke fondsen staan er bewust niet in: daar zitten
pump-and-dumps en grote spreads.

Tickers gebruiken het Yahoo Finance-formaat:
  geen achtervoegsel = VS (USD) · .AS = Amsterdam · .DE = Xetra · .PA = Parijs (EUR)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Instrument:
    ticker: str
    name: str
    region: str      # "US" of "EU"
    currency: str    # "USD" of "EUR"
    kind: str        # "STOCK" of "ETF"


def _us(ticker: str, name: str, kind: str = "STOCK") -> Instrument:
    return Instrument(ticker, name, "US", "USD", kind)


def _eu(ticker: str, name: str, kind: str = "STOCK") -> Instrument:
    return Instrument(ticker, name, "EU", "EUR", kind)


UNIVERSE: tuple[Instrument, ...] = (
    # --- VS: grote aandelen
    _us("AAPL", "Apple"), _us("MSFT", "Microsoft"), _us("NVDA", "Nvidia"),
    _us("AMZN", "Amazon"), _us("GOOGL", "Alphabet"), _us("META", "Meta Platforms"),
    _us("AVGO", "Broadcom"), _us("TSLA", "Tesla"), _us("AMD", "AMD"),
    _us("MU", "Micron"), _us("ORCL", "Oracle"), _us("CRM", "Salesforce"),
    _us("NFLX", "Netflix"), _us("PLTR", "Palantir"), _us("CRWD", "CrowdStrike"),
    _us("PANW", "Palo Alto Networks"), _us("ANET", "Arista Networks"),
    _us("JPM", "JPMorgan Chase"), _us("V", "Visa"), _us("LLY", "Eli Lilly"),
    _us("COST", "Costco"), _us("XOM", "ExxonMobil"),
    # --- VS: ETF's (brede markt, thema's, goud)
    _us("SPY", "S&P 500 ETF", "ETF"), _us("QQQ", "Nasdaq-100 ETF", "ETF"),
    _us("SMH", "Halfgeleider-ETF", "ETF"), _us("XLE", "Energie-ETF", "ETF"),
    _us("GLD", "Goud-ETF", "ETF"),
    # --- Europa: Amsterdam
    _eu("ASML.AS", "ASML"), _eu("ASM.AS", "ASM International"), _eu("BESI.AS", "BE Semiconductor"),
    _eu("ADYEN.AS", "Adyen"), _eu("INGA.AS", "ING"), _eu("SHELL.AS", "Shell"),
    _eu("PRX.AS", "Prosus"), _eu("AD.AS", "Ahold Delhaize"), _eu("HEIA.AS", "Heineken"),
    _eu("WKL.AS", "Wolters Kluwer"),
    # --- Europa: Duitsland
    _eu("SAP.DE", "SAP"), _eu("SIE.DE", "Siemens"), _eu("ALV.DE", "Allianz"),
    _eu("DTE.DE", "Deutsche Telekom"), _eu("RHM.DE", "Rheinmetall"), _eu("IFX.DE", "Infineon"),
    # --- Europa: Frankrijk
    _eu("MC.PA", "LVMH"), _eu("OR.PA", "L'Oreal"), _eu("TTE.PA", "TotalEnergies"),
    _eu("SU.PA", "Schneider Electric"), _eu("AIR.PA", "Airbus"), _eu("BNP.PA", "BNP Paribas"),
    # --- Europa: ETF
    _eu("IWDA.AS", "iShares MSCI World", "ETF"),
)

# Crypto: alleen de twee grootste munten. Geen kleine of onbekende tokens.
# Wordt alleen gebruikt door de investeerder, niet door de trend-agent.
CRYPTO: tuple[Instrument, ...] = (
    Instrument("BTC-USD", "Bitcoin", "CRYPTO", "USD", "CRYPTO"),
    Instrument("ETH-USD", "Ethereum", "CRYPTO", "USD", "CRYPTO"),
)

BY_TICKER = {i.ticker: i for i in UNIVERSE + CRYPTO}


def select(tickers: tuple[str, ...] = ()) -> tuple[Instrument, ...]:
    """Geeft het hele universum terug, of alleen de gekozen tickers (die er wel in moeten staan)."""
    if not tickers:
        return UNIVERSE
    unknown = [t for t in tickers if t not in BY_TICKER]
    if unknown:
        raise ValueError(f"Onbekende tickers (niet in het universum): {unknown}")
    return tuple(BY_TICKER[t] for t in tickers)


# Sector per belegging, om te spreiden (de trend-agent koopt niet te veel uit dezelfde hoek).
SECTOR: dict[str, str] = {
    **dict.fromkeys(["AAPL", "MSFT", "GOOGL", "META", "ORCL", "CRM", "PLTR", "CRWD", "PANW", "SAP.DE", "PRX.AS",
                     "QQQ"], "Software en internet"),
    **dict.fromkeys(["NVDA", "AVGO", "AMD", "MU", "ANET", "SMH", "ASML.AS", "ASM.AS", "BESI.AS", "IFX.DE"], "Chips"),
    **dict.fromkeys(["AMZN", "TSLA", "COST", "AD.AS", "HEIA.AS", "MC.PA", "OR.PA"], "Consument"),
    **dict.fromkeys(["JPM", "V", "INGA.AS", "ALV.DE", "BNP.PA", "ADYEN.AS"], "Financieel"),
    **dict.fromkeys(["XOM", "XLE", "SHELL.AS", "TTE.PA"], "Energie"),
    **dict.fromkeys(["LLY"], "Zorg"),
    **dict.fromkeys(["SIE.DE", "RHM.DE", "SU.PA", "AIR.PA"], "Industrie en defensie"),
    **dict.fromkeys(["DTE.DE", "NFLX"], "Telecom en media"),
    **dict.fromkeys(["WKL.AS"], "Zakelijke diensten"),
    **dict.fromkeys(["SPY", "IWDA.AS"], "Brede markt"),
    **dict.fromkeys(["GLD"], "Goud"),
}


def sector(ticker: str) -> str:
    return SECTOR.get(ticker, "Overig")
