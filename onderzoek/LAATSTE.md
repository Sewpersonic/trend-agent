# Onderzoeksrapport 2026-10-26

Dit rapport test varianten van beide strategieën op echte koersen en kijkt wat de bots leren van hun eigen trades. **Er wordt niets automatisch aangepast.** Een aanbevolen variant gaat pas in productie als jij (of iemand die je vertrouwt) de instelling in de code aanpast; daarna draait de backtest opnieuw en loopt de nieuwe versie eerst weken mee op papier.

> Resultaten uit het verleden zijn geen garantie. De aandelenlijst is in 2026 gekozen (survivorship bias).

## Trend-agent

Periode 2021-10-26 t/m 2026-10-26. Ontwikkeldeel 2021-10-26 t/m 2025-04-30, holdout 2025-05-01 t/m 2026-10-26. 6 varianten getest tegen productie.

### Uitkomst

- **rem-pas-na-5-verliezen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.34 vs productie 0.60 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.27 vs 0.29
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.1% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.08 vs 0.10
    - ✓ Genoeg trades: 200 afgesloten trades (nodig: 30)
- **regimefilter: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.89 vs productie 0.60 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.24 vs 0.29
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.9% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe -0.18 vs 0.10
    - ✓ Genoeg trades: 170 afgesloten trades (nodig: 30)
- **niet-kopen-boven-rsi-75: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.47 vs productie 0.60 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.13 vs 0.29
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -4.8% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.03 vs 0.10
    - ✓ Genoeg trades: 197 afgesloten trades (nodig: 30)
- **koop-na-terugval: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.83 vs productie 0.60 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.27 vs 0.29
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -6.9% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe -0.34 vs 0.10
    - ✓ Genoeg trades: 203 afgesloten trades (nodig: 30)
- **koop-bij-nieuwe-top: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.47 vs productie 0.60 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.30 vs 0.29
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.1% vs -4.5%
    - ✓ Dubbele kosten en slippage: Sharpe 0.16 vs 0.10
    - ✓ Genoeg trades: 172 afgesloten trades (nodig: 30)
- **verkoop-na-2-rode-trendkaarsen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe -0.30 vs productie 0.60 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.87 vs 0.29
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -13.8% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe -1.80 vs 0.10
    - ✓ Genoeg trades: 587 afgesloten trades (nodig: 30)

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +7.4% | +1.4% | -4.5% | 0.37 | 0.60 | 0.10 | 193 | 35% | 2.31 |
| rem-pas-na-5-verliezen | +5.7% | +1.1% | -5.1% | 0.29 | 0.34 | 0.08 | 200 | 36% | 2.04 |
| regimefilter | +2.0% | +0.4% | -5.9% | 0.12 | 0.89 | -0.18 | 170 | 29% | 2.52 |
| niet-kopen-boven-rsi-75 | +4.3% | +0.8% | -4.8% | 0.23 | 0.47 | 0.03 | 197 | 36% | 2.03 |
| koop-na-terugval | +0.9% | +0.2% | -6.9% | 0.06 | 0.83 | -0.34 | 203 | 31% | 2.18 |
| koop-bij-nieuwe-top | +6.3% | +1.2% | -5.1% | 0.35 | 0.47 | 0.16 | 172 | 38% | 2.02 |
| verkoop-na-2-rode-trendkaarsen | -11.8% | -2.5% | -13.8% | -0.69 | -0.30 | -1.80 | 587 | 31% | 1.58 |

### Per periode (rendement)

| Variant | Oct 2021–Oct 2022 | Oct 2022–Oct 2023 | Oct 2023–Oct 2024 | Oct 2024–Oct 2025 | Oct 2025–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | -1.3% | +1.0% | +1.1% | +4.5% | +1.9% |
| rem-pas-na-5-verliezen | -1.6% | +2.9% | +1.2% | +1.4% | +1.6% |
| regimefilter | -2.5% | +0.4% | -2.5% | +3.4% | +3.2% |
| niet-kopen-boven-rsi-75 | -2.1% | -1.3% | +2.0% | +1.6% | +3.7% |
| koop-na-terugval | -5.7% | +0.1% | +3.2% | +0.5% | +2.6% |
| koop-bij-nieuwe-top | -0.8% | -0.6% | +4.5% | -0.4% | +3.1% |
| verkoop-na-2-rode-trendkaarsen | -3.6% | -5.4% | -2.1% | +0.1% | -1.3% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (koop-bij-nieuwe-top, rem-pas-na-5-verliezen, koop-bij-nieuwe-top, productie), was het resultaat over de laatste 4 periodes +2.1%, tegen +8.8% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +5% (92 d) | -0% (69 d) | -2% (100 d) | +19% (2 d) | +1% (226 d) | +1% (396 d) | +2% (615 d) | -2% (77 d) | -2% (93 d) | -1% (142 d) |
| rem-pas-na-5-verliezen | +6% (92 d) | -1% (69 d) | -1% (100 d) | +19% (2 d) | +1% (226 d) | +2% (396 d) | +1% (615 d) | -3% (73 d) | -0% (93 d) | -1% (142 d) |
| regimefilter | +0% (92 d) | +1% (69 d) | -1% (98 d) | +19% (2 d) | -1% (221 d) | +1% (396 d) | +1% (610 d) | -3% (77 d) | -3% (93 d) | +1% (139 d) |
| niet-kopen-boven-rsi-75 | +5% (92 d) | -1% (69 d) | -2% (100 d) | -37% (2 d) | +2% (221 d) | -0% (394 d) | +3% (613 d) | -3% (77 d) | -5% (93 d) | -2% (142 d) |
| koop-na-terugval | +4% (92 d) | -1% (69 d) | +2% (100 d) | -48% (2 d) | -1% (218 d) | +2% (396 d) | -0% (610 d) | -1% (76 d) | -3% (90 d) | +1% (142 d) |
| koop-bij-nieuwe-top | +0% (92 d) | +1% (69 d) | +1% (100 d) | -20% (2 d) | +3% (221 d) | -0% (396 d) | +2% (612 d) | -1% (77 d) | -6% (88 d) | +1% (142 d) |
| verkoop-na-2-rode-trendkaarsen | +1% (92 d) | -5% (67 d) | -2% (90 d) | +19% (2 d) | +1% (202 d) | -0% (366 d) | -2% (591 d) | -5% (74 d) | -10% (84 d) | -2% (135 d) |

## Trend-agent: lessen uit 5 jaar backtest (productie)

193 afgesloten trades, 35% winst, gemiddeld +0.14 R per trade (mediaan -0.42 R), totaal €585, gemiddeld 26 dagen vastgehouden.

### Bevindingen

- Sterkte: RSI bij instap = 70-80: gemiddeld +0.65 R over 52 trades (+0.70 R t.o.v. de rest, t = 2.3). Te testen via instelling `max_rsi_entry`.
- Zwakte: RSI bij instap = 60-70: gemiddeld -0.21 R over 55 trades (-0.49 R t.o.v. de rest, t = -2.3). Te testen via instelling `max_rsi_entry`.
- Sterkte: Marktbeweeglijkheid bij instap = normaal: gemiddeld +0.40 R over 92 trades (+0.50 R t.o.v. de rest, t = 2.0). Te testen via instelling `regime_filter`.

_Dit zijn hypotheses. Een regel verandert pas na een test op ongeziene data (zie het onderzoeksrapport)._

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend | 129 | 33% | +0.14 | 452 |
| zijwaarts | 36 | 42% | +0.15 | 132 |
| dalend | 25 | 36% | +0.14 | 34 |
| onbekend (te weinig) | 3 | 33% | -0.38 | -33 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 92 | 37% | +0.40 | 880 |
| laag | 51 | 35% | -0.01 | -54 |
| hoog | 47 | 32% | -0.19 | -209 |
| onbekend (te weinig) | 3 | 33% | -0.38 | -33 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 50-60 | 61 | 33% | +0.16 | 191 |
| 60-70 | 55 | 27% | -0.21 | -257 |
| 70-80 | 52 | 50% | +0.65 | 801 |
| 80 of hoger (te weinig) | 15 | 27% | -0.14 | -66 |
| onder 50 (te weinig) | 10 | 30% | -0.33 | -84 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| positief | 113 | 36% | +0.23 | 585 |
| negatief | 80 | 34% | +0.00 | -1 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| hoger (>1,1) | 80 | 36% | +0.03 | 80 |
| normaal | 74 | 36% | +0.31 | 519 |
| lager (<0,9) | 39 | 31% | +0.01 | -15 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% | 91 | 29% | -0.09 | -219 |
| meer dan 25% | 82 | 39% | +0.34 | 650 |
| tot 10% | 20 | 50% | +0.31 | 154 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 112 | 31% | -0.01 | -115 |
| wild (>3%) | 57 | 44% | +0.42 | 626 |
| rustig (<1,5%) | 24 | 33% | +0.13 | 74 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt | 175 | 38% | +0.18 | 718 |
| trend gebroken (slot onder 50-daags gemiddelde) (te weinig) | 18 | 11% | -0.32 | -133 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| middel | 75 | 15% | -0.50 | -856 |
| lang (>30 d) | 66 | 85% | +1.72 | 2,646 |
| kort (<10 d) | 52 | 2% | -0.96 | -1,206 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-d373c7 | 193 | 35% | +0.14 | 585 |

## Trend-agent: lessen uit het oefenen (nepgeld, live)

Live van 2026-10-13 t/m 2026-10-23 (9 handelsdagen): bot +0.61%, wereld-ETF -1.84%, verschil +2.46%.

Nog geen afgesloten trades om van te leren.

## Investeerder

Periode 2021-10-26 t/m 2026-10-26. Ontwikkeldeel 2021-10-26 t/m 2025-04-24, holdout 2025-04-25 t/m 2026-10-26. 2 varianten getest tegen productie.

### Uitkomst

- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.70 vs productie 1.74 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.82 vs 0.88
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -20.2% vs -21.8%
    - ✗ Dubbele kosten en slippage: Sharpe 1.05 vs 1.10
- **satelliet-3-aandelen: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 1.86 vs productie 1.74 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.72 vs 0.88
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -24.2% vs -21.8%
    - ✗ Dubbele kosten en slippage: Sharpe 1.04 vs 1.10

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +147.4% | +19.9% | -21.8% | 1.14 | 1.74 | 1.10 | 148 | 65% | 1.40 |
| regimefilter | +128.1% | +17.9% | -20.2% | 1.09 | 1.70 | 1.05 | 153 | 63% | 1.36 |
| satelliet-3-aandelen | +146.3% | +19.8% | -24.2% | 1.07 | 1.86 | 1.04 | 124 | 65% | 1.33 |

### Per periode (rendement)

| Variant | Oct 2021–Oct 2022 | Oct 2022–Oct 2023 | Oct 2023–Oct 2024 | Oct 2024–Oct 2025 | Oct 2025–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | -10.7% | +10.4% | +56.0% | +26.7% | +25.6% |
| regimefilter | -10.0% | +3.3% | +56.0% | +24.1% | +25.6% |
| satelliet-3-aandelen | -13.9% | +9.2% | +47.1% | +32.5% | +32.4% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (productie, productie, productie, productie), was het resultaat over de laatste 4 periodes +174.1%, tegen +174.1% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +66% (66 d) | +14% (51 d) | +30% (74 d) | +140% (2 d) | +37% (162 d) | +25% (280 d) | +4% (446 d) | +36% (56 d) | -22% (67 d) | +21% (100 d) |
| regimefilter | +61% (66 d) | +10% (51 d) | +28% (74 d) | +140% (2 d) | +37% (162 d) | +24% (280 d) | +3% (446 d) | +31% (56 d) | -27% (67 d) | +14% (100 d) |
| satelliet-3-aandelen | +57% (66 d) | +17% (51 d) | +32% (74 d) | +240% (2 d) | +33% (162 d) | +24% (280 d) | +6% (446 d) | +47% (56 d) | -25% (67 d) | +17% (100 d) |

## Investeerder live (nepgeld)

Van 2026-10-13 t/m 2026-10-23: investeerder -5.09%, wereld-ETF -1.84%, verschil -3.24%.
