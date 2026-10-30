# Onderzoeksrapport 2026-10-30

Dit rapport test varianten van beide strategieën op echte koersen en kijkt wat de bots leren van hun eigen trades. **Er wordt niets automatisch aangepast.** Een aanbevolen variant gaat pas in productie als jij (of iemand die je vertrouwt) de instelling in de code aanpast; daarna draait de backtest opnieuw en loopt de nieuwe versie eerst weken mee op papier.

> Resultaten uit het verleden zijn geen garantie. De aandelenlijst is in 2026 gekozen (survivorship bias).

## Trend-agent

Periode 2016-10-30 t/m 2026-10-30. Ontwikkeldeel 2016-10-30 t/m 2023-11-01, holdout 2023-11-02 t/m 2026-10-30. 10 varianten getest tegen productie.

### Uitkomst

- **rem-pas-na-5-verliezen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.64 vs productie 0.68 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.43 vs 0.54
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -16.7% vs -17.5%
    - ✓ Dubbele kosten en slippage: Sharpe 0.35 vs 0.30
    - ✓ Genoeg trades: 936 afgesloten trades (nodig: 30)
- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.38 vs productie 0.68 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.49 vs 0.54
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -19.3% vs -17.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.26 vs 0.30
    - ✓ Genoeg trades: 788 afgesloten trades (nodig: 30)
- **koop-na-terugval: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.83 vs productie 0.68 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.37 vs 0.54
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -14.9% vs -17.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.26 vs 0.30
    - ✓ Genoeg trades: 932 afgesloten trades (nodig: 30)
- **koop-bij-nieuwe-top: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.67 vs productie 0.68 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.38 vs 0.54
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -15.3% vs -17.5%
    - ✓ Dubbele kosten en slippage: Sharpe 0.43 vs 0.30
    - ✓ Genoeg trades: 865 afgesloten trades (nodig: 30)
- **verkoop-na-2-rode-trendkaarsen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe -0.06 vs productie 0.68 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.24 vs 0.54
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -37.8% vs -17.5%
    - ✗ Dubbele kosten en slippage: Sharpe -2.75 vs 0.30
    - ✓ Genoeg trades: 2755 afgesloten trades (nodig: 30)
- **4-plekken: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.11 vs productie 0.68 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.15 vs 0.54
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -16.5% vs -17.5%
    - ✗ Dubbele kosten en slippage: Sharpe -0.11 vs 0.30
    - ✓ Genoeg trades: 497 afgesloten trades (nodig: 30)
- **5-plekken: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.01 vs productie 0.68 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.15 vs 0.54
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -15.0% vs -17.5%
    - ✗ Dubbele kosten en slippage: Sharpe -0.13 vs 0.30
    - ✓ Genoeg trades: 614 afgesloten trades (nodig: 30)
- **meer-per-aankoop: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.31 vs productie 0.68 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.41 vs 0.54
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -16.6% vs -17.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.13 vs 0.30
    - ✓ Genoeg trades: 944 afgesloten trades (nodig: 30)
- **veel-meer-per-aankoop: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.10 vs productie 0.68 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.37 vs 0.54
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -28.5% vs -17.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.21 vs 0.30
    - ✓ Genoeg trades: 913 afgesloten trades (nodig: 30)
- **rest-in-wereld-etf: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.75 vs productie 0.68 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.51 vs 0.54
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -26.3% vs -17.5%
    - ✓ Dubbele kosten en slippage: Sharpe 0.38 vs 0.30
    - ✓ Genoeg trades: 926 afgesloten trades (nodig: 30)

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +117.3% | +8.1% | -17.5% | 0.59 | 0.68 | 0.30 | 927 | 36% | 2.34 |
| rem-pas-na-5-verliezen | +91.9% | +6.7% | -16.7% | 0.50 | 0.64 | 0.35 | 936 | 37% | 2.18 |
| regimefilter | +72.3% | +5.6% | -19.3% | 0.46 | 0.38 | 0.26 | 788 | 34% | 2.38 |
| koop-na-terugval | +89.6% | +6.6% | -14.9% | 0.53 | 0.83 | 0.26 | 932 | 37% | 2.20 |
| koop-bij-nieuwe-top | +80.3% | +6.1% | -15.3% | 0.47 | 0.67 | 0.43 | 865 | 35% | 2.31 |
| verkoop-na-2-rode-trendkaarsen | -25.0% | -2.8% | -37.8% | -0.18 | -0.06 | -2.75 | 2755 | 36% | 1.64 |
| 4-plekken | +10.8% | +1.0% | -16.5% | 0.15 | 0.11 | -0.11 | 497 | 35% | 1.97 |
| 5-plekken | +6.9% | +0.7% | -15.0% | 0.11 | 0.01 | -0.13 | 614 | 32% | 2.13 |
| meer-per-aankoop | +57.0% | +4.6% | -16.6% | 0.38 | 0.31 | 0.13 | 944 | 35% | 2.24 |
| veel-meer-per-aankoop | +49.1% | +4.1% | -28.5% | 0.28 | 0.10 | 0.21 | 913 | 32% | 2.29 |
| rest-in-wereld-etf | +142.8% | +9.3% | -26.3% | 0.59 | 0.75 | 0.38 | 926 | 35% | 2.37 |

### Per periode (rendement)

| Variant | Oct 2016–Oct 2018 | Oct 2018–Nov 2020 | Nov 2020–Oct 2022 | Nov 2022–Oct 2024 | Oct 2024–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +14.8% | +13.1% | +13.0% | +24.1% | +17.3% |
| rem-pas-na-5-verliezen | +13.5% | +11.7% | +6.9% | +23.7% | +12.8% |
| regimefilter | +26.8% | +7.9% | +12.0% | +3.3% | +7.1% |
| koop-na-terugval | +14.8% | +16.5% | +2.5% | +15.6% | +18.2% |
| koop-bij-nieuwe-top | +25.2% | -2.6% | +8.3% | +14.6% | +19.6% |
| verkoop-na-2-rode-trendkaarsen | -7.5% | -4.6% | +5.8% | -21.8% | +0.2% |
| 4-plekken | +1.5% | +2.6% | -7.1% | +15.9% | -2.4% |
| 5-plekken | +1.6% | +1.8% | -6.8% | +10.3% | -0.9% |
| meer-per-aankoop | +16.6% | +10.7% | -1.5% | +18.9% | +2.4% |
| veel-meer-per-aankoop | +11.0% | +30.0% | +3.6% | -6.5% | +3.9% |
| rest-in-wereld-etf | +14.0% | +11.2% | +24.5% | +22.4% | +22.7% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (regimefilter, regimefilter, regimefilter, productie), was het resultaat over de laatste 4 periodes +46.4%, tegen +86.0% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | -7% (205 d) | +13% (69 d) | +18% (163 d) | -229% (4 d) | +8% (345 d) | +6% (885 d) | +6% (1406 d) | +2% (166 d) | +0% (126 d) | +11% (274 d) |
| rem-pas-na-5-verliezen | -5% (205 d) | +17% (69 d) | +18% (163 d) | -229% (4 d) | +9% (342 d) | +4% (885 d) | +6% (1406 d) | -5% (162 d) | -2% (126 d) | +7% (269 d) |
| regimefilter | -3% (202 d) | +5% (69 d) | -0% (162 d) | -229% (4 d) | +7% (345 d) | +4% (883 d) | +5% (1406 d) | -1% (164 d) | +2% (126 d) | +10% (273 d) |
| koop-na-terugval | -2% (205 d) | -5% (69 d) | +11% (163 d) | -183% (4 d) | +5% (343 d) | +2% (885 d) | +9% (1401 d) | +0% (156 d) | -5% (126 d) | +6% (274 d) |
| koop-bij-nieuwe-top | -2% (205 d) | +22% (69 d) | +13% (163 d) | -137% (4 d) | +20% (344 d) | +8% (885 d) | +1% (1406 d) | +1% (163 d) | -8% (126 d) | +1% (269 d) |
| verkoop-na-2-rode-trendkaarsen | -9% (200 d) | -3% (69 d) | +9% (157 d) | -198% (4 d) | +8% (342 d) | -4% (861 d) | -1% (1371 d) | -7% (155 d) | -13% (123 d) | +0% (269 d) |
| 4-plekken | -6% (203 d) | +4% (69 d) | +1% (163 d) | -115% (4 d) | +3% (337 d) | +1% (880 d) | +1% (1399 d) | -4% (159 d) | +0% (126 d) | +7% (274 d) |
| 5-plekken | -2% (196 d) | +11% (69 d) | +5% (163 d) | -72% (4 d) | +1% (344 d) | +1% (885 d) | +0% (1406 d) | -6% (149 d) | -1% (126 d) | +4% (269 d) |
| meer-per-aankoop | -8% (203 d) | +7% (69 d) | +16% (163 d) | -151% (4 d) | +4% (345 d) | +2% (885 d) | +5% (1406 d) | -1% (164 d) | +0% (126 d) | +7% (274 d) |
| veel-meer-per-aankoop | -4% (205 d) | +12% (68 d) | +22% (159 d) | -259% (4 d) | +4% (345 d) | +1% (885 d) | +6% (1402 d) | -4% (164 d) | -3% (126 d) | +3% (274 d) |
| rest-in-wereld-etf | +13% (205 d) | +13% (69 d) | +31% (163 d) | -229% (4 d) | +8% (345 d) | +6% (885 d) | +6% (1406 d) | -7% (166 d) | -2% (126 d) | +7% (274 d) |

## Trend-agent: lessen uit 10 jaar backtest (productie)

927 afgesloten trades, 36% winst, gemiddeld +0.14 R per trade (mediaan -0.41 R), totaal €10,073, gemiddeld 28 dagen vastgehouden.

### Bevindingen

- Geen overtuigende verschillen (minimaal 20 trades per groep, verschil ≥ 0.15 R en t ≥ 2.0).

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend | 650 | 35% | +0.10 | 6,056 |
| zijwaarts | 146 | 40% | +0.22 | 3,100 |
| dalend | 123 | 38% | +0.21 | 720 |
| onbekend (te weinig) | 8 | 12% | +0.48 | 197 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 467 | 39% | +0.22 | 7,290 |
| laag | 229 | 32% | +0.04 | 2,164 |
| hoog | 223 | 36% | +0.07 | 421 |
| onbekend (te weinig) | 8 | 12% | +0.48 | 197 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 60-70 | 424 | 39% | +0.25 | 8,906 |
| 50-60 | 235 | 37% | +0.17 | 2,415 |
| 70-80 | 223 | 30% | -0.05 | -1,039 |
| onder 50 | 45 | 31% | -0.09 | -209 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| positief | 480 | 37% | +0.14 | 5,235 |
| negatief | 447 | 35% | +0.13 | 4,838 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| hoger (>1,1) | 410 | 37% | +0.17 | 5,498 |
| normaal | 352 | 35% | +0.09 | 2,019 |
| lager (<0,9) | 165 | 36% | +0.17 | 2,556 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% | 482 | 35% | +0.11 | 3,978 |
| meer dan 25% | 310 | 38% | +0.18 | 4,346 |
| tot 10% | 135 | 35% | +0.15 | 1,749 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 507 | 35% | +0.16 | 6,010 |
| wild (>3%) | 237 | 39% | +0.14 | 2,684 |
| rustig (<1,5%) | 183 | 36% | +0.07 | 1,378 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt | 832 | 39% | +0.18 | 12,057 |
| trend gebroken (slot onder 50-daags gemiddelde) | 95 | 13% | -0.26 | -1,985 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| lang (>30 d) | 358 | 75% | +1.42 | 35,911 |
| middel | 303 | 22% | -0.42 | -9,039 |
| kort (<10 d) | 266 | 0% | -0.95 | -16,799 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-081d85 | 927 | 36% | +0.14 | 10,073 |

## Trend-agent: lessen uit het oefenen (nepgeld, live)

Live van 2026-10-13 t/m 2026-10-29 (13 handelsdagen): bot +0.53%, wereld-ETF -0.53%, verschil +1.06%.

Nog geen afgesloten trades om van te leren.

## Investeerder

Periode 2016-10-31 t/m 2026-10-30. Ontwikkeldeel 2016-10-31 t/m 2023-10-30, holdout 2023-10-31 t/m 2026-10-30. 2 varianten getest tegen productie.

### Uitkomst

- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.69 vs productie 1.76 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.95 vs 1.11
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -36.7% vs -36.8%
    - ✗ Dubbele kosten en slippage: Sharpe 1.16 vs 1.29
- **satelliet-3-aandelen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.72 vs productie 1.76 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 1.13 vs 1.11
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -38.1% vs -36.8%
    - ✓ Dubbele kosten en slippage: Sharpe 1.29 vs 1.29

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +870.2% | +25.5% | -36.8% | 1.31 | 1.76 | 1.29 | 285 | 73% | 1.61 |
| regimefilter | +605.0% | +21.6% | -36.7% | 1.18 | 1.69 | 1.16 | 282 | 71% | 1.49 |
| satelliet-3-aandelen | +1035.8% | +27.5% | -38.1% | 1.31 | 1.72 | 1.29 | 243 | 74% | 1.43 |

### Per periode (rendement)

| Variant | Oct 2016–Oct 2018 | Oct 2018–Oct 2020 | Oct 2020–Oct 2022 | Nov 2022–Oct 2024 | Oct 2024–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +50.1% | +46.3% | +61.0% | +56.6% | +75.7% |
| regimefilter | +50.1% | +12.3% | +62.8% | +53.2% | +68.1% |
| satelliet-3-aandelen | +61.1% | +46.3% | +59.3% | +59.3% | +89.8% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (satelliet-3-aandelen, satelliet-3-aandelen, productie, productie), was het resultaat over de laatste 4 periodes +541.3%, tegen +547.8% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +59% (147 d) | +18% (51 d) | +65% (117 d) | -287% (3 d) | +19% (251 d) | +22% (625 d) | +22% (1013 d) | -2% (118 d) | -5% (90 d) | +30% (194 d) |
| regimefilter | +43% (147 d) | +11% (51 d) | +41% (117 d) | -287% (3 d) | +19% (251 d) | +22% (625 d) | +22% (1013 d) | -4% (118 d) | -6% (90 d) | +14% (194 d) |
| satelliet-3-aandelen | +60% (147 d) | +20% (51 d) | +69% (117 d) | -336% (3 d) | +27% (251 d) | +23% (625 d) | +21% (1013 d) | +6% (118 d) | +0% (90 d) | +32% (194 d) |

## Investeerder live (nepgeld)

Van 2026-10-13 t/m 2026-10-29: investeerder -2.17%, wereld-ETF -0.53%, verschil -1.65%.
