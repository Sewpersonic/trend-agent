# Onderzoeksrapport 2026-10-29

Dit rapport test varianten van beide strategieën op echte koersen en kijkt wat de bots leren van hun eigen trades. **Er wordt niets automatisch aangepast.** Een aanbevolen variant gaat pas in productie als jij (of iemand die je vertrouwt) de instelling in de code aanpast; daarna draait de backtest opnieuw en loopt de nieuwe versie eerst weken mee op papier.

> Resultaten uit het verleden zijn geen garantie. De aandelenlijst is in 2026 gekozen (survivorship bias).

## Trend-agent

Periode 2021-10-29 t/m 2026-10-29. Ontwikkeldeel 2021-10-29 t/m 2025-05-01, holdout 2025-05-02 t/m 2026-10-29. 8 varianten getest tegen productie.

### Uitkomst

- **rem-pas-na-5-verliezen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.63 vs productie 0.80 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.46 vs 0.32
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -7.6% vs -7.3%
    - ✗ Dubbele kosten en slippage: Sharpe 0.08 vs 0.15
    - ✓ Genoeg trades: 320 afgesloten trades (nodig: 30)
- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.77 vs productie 0.80 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.12 vs 0.32
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -8.3% vs -7.3%
    - ✗ Dubbele kosten en slippage: Sharpe -0.16 vs 0.15
    - ✓ Genoeg trades: 266 afgesloten trades (nodig: 30)
- **niet-kopen-boven-rsi-75: AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 1.14 vs productie 0.80 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.39 vs 0.32
    - ✓ Consistent over periodes: beter in 4 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -6.8% vs -7.3%
    - ✓ Dubbele kosten en slippage: Sharpe 0.22 vs 0.15
    - ✓ Genoeg trades: 307 afgesloten trades (nodig: 30)
- **koop-na-terugval: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.80 vs productie 0.80 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.21 vs 0.32
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.8% vs -7.3%
    - ✗ Dubbele kosten en slippage: Sharpe -0.06 vs 0.15
    - ✓ Genoeg trades: 317 afgesloten trades (nodig: 30)
- **koop-bij-nieuwe-top: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.43 vs productie 0.80 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.12 vs 0.32
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -6.7% vs -7.3%
    - ✗ Dubbele kosten en slippage: Sharpe -0.06 vs 0.15
    - ✓ Genoeg trades: 281 afgesloten trades (nodig: 30)
- **verkoop-na-2-rode-trendkaarsen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.08 vs productie 0.80 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.91 vs 0.32
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -17.5% vs -7.3%
    - ✗ Dubbele kosten en slippage: Sharpe -1.74 vs 0.15
    - ✓ Genoeg trades: 929 afgesloten trades (nodig: 30)
- **4-plekken: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.61 vs productie 0.80 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.40 vs 0.32
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -4.6% vs -7.3%
    - ✗ Dubbele kosten en slippage: Sharpe 0.07 vs 0.15
    - ✓ Genoeg trades: 256 afgesloten trades (nodig: 30)
- **zonder-sectorgrens: AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.98 vs productie 0.80 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.49 vs 0.32
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.6% vs -7.3%
    - ✓ Dubbele kosten en slippage: Sharpe 0.21 vs 0.15
    - ✓ Genoeg trades: 304 afgesloten trades (nodig: 30)

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +11.7% | +2.2% | -7.3% | 0.46 | 0.80 | 0.15 | 314 | 32% | 2.54 |
| rem-pas-na-5-verliezen | +13.4% | +2.5% | -7.6% | 0.52 | 0.63 | 0.08 | 320 | 33% | 2.61 |
| regimefilter | +3.4% | +0.7% | -8.3% | 0.16 | 0.77 | -0.16 | 266 | 30% | 2.38 |
| niet-kopen-boven-rsi-75 | +16.3% | +3.1% | -6.8% | 0.61 | 1.14 | 0.22 | 307 | 36% | 2.41 |
| koop-na-terugval | +9.4% | +1.8% | -5.8% | 0.38 | 0.80 | -0.06 | 317 | 33% | 2.39 |
| koop-bij-nieuwe-top | +5.0% | +1.0% | -6.7% | 0.22 | 0.43 | -0.06 | 281 | 36% | 1.97 |
| verkoop-na-2-rode-trendkaarsen | -13.4% | -2.8% | -17.5% | -0.60 | 0.08 | -1.74 | 929 | 32% | 1.64 |
| 4-plekken | +10.4% | +2.0% | -4.6% | 0.46 | 0.61 | 0.07 | 256 | 35% | 2.32 |
| zonder-sectorgrens | +18.9% | +3.5% | -5.6% | 0.64 | 0.98 | 0.21 | 304 | 38% | 2.40 |

### Per periode (rendement)

| Variant | Oct 2021–Oct 2022 | Nov 2022–Oct 2023 | Oct 2023–Oct 2024 | Oct 2024–Oct 2025 | Oct 2025–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | -4.2% | -0.7% | +7.9% | +3.9% | +4.8% |
| rem-pas-na-5-verliezen | -4.7% | +2.3% | +7.3% | +4.5% | +3.8% |
| regimefilter | -5.7% | -1.2% | +3.8% | +3.2% | +3.3% |
| niet-kopen-boven-rsi-75 | -2.7% | -0.2% | +7.1% | +5.8% | +5.8% |
| koop-na-terugval | -3.3% | -1.6% | +8.0% | +1.8% | +4.4% |
| koop-bij-nieuwe-top | -1.0% | -3.2% | +5.6% | +2.3% | +1.6% |
| verkoop-na-2-rode-trendkaarsen | -3.8% | -8.8% | +0.8% | -3.4% | +1.5% |
| 4-plekken | -2.1% | +0.9% | +5.0% | +2.9% | +3.3% |
| zonder-sectorgrens | -2.1% | +2.3% | +6.5% | +4.9% | +5.9% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (koop-bij-nieuwe-top, zonder-sectorgrens, zonder-sectorgrens, zonder-sectorgrens), was het resultaat over de laatste 4 periodes +14.4%, tegen +16.7% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +6% (92 d) | -4% (69 d) | +1% (100 d) | +27% (4 d) | +6% (226 d) | +3% (399 d) | +1% (615 d) | -0% (79 d) | -6% (93 d) | -1% (142 d) |
| rem-pas-na-5-verliezen | +7% (92 d) | -2% (69 d) | +2% (100 d) | +27% (4 d) | +5% (226 d) | +3% (399 d) | +2% (615 d) | -1% (79 d) | -6% (93 d) | -2% (142 d) |
| regimefilter | -0% (92 d) | +0% (69 d) | -0% (100 d) | +27% (4 d) | +0% (221 d) | +3% (399 d) | -1% (612 d) | -1% (78 d) | -2% (90 d) | +1% (142 d) |
| niet-kopen-boven-rsi-75 | +6% (92 d) | -6% (69 d) | +3% (100 d) | +31% (4 d) | +6% (222 d) | +4% (399 d) | +2% (615 d) | +0% (79 d) | -8% (93 d) | -1% (142 d) |
| koop-na-terugval | +7% (92 d) | -4% (69 d) | +3% (100 d) | +9% (4 d) | +2% (221 d) | +3% (399 d) | +1% (615 d) | +0% (77 d) | -8% (90 d) | +1% (142 d) |
| koop-bij-nieuwe-top | +2% (92 d) | -4% (69 d) | -1% (100 d) | +30% (4 d) | +6% (224 d) | +3% (399 d) | -0% (615 d) | -2% (79 d) | -8% (90 d) | -0% (142 d) |
| verkoop-na-2-rode-trendkaarsen | +2% (87 d) | -5% (69 d) | -2% (96 d) | +27% (4 d) | +4% (219 d) | -0% (395 d) | -4% (592 d) | -4% (73 d) | -16% (90 d) | -1% (135 d) |
| 4-plekken | +6% (92 d) | -1% (69 d) | -1% (100 d) | +21% (4 d) | +6% (226 d) | +2% (399 d) | +1% (615 d) | +0% (74 d) | -4% (93 d) | +0% (142 d) |
| zonder-sectorgrens | +7% (92 d) | -1% (69 d) | +2% (100 d) | +27% (4 d) | +5% (222 d) | +3% (399 d) | +2% (612 d) | +2% (74 d) | -1% (93 d) | -1% (142 d) |

## Trend-agent: lessen uit 5 jaar backtest (productie)

314 afgesloten trades, 32% winst, gemiddeld +0.14 R per trade (mediaan -0.47 R), totaal €849, gemiddeld 26 dagen vastgehouden.

### Bevindingen

- Zwakte: Volume t.o.v. normaal = normaal: gemiddeld -0.10 R over 139 trades (-0.42 R t.o.v. de rest, t = -2.1).

_Dit zijn hypotheses. Een regel verandert pas na een test op ongeziene data (zie het onderzoeksrapport)._

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend | 207 | 35% | +0.17 | 790 |
| zijwaarts | 61 | 26% | +0.09 | 84 |
| dalend | 41 | 29% | +0.08 | 7 |
| onbekend (te weinig) | 5 | 40% | -0.18 | -32 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 156 | 33% | +0.15 | 487 |
| laag | 77 | 30% | +0.11 | 121 |
| hoog | 76 | 34% | +0.17 | 272 |
| onbekend (te weinig) | 5 | 40% | -0.18 | -32 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 50-60 | 116 | 34% | +0.30 | 786 |
| 60-70 | 92 | 28% | -0.03 | -124 |
| 70-80 | 65 | 40% | +0.25 | 292 |
| onder 50 | 24 | 29% | -0.09 | -37 |
| 80 of hoger (te weinig) | 17 | 24% | -0.15 | -68 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| positief | 176 | 31% | +0.16 | 533 |
| negatief | 138 | 34% | +0.11 | 316 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 139 | 25% | -0.10 | -296 |
| hoger (>1,1) | 110 | 38% | +0.24 | 545 |
| lager (<0,9) | 65 | 38% | +0.48 | 600 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% | 153 | 34% | +0.04 | 104 |
| meer dan 25% | 105 | 30% | +0.16 | 349 |
| tot 10% | 56 | 32% | +0.37 | 396 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 173 | 35% | +0.10 | 261 |
| wild (>3%) | 98 | 29% | +0.23 | 514 |
| rustig (<1,5%) | 43 | 33% | +0.08 | 74 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt | 267 | 37% | +0.24 | 1,321 |
| trend gebroken (slot onder 50-daags gemiddelde) | 47 | 4% | -0.46 | -472 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| middel | 112 | 13% | -0.50 | -1,270 |
| kort (<10 d) | 101 | 0% | -0.92 | -2,156 |
| lang (>30 d) | 101 | 86% | +1.91 | 4,275 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-743b8c | 314 | 32% | +0.14 | 849 |

## Trend-agent: lessen uit het oefenen (nepgeld, live)

Live van 2026-10-13 t/m 2026-10-28 (12 handelsdagen): bot +0.52%, wereld-ETF -0.44%, verschil +0.96%.

Nog geen afgesloten trades om van te leren.

## Investeerder

Periode 2021-10-29 t/m 2026-10-29. Ontwikkeldeel 2021-10-29 t/m 2025-04-29, holdout 2025-04-30 t/m 2026-10-29. 2 varianten getest tegen productie.

### Uitkomst

- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.71 vs productie 1.75 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.82 vs 0.88
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -20.2% vs -21.6%
    - ✗ Dubbele kosten en slippage: Sharpe 1.06 vs 1.11
- **satelliet-3-aandelen: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 1.87 vs productie 1.75 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.70 vs 0.88
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -24.4% vs -21.6%
    - ✗ Dubbele kosten en slippage: Sharpe 1.04 vs 1.11

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +149.4% | +20.1% | -21.6% | 1.15 | 1.75 | 1.11 | 145 | 64% | 1.42 |
| regimefilter | +130.1% | +18.1% | -20.2% | 1.10 | 1.71 | 1.06 | 151 | 62% | 1.36 |
| satelliet-3-aandelen | +146.3% | +19.8% | -24.4% | 1.07 | 1.87 | 1.04 | 122 | 65% | 1.32 |

### Per periode (rendement)

| Variant | Oct 2021–Oct 2022 | Oct 2022–Oct 2023 | Oct 2023–Oct 2024 | Oct 2024–Oct 2025 | Oct 2025–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | -10.6% | +7.9% | +56.3% | +29.2% | +28.1% |
| regimefilter | -10.0% | +1.1% | +56.2% | +26.5% | +28.1% |
| satelliet-3-aandelen | -15.0% | +7.7% | +47.2% | +35.7% | +35.1% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (productie, productie, productie, productie), was het resultaat over de laatste 4 periodes +179.1%, tegen +179.1% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +66% (66 d) | +14% (51 d) | +30% (74 d) | +134% (2 d) | +37% (162 d) | +26% (283 d) | +3% (443 d) | +36% (56 d) | -22% (67 d) | +21% (100 d) |
| regimefilter | +61% (66 d) | +10% (51 d) | +28% (74 d) | +134% (2 d) | +37% (162 d) | +26% (283 d) | +3% (443 d) | +30% (56 d) | -27% (67 d) | +15% (100 d) |
| satelliet-3-aandelen | +57% (66 d) | +17% (51 d) | +33% (74 d) | +169% (2 d) | +32% (162 d) | +26% (283 d) | +5% (443 d) | +47% (56 d) | -25% (67 d) | +16% (100 d) |

## Investeerder live (nepgeld)

Van 2026-10-13 t/m 2026-10-28: investeerder -1.70%, wereld-ETF -0.44%, verschil -1.26%.
