# Onderzoeksrapport 2026-11-07

Dit rapport test varianten van beide strategieën op echte koersen en kijkt wat de bots leren van hun eigen trades. **Er wordt niets automatisch aangepast.** Een aanbevolen variant gaat pas in productie als jij (of iemand die je vertrouwt) de instelling in de code aanpast; daarna draait de backtest opnieuw en loopt de nieuwe versie eerst weken mee op papier.

> Resultaten uit het verleden zijn geen garantie. De aandelenlijst is in 2026 gekozen (survivorship bias).

## Trend-agent

Periode 2016-11-07 t/m 2026-11-07. Ontwikkeldeel 2016-11-07 t/m 2023-11-09, holdout 2023-11-10 t/m 2026-11-07. 10 varianten getest tegen productie.

### Uitkomst

- **rem-pas-na-5-verliezen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.66 vs productie 0.64 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.54 vs 0.25
    - ✓ Consistent over periodes: beter in 5 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -19.9% vs -20.5%
    - ✓ Dubbele kosten en slippage: Sharpe 0.33 vs 0.16
    - ✓ Genoeg trades: 981 afgesloten trades (nodig: 30)
- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.53 vs productie 0.64 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.34 vs 0.25
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -18.2% vs -20.5%
    - ✓ Dubbele kosten en slippage: Sharpe 0.19 vs 0.16
    - ✓ Genoeg trades: 810 afgesloten trades (nodig: 30)
- **koop-na-terugval: AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.86 vs productie 0.64 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.29 vs 0.25
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -14.0% vs -20.5%
    - ✓ Dubbele kosten en slippage: Sharpe 0.43 vs 0.16
    - ✓ Genoeg trades: 990 afgesloten trades (nodig: 30)
- **koop-bij-nieuwe-top: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.69 vs productie 0.64 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.58 vs 0.25
    - ✓ Consistent over periodes: beter in 4 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -13.7% vs -20.5%
    - ✓ Dubbele kosten en slippage: Sharpe 0.45 vs 0.16
    - ✓ Genoeg trades: 871 afgesloten trades (nodig: 30)
- **verkoop-na-2-rode-trendkaarsen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe -0.14 vs productie 0.64 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.01 vs 0.25
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -32.7% vs -20.5%
    - ✗ Dubbele kosten en slippage: Sharpe -1.69 vs 0.16
    - ✓ Genoeg trades: 2955 afgesloten trades (nodig: 30)
- **4-plekken: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe -0.14 vs productie 0.64 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.11 vs 0.25
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -20.3% vs -20.5%
    - ✗ Dubbele kosten en slippage: Sharpe -0.34 vs 0.16
    - ✓ Genoeg trades: 531 afgesloten trades (nodig: 30)
- **5-plekken: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.30 vs productie 0.64 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.15 vs 0.25
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -14.7% vs -20.5%
    - ✗ Dubbele kosten en slippage: Sharpe -0.25 vs 0.16
    - ✓ Genoeg trades: 601 afgesloten trades (nodig: 30)
- **meer-per-aankoop: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.62 vs productie 0.64 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.21 vs 0.25
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -18.9% vs -20.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.13 vs 0.16
    - ✓ Genoeg trades: 943 afgesloten trades (nodig: 30)
- **veel-meer-per-aankoop: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.05 vs productie 0.64 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.24 vs 0.25
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -26.1% vs -20.5%
    - ✓ Dubbele kosten en slippage: Sharpe 0.20 vs 0.16
    - ✓ Genoeg trades: 938 afgesloten trades (nodig: 30)
- **rest-in-wereld-etf: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.83 vs productie 0.64 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.41 vs 0.25
    - ✓ Consistent over periodes: beter in 5 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -25.2% vs -20.5%
    - ✓ Dubbele kosten en slippage: Sharpe 0.36 vs 0.16
    - ✓ Genoeg trades: 977 afgesloten trades (nodig: 30)

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +62.5% | +5.0% | -20.5% | 0.38 | 0.64 | 0.16 | 984 | 35% | 2.24 |
| rem-pas-na-5-verliezen | +121.6% | +8.3% | -19.9% | 0.58 | 0.66 | 0.33 | 981 | 37% | 2.25 |
| regimefilter | +62.3% | +5.0% | -18.2% | 0.41 | 0.53 | 0.19 | 810 | 35% | 2.26 |
| koop-na-terugval | +84.5% | +6.3% | -14.0% | 0.48 | 0.86 | 0.43 | 990 | 37% | 2.16 |
| koop-bij-nieuwe-top | +122.0% | +8.3% | -13.7% | 0.62 | 0.69 | 0.45 | 871 | 36% | 2.36 |
| verkoop-na-2-rode-trendkaarsen | -10.0% | -1.0% | -32.7% | -0.03 | -0.14 | -1.69 | 2955 | 36% | 1.71 |
| 4-plekken | -11.8% | -1.2% | -20.3% | -0.11 | -0.14 | -0.34 | 531 | 32% | 1.88 |
| 5-plekken | +16.0% | +1.5% | -14.7% | 0.20 | 0.30 | -0.25 | 601 | 36% | 2.00 |
| meer-per-aankoop | +49.8% | +4.1% | -18.9% | 0.35 | 0.62 | 0.13 | 943 | 37% | 2.06 |
| veel-meer-per-aankoop | +25.5% | +2.3% | -26.1% | 0.19 | 0.05 | 0.20 | 938 | 31% | 2.31 |
| rest-in-wereld-etf | +125.0% | +8.4% | -25.2% | 0.54 | 0.83 | 0.36 | 977 | 36% | 2.15 |

### Per periode (rendement)

| Variant | Nov 2016–Nov 2018 | Nov 2018–Nov 2020 | Nov 2020–Nov 2022 | Nov 2022–Nov 2024 | Nov 2024–Nov 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +10.0% | +11.9% | -1.8% | +18.0% | +14.7% |
| rem-pas-na-5-verliezen | +27.2% | +13.7% | +5.8% | +22.9% | +17.9% |
| regimefilter | +25.0% | +7.8% | +2.2% | +5.7% | +13.5% |
| koop-na-terugval | +6.2% | +15.4% | +4.6% | +8.5% | +31.3% |
| koop-bij-nieuwe-top | +39.2% | +5.5% | +8.7% | +18.4% | +21.0% |
| verkoop-na-2-rode-trendkaarsen | +9.6% | -3.7% | +5.5% | -15.2% | -4.3% |
| 4-plekken | +0.1% | +1.2% | -10.1% | +5.5% | -7.1% |
| 5-plekken | +5.8% | +3.0% | -7.4% | +15.6% | +1.0% |
| meer-per-aankoop | +1.1% | +9.9% | -3.7% | +21.6% | +16.0% |
| veel-meer-per-aankoop | +8.3% | +20.8% | -3.3% | +10.3% | -7.9% |
| rest-in-wereld-etf | +17.9% | +22.3% | +3.6% | +22.0% | +25.4% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (koop-bij-nieuwe-top, koop-bij-nieuwe-top, koop-bij-nieuwe-top, koop-bij-nieuwe-top), was het resultaat over de laatste 4 periodes +64.4%, tegen +48.6% voor gewoon productie houden. Bijsturen hielp hier, maar met zo weinig periodes kan dat toeval zijn.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | -4% (204 d) | +10% (69 d) | +20% (163 d) | +322% (3 d) | +8% (347 d) | +6% (882 d) | +1% (1410 d) | -9% (164 d) | -1% (126 d) | +8% (274 d) |
| rem-pas-na-5-verliezen | -1% (204 d) | +16% (69 d) | +22% (163 d) | +319% (3 d) | +11% (347 d) | +6% (882 d) | +4% (1410 d) | -8% (164 d) | +3% (126 d) | +11% (274 d) |
| regimefilter | -3% (204 d) | +12% (69 d) | +2% (162 d) | +322% (3 d) | +4% (343 d) | +5% (882 d) | +2% (1410 d) | -4% (164 d) | +3% (126 d) | +10% (273 d) |
| koop-na-terugval | -2% (204 d) | +2% (69 d) | +13% (163 d) | -146% (3 d) | +5% (342 d) | +1% (882 d) | +8% (1410 d) | +2% (160 d) | -1% (126 d) | +10% (274 d) |
| koop-bij-nieuwe-top | -4% (199 d) | +6% (69 d) | +18% (163 d) | +683% (3 d) | +15% (343 d) | +5% (882 d) | +4% (1407 d) | +4% (163 d) | -1% (126 d) | +6% (269 d) |
| verkoop-na-2-rode-trendkaarsen | -5% (201 d) | +1% (68 d) | +10% (157 d) | +320% (3 d) | +5% (341 d) | +1% (864 d) | -3% (1368 d) | -4% (153 d) | -3% (126 d) | +3% (266 d) |
| 4-plekken | -5% (201 d) | +3% (69 d) | +2% (163 d) | -22% (3 d) | +6% (343 d) | -0% (882 d) | -2% (1405 d) | -8% (159 d) | +0% (126 d) | +3% (272 d) |
| 5-plekken | -2% (202 d) | +3% (69 d) | +4% (163 d) | +7% (3 d) | +4% (345 d) | +0% (882 d) | +1% (1410 d) | -5% (160 d) | +0% (126 d) | +4% (272 d) |
| meer-per-aankoop | -3% (204 d) | +19% (69 d) | +19% (163 d) | +112% (3 d) | +7% (347 d) | +2% (882 d) | +1% (1410 d) | -9% (164 d) | +4% (126 d) | +7% (274 d) |
| veel-meer-per-aankoop | -6% (204 d) | +18% (69 d) | +26% (163 d) | +193% (3 d) | +4% (345 d) | -2% (882 d) | +2% (1410 d) | -4% (164 d) | +0% (126 d) | +10% (274 d) |
| rest-in-wereld-etf | +18% (204 d) | +8% (69 d) | +30% (163 d) | +322% (3 d) | +5% (347 d) | +7% (882 d) | +3% (1410 d) | -1% (164 d) | -12% (126 d) | +5% (274 d) |

## Trend-agent: lessen uit 10 jaar backtest (productie)

984 afgesloten trades, 35% winst, gemiddeld +0.07 R per trade (mediaan -0.42 R), totaal €5,790, gemiddeld 27 dagen vastgehouden.

### Bevindingen

- Zwakte: Markttrend bij instap = stijgend: gemiddeld -0.01 R over 675 trades (-0.28 R t.o.v. de rest, t = -2.3). Te testen via instelling `regime_filter`.

_Dit zijn hypotheses. Een regel verandert pas na een test op ongeziene data (zie het onderzoeksrapport)._

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend | 675 | 33% | -0.01 | 973 |
| zijwaarts | 174 | 40% | +0.21 | 2,509 |
| dalend | 126 | 39% | +0.19 | 1,320 |
| onbekend (te weinig) | 9 | 44% | +2.21 | 989 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 499 | 36% | +0.14 | 5,187 |
| laag | 245 | 31% | -0.08 | -115 |
| hoog | 231 | 37% | +0.00 | -270 |
| onbekend (te weinig) | 9 | 44% | +2.21 | 989 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 60-70 | 397 | 34% | +0.06 | 1,620 |
| 50-60 | 269 | 39% | +0.18 | 3,728 |
| 70-80 | 263 | 32% | +0.00 | 536 |
| onder 50 | 55 | 33% | -0.03 | -94 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| positief | 526 | 36% | +0.07 | 2,690 |
| negatief | 458 | 34% | +0.07 | 3,101 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| hoger (>1,1) | 418 | 37% | +0.08 | 2,230 |
| normaal | 399 | 33% | +0.06 | 1,995 |
| lager (<0,9) | 167 | 36% | +0.08 | 1,565 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% | 521 | 34% | +0.05 | 2,170 |
| meer dan 25% | 325 | 37% | +0.12 | 2,861 |
| tot 10% | 138 | 34% | +0.03 | 759 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 547 | 33% | +0.05 | 2,313 |
| wild (>3%) | 250 | 39% | +0.12 | 1,935 |
| rustig (<1,5%) | 187 | 35% | +0.08 | 1,543 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt | 880 | 38% | +0.12 | 7,278 |
| trend gebroken (slot onder 50-daags gemiddelde) | 104 | 12% | -0.32 | -1,488 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| lang (>30 d) | 371 | 74% | +1.30 | 29,308 |
| middel | 326 | 21% | -0.42 | -8,213 |
| kort (<10 d) | 287 | 0% | -0.96 | -15,305 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-f132c3 | 984 | 35% | +0.07 | 5,790 |

## Trend-agent: lessen uit het oefenen (nepgeld, live)

Live van 2026-10-13 t/m 2026-11-06 (19 handelsdagen): bot -1.23%, wereld-ETF -3.80%, verschil +2.58%.

Live pas 5 afgesloten trades (gemiddeld -0.87 R); vanaf 20 trades is een vergelijking met de backtest (+0.07 R) zinvol.

5 afgesloten trades, 20% winst, gemiddeld -0.87 R per trade (mediaan -1.04 R), totaal €-187, gemiddeld 11 dagen vastgehouden.

### Bevindingen

- Geen overtuigende verschillen (minimaal 20 trades per groep, verschil ≥ 0.15 R en t ≥ 2.0).

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend (te weinig) | 3 | 0% | -1.26 | -174 |
| onbekend (te weinig) | 2 | 50% | -0.28 | -13 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal (te weinig) | 3 | 0% | -1.26 | -174 |
| onbekend (te weinig) | 2 | 50% | -0.28 | -13 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| onbekend (te weinig) | 2 | 50% | -0.28 | -13 |
| 70-80 (te weinig) | 1 | 0% | -1.35 | -59 |
| 60-70 (te weinig) | 1 | 0% | -1.39 | -69 |
| 50-60 (te weinig) | 1 | 0% | -1.04 | -47 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| onbekend (te weinig) | 2 | 50% | -0.28 | -13 |
| positief (te weinig) | 2 | 0% | -1.37 | -127 |
| negatief (te weinig) | 1 | 0% | -1.04 | -47 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| onbekend (te weinig) | 2 | 50% | -0.28 | -13 |
| normaal (te weinig) | 2 | 0% | -1.22 | -116 |
| lager (<0,9) (te weinig) | 1 | 0% | -1.35 | -59 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% (te weinig) | 3 | 0% | -1.26 | -174 |
| onbekend (te weinig) | 2 | 50% | -0.28 | -13 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal (te weinig) | 3 | 0% | -1.26 | -174 |
| onbekend (te weinig) | 2 | 50% | -0.28 | -13 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt (te weinig) | 5 | 20% | -0.87 | -187 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| kort (<10 d) (te weinig) | 3 | 0% | -1.26 | -174 |
| middel (te weinig) | 2 | 50% | -0.28 | -13 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-081d85 (te weinig) | 3 | 0% | -1.26 | -174 |
| onbekend (te weinig) | 2 | 50% | -0.28 | -13 |

## Investeerder

Periode 2016-11-07 t/m 2026-11-06. Ontwikkeldeel 2016-11-07 t/m 2023-11-06, holdout 2023-11-07 t/m 2026-11-06. 6 varianten getest tegen productie.

### Uitkomst

- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.51 vs productie 1.57 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.97 vs 1.12
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -36.7% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.12 vs 1.25
- **satelliet-3-aandelen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.55 vs productie 1.57 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 1.14 vs 1.12
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -38.1% vs -36.7%
    - ✓ Dubbele kosten en slippage: Sharpe 1.25 vs 1.25
- **zonder-crypto: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.58 vs productie 1.57 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.88 vs 1.12
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -34.8% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.08 vs 1.25
- **minder-satelliet: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.60 vs productie 1.57 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 1.09 vs 1.12
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -35.3% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.22 vs 1.25
- **hooguit-1-per-sector: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.50 vs productie 1.57 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 1.12 vs 1.12
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -35.7% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.21 vs 1.25
- **voorzichtig: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.59 vs productie 1.57 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.98 vs 1.12
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -33.9% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.13 vs 1.25

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +796.8% | +24.5% | -36.7% | 1.26 | 1.57 | 1.25 | 292 | 73% | 1.49 |
| regimefilter | +554.2% | +20.7% | -36.7% | 1.14 | 1.51 | 1.12 | 290 | 71% | 1.39 |
| satelliet-3-aandelen | +952.8% | +26.6% | -38.1% | 1.27 | 1.55 | 1.25 | 244 | 75% | 1.33 |
| zonder-crypto | +534.7% | +20.3% | -34.8% | 1.10 | 1.58 | 1.08 | 242 | 73% | 1.44 |
| minder-satelliet | +571.7% | +21.0% | -35.3% | 1.24 | 1.60 | 1.22 | 271 | 70% | 2.09 |
| hooguit-1-per-sector | +621.8% | +21.9% | -35.7% | 1.23 | 1.50 | 1.21 | 338 | 70% | 1.27 |
| voorzichtig | +486.0% | +19.3% | -33.9% | 1.16 | 1.59 | 1.13 | 292 | 68% | 1.71 |

### Per periode (rendement)

| Variant | Nov 2016–Nov 2018 | Nov 2018–Nov 2020 | Nov 2020–Nov 2022 | Nov 2022–Nov 2024 | Nov 2024–Nov 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +53.0% | +50.5% | +47.2% | +63.7% | +55.1% |
| regimefilter | +53.0% | +16.1% | +48.4% | +59.9% | +48.4% |
| satelliet-3-aandelen | +65.2% | +50.9% | +45.1% | +68.6% | +65.5% |
| zonder-crypto | +34.6% | +42.9% | +25.1% | +59.6% | +59.2% |
| minder-satelliet | +46.7% | +37.7% | +47.8% | +54.7% | +40.8% |
| hooguit-1-per-sector | +47.6% | +40.5% | +47.1% | +68.9% | +35.1% |
| voorzichtig | +38.4% | +36.5% | +36.4% | +52.9% | +43.7% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (satelliet-3-aandelen, satelliet-3-aandelen, productie, hooguit-1-per-sector), was het resultaat over de laatste 4 periodes +383.9%, tegen +462.6% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +59% (147 d) | +18% (51 d) | +65% (117 d) | +218% (3 d) | +19% (252 d) | +21% (624 d) | +18% (1013 d) | -2% (118 d) | -5% (90 d) | +29% (194 d) |
| regimefilter | +43% (147 d) | +11% (51 d) | +41% (117 d) | +218% (3 d) | +19% (252 d) | +22% (624 d) | +19% (1013 d) | -5% (118 d) | -6% (90 d) | +14% (194 d) |
| satelliet-3-aandelen | +60% (147 d) | +20% (51 d) | +69% (117 d) | +154% (3 d) | +28% (252 d) | +23% (624 d) | +18% (1013 d) | +6% (118 d) | +0% (90 d) | +32% (194 d) |
| zonder-crypto | +63% (147 d) | +18% (51 d) | +70% (117 d) | +225% (3 d) | +16% (252 d) | +16% (624 d) | +15% (1013 d) | +6% (118 d) | -11% (90 d) | +16% (194 d) |
| minder-satelliet | +58% (147 d) | +20% (51 d) | +57% (117 d) | +213% (3 d) | +13% (252 d) | +20% (624 d) | +15% (1013 d) | -2% (118 d) | -9% (90 d) | +22% (194 d) |
| hooguit-1-per-sector | +59% (147 d) | +17% (51 d) | +54% (117 d) | +181% (3 d) | +19% (252 d) | +19% (624 d) | +16% (1013 d) | -6% (118 d) | -4% (90 d) | +29% (194 d) |
| voorzichtig | +59% (147 d) | +18% (51 d) | +61% (117 d) | +218% (3 d) | +14% (252 d) | +16% (624 d) | +14% (1013 d) | +3% (118 d) | -9% (90 d) | +16% (194 d) |

## Investeerder live (nepgeld)

Van 2026-10-13 t/m 2026-11-06: investeerder -8.54%, wereld-ETF -3.80%, verschil -4.73%.
