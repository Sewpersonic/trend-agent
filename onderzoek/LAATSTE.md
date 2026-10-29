# Onderzoeksrapport 2026-10-29

Dit rapport test varianten van beide strategieën op echte koersen en kijkt wat de bots leren van hun eigen trades. **Er wordt niets automatisch aangepast.** Een aanbevolen variant gaat pas in productie als jij (of iemand die je vertrouwt) de instelling in de code aanpast; daarna draait de backtest opnieuw en loopt de nieuwe versie eerst weken mee op papier.

> Resultaten uit het verleden zijn geen garantie. De aandelenlijst is in 2026 gekozen (survivorship bias).

## Trend-agent

Periode 2016-10-29 t/m 2026-10-29. Ontwikkeldeel 2016-10-29 t/m 2023-10-28, holdout 2023-10-29 t/m 2026-10-29. 6 varianten getest tegen productie.

### Uitkomst

- **rem-pas-na-5-verliezen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.35 vs productie 0.41 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.37 vs 0.20
    - ✓ Consistent over periodes: beter in 4 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -8.6% vs -10.4%
    - ✗ Dubbele kosten en slippage: Sharpe -0.09 vs -0.08
    - ✓ Genoeg trades: 633 afgesloten trades (nodig: 30)
- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.23 vs productie 0.41 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.15 vs 0.20
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -10.7% vs -10.4%
    - ✗ Dubbele kosten en slippage: Sharpe -0.17 vs -0.08
    - ✓ Genoeg trades: 516 afgesloten trades (nodig: 30)
- **koop-na-terugval: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.67 vs productie 0.41 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.32 vs 0.20
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -9.0% vs -10.4%
    - ✓ Dubbele kosten en slippage: Sharpe 0.05 vs -0.08
    - ✓ Genoeg trades: 643 afgesloten trades (nodig: 30)
- **koop-bij-nieuwe-top: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.46 vs productie 0.41 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.50 vs 0.20
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -6.4% vs -10.4%
    - ✓ Dubbele kosten en slippage: Sharpe 0.21 vs -0.08
    - ✓ Genoeg trades: 546 afgesloten trades (nodig: 30)
- **verkoop-na-2-rode-trendkaarsen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe -0.64 vs productie 0.41 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.24 vs 0.20
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -23.5% vs -10.4%
    - ✗ Dubbele kosten en slippage: Sharpe -2.31 vs -0.08
    - ✓ Genoeg trades: 1913 afgesloten trades (nodig: 30)
- **4-plekken: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe -0.10 vs productie 0.41 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.13 vs 0.20
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -8.9% vs -10.4%
    - ✗ Dubbele kosten en slippage: Sharpe -0.21 vs -0.08
    - ✓ Genoeg trades: 514 afgesloten trades (nodig: 30)

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +14.1% | +1.3% | -10.4% | 0.26 | 0.41 | -0.08 | 619 | 35% | 2.07 |
| rem-pas-na-5-verliezen | +21.5% | +2.0% | -8.6% | 0.37 | 0.35 | -0.09 | 633 | 35% | 2.26 |
| regimefilter | +8.0% | +0.8% | -10.7% | 0.17 | 0.23 | -0.17 | 516 | 33% | 2.12 |
| koop-na-terugval | +24.5% | +2.2% | -9.0% | 0.43 | 0.67 | 0.05 | 643 | 37% | 2.16 |
| koop-bij-nieuwe-top | +29.0% | +2.6% | -6.4% | 0.49 | 0.46 | 0.21 | 546 | 39% | 2.05 |
| verkoop-na-2-rode-trendkaarsen | -17.3% | -1.9% | -23.5% | -0.36 | -0.64 | -2.31 | 1913 | 34% | 1.64 |
| 4-plekken | +2.2% | +0.2% | -8.9% | 0.06 | -0.10 | -0.21 | 514 | 33% | 2.07 |

### Per periode (rendement)

| Variant | Oct 2016–Oct 2018 | Oct 2018–Oct 2020 | Oct 2020–Oct 2022 | Oct 2022–Oct 2024 | Oct 2024–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +1.3% | +2.6% | -0.8% | +8.0% | +2.4% |
| rem-pas-na-5-verliezen | +3.9% | +4.3% | +1.1% | +8.7% | +1.8% |
| regimefilter | +1.8% | +2.3% | +0.4% | +2.6% | +0.4% |
| koop-na-terugval | +1.1% | +11.6% | -0.8% | +5.0% | +5.8% |
| koop-bij-nieuwe-top | +11.6% | +0.8% | +4.9% | +8.0% | +0.9% |
| verkoop-na-2-rode-trendkaarsen | -3.3% | +1.0% | +0.5% | -10.2% | -6.3% |
| 4-plekken | +2.1% | +0.2% | -4.0% | +6.8% | -2.7% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (koop-bij-nieuwe-top, koop-na-terugval, koop-bij-nieuwe-top, koop-bij-nieuwe-top), was het resultaat over de laatste 4 periodes +8.8%, tegen +12.4% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | -2% (204 d) | +4% (69 d) | +3% (163 d) | -73% (4 d) | +2% (342 d) | +1% (885 d) | +1% (1410 d) | -5% (164 d) | -0% (126 d) | +4% (274 d) |
| rem-pas-na-5-verliezen | -2% (204 d) | +6% (69 d) | +3% (163 d) | -76% (4 d) | +2% (342 d) | +1% (885 d) | +2% (1407 d) | -1% (160 d) | +1% (126 d) | +4% (274 d) |
| regimefilter | -1% (204 d) | +0% (68 d) | -1% (157 d) | -73% (4 d) | -1% (331 d) | +0% (885 d) | +1% (1410 d) | -3% (164 d) | +0% (126 d) | +5% (269 d) |
| koop-na-terugval | -1% (204 d) | -1% (68 d) | +2% (159 d) | -62% (4 d) | +2% (338 d) | -1% (882 d) | +3% (1396 d) | +3% (160 d) | -2% (126 d) | +4% (274 d) |
| koop-bij-nieuwe-top | -1% (204 d) | +2% (69 d) | +4% (163 d) | -55% (4 d) | +8% (338 d) | +2% (885 d) | +2% (1399 d) | -1% (154 d) | -3% (126 d) | +1% (268 d) |
| verkoop-na-2-rode-trendkaarsen | -4% (194 d) | -6% (67 d) | -2% (151 d) | -76% (4 d) | +2% (332 d) | -2% (852 d) | -1% (1354 d) | -2% (150 d) | -2% (118 d) | +2% (257 d) |
| 4-plekken | -3% (204 d) | +3% (69 d) | +2% (163 d) | -58% (4 d) | +1% (342 d) | +0% (885 d) | +0% (1410 d) | -3% (164 d) | +0% (126 d) | +3% (269 d) |

## Trend-agent: lessen uit 5 jaar backtest (productie)

619 afgesloten trades, 35% winst, gemiddeld +0.06 R per trade (mediaan -0.43 R), totaal €1,031, gemiddeld 27 dagen vastgehouden.

### Bevindingen

- Zwakte: MACD-histogram bij instap = positief: gemiddeld -0.07 R over 347 trades (-0.31 R t.o.v. de rest, t = -2.3).
- Sterkte: MACD-histogram bij instap = negatief: gemiddeld +0.24 R over 272 trades (+0.31 R t.o.v. de rest, t = 2.3).

_Dit zijn hypotheses. Een regel verandert pas na een test op ongeziene data (zie het onderzoeksrapport)._

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend | 414 | 34% | +0.04 | 402 |
| zijwaarts | 112 | 37% | +0.12 | 399 |
| dalend | 88 | 40% | +0.17 | 364 |
| onbekend (te weinig) | 5 | 0% | -1.03 | -133 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 316 | 36% | +0.12 | 971 |
| hoog | 158 | 35% | -0.04 | -102 |
| laag | 140 | 35% | +0.09 | 295 |
| onbekend (te weinig) | 5 | 0% | -1.03 | -133 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 60-70 | 260 | 35% | +0.10 | 695 |
| 70-80 | 181 | 35% | -0.05 | -261 |
| 50-60 | 145 | 37% | +0.14 | 536 |
| onder 50 | 33 | 27% | +0.05 | 60 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| positief | 347 | 33% | -0.07 | -707 |
| negatief | 272 | 38% | +0.24 | 1,738 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| hoger (>1,1) | 295 | 38% | +0.12 | 937 |
| normaal | 224 | 32% | -0.06 | -405 |
| lager (<0,9) | 100 | 35% | +0.18 | 499 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% | 316 | 35% | +0.05 | 308 |
| meer dan 25% | 221 | 36% | +0.11 | 750 |
| tot 10% | 82 | 33% | -0.02 | -27 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 348 | 36% | +0.02 | 68 |
| wild (>3%) | 155 | 32% | +0.14 | 696 |
| rustig (<1,5%) | 116 | 36% | +0.10 | 267 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt | 562 | 37% | +0.09 | 1,349 |
| trend gebroken (slot onder 50-daags gemiddelde) | 57 | 16% | -0.24 | -318 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| lang (>30 d) | 227 | 76% | +1.33 | 7,596 |
| middel | 218 | 21% | -0.41 | -2,264 |
| kort (<10 d) | 174 | 1% | -0.99 | -4,301 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-a0ddd5 | 619 | 35% | +0.06 | 1,031 |

## Trend-agent: lessen uit het oefenen (nepgeld, live)

Live van 2026-10-13 t/m 2026-10-28 (12 handelsdagen): bot +0.52%, wereld-ETF -0.44%, verschil +0.96%.

Nog geen afgesloten trades om van te leren.

## Investeerder

Periode 2016-10-31 t/m 2026-10-29. Ontwikkeldeel 2016-10-31 t/m 2023-10-30, holdout 2023-10-31 t/m 2026-10-29. 2 varianten getest tegen productie.

### Uitkomst

- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.76 vs productie 1.83 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.95 vs 1.11
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -36.7% vs -36.8%
    - ✗ Dubbele kosten en slippage: Sharpe 1.18 vs 1.31
- **satelliet-3-aandelen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.79 vs productie 1.83 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 1.13 vs 1.11
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -38.1% vs -36.8%
    - ✓ Dubbele kosten en slippage: Sharpe 1.31 vs 1.31

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +900.8% | +25.9% | -36.8% | 1.33 | 1.83 | 1.31 | 286 | 73% | 1.64 |
| regimefilter | +627.7% | +22.0% | -36.7% | 1.20 | 1.76 | 1.18 | 282 | 71% | 1.47 |
| satelliet-3-aandelen | +1078.2% | +28.0% | -38.1% | 1.33 | 1.79 | 1.31 | 244 | 75% | 1.39 |

### Per periode (rendement)

| Variant | Oct 2016–Oct 2018 | Oct 2018–Oct 2020 | Oct 2020–Oct 2022 | Oct 2022–Oct 2024 | Oct 2024–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +50.0% | +53.3% | +58.0% | +59.8% | +71.6% |
| regimefilter | +50.0% | +17.7% | +59.8% | +56.4% | +64.2% |
| satelliet-3-aandelen | +61.5% | +53.1% | +56.3% | +64.1% | +85.5% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (satelliet-3-aandelen, satelliet-3-aandelen, productie, productie), was het resultaat over de laatste 4 periodes +556.5%, tegen +564.0% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +59% (147 d) | +18% (51 d) | +65% (117 d) | -294% (2 d) | +19% (251 d) | +23% (625 d) | +22% (1013 d) | -2% (118 d) | -5% (90 d) | +30% (194 d) |
| regimefilter | +43% (147 d) | +11% (51 d) | +41% (117 d) | -294% (2 d) | +19% (251 d) | +23% (625 d) | +22% (1013 d) | -4% (118 d) | -6% (90 d) | +14% (194 d) |
| satelliet-3-aandelen | +60% (147 d) | +20% (51 d) | +69% (117 d) | -323% (2 d) | +27% (251 d) | +24% (625 d) | +21% (1013 d) | +6% (118 d) | +0% (90 d) | +32% (194 d) |

## Investeerder live (nepgeld)

Van 2026-10-13 t/m 2026-10-28: investeerder -1.70%, wereld-ETF -0.44%, verschil -1.26%.
