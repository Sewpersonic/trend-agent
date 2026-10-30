"""De lijst met instrumenten waaruit de agent mag kiezen.

Alleen grote, liquide aandelen en ETF's uit de VS en de eurozone. Kleine,
onbekende of zeer beweeglijke fondsen staan er bewust niet in: daar zitten
pump-and-dumps en grote spreads.

Tickers gebruiken het Yahoo Finance-formaat:
  geen achtervoegsel = VS (USD) · .AS = Amsterdam · .DE = Xetra · .PA = Parijs · .MC = Madrid ·
  .MI = Milaan · .HE = Helsinki (allemaal EUR)

Oktober 2026 uitgebreid van 49 naar ruim 120 (op verzoek van de eigenaar): meer keus betekent vaker een sterke trend
om te volgen. Allemaal grote bedrijven met veel handel; de daytrader houdt zijn eigen vaste lijst (DAYTRADE).
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
    # --- VS: uitbreiding oktober 2026 (grote, veel verhandelde aandelen)
    _us("BRK-B", "Berkshire Hathaway"), _us("UNH", "UnitedHealth"), _us("JNJ", "Johnson & Johnson"),
    _us("PG", "Procter & Gamble"), _us("HD", "Home Depot"), _us("MA", "Mastercard"),
    _us("ABBV", "AbbVie"), _us("MRK", "Merck & Co"), _us("PEP", "PepsiCo"), _us("KO", "Coca-Cola"),
    _us("WMT", "Walmart"), _us("BAC", "Bank of America"), _us("CVX", "Chevron"), _us("ADBE", "Adobe"),
    _us("CSCO", "Cisco"), _us("QCOM", "Qualcomm"), _us("TXN", "Texas Instruments"),
    _us("AMAT", "Applied Materials"), _us("LRCX", "Lam Research"), _us("KLAC", "KLA"),
    _us("NOW", "ServiceNow"), _us("INTU", "Intuit"), _us("UBER", "Uber"), _us("GS", "Goldman Sachs"),
    _us("MS", "Morgan Stanley"), _us("CAT", "Caterpillar"), _us("GE", "GE Aerospace"), _us("RTX", "RTX"),
    _us("LMT", "Lockheed Martin"), _us("HON", "Honeywell"), _us("UNP", "Union Pacific"),
    _us("ISRG", "Intuitive Surgical"), _us("TMO", "Thermo Fisher"), _us("ABT", "Abbott"),
    _us("MCD", "McDonald's"), _us("DIS", "Disney"), _us("T", "AT&T"), _us("VZ", "Verizon"),
    _us("NEE", "NextEra Energy"), _us("LIN", "Linde"), _us("BKNG", "Booking"), _us("NKE", "Nike"),
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
    # --- Europa: uitbreiding oktober 2026
    _eu("PHIA.AS", "Philips"), _eu("UNA.AS", "Unilever"), _eu("ABN.AS", "ABN AMRO"), _eu("NN.AS", "NN Group"),
    _eu("ASRNL.AS", "ASR Nederland"), _eu("KPN.AS", "KPN"), _eu("RAND.AS", "Randstad"), _eu("UMG.AS", "Universal Music"),
    _eu("AKZA.AS", "AkzoNobel"), _eu("MT.AS", "ArcelorMittal"), _eu("DSFIR.AS", "DSM-Firmenich"),
    _eu("MBG.DE", "Mercedes-Benz"), _eu("BMW.DE", "BMW"), _eu("BAS.DE", "BASF"), _eu("BAYN.DE", "Bayer"),
    _eu("MUV2.DE", "Munich Re"), _eu("DBK.DE", "Deutsche Bank"), _eu("ADS.DE", "Adidas"),
    _eu("DB1.DE", "Deutsche Börse"), _eu("ENR.DE", "Siemens Energy"), _eu("MTX.DE", "MTU Aero Engines"),
    _eu("SAN.PA", "Sanofi"), _eu("AI.PA", "Air Liquide"), _eu("SAF.PA", "Safran"), _eu("EL.PA", "EssilorLuxottica"),
    _eu("RMS.PA", "Hermès"), _eu("CS.PA", "AXA"), _eu("DG.PA", "Vinci"), _eu("HO.PA", "Thales"),
    _eu("ITX.MC", "Inditex"), _eu("SAN.MC", "Banco Santander"), _eu("IBE.MC", "Iberdrola"),
    _eu("ISP.MI", "Intesa Sanpaolo"), _eu("UCG.MI", "UniCredit"), _eu("ENEL.MI", "Enel"), _eu("RACE.MI", "Ferrari"),
    _eu("NOKIA.HE", "Nokia"),
    # --- Europa: ETF
    _eu("IWDA.AS", "iShares MSCI World", "ETF"),
)

# De daytrader houdt zijn eigen, vaste lijst: de Amerikaanse beleggingen waarop zijn regels getest zijn.
DAYTRADE: tuple[str, ...] = (
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "AVGO", "TSLA", "AMD", "MU", "ORCL", "CRM", "NFLX", "PLTR",
    "CRWD", "PANW", "ANET", "JPM", "V", "LLY", "COST", "XOM", "SPY", "QQQ", "SMH", "XLE", "GLD",
)

# Crypto: alleen de twee grootste munten. Geen kleine of onbekende tokens.
# Wordt alleen gebruikt door de investeerder, niet door de trend-agent.
CRYPTO: tuple[Instrument, ...] = (
    Instrument("BTC-USD", "Bitcoin", "CRYPTO", "USD", "CRYPTO"),
    Instrument("ETH-USD", "Ethereum", "CRYPTO", "USD", "CRYPTO"),
)

BY_TICKER = {i.ticker: i for i in UNIVERSE + CRYPTO}

# Eerlijke test (alleen voor de backtest, nooit voor de echte keuze): de grootste bedrijven van begin 2016,
# zonder te weten welke daarna goed liepen. Zo meet de test minder 'achteraf gekozen' winnaars.
# (Bedrijven die sindsdien van de beurs verdwenen zijn ontbreken nog; ook dat maakt de uitkomst iets te mooi.)
_EXTRA_2016 = (
    _us("XOM", "ExxonMobil"), _us("GE", "General Electric"), _us("WFC", "Wells Fargo"), _us("PFE", "Pfizer"),
    _us("CMCSA", "Comcast"), _us("INTC", "Intel"), _us("PM", "Philip Morris"), _us("C", "Citigroup"),
    _us("MO", "Altria"), _us("IBM", "IBM"), _us("AMGN", "Amgen"), _us("GILD", "Gilead"), _us("MDT", "Medtronic"),
    _us("SLB", "Schlumberger"), _us("CVS", "CVS Health"), _us("BA", "Boeing"), _us("MMM", "3M"),
    _eu("VOW3.DE", "Volkswagen"), _eu("ENI.MI", "Eni"), _eu("TEF.MC", "Telefonica"), _eu("BBVA.MC", "BBVA"),
    _eu("SGO.PA", "Saint-Gobain"), _eu("ORA.PA", "Orange"), _eu("DG.PA", "Vinci"),
)
UNIVERSE_2016: tuple[Instrument, ...] = tuple({i.ticker: i for i in (
    *(BY_TICKER[t] for t in (
        "AAPL", "GOOGL", "MSFT", "AMZN", "META", "JNJ", "JPM", "V", "MA", "BRK-B", "PG", "VZ", "T", "CVX", "KO",
        "HD", "DIS", "BAC", "MRK", "PEP", "CSCO", "ORCL", "UNH", "MCD", "WMT", "QCOM", "ABBV", "LLY", "TXN", "HON",
        "SAP.DE", "SIE.DE", "ALV.DE", "BAYN.DE", "BAS.DE", "DTE.DE", "MBG.DE", "BMW.DE", "MUV2.DE", "SAN.PA",
        "TTE.PA", "MC.PA", "OR.PA", "BNP.PA", "AI.PA", "CS.PA", "AIR.PA", "SAN.MC", "ITX.MC", "IBE.MC", "ENEL.MI",
        "ISP.MI", "UNA.AS", "INGA.AS", "PHIA.AS", "ASML.AS", "AD.AS", "HEIA.AS", "NOKIA.HE",
        "SPY", "QQQ", "GLD", "XLE", "IWDA.AS")),
    *_EXTRA_2016)}.values())


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
    # uitbreiding oktober 2026
    **dict.fromkeys(["ADBE", "NOW", "INTU", "UBER", "BKNG", "CSCO", "NOKIA.HE"], "Software en internet"),
    **dict.fromkeys(["QCOM", "TXN", "AMAT", "LRCX", "KLAC"], "Chips"),
    **dict.fromkeys(["PG", "HD", "PEP", "KO", "WMT", "MCD", "NKE", "DIS", "UNA.AS", "MBG.DE", "BMW.DE", "ADS.DE",
                     "RMS.PA", "EL.PA", "ITX.MC", "RACE.MI", "UMG.AS"], "Consument"),
    **dict.fromkeys(["BRK-B", "MA", "BAC", "GS", "MS", "ABN.AS", "NN.AS", "ASRNL.AS", "MUV2.DE", "DBK.DE", "DB1.DE",
                     "CS.PA", "SAN.MC", "ISP.MI", "UCG.MI"], "Financieel"),
    **dict.fromkeys(["CVX"], "Energie"),
    **dict.fromkeys(["UNH", "JNJ", "ABBV", "MRK", "ISRG", "TMO", "ABT", "PHIA.AS", "BAYN.DE", "SAN.PA"], "Zorg"),
    **dict.fromkeys(["CAT", "GE", "RTX", "LMT", "HON", "UNP", "MTX.DE", "ENR.DE", "SAF.PA", "DG.PA", "HO.PA"],
                    "Industrie en defensie"),
    **dict.fromkeys(["T", "VZ", "KPN.AS"], "Telecom en media"),
    **dict.fromkeys(["RAND.AS"], "Zakelijke diensten"),
    **dict.fromkeys(["NEE", "IBE.MC", "ENEL.MI"], "Nutsbedrijven"),
    **dict.fromkeys(["LIN", "AKZA.AS", "MT.AS", "DSFIR.AS", "BAS.DE", "AI.PA"], "Grondstoffen en chemie"),
    **dict.fromkeys(["SPY", "IWDA.AS"], "Brede markt"),
    **dict.fromkeys(["GLD"], "Goud"),
}


def sector(ticker: str) -> str:
    return SECTOR.get(ticker, "Overig")
