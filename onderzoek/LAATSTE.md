# Onderzoeksrapport 2026-10-31

Dit rapport test varianten van beide strategieën op echte koersen en kijkt wat de bots leren van hun eigen trades. **Er wordt niets automatisch aangepast.** Een aanbevolen variant gaat pas in productie als jij (of iemand die je vertrouwt) de instelling in de code aanpast; daarna draait de backtest opnieuw en loopt de nieuwe versie eerst weken mee op papier.

> Resultaten uit het verleden zijn geen garantie. De aandelenlijst is in 2026 gekozen (survivorship bias).

## Trend-agent

Periode 2016-10-31 t/m 2026-10-31. Ontwikkeldeel 2016-10-31 t/m 2023-11-02, holdout 2023-11-03 t/m 2026-10-31. 10 varianten getest tegen productie.

### Uitkomst

- **rem-pas-na-5-verliezen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.63 vs productie 0.62 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.48 vs 0.54
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -16.7% vs -17.5%
    - ✓ Dubbele kosten en slippage: Sharpe 0.35 vs 0.31
    - ✓ Genoeg trades: 947 afgesloten trades (nodig: 30)
- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.37 vs productie 0.62 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.46 vs 0.54
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -18.9% vs -17.5%
    - ✓ Dubbele kosten en slippage: Sharpe 0.33 vs 0.31
    - ✓ Genoeg trades: 787 afgesloten trades (nodig: 30)
- **koop-na-terugval: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.89 vs productie 0.62 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.40 vs 0.54
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -14.8% vs -17.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.30 vs 0.31
    - ✓ Genoeg trades: 944 afgesloten trades (nodig: 30)
- **koop-bij-nieuwe-top: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.87 vs productie 0.62 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.48 vs 0.54
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -13.5% vs -17.5%
    - ✓ Dubbele kosten en slippage: Sharpe 0.42 vs 0.31
    - ✓ Genoeg trades: 851 afgesloten trades (nodig: 30)
- **verkoop-na-2-rode-trendkaarsen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe -0.13 vs productie 0.62 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.11 vs 0.54
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -40.0% vs -17.5%
    - ✗ Dubbele kosten en slippage: Sharpe -2.72 vs 0.31
    - ✓ Genoeg trades: 2768 afgesloten trades (nodig: 30)
- **4-plekken: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.15 vs productie 0.62 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.17 vs 0.54
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -16.5% vs -17.5%
    - ✗ Dubbele kosten en slippage: Sharpe -0.11 vs 0.31
    - ✓ Genoeg trades: 497 afgesloten trades (nodig: 30)
- **5-plekken: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe -0.28 vs productie 0.62 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.10 vs 0.54
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -15.2% vs -17.5%
    - ✗ Dubbele kosten en slippage: Sharpe -0.12 vs 0.31
    - ✓ Genoeg trades: 620 afgesloten trades (nodig: 30)
- **meer-per-aankoop: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.43 vs productie 0.62 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.37 vs 0.54
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -19.2% vs -17.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.12 vs 0.31
    - ✓ Genoeg trades: 942 afgesloten trades (nodig: 30)
- **veel-meer-per-aankoop: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.11 vs productie 0.62 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.40 vs 0.54
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -25.7% vs -17.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.30 vs 0.31
    - ✓ Genoeg trades: 890 afgesloten trades (nodig: 30)
- **rest-in-wereld-etf: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.79 vs productie 0.62 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.58 vs 0.54
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -26.2% vs -17.5%
    - ✓ Dubbele kosten en slippage: Sharpe 0.39 vs 0.31
    - ✓ Genoeg trades: 929 afgesloten trades (nodig: 30)

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +106.2% | +7.5% | -17.5% | 0.55 | 0.62 | 0.31 | 929 | 36% | 2.30 |
| rem-pas-na-5-verliezen | +95.4% | +6.9% | -16.7% | 0.51 | 0.63 | 0.35 | 947 | 36% | 2.20 |
| regimefilter | +62.2% | +5.0% | -18.9% | 0.42 | 0.37 | 0.33 | 787 | 34% | 2.35 |
| koop-na-terugval | +92.1% | +6.7% | -14.8% | 0.53 | 0.89 | 0.30 | 944 | 36% | 2.30 |
| koop-bij-nieuwe-top | +116.3% | +8.0% | -13.5% | 0.60 | 0.87 | 0.42 | 851 | 37% | 2.33 |
| verkoop-na-2-rode-trendkaarsen | -19.9% | -2.2% | -40.0% | -0.13 | -0.13 | -2.72 | 2768 | 36% | 1.63 |
| 4-plekken | +10.8% | +1.0% | -16.5% | 0.15 | 0.15 | -0.11 | 497 | 35% | 1.97 |
| 5-plekken | -4.9% | -0.5% | -15.2% | -0.03 | -0.28 | -0.12 | 620 | 33% | 1.92 |
| meer-per-aankoop | +55.2% | +4.5% | -19.2% | 0.38 | 0.43 | 0.12 | 942 | 34% | 2.24 |
| veel-meer-per-aankoop | +52.0% | +4.3% | -25.7% | 0.29 | 0.11 | 0.30 | 890 | 33% | 2.21 |
| rest-in-wereld-etf | +162.0% | +10.1% | -26.2% | 0.63 | 0.79 | 0.39 | 929 | 36% | 2.35 |

### Per periode (rendement)

| Variant | Oct 2016–Oct 2018 | Nov 2018–Nov 2020 | Nov 2020–Nov 2022 | Nov 2022–Oct 2024 | Oct 2024–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +13.8% | +14.6% | +13.1% | +25.7% | +11.2% |
| rem-pas-na-5-verliezen | +14.0% | +14.6% | +8.6% | +26.0% | +9.7% |
| regimefilter | +22.6% | +8.7% | +12.4% | +2.5% | +5.7% |
| koop-na-terugval | +20.4% | +13.5% | +2.2% | +16.8% | +18.1% |
| koop-bij-nieuwe-top | +28.3% | +3.7% | +8.1% | +15.9% | +30.4% |
| verkoop-na-2-rode-trendkaarsen | -2.4% | -1.0% | +7.3% | -21.0% | -2.8% |
| 4-plekken | +1.4% | +3.2% | -6.6% | +16.5% | -2.0% |
| 5-plekken | +1.3% | -0.6% | -1.8% | +4.9% | -7.2% |
| meer-per-aankoop | +16.6% | +8.9% | -3.5% | +20.6% | +4.6% |
| veel-meer-per-aankoop | +14.1% | +28.3% | +6.9% | -4.9% | +3.2% |
| rest-in-wereld-etf | +15.4% | +18.5% | +24.5% | +25.4% | +22.4% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (koop-bij-nieuwe-top, koop-na-terugval, rest-in-wereld-etf, rest-in-wereld-etf), was het resultaat over de laatste 4 periodes +62.7%, tegen +81.1% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | -8% (205 d) | +13% (69 d) | +19% (163 d) | -295% (3 d) | +8% (345 d) | +5% (885 d) | +6% (1407 d) | +2% (166 d) | +2% (126 d) | +11% (274 d) |
| rem-pas-na-5-verliezen | -4% (205 d) | +12% (69 d) | +18% (163 d) | -295% (3 d) | +10% (342 d) | +3% (885 d) | +6% (1407 d) | -5% (162 d) | +2% (126 d) | +10% (274 d) |
| regimefilter | -4% (202 d) | +8% (69 d) | -0% (163 d) | -295% (3 d) | +7% (345 d) | +3% (883 d) | +5% (1407 d) | -1% (164 d) | +3% (126 d) | +10% (274 d) |
| koop-na-terugval | -2% (205 d) | -5% (69 d) | +8% (163 d) | -233% (3 d) | +6% (343 d) | +5% (885 d) | +8% (1402 d) | +0% (156 d) | -7% (126 d) | +5% (274 d) |
| koop-bij-nieuwe-top | -0% (205 d) | +22% (69 d) | +17% (163 d) | -174% (3 d) | +22% (344 d) | +6% (885 d) | +3% (1407 d) | +2% (163 d) | -5% (126 d) | +4% (269 d) |
| verkoop-na-2-rode-trendkaarsen | -10% (201 d) | -6% (66 d) | +12% (156 d) | -253% (3 d) | +8% (336 d) | -2% (857 d) | -1% (1365 d) | -7% (155 d) | -9% (122 d) | +2% (269 d) |
| 4-plekken | -6% (203 d) | +4% (69 d) | +1% (163 d) | -148% (3 d) | +3% (337 d) | +1% (880 d) | +1% (1400 d) | -4% (159 d) | +0% (126 d) | +7% (274 d) |
| 5-plekken | -4% (199 d) | +2% (69 d) | +2% (163 d) | -90% (3 d) | -0% (342 d) | -1% (877 d) | +0% (1406 d) | -2% (151 d) | -1% (126 d) | +3% (274 d) |
| meer-per-aankoop | -8% (205 d) | +8% (69 d) | +17% (163 d) | -193% (3 d) | +6% (345 d) | +2% (885 d) | +4% (1407 d) | -3% (164 d) | +1% (126 d) | +7% (274 d) |
| veel-meer-per-aankoop | -3% (205 d) | +6% (68 d) | +15% (159 d) | -334% (3 d) | +0% (342 d) | +5% (885 d) | +4% (1407 d) | +4% (164 d) | -6% (126 d) | +9% (274 d) |
| rest-in-wereld-etf | +13% (205 d) | +13% (69 d) | +30% (163 d) | -295% (3 d) | +7% (345 d) | +6% (885 d) | +7% (1407 d) | -7% (166 d) | -2% (126 d) | +8% (274 d) |

## Trend-agent: lessen uit 10 jaar backtest (productie)

929 afgesloten trades, 36% winst, gemiddeld +0.12 R per trade (mediaan -0.40 R), totaal €9,023, gemiddeld 28 dagen vastgehouden.

### Bevindingen

- Geen overtuigende verschillen (minimaal 20 trades per groep, verschil ≥ 0.15 R en t ≥ 2.0).

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend | 655 | 35% | +0.08 | 4,963 |
| zijwaarts | 143 | 39% | +0.25 | 3,039 |
| dalend | 123 | 38% | +0.20 | 824 |
| onbekend (te weinig) | 8 | 12% | +0.48 | 197 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 468 | 39% | +0.23 | 7,622 |
| laag | 228 | 32% | -0.02 | 960 |
| hoog | 225 | 36% | +0.04 | 244 |
| onbekend (te weinig) | 8 | 12% | +0.48 | 197 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 60-70 | 418 | 39% | +0.22 | 7,476 |
| 50-60 | 235 | 36% | +0.12 | 2,006 |
| 70-80 | 231 | 32% | -0.01 | -217 |
| onder 50 | 45 | 29% | -0.11 | -243 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| positief | 485 | 37% | +0.12 | 3,865 |
| negatief | 444 | 35% | +0.13 | 5,157 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| hoger (>1,1) | 406 | 37% | +0.16 | 4,651 |
| normaal | 357 | 35% | +0.06 | 1,404 |
| lager (<0,9) | 166 | 36% | +0.17 | 2,968 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% | 482 | 35% | +0.08 | 3,472 |
| meer dan 25% | 314 | 38% | +0.16 | 3,456 |
| tot 10% | 133 | 35% | +0.18 | 2,094 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 507 | 34% | +0.14 | 4,983 |
| wild (>3%) | 241 | 39% | +0.11 | 1,902 |
| rustig (<1,5%) | 181 | 38% | +0.10 | 2,138 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt | 833 | 39% | +0.17 | 11,009 |
| trend gebroken (slot onder 50-daags gemiddelde) | 96 | 11% | -0.30 | -1,986 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| lang (>30 d) | 357 | 75% | +1.40 | 34,795 |
| middel | 307 | 22% | -0.43 | -9,092 |
| kort (<10 d) | 265 | 0% | -0.96 | -16,680 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-081d85 | 929 | 36% | +0.12 | 9,023 |

## Trend-agent: lessen uit het oefenen (nepgeld, live)

Live van 2026-10-13 t/m 2026-10-30 (14 handelsdagen): bot +0.64%, wereld-ETF -1.94%, verschil +2.58%.

Nog geen afgesloten trades om van te leren.

## Investeerder

Periode 2016-10-31 t/m 2026-10-30. Ontwikkeldeel 2016-10-31 t/m 2023-10-30, holdout 2023-10-31 t/m 2026-10-30. 2 varianten getest tegen productie.

### Uitkomst

- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.70 vs productie 1.76 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.95 vs 1.11
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -36.7% vs -36.8%
    - ✗ Dubbele kosten en slippage: Sharpe 1.16 vs 1.29
- **satelliet-3-aandelen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.72 vs productie 1.76 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 1.12 vs 1.11
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -38.1% vs -36.8%
    - ✓ Dubbele kosten en slippage: Sharpe 1.29 vs 1.29

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +875.1% | +25.6% | -36.8% | 1.31 | 1.76 | 1.29 | 290 | 72% | 1.68 |
| regimefilter | +606.8% | +21.6% | -36.7% | 1.18 | 1.70 | 1.16 | 286 | 70% | 1.53 |
| satelliet-3-aandelen | +1033.7% | +27.5% | -38.1% | 1.31 | 1.72 | 1.29 | 245 | 74% | 1.47 |

### Per periode (rendement)

| Variant | Oct 2016–Oct 2018 | Oct 2018–Oct 2020 | Oct 2020–Oct 2022 | Nov 2022–Oct 2024 | Oct 2024–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +50.5% | +46.3% | +60.9% | +56.9% | +75.9% |
| regimefilter | +50.4% | +12.3% | +62.7% | +53.3% | +68.3% |
| satelliet-3-aandelen | +61.2% | +46.3% | +58.7% | +59.4% | +89.9% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (satelliet-3-aandelen, satelliet-3-aandelen, productie, productie), was het resultaat over de laatste 4 periodes +540.7%, tegen +549.2% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +59% (147 d) | +18% (51 d) | +65% (117 d) | -290% (3 d) | +19% (251 d) | +22% (625 d) | +22% (1013 d) | -2% (118 d) | -5% (90 d) | +30% (194 d) |
| regimefilter | +43% (147 d) | +11% (51 d) | +41% (117 d) | -290% (3 d) | +19% (251 d) | +22% (625 d) | +22% (1013 d) | -4% (118 d) | -6% (90 d) | +14% (194 d) |
| satelliet-3-aandelen | +60% (147 d) | +20% (51 d) | +69% (117 d) | -337% (3 d) | +27% (251 d) | +23% (625 d) | +21% (1013 d) | +6% (118 d) | +0% (90 d) | +32% (194 d) |

## Investeerder live (nepgeld)

Van 2026-10-13 t/m 2026-10-30: investeerder -5.48%, wereld-ETF -1.94%, verschil -3.55%.
