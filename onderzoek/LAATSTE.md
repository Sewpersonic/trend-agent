# Onderzoeksrapport 2026-11-28

Dit rapport test varianten van beide strategieën op echte koersen en kijkt wat de bots leren van hun eigen trades. **Er wordt niets automatisch aangepast.** Een aanbevolen variant gaat pas in productie als jij (of iemand die je vertrouwt) de instelling in de code aanpast; daarna draait de backtest opnieuw en loopt de nieuwe versie eerst weken mee op papier.

> Resultaten uit het verleden zijn geen garantie. De aandelenlijst is in 2026 gekozen (survivorship bias).

## Trend-agent

Periode 2016-11-28 t/m 2026-11-28. Ontwikkeldeel 2016-11-28 t/m 2023-11-28, holdout 2023-11-29 t/m 2026-11-28. 9 varianten getest tegen productie.

### Uitkomst

- **rem-pas-na-5-verliezen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.62 vs productie 0.62 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.43 vs 0.41
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -15.2% vs -13.8%
    - ✗ Dubbele kosten en slippage: Sharpe 0.18 vs 0.42
    - ✓ Genoeg trades: 1013 afgesloten trades (nodig: 30)
- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.58 vs productie 0.62 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.34 vs 0.41
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -19.5% vs -13.8%
    - ✗ Dubbele kosten en slippage: Sharpe 0.19 vs 0.42
    - ✓ Genoeg trades: 836 afgesloten trades (nodig: 30)
- **koop-bij-nieuwe-top: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.58 vs productie 0.62 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.42 vs 0.41
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -13.9% vs -13.8%
    - ✗ Dubbele kosten en slippage: Sharpe 0.23 vs 0.42
    - ✓ Genoeg trades: 868 afgesloten trades (nodig: 30)
- **verkoop-na-2-rode-trendkaarsen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe -0.19 vs productie 0.62 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.47 vs 0.41
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -47.2% vs -13.8%
    - ✗ Dubbele kosten en slippage: Sharpe -3.53 vs 0.42
    - ✓ Genoeg trades: 3437 afgesloten trades (nodig: 30)
- **4-plekken: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.68 vs productie 0.62 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.02 vs 0.41
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -18.3% vs -13.8%
    - ✗ Dubbele kosten en slippage: Sharpe 0.01 vs 0.42
    - ✓ Genoeg trades: 523 afgesloten trades (nodig: 30)
- **5-plekken: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.27 vs productie 0.62 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.02 vs 0.41
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -15.3% vs -13.8%
    - ✗ Dubbele kosten en slippage: Sharpe 0.01 vs 0.42
    - ✓ Genoeg trades: 651 afgesloten trades (nodig: 30)
- **meer-per-aankoop: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.82 vs productie 0.62 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.19 vs 0.41
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -21.8% vs -13.8%
    - ✗ Dubbele kosten en slippage: Sharpe 0.23 vs 0.42
    - ✓ Genoeg trades: 989 afgesloten trades (nodig: 30)
- **veel-meer-per-aankoop: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.80 vs productie 0.62 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.34 vs 0.41
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -19.8% vs -13.8%
    - ✗ Dubbele kosten en slippage: Sharpe 0.34 vs 0.42
    - ✓ Genoeg trades: 975 afgesloten trades (nodig: 30)
- **rest-in-wereld-etf: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.92 vs productie 0.62 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.45 vs 0.41
    - ✓ Consistent over periodes: beter in 4 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -27.5% vs -13.8%
    - ✓ Dubbele kosten en slippage: Sharpe 0.44 vs 0.42
    - ✓ Genoeg trades: 995 afgesloten trades (nodig: 30)

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +84.1% | +6.3% | -13.8% | 0.48 | 0.62 | 0.42 | 1005 | 37% | 2.14 |
| rem-pas-na-5-verliezen | +93.4% | +6.8% | -15.2% | 0.50 | 0.62 | 0.18 | 1013 | 38% | 2.10 |
| regimefilter | +63.4% | +5.0% | -19.5% | 0.43 | 0.58 | 0.19 | 836 | 36% | 2.18 |
| koop-bij-nieuwe-top | +77.6% | +5.9% | -13.9% | 0.47 | 0.58 | 0.23 | 868 | 36% | 2.24 |
| verkoop-na-2-rode-trendkaarsen | -38.9% | -4.8% | -47.2% | -0.37 | -0.19 | -3.53 | 3437 | 35% | 1.61 |
| 4-plekken | +17.4% | +1.6% | -18.3% | 0.21 | 0.68 | 0.01 | 523 | 36% | 2.01 |
| 5-plekken | +6.8% | +0.7% | -15.3% | 0.11 | 0.27 | 0.01 | 651 | 36% | 1.89 |
| meer-per-aankoop | +60.5% | +4.8% | -21.8% | 0.40 | 0.82 | 0.23 | 989 | 37% | 2.13 |
| veel-meer-per-aankoop | +118.1% | +8.1% | -19.8% | 0.49 | 0.80 | 0.34 | 975 | 34% | 2.53 |
| rest-in-wereld-etf | +149.2% | +9.6% | -27.5% | 0.59 | 0.92 | 0.44 | 995 | 38% | 2.11 |

### Per periode (rendement)

| Variant | Nov 2016–Nov 2018 | Nov 2018–Nov 2020 | Dec 2020–Nov 2022 | Nov 2022–Nov 2024 | Nov 2024–Nov 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +15.4% | +17.0% | +1.9% | +14.0% | +15.1% |
| rem-pas-na-5-verliezen | +9.0% | +19.7% | +15.2% | +18.1% | +6.7% |
| regimefilter | +21.7% | +12.5% | -7.0% | +13.3% | +11.3% |
| koop-bij-nieuwe-top | +13.3% | +3.9% | +5.4% | +24.4% | +12.8% |
| verkoop-na-2-rode-trendkaarsen | -1.7% | -3.7% | -12.5% | -25.5% | -4.0% |
| 4-plekken | +2.2% | +10.8% | -13.7% | +9.1% | +8.8% |
| 5-plekken | -1.4% | +9.6% | -9.6% | +4.2% | +4.3% |
| meer-per-aankoop | +18.3% | +11.5% | -6.9% | +5.7% | +21.7% |
| veel-meer-per-aankoop | +11.4% | +11.4% | +3.0% | +48.7% | +13.0% |
| rest-in-wereld-etf | +16.7% | +23.1% | +8.4% | +21.4% | +29.1% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (regimefilter, regimefilter, rem-pas-na-5-verliezen, rem-pas-na-5-verliezen), was het resultaat over de laatste 4 periodes +31.9%, tegen +56.5% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | -1% (204 d) | -4% (69 d) | +12% (163 d) | +94% (3 d) | +4% (364 d) | +1% (880 d) | +8% (1393 d) | +2% (161 d) | -2% (126 d) | +8% (274 d) |
| rem-pas-na-5-verliezen | -4% (204 d) | +6% (69 d) | +9% (163 d) | +94% (3 d) | +6% (364 d) | +6% (880 d) | +5% (1390 d) | +4% (158 d) | -5% (126 d) | +9% (274 d) |
| regimefilter | -3% (204 d) | +3% (69 d) | +4% (163 d) | +94% (3 d) | +0% (356 d) | +3% (880 d) | +6% (1385 d) | -8% (159 d) | +5% (126 d) | +9% (269 d) |
| koop-bij-nieuwe-top | -6% (199 d) | +7% (69 d) | +16% (163 d) | -112% (3 d) | +15% (364 d) | +3% (880 d) | +4% (1390 d) | +3% (161 d) | -11% (126 d) | +6% (269 d) |
| verkoop-na-2-rode-trendkaarsen | -1% (193 d) | -13% (61 d) | +2% (148 d) | +72% (3 d) | -4% (357 d) | -8% (855 d) | +1% (1343 d) | +1% (153 d) | -5% (120 d) | -10% (266 d) |
| 4-plekken | -2% (204 d) | +0% (68 d) | +4% (159 d) | +39% (3 d) | +0% (356 d) | -3% (877 d) | +5% (1392 d) | +2% (148 d) | -6% (126 d) | +1% (273 d) |
| 5-plekken | -1% (204 d) | +6% (68 d) | +8% (159 d) | +16% (3 d) | -1% (362 d) | -2% (880 d) | +3% (1385 d) | -3% (154 d) | -5% (126 d) | +1% (274 d) |
| meer-per-aankoop | -3% (204 d) | -3% (69 d) | +13% (163 d) | +40% (3 d) | +2% (364 d) | +2% (880 d) | +5% (1388 d) | +7% (161 d) | +0% (126 d) | +9% (274 d) |
| veel-meer-per-aankoop | -4% (204 d) | +9% (69 d) | +18% (163 d) | +96% (3 d) | +4% (364 d) | +6% (880 d) | +7% (1388 d) | +11% (161 d) | -1% (126 d) | +4% (272 d) |
| rest-in-wereld-etf | +23% (204 d) | -7% (69 d) | +27% (163 d) | +89% (3 d) | +6% (362 d) | +3% (880 d) | +8% (1393 d) | -1% (161 d) | +3% (126 d) | +6% (274 d) |

## Trend-agent: lessen uit 10 jaar backtest (productie)

1005 afgesloten trades, 37% winst, gemiddeld +0.09 R per trade (mediaan -0.36 R), totaal €7,967, gemiddeld 26 dagen vastgehouden.

### Bevindingen

- Zwakte: Marktbeweeglijkheid bij instap = laag: gemiddeld -0.17 R over 277 trades (-0.35 R t.o.v. de rest, t = -3.2). Te testen via instelling `regime_filter`.
- Sterkte: Marktbeweeglijkheid bij instap = normaal: gemiddeld +0.22 R over 500 trades (+0.26 R t.o.v. de rest, t = 2.6). Te testen via instelling `regime_filter`.
- Zwakte: RSI bij instap = 70-80: gemiddeld -0.29 R over 41 trades (-0.39 R t.o.v. de rest, t = -2.2). Te testen via instelling `max_rsi_entry`.

_Dit zijn hypotheses. Een regel verandert pas na een test op ongeziene data (zie het onderzoeksrapport)._

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend | 716 | 36% | +0.06 | 4,464 |
| zijwaarts | 176 | 39% | +0.12 | 1,931 |
| dalend | 105 | 41% | +0.15 | 1,100 |
| onbekend (te weinig) | 8 | 88% | +1.18 | 473 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 500 | 38% | +0.22 | 7,156 |
| laag | 277 | 29% | -0.17 | -644 |
| hoog | 220 | 43% | +0.07 | 982 |
| onbekend (te weinig) | 8 | 88% | +1.18 | 473 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 50-60 | 462 | 40% | +0.15 | 5,581 |
| 60-70 | 379 | 38% | +0.06 | 2,169 |
| onder 50 | 123 | 28% | +0.09 | 878 |
| 70-80 | 41 | 32% | -0.29 | -661 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| negatief | 713 | 36% | +0.13 | 7,997 |
| positief | 292 | 41% | -0.01 | -29 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| hoger (>1,1) | 412 | 41% | +0.16 | 4,834 |
| normaal | 412 | 36% | +0.09 | 2,983 |
| lager (<0,9) | 181 | 31% | -0.07 | 150 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% | 539 | 37% | +0.06 | 3,324 |
| meer dan 25% | 291 | 36% | +0.13 | 2,893 |
| tot 10% | 175 | 40% | +0.11 | 1,751 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 584 | 36% | +0.05 | 2,805 |
| wild (>3%) | 231 | 42% | +0.21 | 3,422 |
| rustig (<1,5%) | 190 | 35% | +0.06 | 1,740 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt | 840 | 42% | +0.18 | 11,131 |
| trend gebroken (slot onder 50-daags gemiddelde) | 165 | 13% | -0.36 | -3,163 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| middel | 351 | 27% | -0.32 | -6,542 |
| lang (>30 d) | 345 | 81% | +1.43 | 31,846 |
| kort (<10 d) | 309 | 0% | -0.94 | -17,337 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-eaf4f8 | 1005 | 37% | +0.09 | 7,967 |

## Trend-agent: lessen uit het oefenen (nepgeld, live)

Live van 2026-10-13 t/m 2026-11-27 (34 handelsdagen): bot -1.00%, wereld-ETF -3.98%, verschil +2.98%.

Live pas 10 afgesloten trades (gemiddeld -0.47 R); vanaf 20 trades is een vergelijking met de backtest (+0.09 R) zinvol.

10 afgesloten trades, 30% winst, gemiddeld -0.47 R per trade (mediaan -0.52 R), totaal €-205, gemiddeld 18 dagen vastgehouden.

### Bevindingen

- Geen overtuigende verschillen (minimaal 20 trades per groep, verschil ≥ 0.15 R en t ≥ 2.0).

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend (te weinig) | 7 | 14% | -0.69 | -208 |
| onbekend (te weinig) | 3 | 67% | +0.04 | 2 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal (te weinig) | 6 | 17% | -0.72 | -201 |
| onbekend (te weinig) | 3 | 67% | +0.04 | 2 |
| laag (te weinig) | 1 | 0% | -0.49 | -7 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| onbekend (te weinig) | 3 | 67% | +0.04 | 2 |
| 70-80 (te weinig) | 3 | 0% | -0.80 | -91 |
| 60-70 (te weinig) | 3 | 33% | -0.46 | -69 |
| 50-60 (te weinig) | 1 | 0% | -1.04 | -47 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| positief (te weinig) | 6 | 17% | -0.63 | -161 |
| onbekend (te weinig) | 3 | 67% | +0.04 | 2 |
| negatief (te weinig) | 1 | 0% | -1.04 | -47 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal (te weinig) | 4 | 25% | -0.71 | -119 |
| onbekend (te weinig) | 3 | 67% | +0.04 | 2 |
| lager (<0,9) (te weinig) | 2 | 0% | -0.95 | -85 |
| hoger (>1,1) (te weinig) | 1 | 0% | -0.09 | -4 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% (te weinig) | 6 | 17% | -0.71 | -182 |
| onbekend (te weinig) | 3 | 67% | +0.04 | 2 |
| meer dan 25% (te weinig) | 1 | 0% | -0.54 | -26 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal (te weinig) | 7 | 14% | -0.69 | -208 |
| onbekend (te weinig) | 3 | 67% | +0.04 | 2 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt (te weinig) | 10 | 30% | -0.47 | -205 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| middel (te weinig) | 6 | 33% | -0.27 | -46 |
| kort (<10 d) (te weinig) | 3 | 0% | -1.26 | -174 |
| lang (>30 d) (te weinig) | 1 | 100% | +0.69 | 15 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-081d85 (te weinig) | 6 | 17% | -0.72 | -201 |
| onbekend (te weinig) | 3 | 67% | +0.04 | 2 |
| trend-1.1-a0ddd5 (te weinig) | 1 | 0% | -0.49 | -7 |

## Investeerder

Periode 2016-11-28 t/m 2026-11-27. Ontwikkeldeel 2016-11-28 t/m 2023-11-27, holdout 2023-11-28 t/m 2026-11-27. 6 varianten getest tegen productie.

### Uitkomst

- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.39 vs productie 1.46 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.95 vs 1.11
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -36.7% vs -36.8%
    - ✗ Dubbele kosten en slippage: Sharpe 1.07 vs 1.20
- **satelliet-3-aandelen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.42 vs productie 1.46 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 1.13 vs 1.11
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -38.1% vs -36.8%
    - ✓ Dubbele kosten en slippage: Sharpe 1.20 vs 1.20
- **zonder-crypto: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.50 vs productie 1.46 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.87 vs 1.11
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -34.7% vs -36.8%
    - ✗ Dubbele kosten en slippage: Sharpe 1.04 vs 1.20
- **minder-satelliet: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.46 vs productie 1.46 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 1.07 vs 1.11
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -35.3% vs -36.8%
    - ✗ Dubbele kosten en slippage: Sharpe 1.16 vs 1.20
- **hooguit-1-per-sector: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.35 vs productie 1.46 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 1.11 vs 1.11
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -35.7% vs -36.8%
    - ✗ Dubbele kosten en slippage: Sharpe 1.16 vs 1.20
- **voorzichtig: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.48 vs productie 1.46 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.96 vs 1.11
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -33.9% vs -36.8%
    - ✗ Dubbele kosten en slippage: Sharpe 1.09 vs 1.20

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +740.8% | +23.7% | -36.8% | 1.22 | 1.46 | 1.20 | 290 | 72% | 1.55 |
| regimefilter | +510.7% | +19.8% | -36.7% | 1.09 | 1.39 | 1.07 | 286 | 70% | 1.41 |
| satelliet-3-aandelen | +874.3% | +25.6% | -38.1% | 1.22 | 1.42 | 1.20 | 242 | 74% | 1.37 |
| zonder-crypto | +507.0% | +19.8% | -34.7% | 1.07 | 1.50 | 1.04 | 247 | 72% | 1.51 |
| minder-satelliet | +526.8% | +20.2% | -35.3% | 1.18 | 1.46 | 1.16 | 272 | 69% | 2.17 |
| hooguit-1-per-sector | +568.2% | +20.9% | -35.7% | 1.18 | 1.35 | 1.16 | 334 | 70% | 1.25 |
| voorzichtig | +450.6% | +18.6% | -33.9% | 1.11 | 1.48 | 1.09 | 291 | 68% | 1.67 |

### Per periode (rendement)

| Variant | Nov 2016–Nov 2018 | Nov 2018–Nov 2020 | Nov 2020–Nov 2022 | Nov 2022–Nov 2024 | Nov 2024–Nov 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +41.7% | +62.8% | +38.9% | +75.3% | +45.4% |
| regimefilter | +41.8% | +25.4% | +42.2% | +69.3% | +39.2% |
| satelliet-3-aandelen | +53.9% | +63.6% | +36.7% | +84.3% | +49.4% |
| zonder-crypto | +24.2% | +53.1% | +19.4% | +68.1% | +54.5% |
| minder-satelliet | +36.4% | +48.1% | +41.3% | +63.5% | +32.2% |
| hooguit-1-per-sector | +37.2% | +52.1% | +40.9% | +80.7% | +23.4% |
| voorzichtig | +28.5% | +46.1% | +30.9% | +60.8% | +37.0% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (satelliet-3-aandelen, satelliet-3-aandelen, satelliet-3-aandelen, hooguit-1-per-sector), was het resultaat over de laatste 4 periodes +408.4%, tegen +476.6% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +59% (147 d) | +18% (51 d) | +65% (117 d) | -28% (3 d) | +16% (266 d) | +22% (622 d) | +18% (1000 d) | +2% (119 d) | -5% (90 d) | +30% (194 d) |
| regimefilter | +43% (147 d) | +11% (51 d) | +41% (117 d) | -28% (3 d) | +16% (266 d) | +22% (622 d) | +18% (1000 d) | -1% (119 d) | -6% (90 d) | +14% (194 d) |
| satelliet-3-aandelen | +60% (147 d) | +20% (51 d) | +69% (117 d) | -0% (3 d) | +23% (266 d) | +23% (622 d) | +17% (1000 d) | +9% (119 d) | +0% (90 d) | +32% (194 d) |
| zonder-crypto | +63% (147 d) | +18% (51 d) | +70% (117 d) | -45% (3 d) | +14% (266 d) | +16% (622 d) | +14% (1000 d) | +9% (119 d) | -11% (90 d) | +16% (194 d) |
| minder-satelliet | +58% (147 d) | +20% (51 d) | +57% (117 d) | -32% (3 d) | +9% (266 d) | +20% (622 d) | +15% (1000 d) | +3% (119 d) | -9% (90 d) | +22% (194 d) |
| hooguit-1-per-sector | +59% (147 d) | +17% (51 d) | +55% (117 d) | -25% (3 d) | +14% (266 d) | +19% (622 d) | +15% (1000 d) | -2% (119 d) | -4% (90 d) | +29% (194 d) |
| voorzichtig | +59% (147 d) | +18% (51 d) | +61% (117 d) | -37% (3 d) | +11% (266 d) | +16% (622 d) | +14% (1000 d) | +8% (119 d) | -9% (90 d) | +16% (194 d) |

## Investeerder live (nepgeld)

Van 2026-10-13 t/m 2026-11-27: investeerder -10.81%, wereld-ETF -3.98%, verschil -6.84%.
