# Onderzoeksrapport 2026-11-14

Dit rapport test varianten van beide strategieën op echte koersen en kijkt wat de bots leren van hun eigen trades. **Er wordt niets automatisch aangepast.** Een aanbevolen variant gaat pas in productie als jij (of iemand die je vertrouwt) de instelling in de code aanpast; daarna draait de backtest opnieuw en loopt de nieuwe versie eerst weken mee op papier.

> Resultaten uit het verleden zijn geen garantie. De aandelenlijst is in 2026 gekozen (survivorship bias).

## Trend-agent

Periode 2016-11-14 t/m 2026-11-14. Ontwikkeldeel 2016-11-14 t/m 2023-11-14, holdout 2023-11-15 t/m 2026-11-14. 9 varianten getest tegen productie.

### Uitkomst

- **rem-pas-na-5-verliezen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.64 vs productie 0.74 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.54 vs 0.46
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -12.8% vs -13.7%
    - ✗ Dubbele kosten en slippage: Sharpe 0.18 vs 0.31
    - ✓ Genoeg trades: 1006 afgesloten trades (nodig: 30)
- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.61 vs productie 0.74 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.31 vs 0.46
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -22.0% vs -13.7%
    - ✗ Dubbele kosten en slippage: Sharpe 0.21 vs 0.31
    - ✓ Genoeg trades: 841 afgesloten trades (nodig: 30)
- **koop-bij-nieuwe-top: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.78 vs productie 0.74 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.37 vs 0.46
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -15.9% vs -13.7%
    - ✗ Dubbele kosten en slippage: Sharpe 0.26 vs 0.31
    - ✓ Genoeg trades: 862 afgesloten trades (nodig: 30)
- **verkoop-na-2-rode-trendkaarsen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe -0.22 vs productie 0.74 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.15 vs 0.46
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -39.2% vs -13.7%
    - ✗ Dubbele kosten en slippage: Sharpe -3.56 vs 0.31
    - ✓ Genoeg trades: 3444 afgesloten trades (nodig: 30)
- **4-plekken: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.71 vs productie 0.74 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.00 vs 0.46
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -18.3% vs -13.7%
    - ✗ Dubbele kosten en slippage: Sharpe 0.01 vs 0.31
    - ✓ Genoeg trades: 518 afgesloten trades (nodig: 30)
- **5-plekken: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.47 vs productie 0.74 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.07 vs 0.46
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -16.0% vs -13.7%
    - ✗ Dubbele kosten en slippage: Sharpe 0.02 vs 0.31
    - ✓ Genoeg trades: 631 afgesloten trades (nodig: 30)
- **meer-per-aankoop: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.70 vs productie 0.74 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.19 vs 0.46
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -21.5% vs -13.7%
    - ✗ Dubbele kosten en slippage: Sharpe 0.28 vs 0.31
    - ✓ Genoeg trades: 989 afgesloten trades (nodig: 30)
- **veel-meer-per-aankoop: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.57 vs productie 0.74 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.57 vs 0.46
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -25.8% vs -13.7%
    - ✓ Dubbele kosten en slippage: Sharpe 0.39 vs 0.31
    - ✓ Genoeg trades: 952 afgesloten trades (nodig: 30)
- **rest-in-wereld-etf: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 1.00 vs productie 0.74 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.45 vs 0.46
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -27.6% vs -13.7%
    - ✓ Dubbele kosten en slippage: Sharpe 0.47 vs 0.31
    - ✓ Genoeg trades: 988 afgesloten trades (nodig: 30)

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +101.9% | +7.3% | -13.7% | 0.54 | 0.74 | 0.31 | 989 | 38% | 2.12 |
| rem-pas-na-5-verliezen | +111.8% | +7.8% | -12.8% | 0.57 | 0.64 | 0.18 | 1006 | 39% | 2.06 |
| regimefilter | +58.6% | +4.7% | -22.0% | 0.41 | 0.61 | 0.21 | 841 | 35% | 2.20 |
| koop-bij-nieuwe-top | +84.4% | +6.3% | -15.9% | 0.50 | 0.78 | 0.26 | 862 | 36% | 2.29 |
| verkoop-na-2-rode-trendkaarsen | -23.4% | -2.6% | -39.2% | -0.18 | -0.22 | -3.56 | 3444 | 36% | 1.62 |
| 4-plekken | +19.1% | +1.8% | -18.3% | 0.23 | 0.71 | 0.01 | 518 | 36% | 2.01 |
| 5-plekken | +14.4% | +1.4% | -16.0% | 0.19 | 0.47 | 0.02 | 631 | 36% | 1.94 |
| meer-per-aankoop | +48.3% | +4.0% | -21.5% | 0.34 | 0.70 | 0.28 | 989 | 37% | 2.01 |
| veel-meer-per-aankoop | +146.0% | +9.4% | -25.8% | 0.56 | 0.57 | 0.39 | 952 | 36% | 2.30 |
| rest-in-wereld-etf | +150.0% | +9.6% | -27.6% | 0.60 | 1.00 | 0.47 | 988 | 37% | 2.13 |

### Per periode (rendement)

| Variant | Nov 2016–Nov 2018 | Nov 2018–Nov 2020 | Nov 2020–Nov 2022 | Nov 2022–Nov 2024 | Nov 2024–Nov 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +18.8% | +19.3% | -0.1% | +17.5% | +19.1% |
| rem-pas-na-5-verliezen | +16.8% | +22.1% | +11.9% | +20.4% | +8.9% |
| regimefilter | +25.1% | +13.4% | -7.5% | +5.2% | +13.6% |
| koop-bij-nieuwe-top | +11.5% | +3.9% | +5.5% | +24.0% | +18.6% |
| verkoop-na-2-rode-trendkaarsen | +10.4% | -1.1% | -3.9% | -24.1% | -5.0% |
| 4-plekken | +1.6% | +11.4% | -14.4% | +9.6% | +10.7% |
| 5-plekken | +3.5% | +10.1% | -12.3% | +3.7% | +10.1% |
| meer-per-aankoop | +12.7% | +14.7% | -17.6% | +20.5% | +14.2% |
| veel-meer-per-aankoop | +40.5% | +35.5% | -1.2% | +15.9% | +10.5% |
| rest-in-wereld-etf | +18.3% | +24.3% | +4.7% | +21.3% | +30.9% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (veel-meer-per-aankoop, veel-meer-per-aankoop, veel-meer-per-aankoop, rem-pas-na-5-verliezen), was het resultaat over de laatste 4 periodes +69.0%, tegen +66.6% voor gewoon productie houden. Bijsturen hielp hier, maar met zo weinig periodes kan dat toeval zijn.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | -1% (204 d) | -2% (69 d) | +12% (163 d) | +226% (3 d) | +5% (351 d) | +2% (882 d) | +7% (1405 d) | +3% (161 d) | +6% (126 d) | +8% (274 d) |
| rem-pas-na-5-verliezen | -2% (204 d) | +10% (69 d) | +13% (163 d) | +226% (3 d) | +6% (350 d) | +3% (882 d) | +7% (1402 d) | +3% (157 d) | -4% (126 d) | +12% (274 d) |
| regimefilter | -2% (204 d) | +3% (69 d) | +4% (163 d) | +226% (3 d) | +2% (346 d) | +0% (882 d) | +7% (1397 d) | -8% (159 d) | +5% (126 d) | +7% (269 d) |
| koop-bij-nieuwe-top | -6% (199 d) | +6% (69 d) | +14% (163 d) | -19% (3 d) | +19% (350 d) | +3% (882 d) | +4% (1402 d) | +3% (160 d) | -8% (126 d) | +4% (269 d) |
| verkoop-na-2-rode-trendkaarsen | -1% (192 d) | -13% (61 d) | +11% (146 d) | +231% (3 d) | +1% (348 d) | -8% (852 d) | +2% (1350 d) | +7% (151 d) | -5% (124 d) | -12% (265 d) |
| 4-plekken | -2% (204 d) | +0% (68 d) | +4% (159 d) | +58% (3 d) | +1% (344 d) | -3% (879 d) | +5% (1404 d) | +2% (147 d) | -6% (126 d) | +1% (273 d) |
| 5-plekken | -1% (204 d) | +4% (68 d) | +7% (159 d) | +42% (3 d) | +0% (348 d) | -1% (882 d) | +3% (1397 d) | -4% (157 d) | -2% (126 d) | +1% (274 d) |
| meer-per-aankoop | -7% (204 d) | +2% (69 d) | +14% (163 d) | +100% (3 d) | +3% (351 d) | -1% (882 d) | +5% (1405 d) | +3% (161 d) | -2% (126 d) | +10% (274 d) |
| veel-meer-per-aankoop | +1% (204 d) | +12% (69 d) | +10% (163 d) | +196% (3 d) | +10% (351 d) | +4% (882 d) | +9% (1400 d) | +13% (161 d) | -14% (126 d) | +9% (274 d) |
| rest-in-wereld-etf | +25% (204 d) | -5% (69 d) | +25% (163 d) | +265% (3 d) | +9% (348 d) | +1% (882 d) | +9% (1405 d) | -6% (160 d) | -7% (126 d) | +4% (274 d) |

## Trend-agent: lessen uit 10 jaar backtest (productie)

989 afgesloten trades, 38% winst, gemiddeld +0.12 R per trade (mediaan -0.36 R), totaal €8,821, gemiddeld 26 dagen vastgehouden.

### Bevindingen

- Zwakte: RSI bij instap = 70-80: gemiddeld -0.33 R over 41 trades (-0.46 R t.o.v. de rest, t = -2.7). Te testen via instelling `max_rsi_entry`.
- Zwakte: Marktbeweeglijkheid bij instap = laag: gemiddeld -0.09 R over 267 trades (-0.29 R t.o.v. de rest, t = -2.6). Te testen via instelling `regime_filter`.
- Sterkte: Marktbeweeglijkheid bij instap = normaal: gemiddeld +0.23 R over 491 trades (+0.23 R t.o.v. de rest, t = 2.1). Te testen via instelling `regime_filter`.

_Dit zijn hypotheses. Een regel verandert pas na een test op ongeziene data (zie het onderzoeksrapport)._

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend | 700 | 37% | +0.09 | 4,993 |
| zijwaarts | 170 | 38% | +0.08 | 1,584 |
| dalend | 111 | 42% | +0.21 | 1,515 |
| onbekend (te weinig) | 8 | 62% | +1.80 | 729 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 491 | 38% | +0.23 | 7,162 |
| laag | 267 | 33% | -0.09 | 181 |
| hoog | 223 | 42% | +0.06 | 749 |
| onbekend (te weinig) | 8 | 62% | +1.80 | 729 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 50-60 | 459 | 40% | +0.17 | 5,591 |
| 60-70 | 364 | 38% | +0.10 | 2,864 |
| onder 50 | 125 | 32% | +0.14 | 1,117 |
| 70-80 | 41 | 32% | -0.33 | -752 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| negatief | 697 | 36% | +0.13 | 6,418 |
| positief | 292 | 41% | +0.10 | 2,403 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| hoger (>1,1) | 402 | 42% | +0.22 | 5,570 |
| normaal | 398 | 36% | +0.10 | 2,923 |
| lager (<0,9) | 189 | 33% | -0.07 | 328 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% | 538 | 37% | +0.04 | 2,032 |
| meer dan 25% | 285 | 39% | +0.19 | 4,113 |
| tot 10% | 166 | 40% | +0.24 | 2,676 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 573 | 36% | +0.06 | 2,718 |
| wild (>3%) | 238 | 43% | +0.29 | 4,728 |
| rustig (<1,5%) | 178 | 35% | +0.08 | 1,374 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt | 830 | 43% | +0.20 | 12,286 |
| trend gebroken (slot onder 50-daags gemiddelde) | 159 | 13% | -0.35 | -3,465 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| lang (>30 d) | 353 | 80% | +1.43 | 33,626 |
| middel | 339 | 27% | -0.34 | -7,377 |
| kort (<10 d) | 297 | 0% | -0.93 | -17,428 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-eaf4f8 | 989 | 38% | +0.12 | 8,821 |

## Trend-agent: lessen uit het oefenen (nepgeld, live)

Live van 2026-10-13 t/m 2026-11-13 (24 handelsdagen): bot +0.33%, wereld-ETF -1.39%, verschil +1.72%.

Live pas 5 afgesloten trades (gemiddeld -0.87 R); vanaf 20 trades is een vergelijking met de backtest (+0.12 R) zinvol.

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

Periode 2016-11-14 t/m 2026-11-13. Ontwikkeldeel 2016-11-14 t/m 2023-11-13, holdout 2023-11-14 t/m 2026-11-13. 6 varianten getest tegen productie.

### Uitkomst

- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.51 vs productie 1.57 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.97 vs 1.13
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -36.7% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.12 vs 1.25
- **satelliet-3-aandelen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.56 vs productie 1.57 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 1.15 vs 1.13
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -38.1% vs -36.7%
    - ✓ Dubbele kosten en slippage: Sharpe 1.26 vs 1.25
- **zonder-crypto: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.60 vs productie 1.57 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.88 vs 1.13
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -34.8% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.08 vs 1.25
- **minder-satelliet: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.60 vs productie 1.57 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 1.08 vs 1.13
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -35.3% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.21 vs 1.25
- **hooguit-1-per-sector: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.48 vs productie 1.57 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 1.12 vs 1.13
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -35.7% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.21 vs 1.25
- **voorzichtig: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.59 vs productie 1.57 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.99 vs 1.13
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -33.9% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.14 vs 1.25

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +809.5% | +24.7% | -36.7% | 1.27 | 1.57 | 1.25 | 291 | 73% | 1.52 |
| regimefilter | +561.9% | +20.8% | -36.7% | 1.14 | 1.51 | 1.12 | 287 | 71% | 1.40 |
| satelliet-3-aandelen | +973.7% | +26.8% | -38.1% | 1.28 | 1.56 | 1.26 | 243 | 74% | 1.34 |
| zonder-crypto | +543.5% | +20.5% | -34.8% | 1.11 | 1.60 | 1.08 | 248 | 72% | 1.50 |
| minder-satelliet | +565.1% | +20.9% | -35.3% | 1.23 | 1.60 | 1.21 | 271 | 69% | 2.12 |
| hooguit-1-per-sector | +620.4% | +21.8% | -35.7% | 1.23 | 1.48 | 1.21 | 334 | 71% | 1.20 |
| voorzichtig | +489.0% | +19.4% | -33.9% | 1.16 | 1.59 | 1.14 | 293 | 68% | 1.67 |

### Per periode (rendement)

| Variant | Nov 2016–Nov 2018 | Nov 2018–Nov 2020 | Nov 2020–Nov 2022 | Nov 2022–Nov 2024 | Nov 2024–Nov 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +49.1% | +58.0% | +45.9% | +72.2% | +55.2% |
| regimefilter | +49.0% | +21.1% | +49.8% | +67.4% | +48.4% |
| satelliet-3-aandelen | +60.5% | +56.8% | +44.9% | +80.2% | +64.6% |
| zonder-crypto | +30.3% | +48.8% | +24.7% | +65.4% | +62.7% |
| minder-satelliet | +43.1% | +43.5% | +46.7% | +59.3% | +39.9% |
| hooguit-1-per-sector | +43.8% | +46.7% | +46.1% | +77.2% | +32.9% |
| voorzichtig | +34.7% | +41.6% | +36.3% | +58.7% | +44.1% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (satelliet-3-aandelen, satelliet-3-aandelen, productie, hooguit-1-per-sector), was het resultaat over de laatste 4 periodes +419.8%, tegen +516.3% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +59% (147 d) | +18% (51 d) | +65% (117 d) | +122% (3 d) | +22% (257 d) | +21% (624 d) | +18% (1008 d) | -2% (118 d) | -5% (90 d) | +30% (194 d) |
| regimefilter | +43% (147 d) | +11% (51 d) | +41% (117 d) | +122% (3 d) | +23% (257 d) | +22% (624 d) | +18% (1008 d) | -4% (118 d) | -6% (90 d) | +14% (194 d) |
| satelliet-3-aandelen | +60% (147 d) | +20% (51 d) | +69% (117 d) | +154% (3 d) | +32% (257 d) | +23% (624 d) | +17% (1008 d) | +6% (118 d) | +0% (90 d) | +32% (194 d) |
| zonder-crypto | +63% (147 d) | +18% (51 d) | +70% (117 d) | +109% (3 d) | +20% (257 d) | +16% (624 d) | +15% (1008 d) | +5% (118 d) | -11% (90 d) | +15% (194 d) |
| minder-satelliet | +58% (147 d) | +20% (51 d) | +57% (117 d) | +133% (3 d) | +15% (257 d) | +20% (624 d) | +15% (1008 d) | -2% (118 d) | -9% (90 d) | +21% (194 d) |
| hooguit-1-per-sector | +59% (147 d) | +17% (51 d) | +55% (117 d) | +139% (3 d) | +21% (257 d) | +19% (624 d) | +16% (1008 d) | -6% (118 d) | -4% (90 d) | +28% (194 d) |
| voorzichtig | +59% (147 d) | +18% (51 d) | +61% (117 d) | +123% (3 d) | +17% (257 d) | +16% (624 d) | +14% (1008 d) | +3% (118 d) | -9% (90 d) | +16% (194 d) |

## Investeerder live (nepgeld)

Van 2026-10-13 t/m 2026-11-13: investeerder -6.18%, wereld-ETF -1.39%, verschil -4.79%.
