# Onderzoeksrapport 2026-11-21

Dit rapport test varianten van beide strategieën op echte koersen en kijkt wat de bots leren van hun eigen trades. **Er wordt niets automatisch aangepast.** Een aanbevolen variant gaat pas in productie als jij (of iemand die je vertrouwt) de instelling in de code aanpast; daarna draait de backtest opnieuw en loopt de nieuwe versie eerst weken mee op papier.

> Resultaten uit het verleden zijn geen garantie. De aandelenlijst is in 2026 gekozen (survivorship bias).

## Trend-agent

Periode 2016-11-21 t/m 2026-11-21. Ontwikkeldeel 2016-11-21 t/m 2023-11-23, holdout 2023-11-24 t/m 2026-11-21. 9 varianten getest tegen productie.

### Uitkomst

- **rem-pas-na-5-verliezen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.57 vs productie 0.83 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.59 vs 0.35
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -13.4% vs -14.4%
    - ✗ Dubbele kosten en slippage: Sharpe 0.27 vs 0.36
    - ✓ Genoeg trades: 997 afgesloten trades (nodig: 30)
- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.63 vs productie 0.83 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.18 vs 0.35
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -19.4% vs -14.4%
    - ✗ Dubbele kosten en slippage: Sharpe 0.18 vs 0.36
    - ✓ Genoeg trades: 841 afgesloten trades (nodig: 30)
- **koop-bij-nieuwe-top: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.55 vs productie 0.83 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.44 vs 0.35
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -14.2% vs -14.4%
    - ✗ Dubbele kosten en slippage: Sharpe 0.19 vs 0.36
    - ✓ Genoeg trades: 860 afgesloten trades (nodig: 30)
- **verkoop-na-2-rode-trendkaarsen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe -0.15 vs productie 0.83 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.39 vs 0.35
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -42.6% vs -14.4%
    - ✗ Dubbele kosten en slippage: Sharpe -3.60 vs 0.36
    - ✓ Genoeg trades: 3382 afgesloten trades (nodig: 30)
- **4-plekken: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.64 vs productie 0.83 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.02 vs 0.35
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -17.7% vs -14.4%
    - ✗ Dubbele kosten en slippage: Sharpe -0.00 vs 0.36
    - ✓ Genoeg trades: 522 afgesloten trades (nodig: 30)
- **5-plekken: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.01 vs productie 0.83 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.02 vs 0.35
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -19.5% vs -14.4%
    - ✗ Dubbele kosten en slippage: Sharpe -0.00 vs 0.36
    - ✓ Genoeg trades: 638 afgesloten trades (nodig: 30)
- **meer-per-aankoop: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.70 vs productie 0.83 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.19 vs 0.35
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -21.0% vs -14.4%
    - ✗ Dubbele kosten en slippage: Sharpe 0.21 vs 0.36
    - ✓ Genoeg trades: 995 afgesloten trades (nodig: 30)
- **veel-meer-per-aankoop: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.70 vs productie 0.83 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.67 vs 0.35
    - ✓ Consistent over periodes: beter in 4 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -18.3% vs -14.4%
    - ✓ Dubbele kosten en slippage: Sharpe 0.48 vs 0.36
    - ✓ Genoeg trades: 938 afgesloten trades (nodig: 30)
- **rest-in-wereld-etf: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.92 vs productie 0.83 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.43 vs 0.35
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -27.6% vs -14.4%
    - ✓ Dubbele kosten en slippage: Sharpe 0.40 vs 0.36
    - ✓ Genoeg trades: 993 afgesloten trades (nodig: 30)

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +88.8% | +6.6% | -14.4% | 0.50 | 0.83 | 0.36 | 989 | 37% | 2.17 |
| rem-pas-na-5-verliezen | +118.5% | +8.1% | -13.4% | 0.59 | 0.57 | 0.27 | 997 | 40% | 2.04 |
| regimefilter | +42.9% | +3.6% | -19.4% | 0.32 | 0.63 | 0.18 | 841 | 34% | 2.24 |
| koop-bij-nieuwe-top | +79.8% | +6.0% | -14.2% | 0.48 | 0.55 | 0.19 | 860 | 36% | 2.24 |
| verkoop-na-2-rode-trendkaarsen | -34.3% | -4.1% | -42.6% | -0.31 | -0.15 | -3.60 | 3382 | 35% | 1.64 |
| 4-plekken | +18.0% | +1.7% | -17.7% | 0.22 | 0.64 | -0.00 | 522 | 36% | 2.00 |
| 5-plekken | -3.0% | -0.3% | -19.5% | -0.01 | 0.01 | -0.00 | 638 | 34% | 1.89 |
| meer-per-aankoop | +50.4% | +4.2% | -21.0% | 0.35 | 0.70 | 0.21 | 995 | 37% | 2.08 |
| veel-meer-per-aankoop | +205.1% | +11.8% | -18.3% | 0.68 | 0.70 | 0.48 | 938 | 36% | 2.53 |
| rest-in-wereld-etf | +141.0% | +9.2% | -27.6% | 0.57 | 0.92 | 0.40 | 993 | 37% | 2.13 |

### Per periode (rendement)

| Variant | Nov 2016–Nov 2018 | Nov 2018–Nov 2020 | Nov 2020–Nov 2022 | Nov 2022–Nov 2024 | Nov 2024–Nov 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +8.4% | +17.9% | +2.4% | +21.0% | +17.7% |
| rem-pas-na-5-verliezen | +18.8% | +22.7% | +17.1% | +21.4% | +4.3% |
| regimefilter | +12.8% | +6.9% | -5.3% | +9.6% | +13.5% |
| koop-bij-nieuwe-top | +14.5% | +6.1% | +6.7% | +23.1% | +11.1% |
| verkoop-na-2-rode-trendkaarsen | -5.9% | +6.0% | -9.3% | -26.8% | -1.5% |
| 4-plekken | +2.3% | +11.9% | -12.7% | +8.8% | +8.1% |
| 5-plekken | +4.2% | +8.9% | -14.7% | +2.6% | -2.8% |
| meer-per-aankoop | +4.6% | +14.9% | -7.5% | +20.0% | +11.1% |
| veel-meer-per-aankoop | +35.4% | +34.4% | +5.1% | +38.6% | +13.5% |
| rest-in-wereld-etf | +10.9% | +25.6% | +9.9% | +21.4% | +26.8% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (veel-meer-per-aankoop, veel-meer-per-aankoop, veel-meer-per-aankoop, veel-meer-per-aankoop), was het resultaat over de laatste 4 periodes +122.2%, tegen +71.9% voor gewoon productie houden. Bijsturen hielp hier, maar met zo weinig periodes kan dat toeval zijn.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | -2% (204 d) | -4% (69 d) | +14% (163 d) | +67% (3 d) | +3% (358 d) | +1% (882 d) | +8% (1398 d) | -0% (163 d) | +1% (126 d) | +8% (274 d) |
| rem-pas-na-5-verliezen | -4% (204 d) | +10% (69 d) | +11% (163 d) | +67% (3 d) | +4% (358 d) | +5% (882 d) | +7% (1395 d) | +5% (160 d) | +1% (126 d) | +12% (274 d) |
| regimefilter | -3% (204 d) | +3% (69 d) | +4% (163 d) | +67% (3 d) | -1% (353 d) | +2% (882 d) | +6% (1393 d) | -8% (161 d) | -6% (126 d) | +9% (269 d) |
| koop-bij-nieuwe-top | -7% (199 d) | +8% (69 d) | +16% (163 d) | +62% (3 d) | +14% (358 d) | +4% (882 d) | +3% (1398 d) | +3% (163 d) | -4% (126 d) | +5% (269 d) |
| verkoop-na-2-rode-trendkaarsen | -1% (199 d) | -11% (63 d) | +3% (155 d) | +60% (3 d) | -2% (353 d) | -7% (860 d) | +2% (1356 d) | -2% (149 d) | -13% (120 d) | -11% (262 d) |
| 4-plekken | -2% (204 d) | +0% (68 d) | +4% (159 d) | +9% (3 d) | -0% (350 d) | -2% (879 d) | +5% (1397 d) | +2% (150 d) | -6% (126 d) | +1% (273 d) |
| 5-plekken | -0% (204 d) | +6% (69 d) | +9% (163 d) | +15% (3 d) | -3% (353 d) | -3% (882 d) | +2% (1390 d) | -6% (151 d) | -2% (126 d) | -1% (272 d) |
| meer-per-aankoop | -2% (204 d) | +6% (69 d) | +10% (163 d) | +18% (3 d) | +1% (358 d) | +1% (882 d) | +4% (1398 d) | +10% (163 d) | -3% (126 d) | +9% (274 d) |
| veel-meer-per-aankoop | +3% (204 d) | +11% (69 d) | +12% (163 d) | +39% (3 d) | +3% (358 d) | +9% (882 d) | +9% (1390 d) | +14% (163 d) | -2% (126 d) | +15% (274 d) |
| rest-in-wereld-etf | +24% (204 d) | -6% (69 d) | +25% (163 d) | +84% (3 d) | +5% (356 d) | +3% (882 d) | +8% (1398 d) | -2% (159 d) | -5% (126 d) | +6% (274 d) |

## Trend-agent: lessen uit 10 jaar backtest (productie)

989 afgesloten trades, 37% winst, gemiddeld +0.12 R per trade (mediaan -0.37 R), totaal €8,467, gemiddeld 26 dagen vastgehouden.

### Bevindingen

- Zwakte: Marktbeweeglijkheid bij instap = laag: gemiddeld -0.17 R over 261 trades (-0.38 R t.o.v. de rest, t = -3.4). Te testen via instelling `regime_filter`.
- Sterkte: Marktbeweeglijkheid bij instap = normaal: gemiddeld +0.26 R over 504 trades (+0.30 R t.o.v. de rest, t = 2.9). Te testen via instelling `regime_filter`.

_Dit zijn hypotheses. Een regel verandert pas na een test op ongeziene data (zie het onderzoeksrapport)._

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend | 706 | 36% | +0.10 | 5,317 |
| zijwaarts | 169 | 38% | +0.13 | 1,712 |
| dalend | 106 | 41% | +0.18 | 1,241 |
| onbekend (te weinig) | 8 | 62% | +0.49 | 198 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 504 | 39% | +0.26 | 7,988 |
| laag | 261 | 30% | -0.17 | -772 |
| hoog | 216 | 43% | +0.10 | 1,054 |
| onbekend (te weinig) | 8 | 62% | +0.49 | 198 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 50-60 | 452 | 40% | +0.19 | 5,797 |
| 60-70 | 372 | 37% | +0.06 | 1,894 |
| onder 50 | 121 | 30% | +0.13 | 1,210 |
| 70-80 | 44 | 39% | -0.17 | -434 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| negatief | 700 | 35% | +0.15 | 7,788 |
| positief | 289 | 43% | +0.04 | 679 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| hoger (>1,1) | 421 | 41% | +0.20 | 5,457 |
| normaal | 388 | 35% | +0.08 | 2,602 |
| lager (<0,9) | 180 | 33% | +0.00 | 408 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% | 534 | 36% | +0.07 | 2,704 |
| meer dan 25% | 282 | 39% | +0.19 | 4,056 |
| tot 10% | 173 | 39% | +0.15 | 1,708 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 579 | 36% | +0.08 | 3,444 |
| wild (>3%) | 226 | 44% | +0.25 | 3,823 |
| rustig (<1,5%) | 184 | 35% | +0.07 | 1,200 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt | 823 | 42% | +0.21 | 11,401 |
| trend gebroken (slot onder 50-daags gemiddelde) | 166 | 14% | -0.33 | -2,934 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| middel | 347 | 26% | -0.34 | -6,817 |
| lang (>30 d) | 344 | 81% | +1.48 | 31,762 |
| kort (<10 d) | 298 | 0% | -0.92 | -16,478 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-eaf4f8 | 989 | 37% | +0.12 | 8,467 |

## Trend-agent: lessen uit het oefenen (nepgeld, live)

Live van 2026-10-13 t/m 2026-11-20 (29 handelsdagen): bot -2.26%, wereld-ETF -7.05%, verschil +4.79%.

Live pas 8 afgesloten trades (gemiddeld -0.46 R); vanaf 20 trades is een vergelijking met de backtest (+0.12 R) zinvol.

8 afgesloten trades, 38% winst, gemiddeld -0.46 R per trade (mediaan -0.52 R), totaal €-173, gemiddeld 16 dagen vastgehouden.

### Bevindingen

- Geen overtuigende verschillen (minimaal 20 trades per groep, verschil ≥ 0.15 R en t ≥ 2.0).

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend (te weinig) | 5 | 20% | -0.76 | -175 |
| onbekend (te weinig) | 3 | 67% | +0.04 | 2 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal (te weinig) | 5 | 20% | -0.76 | -175 |
| onbekend (te weinig) | 3 | 67% | +0.04 | 2 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| onbekend (te weinig) | 3 | 67% | +0.04 | 2 |
| 60-70 (te weinig) | 3 | 33% | -0.46 | -69 |
| 70-80 (te weinig) | 1 | 0% | -1.35 | -59 |
| 50-60 (te weinig) | 1 | 0% | -1.04 | -47 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| positief (te weinig) | 4 | 25% | -0.69 | -128 |
| onbekend (te weinig) | 3 | 67% | +0.04 | 2 |
| negatief (te weinig) | 1 | 0% | -1.04 | -47 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| onbekend (te weinig) | 3 | 67% | +0.04 | 2 |
| normaal (te weinig) | 3 | 33% | -0.78 | -112 |
| lager (<0,9) (te weinig) | 1 | 0% | -1.35 | -59 |
| hoger (>1,1) (te weinig) | 1 | 0% | -0.09 | -4 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% (te weinig) | 5 | 20% | -0.76 | -175 |
| onbekend (te weinig) | 3 | 67% | +0.04 | 2 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal (te weinig) | 5 | 20% | -0.76 | -175 |
| onbekend (te weinig) | 3 | 67% | +0.04 | 2 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt (te weinig) | 8 | 38% | -0.46 | -173 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| middel (te weinig) | 4 | 50% | -0.14 | -14 |
| kort (<10 d) (te weinig) | 3 | 0% | -1.26 | -174 |
| lang (>30 d) (te weinig) | 1 | 100% | +0.69 | 15 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-081d85 (te weinig) | 5 | 20% | -0.76 | -175 |
| onbekend (te weinig) | 3 | 67% | +0.04 | 2 |

## Investeerder

Periode 2016-11-21 t/m 2026-11-20. Ontwikkeldeel 2016-11-21 t/m 2023-11-20, holdout 2023-11-21 t/m 2026-11-20. 6 varianten getest tegen productie.

### Uitkomst

- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.36 vs productie 1.42 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.96 vs 1.12
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -36.7% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.06 vs 1.19
- **satelliet-3-aandelen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.40 vs productie 1.42 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 1.13 vs 1.12
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -38.1% vs -36.7%
    - ✓ Dubbele kosten en slippage: Sharpe 1.19 vs 1.19
- **zonder-crypto: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.45 vs productie 1.42 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.87 vs 1.12
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -34.9% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.03 vs 1.19
- **minder-satelliet: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.42 vs productie 1.42 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 1.07 vs 1.12
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -35.3% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.15 vs 1.19
- **hooguit-1-per-sector: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.31 vs productie 1.42 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 1.11 vs 1.12
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -35.7% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.15 vs 1.19
- **voorzichtig: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.42 vs productie 1.42 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.98 vs 1.12
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -33.9% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.08 vs 1.19

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +722.2% | +23.5% | -36.7% | 1.21 | 1.42 | 1.19 | 294 | 73% | 1.52 |
| regimefilter | +497.8% | +19.6% | -36.7% | 1.08 | 1.36 | 1.06 | 290 | 70% | 1.41 |
| satelliet-3-aandelen | +851.8% | +25.3% | -38.1% | 1.21 | 1.40 | 1.19 | 243 | 74% | 1.36 |
| zonder-crypto | +487.3% | +19.4% | -34.9% | 1.05 | 1.45 | 1.03 | 248 | 72% | 1.50 |
| minder-satelliet | +504.0% | +19.7% | -35.3% | 1.17 | 1.42 | 1.15 | 272 | 69% | 2.12 |
| hooguit-1-per-sector | +552.1% | +20.6% | -35.7% | 1.17 | 1.31 | 1.15 | 335 | 70% | 1.25 |
| voorzichtig | +437.3% | +18.3% | -33.9% | 1.10 | 1.42 | 1.08 | 293 | 68% | 1.66 |

### Per periode (rendement)

| Variant | Nov 2016–Nov 2018 | Nov 2018–Nov 2020 | Nov 2020–Nov 2022 | Nov 2022–Nov 2024 | Nov 2024–Nov 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +38.7% | +66.4% | +40.6% | +70.4% | +41.7% |
| regimefilter | +38.6% | +27.4% | +44.9% | +66.2% | +35.5% |
| satelliet-3-aandelen | +49.4% | +67.0% | +38.4% | +79.0% | +47.4% |
| zonder-crypto | +21.2% | +56.0% | +21.5% | +63.1% | +50.5% |
| minder-satelliet | +33.9% | +49.3% | +42.1% | +58.0% | +28.6% |
| hooguit-1-per-sector | +34.2% | +54.4% | +42.5% | +74.8% | +20.9% |
| voorzichtig | +25.9% | +47.9% | +33.3% | +56.1% | +33.4% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (satelliet-3-aandelen, satelliet-3-aandelen, productie, hooguit-1-per-sector), was het resultaat over de laatste 4 periodes +376.5%, tegen +465.1% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +59% (147 d) | +18% (51 d) | +65% (117 d) | +88% (3 d) | +14% (262 d) | +21% (624 d) | +18% (1003 d) | -2% (118 d) | -5% (90 d) | +30% (194 d) |
| regimefilter | +43% (147 d) | +11% (51 d) | +41% (117 d) | +88% (3 d) | +15% (262 d) | +22% (624 d) | +18% (1003 d) | -5% (118 d) | -6% (90 d) | +14% (194 d) |
| satelliet-3-aandelen | +60% (147 d) | +20% (51 d) | +69% (117 d) | +118% (3 d) | +23% (262 d) | +23% (624 d) | +17% (1003 d) | +6% (118 d) | +0% (90 d) | +32% (194 d) |
| zonder-crypto | +63% (147 d) | +18% (51 d) | +70% (117 d) | +93% (3 d) | +13% (262 d) | +16% (624 d) | +14% (1003 d) | +6% (118 d) | -11% (90 d) | +16% (194 d) |
| minder-satelliet | +58% (147 d) | +20% (51 d) | +57% (117 d) | +78% (3 d) | +8% (262 d) | +20% (624 d) | +15% (1003 d) | -2% (118 d) | -9% (90 d) | +22% (194 d) |
| hooguit-1-per-sector | +59% (147 d) | +17% (51 d) | +55% (117 d) | +100% (3 d) | +13% (262 d) | +19% (624 d) | +15% (1003 d) | -6% (118 d) | -4% (90 d) | +28% (194 d) |
| voorzichtig | +59% (147 d) | +18% (51 d) | +61% (117 d) | +84% (3 d) | +10% (262 d) | +16% (624 d) | +13% (1003 d) | +3% (118 d) | -9% (90 d) | +16% (194 d) |

## Investeerder live (nepgeld)

Van 2026-10-13 t/m 2026-11-20: investeerder -12.67%, wereld-ETF -7.05%, verschil -5.63%.
