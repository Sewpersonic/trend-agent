# Onderzoeksrapport 2026-10-11

Dit rapport test varianten van beide strategieën op echte koersen en kijkt wat de bots leren van hun eigen trades. **Er wordt niets automatisch aangepast.** Een aanbevolen variant gaat pas in productie als jij (of iemand die je vertrouwt) de instelling in de code aanpast; daarna draait de backtest opnieuw en loopt de nieuwe versie eerst weken mee op papier.

> Resultaten uit het verleden zijn geen garantie. De aandelenlijst is in 2026 gekozen (survivorship bias).

## Trend-agent

Periode 2021-10-11 t/m 2026-10-11. Ontwikkeldeel 2021-10-11 t/m 2025-04-13, holdout 2025-04-14 t/m 2026-10-11. 3 varianten getest tegen productie.

### Uitkomst

- **rem-pas-na-5-verliezen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.29 vs productie 0.55 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.23 vs 0.23
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.2% vs -5.0%
    - ✗ Dubbele kosten en slippage: Sharpe 0.02 vs 0.04
    - ✓ Genoeg trades: 200 afgesloten trades (nodig: 30)
- **regimefilter: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.76 vs productie 0.55 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.08 vs 0.23
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -6.1% vs -5.0%
    - ✗ Dubbele kosten en slippage: Sharpe -0.19 vs 0.04
    - ✓ Genoeg trades: 167 afgesloten trades (nodig: 30)
- **niet-kopen-boven-rsi-75: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.52 vs productie 0.55 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.00 vs 0.23
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -6.0% vs -5.0%
    - ✗ Dubbele kosten en slippage: Sharpe -0.08 vs 0.04
    - ✓ Genoeg trades: 195 afgesloten trades (nodig: 30)

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +6.2% | +1.2% | -5.0% | 0.32 | 0.55 | 0.04 | 196 | 35% | 2.32 |
| rem-pas-na-5-verliezen | +4.7% | +0.9% | -5.2% | 0.24 | 0.29 | 0.02 | 200 | 34% | 2.24 |
| regimefilter | +3.3% | +0.7% | -6.1% | 0.18 | 0.76 | -0.19 | 167 | 29% | 2.68 |
| niet-kopen-boven-rsi-75 | +2.9% | +0.6% | -6.0% | 0.16 | 0.52 | -0.08 | 195 | 33% | 2.18 |

### Per periode (rendement)

| Variant | Oct 2021–Oct 2022 | Oct 2022–Oct 2023 | Oct 2023–Oct 2024 | Oct 2024–Oct 2025 | Oct 2025–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | -2.3% | +1.8% | -0.2% | +4.5% | +1.8% |
| rem-pas-na-5-verliezen | -2.4% | +3.4% | -0.1% | +1.5% | +1.5% |
| regimefilter | -3.3% | +1.1% | -2.5% | +4.6% | +3.2% |
| niet-kopen-boven-rsi-75 | -3.4% | -0.7% | +0.5% | +1.7% | +4.3% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (productie, rem-pas-na-5-verliezen, rem-pas-na-5-verliezen, productie), was het resultaat over de laatste 4 periodes +5.2%, tegen +8.0% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +5% (92 d) | -0% (69 d) | -2% (100 d) | -29% (2 d) | +2% (240 d) | +1% (381 d) | +2% (619 d) | -2% (78 d) | -2% (93 d) | -0% (142 d) |
| rem-pas-na-5-verliezen | +6% (92 d) | -1% (69 d) | -1% (100 d) | -29% (2 d) | +2% (240 d) | +1% (381 d) | +1% (615 d) | -3% (73 d) | -0% (93 d) | -1% (142 d) |
| regimefilter | +0% (92 d) | +1% (69 d) | -1% (98 d) | -29% (2 d) | +1% (235 d) | +1% (381 d) | +2% (615 d) | -3% (78 d) | -3% (93 d) | +1% (139 d) |
| niet-kopen-boven-rsi-75 | +6% (92 d) | -1% (69 d) | -2% (100 d) | -55% (2 d) | +2% (237 d) | -1% (379 d) | +3% (617 d) | -4% (76 d) | -5% (93 d) | -1% (142 d) |

## Trend-agent: lessen uit 5 jaar backtest (productie)

196 afgesloten trades, 35% winst, gemiddeld +0.12 R per trade (mediaan -0.42 R), totaal €542, gemiddeld 26 dagen vastgehouden.

### Bevindingen

- Zwakte: RSI bij instap = 60-70: gemiddeld -0.22 R over 54 trades (-0.47 R t.o.v. de rest, t = -2.2). Te testen via instelling `max_rsi_entry`.
- Sterkte: Marktbeweeglijkheid bij instap = normaal: gemiddeld +0.38 R over 94 trades (+0.51 R t.o.v. de rest, t = 2.1). Te testen via instelling `regime_filter`.

_Dit zijn hypotheses. Een regel verandert pas na een test op ongeziene data (zie het onderzoeksrapport)._

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend | 135 | 34% | +0.14 | 469 |
| zijwaarts | 33 | 39% | +0.07 | 57 |
| dalend | 25 | 36% | +0.14 | 50 |
| onbekend (te weinig) | 3 | 0% | -0.46 | -35 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 94 | 37% | +0.38 | 871 |
| laag | 51 | 31% | -0.07 | -117 |
| hoog | 48 | 35% | -0.17 | -176 |
| onbekend (te weinig) | 3 | 0% | -0.46 | -35 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 50-60 | 61 | 36% | +0.20 | 266 |
| 70-80 | 56 | 45% | +0.51 | 690 |
| 60-70 | 54 | 28% | -0.22 | -277 |
| 80 of hoger (te weinig) | 14 | 21% | -0.15 | -45 |
| onder 50 (te weinig) | 11 | 27% | -0.33 | -92 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| positief | 118 | 34% | +0.17 | 460 |
| negatief | 78 | 36% | +0.04 | 82 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| hoger (>1,1) | 81 | 35% | +0.03 | 81 |
| normaal | 76 | 38% | +0.30 | 526 |
| lager (<0,9) | 39 | 28% | -0.06 | -65 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% | 93 | 30% | -0.10 | -258 |
| meer dan 25% | 83 | 36% | +0.31 | 628 |
| tot 10% | 20 | 50% | +0.35 | 173 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 110 | 32% | -0.02 | -125 |
| wild (>3%) | 58 | 41% | +0.45 | 689 |
| rustig (<1,5%) | 28 | 32% | -0.02 | -22 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt | 177 | 37% | +0.17 | 687 |
| trend gebroken (slot onder 50-daags gemiddelde) (te weinig) | 19 | 11% | -0.33 | -145 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| middel | 75 | 13% | -0.51 | -879 |
| lang (>30 d) | 66 | 86% | +1.73 | 2,671 |
| kort (<10 d) | 55 | 2% | -0.96 | -1,250 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-d373c7 | 196 | 35% | +0.12 | 542 |

## Trend-agent: lessen uit het oefenen (nepgeld, live)

Nog geen afgesloten trades om van te leren.

## Investeerder

Periode 2021-10-11 t/m 2026-10-09. Ontwikkeldeel 2021-10-11 t/m 2025-04-09, holdout 2025-04-10 t/m 2026-10-09. 2 varianten getest tegen productie.

### Uitkomst

- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 2.12 vs productie 2.19 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.85 vs 0.83
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -20.1% vs -21.4%
    - ✓ Dubbele kosten en slippage: Sharpe 1.24 vs 1.23
- **satelliet-3-aandelen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 2.16 vs productie 2.19 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.65 vs 0.83
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -24.0% vs -21.4%
    - ✗ Dubbele kosten en slippage: Sharpe 1.13 vs 1.23

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +175.5% | +22.5% | -21.4% | 1.27 | 2.19 | 1.23 | 146 | 70% | 1.18 |
| regimefilter | +164.2% | +21.5% | -20.1% | 1.27 | 2.12 | 1.24 | 157 | 68% | 1.24 |
| satelliet-3-aandelen | +164.6% | +21.5% | -24.0% | 1.15 | 2.16 | 1.13 | 118 | 69% | 1.20 |

### Per periode (rendement)

| Variant | Oct 2021–Oct 2022 | Oct 2022–Oct 2023 | Oct 2023–Oct 2024 | Oct 2024–Oct 2025 | Oct 2025–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | -9.3% | +20.8% | +44.3% | +32.4% | +36.0% |
| regimefilter | -8.6% | +18.9% | +44.3% | +28.1% | +35.9% |
| satelliet-3-aandelen | -12.8% | +16.4% | +40.6% | +36.7% | +41.0% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (productie, productie, regimefilter, regimefilter), was het resultaat over de laatste 4 periodes +203.5%, tegen +213.8% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +66% (66 d) | +14% (51 d) | +30% (74 d) | -59% (2 d) | +42% (172 d) | +30% (269 d) | +4% (447 d) | +36% (56 d) | -19% (67 d) | +22% (100 d) |
| regimefilter | +57% (66 d) | +14% (51 d) | +29% (74 d) | -59% (2 d) | +42% (172 d) | +32% (269 d) | +4% (447 d) | +30% (56 d) | -19% (67 d) | +15% (100 d) |
| satelliet-3-aandelen | +56% (66 d) | +16% (51 d) | +33% (74 d) | -24% (2 d) | +40% (172 d) | +28% (269 d) | +6% (447 d) | +46% (56 d) | -27% (67 d) | +17% (100 d) |
