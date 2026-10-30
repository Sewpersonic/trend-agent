# Onderzoeksrapport 2026-10-30

Dit rapport test varianten van beide strategieën op echte koersen en kijkt wat de bots leren van hun eigen trades. **Er wordt niets automatisch aangepast.** Een aanbevolen variant gaat pas in productie als jij (of iemand die je vertrouwt) de instelling in de code aanpast; daarna draait de backtest opnieuw en loopt de nieuwe versie eerst weken mee op papier.

> Resultaten uit het verleden zijn geen garantie. De aandelenlijst is in 2026 gekozen (survivorship bias).

## Trend-agent

Periode 2016-10-30 t/m 2026-10-30. Ontwikkeldeel 2016-10-30 t/m 2023-10-29, holdout 2023-10-30 t/m 2026-10-30. 9 varianten getest tegen productie.

### Uitkomst

- **rem-pas-na-5-verliezen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.36 vs productie 0.35 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.37 vs 0.20
    - ✓ Consistent over periodes: beter in 5 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -8.6% vs -10.4%
    - ✓ Dubbele kosten en slippage: Sharpe -0.09 vs -0.10
    - ✓ Genoeg trades: 632 afgesloten trades (nodig: 30)
- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.21 vs productie 0.35 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.15 vs 0.20
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -10.7% vs -10.4%
    - ✗ Dubbele kosten en slippage: Sharpe -0.18 vs -0.10
    - ✓ Genoeg trades: 516 afgesloten trades (nodig: 30)
- **koop-na-terugval: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.79 vs productie 0.35 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.32 vs 0.20
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -9.0% vs -10.4%
    - ✓ Dubbele kosten en slippage: Sharpe 0.08 vs -0.10
    - ✓ Genoeg trades: 637 afgesloten trades (nodig: 30)
- **koop-bij-nieuwe-top: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.43 vs productie 0.35 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.50 vs 0.20
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -6.4% vs -10.4%
    - ✓ Dubbele kosten en slippage: Sharpe 0.21 vs -0.10
    - ✓ Genoeg trades: 546 afgesloten trades (nodig: 30)
- **verkoop-na-2-rode-trendkaarsen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe -0.64 vs productie 0.35 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.24 vs 0.20
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -23.5% vs -10.4%
    - ✗ Dubbele kosten en slippage: Sharpe -2.31 vs -0.10
    - ✓ Genoeg trades: 1912 afgesloten trades (nodig: 30)
- **4-plekken: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe -0.13 vs productie 0.35 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.13 vs 0.20
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -8.9% vs -10.4%
    - ✗ Dubbele kosten en slippage: Sharpe -0.21 vs -0.10
    - ✓ Genoeg trades: 510 afgesloten trades (nodig: 30)
- **meer-per-aankoop: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.32 vs productie 0.35 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.29 vs 0.20
    - ✓ Consistent over periodes: beter in 4 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -16.6% vs -10.4%
    - ✓ Dubbele kosten en slippage: Sharpe 0.18 vs -0.10
    - ✓ Genoeg trades: 616 afgesloten trades (nodig: 30)
- **veel-meer-per-aankoop: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.16 vs productie 0.35 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.17 vs 0.20
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -31.5% vs -10.4%
    - ✓ Dubbele kosten en slippage: Sharpe 0.17 vs -0.10
    - ✓ Genoeg trades: 601 afgesloten trades (nodig: 30)
- **8-plekken-meer-per-aankoop: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.63 vs productie 0.35 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.53 vs 0.20
    - ✓ Consistent over periodes: beter in 5 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -17.5% vs -10.4%
    - ✓ Dubbele kosten en slippage: Sharpe 0.29 vs -0.10
    - ✓ Genoeg trades: 928 afgesloten trades (nodig: 30)

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +13.1% | +1.2% | -10.4% | 0.25 | 0.35 | -0.10 | 620 | 35% | 2.06 |
| rem-pas-na-5-verliezen | +21.9% | +2.0% | -8.6% | 0.37 | 0.36 | -0.09 | 632 | 35% | 2.25 |
| regimefilter | +7.7% | +0.7% | -10.7% | 0.17 | 0.21 | -0.18 | 516 | 33% | 2.12 |
| koop-na-terugval | +27.1% | +2.4% | -9.0% | 0.47 | 0.79 | 0.08 | 637 | 37% | 2.18 |
| koop-bij-nieuwe-top | +28.7% | +2.6% | -6.4% | 0.49 | 0.43 | 0.21 | 546 | 39% | 2.05 |
| verkoop-na-2-rode-trendkaarsen | -17.4% | -1.9% | -23.5% | -0.36 | -0.64 | -2.31 | 1912 | 34% | 1.64 |
| 4-plekken | +1.9% | +0.2% | -8.9% | 0.06 | -0.13 | -0.21 | 510 | 33% | 2.04 |
| meer-per-aankoop | +33.7% | +2.9% | -16.6% | 0.31 | 0.32 | 0.18 | 616 | 37% | 1.97 |
| veel-meer-per-aankoop | +21.0% | +1.9% | -31.5% | 0.17 | 0.16 | 0.17 | 601 | 36% | 1.81 |
| 8-plekken-meer-per-aankoop | +109.7% | +7.7% | -17.5% | 0.56 | 0.63 | 0.29 | 928 | 36% | 2.32 |

### Per periode (rendement)

| Variant | Oct 2016–Oct 2018 | Nov 2018–Oct 2020 | Oct 2020–Oct 2022 | Oct 2022–Oct 2024 | Oct 2024–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +1.3% | +2.5% | -0.8% | +8.0% | +1.8% |
| rem-pas-na-5-verliezen | +3.9% | +4.2% | +1.1% | +8.7% | +2.4% |
| regimefilter | +1.8% | +2.3% | +0.4% | +2.6% | +0.4% |
| koop-na-terugval | +1.2% | +11.7% | -0.8% | +5.0% | +8.1% |
| koop-bij-nieuwe-top | +11.5% | +0.9% | +4.9% | +8.0% | +1.0% |
| verkoop-na-2-rode-trendkaarsen | -3.5% | +1.1% | +0.5% | -10.2% | -6.1% |
| 4-plekken | +2.0% | +0.4% | -4.0% | +6.8% | -2.8% |
| meer-per-aankoop | +9.4% | +10.3% | -0.4% | +7.6% | +3.5% |
| veel-meer-per-aankoop | +9.1% | +23.0% | -7.4% | -6.0% | +3.7% |
| 8-plekken-meer-per-aankoop | +14.5% | +13.7% | +13.6% | +24.8% | +14.3% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (koop-bij-nieuwe-top, koop-na-terugval, 8-plekken-meer-per-aankoop, 8-plekken-meer-per-aankoop), was het resultaat over de laatste 4 periodes +42.7%, tegen +11.8% voor gewoon productie houden. Bijsturen hielp hier, maar met zo weinig periodes kan dat toeval zijn.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | -2% (204 d) | +5% (69 d) | +3% (163 d) | -98% (3 d) | +2% (342 d) | +1% (886 d) | +1% (1410 d) | -5% (164 d) | -0% (126 d) | +4% (274 d) |
| rem-pas-na-5-verliezen | -2% (204 d) | +7% (69 d) | +3% (163 d) | -101% (3 d) | +2% (342 d) | +1% (886 d) | +2% (1407 d) | -1% (160 d) | +1% (126 d) | +4% (274 d) |
| regimefilter | -1% (204 d) | +0% (68 d) | -1% (157 d) | -98% (3 d) | -1% (331 d) | +0% (886 d) | +1% (1410 d) | -3% (164 d) | +0% (126 d) | +5% (269 d) |
| koop-na-terugval | -1% (204 d) | -1% (68 d) | +2% (159 d) | -83% (3 d) | +2% (338 d) | -0% (883 d) | +3% (1396 d) | +4% (160 d) | -2% (126 d) | +4% (274 d) |
| koop-bij-nieuwe-top | -1% (204 d) | +2% (69 d) | +4% (163 d) | -73% (3 d) | +8% (338 d) | +2% (886 d) | +2% (1399 d) | -1% (154 d) | -3% (126 d) | +1% (268 d) |
| verkoop-na-2-rode-trendkaarsen | -4% (194 d) | -6% (67 d) | -2% (151 d) | -101% (3 d) | +2% (332 d) | -2% (853 d) | -1% (1354 d) | -2% (150 d) | -2% (118 d) | +2% (257 d) |
| 4-plekken | -3% (204 d) | +4% (69 d) | +2% (163 d) | -77% (3 d) | +1% (342 d) | -0% (886 d) | +0% (1410 d) | -3% (164 d) | +1% (126 d) | +3% (269 d) |
| meer-per-aankoop | -3% (204 d) | +1% (69 d) | +8% (163 d) | -189% (3 d) | +7% (341 d) | +2% (883 d) | +4% (1407 d) | -8% (154 d) | -4% (126 d) | +4% (274 d) |
| veel-meer-per-aankoop | -6% (204 d) | +7% (68 d) | +9% (159 d) | -325% (3 d) | -0% (336 d) | -1% (882 d) | +4% (1403 d) | -7% (150 d) | -5% (126 d) | +19% (274 d) |
| 8-plekken-meer-per-aankoop | -7% (204 d) | +13% (69 d) | +18% (163 d) | -282% (3 d) | +8% (342 d) | +5% (886 d) | +6% (1404 d) | +2% (159 d) | +0% (126 d) | +11% (274 d) |

## Trend-agent: lessen uit 10 jaar backtest (productie)

620 afgesloten trades, 35% winst, gemiddeld +0.06 R per trade (mediaan -0.43 R), totaal €1,014, gemiddeld 27 dagen vastgehouden.

### Bevindingen

- Zwakte: MACD-histogram bij instap = positief: gemiddeld -0.07 R over 341 trades (-0.28 R t.o.v. de rest, t = -2.1).
- Sterkte: MACD-histogram bij instap = negatief: gemiddeld +0.22 R over 279 trades (+0.28 R t.o.v. de rest, t = 2.1).

_Dit zijn hypotheses. Een regel verandert pas na een test op ongeziene data (zie het onderzoeksrapport)._

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend | 417 | 34% | +0.03 | 353 |
| zijwaarts | 111 | 36% | +0.12 | 379 |
| dalend | 87 | 41% | +0.20 | 415 |
| onbekend (te weinig) | 5 | 0% | -1.03 | -133 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 315 | 36% | +0.12 | 930 |
| hoog | 158 | 35% | -0.04 | -102 |
| laag | 142 | 36% | +0.09 | 319 |
| onbekend (te weinig) | 5 | 0% | -1.03 | -133 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 60-70 | 261 | 35% | +0.09 | 633 |
| 70-80 | 178 | 35% | -0.04 | -198 |
| 50-60 | 147 | 37% | +0.13 | 497 |
| onder 50 | 34 | 29% | +0.07 | 81 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| positief | 341 | 34% | -0.07 | -607 |
| negatief | 279 | 37% | +0.22 | 1,621 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| hoger (>1,1) | 295 | 38% | +0.12 | 932 |
| normaal | 226 | 31% | -0.08 | -483 |
| lager (<0,9) | 99 | 36% | +0.21 | 565 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% | 316 | 35% | +0.04 | 256 |
| meer dan 25% | 221 | 37% | +0.12 | 799 |
| tot 10% | 83 | 33% | -0.03 | -41 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 346 | 36% | +0.02 | 81 |
| wild (>3%) | 157 | 32% | +0.14 | 699 |
| rustig (<1,5%) | 117 | 36% | +0.08 | 234 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt | 563 | 37% | +0.09 | 1,333 |
| trend gebroken (slot onder 50-daags gemiddelde) | 57 | 16% | -0.24 | -319 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| lang (>30 d) | 227 | 76% | +1.33 | 7,613 |
| middel | 219 | 21% | -0.42 | -2,295 |
| kort (<10 d) | 174 | 1% | -0.99 | -4,304 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-a0ddd5 | 620 | 35% | +0.06 | 1,014 |

## Trend-agent: lessen uit het oefenen (nepgeld, live)

Live van 2026-10-13 t/m 2026-10-29 (13 handelsdagen): bot +0.53%, wereld-ETF -0.53%, verschil +1.06%.

Nog geen afgesloten trades om van te leren.

## Investeerder

Periode 2016-10-31 t/m 2026-10-30. Ontwikkeldeel 2016-10-31 t/m 2023-10-30, holdout 2023-10-31 t/m 2026-10-30. 2 varianten getest tegen productie.

### Uitkomst

- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.76 vs productie 1.82 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.95 vs 1.11
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -36.7% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.18 vs 1.31
- **satelliet-3-aandelen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.78 vs productie 1.82 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 1.12 vs 1.11
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -38.1% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.31 vs 1.31

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +902.5% | +25.9% | -36.7% | 1.33 | 1.82 | 1.31 | 287 | 73% | 1.63 |
| regimefilter | +629.6% | +22.0% | -36.7% | 1.20 | 1.76 | 1.18 | 283 | 71% | 1.50 |
| satelliet-3-aandelen | +1066.9% | +27.9% | -38.1% | 1.32 | 1.78 | 1.31 | 243 | 75% | 1.40 |

### Per periode (rendement)

| Variant | Oct 2016–Oct 2018 | Oct 2018–Oct 2020 | Oct 2020–Oct 2022 | Nov 2022–Oct 2024 | Oct 2024–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +50.0% | +46.4% | +61.0% | +56.6% | +81.4% |
| regimefilter | +50.0% | +12.3% | +62.8% | +53.6% | +73.5% |
| satelliet-3-aandelen | +61.2% | +46.4% | +58.7% | +59.0% | +96.0% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (satelliet-3-aandelen, satelliet-3-aandelen, productie, productie), was het resultaat over de laatste 4 periodes +559.9%, tegen +569.6% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +59% (147 d) | +18% (51 d) | +65% (117 d) | -294% (2 d) | +19% (251 d) | +23% (626 d) | +22% (1013 d) | -2% (118 d) | -5% (90 d) | +30% (194 d) |
| regimefilter | +43% (147 d) | +11% (51 d) | +41% (117 d) | -294% (2 d) | +19% (251 d) | +23% (626 d) | +22% (1013 d) | -4% (118 d) | -6% (90 d) | +14% (194 d) |
| satelliet-3-aandelen | +60% (147 d) | +20% (51 d) | +69% (117 d) | -323% (2 d) | +27% (251 d) | +24% (626 d) | +21% (1013 d) | +6% (118 d) | +0% (90 d) | +32% (194 d) |

## Investeerder live (nepgeld)

Van 2026-10-13 t/m 2026-10-29: investeerder -2.17%, wereld-ETF -0.53%, verschil -1.65%.
