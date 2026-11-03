# Onderzoeksrapport 2026-11-03

Dit rapport test varianten van beide strategieën op echte koersen en kijkt wat de bots leren van hun eigen trades. **Er wordt niets automatisch aangepast.** Een aanbevolen variant gaat pas in productie als jij (of iemand die je vertrouwt) de instelling in de code aanpast; daarna draait de backtest opnieuw en loopt de nieuwe versie eerst weken mee op papier.

> Resultaten uit het verleden zijn geen garantie. De aandelenlijst is in 2026 gekozen (survivorship bias).

## Trend-agent

Periode 2016-11-03 t/m 2026-11-03. Ontwikkeldeel 2016-11-03 t/m 2023-11-03, holdout 2023-11-04 t/m 2026-11-03. 10 varianten getest tegen productie.

### Uitkomst

- **rem-pas-na-5-verliezen: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.75 vs productie 0.60 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.50 vs 0.57
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -17.0% vs -17.0%
    - ✓ Dubbele kosten en slippage: Sharpe 0.41 vs 0.41
    - ✓ Genoeg trades: 937 afgesloten trades (nodig: 30)
- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.37 vs productie 0.60 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.53 vs 0.57
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -18.7% vs -17.0%
    - ✗ Dubbele kosten en slippage: Sharpe 0.31 vs 0.41
    - ✓ Genoeg trades: 781 afgesloten trades (nodig: 30)
- **koop-na-terugval: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 1.04 vs productie 0.60 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.46 vs 0.57
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -15.9% vs -17.0%
    - ✓ Dubbele kosten en slippage: Sharpe 0.43 vs 0.41
    - ✓ Genoeg trades: 932 afgesloten trades (nodig: 30)
- **koop-bij-nieuwe-top: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.85 vs productie 0.60 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.46 vs 0.57
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -12.5% vs -17.0%
    - ✓ Dubbele kosten en slippage: Sharpe 0.42 vs 0.41
    - ✓ Genoeg trades: 846 afgesloten trades (nodig: 30)
- **verkoop-na-2-rode-trendkaarsen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe -0.10 vs productie 0.60 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.18 vs 0.57
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -38.8% vs -17.0%
    - ✗ Dubbele kosten en slippage: Sharpe -3.03 vs 0.41
    - ✓ Genoeg trades: 2766 afgesloten trades (nodig: 30)
- **4-plekken: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.19 vs productie 0.60 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.20 vs 0.57
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -16.8% vs -17.0%
    - ✗ Dubbele kosten en slippage: Sharpe -0.06 vs 0.41
    - ✓ Genoeg trades: 497 afgesloten trades (nodig: 30)
- **5-plekken: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.11 vs productie 0.60 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.02 vs 0.57
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -15.2% vs -17.0%
    - ✗ Dubbele kosten en slippage: Sharpe -0.24 vs 0.41
    - ✓ Genoeg trades: 610 afgesloten trades (nodig: 30)
- **meer-per-aankoop: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.37 vs productie 0.60 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.37 vs 0.57
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -17.3% vs -17.0%
    - ✗ Dubbele kosten en slippage: Sharpe 0.09 vs 0.41
    - ✓ Genoeg trades: 931 afgesloten trades (nodig: 30)
- **veel-meer-per-aankoop: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.37 vs productie 0.60 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.40 vs 0.57
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -25.3% vs -17.0%
    - ✗ Dubbele kosten en slippage: Sharpe 0.15 vs 0.41
    - ✓ Genoeg trades: 892 afgesloten trades (nodig: 30)
- **rest-in-wereld-etf: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.73 vs productie 0.60 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.59 vs 0.57
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -25.4% vs -17.0%
    - ✓ Dubbele kosten en slippage: Sharpe 0.41 vs 0.41
    - ✓ Genoeg trades: 929 afgesloten trades (nodig: 30)

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +115.3% | +8.0% | -17.0% | 0.58 | 0.60 | 0.41 | 920 | 37% | 2.25 |
| rem-pas-na-5-verliezen | +113.0% | +7.9% | -17.0% | 0.57 | 0.75 | 0.41 | 937 | 37% | 2.26 |
| regimefilter | +76.4% | +5.8% | -18.7% | 0.48 | 0.37 | 0.31 | 781 | 34% | 2.37 |
| koop-na-terugval | +127.3% | +8.6% | -15.9% | 0.64 | 1.04 | 0.43 | 932 | 37% | 2.33 |
| koop-bij-nieuwe-top | +112.2% | +7.8% | -12.5% | 0.59 | 0.85 | 0.42 | 846 | 37% | 2.30 |
| verkoop-na-2-rode-trendkaarsen | -22.8% | -2.6% | -38.8% | -0.15 | -0.10 | -3.03 | 2766 | 36% | 1.63 |
| 4-plekken | +16.0% | +1.5% | -16.8% | 0.20 | 0.19 | -0.06 | 497 | 35% | 2.00 |
| 5-plekken | +1.7% | +0.2% | -15.2% | 0.05 | 0.11 | -0.24 | 610 | 33% | 1.98 |
| meer-per-aankoop | +54.0% | +4.4% | -17.3% | 0.37 | 0.37 | 0.09 | 931 | 35% | 2.18 |
| veel-meer-per-aankoop | +80.6% | +6.1% | -25.3% | 0.38 | 0.37 | 0.15 | 892 | 33% | 2.41 |
| rest-in-wereld-etf | +161.3% | +10.1% | -25.4% | 0.63 | 0.73 | 0.41 | 929 | 35% | 2.35 |

### Per periode (rendement)

| Variant | Nov 2016–Nov 2018 | Nov 2018–Nov 2020 | Nov 2020–Nov 2022 | Nov 2022–Nov 2024 | Nov 2024–Nov 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +20.6% | +15.1% | +13.8% | +20.0% | +13.6% |
| rem-pas-na-5-verliezen | +19.0% | +15.5% | +7.7% | +20.8% | +19.1% |
| regimefilter | +32.0% | +12.6% | +9.5% | +0.8% | +7.5% |
| koop-na-terugval | +40.3% | +11.5% | -2.0% | +12.4% | +32.0% |
| koop-bij-nieuwe-top | +26.6% | +4.7% | +9.3% | +12.9% | +29.7% |
| verkoop-na-2-rode-trendkaarsen | -8.3% | +0.4% | +9.4% | -24.7% | +1.8% |
| 4-plekken | +4.4% | +3.2% | -6.5% | +14.7% | +0.3% |
| 5-plekken | -0.2% | +0.7% | -5.4% | +3.9% | +2.9% |
| meer-per-aankoop | +13.1% | +12.4% | -1.0% | +18.3% | +3.4% |
| veel-meer-per-aankoop | +12.5% | +33.3% | +10.9% | +1.4% | +7.2% |
| rest-in-wereld-etf | +20.4% | +22.7% | +19.4% | +20.7% | +22.8% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (koop-na-terugval, koop-na-terugval, regimefilter, rest-in-wereld-etf), was het resultaat over de laatste 4 periodes +35.2%, tegen +78.4% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | -5% (205 d) | +15% (69 d) | +17% (163 d) | +134% (4 d) | +9% (345 d) | +5% (881 d) | +6% (1410 d) | -3% (162 d) | -2% (126 d) | +8% (274 d) |
| rem-pas-na-5-verliezen | -4% (205 d) | +14% (69 d) | +17% (163 d) | +134% (4 d) | +10% (342 d) | +3% (881 d) | +6% (1410 d) | +2% (160 d) | -5% (126 d) | +13% (269 d) |
| regimefilter | -4% (202 d) | +7% (69 d) | -1% (160 d) | +134% (4 d) | +8% (345 d) | +4% (879 d) | +5% (1410 d) | -1% (162 d) | +3% (126 d) | +9% (274 d) |
| koop-na-terugval | -2% (205 d) | -5% (69 d) | +8% (163 d) | +134% (4 d) | +7% (345 d) | +4% (881 d) | +10% (1410 d) | +0% (157 d) | -7% (126 d) | +5% (274 d) |
| koop-bij-nieuwe-top | +0% (205 d) | +22% (69 d) | +17% (163 d) | -8% (4 d) | +20% (344 d) | +5% (881 d) | +3% (1410 d) | +0% (159 d) | -5% (126 d) | +4% (269 d) |
| verkoop-na-2-rode-trendkaarsen | -10% (200 d) | -2% (69 d) | +12% (157 d) | -13% (4 d) | +9% (345 d) | -4% (859 d) | -2% (1369 d) | -4% (153 d) | -7% (123 d) | +1% (269 d) |
| 4-plekken | -7% (205 d) | +4% (69 d) | +2% (163 d) | +38% (4 d) | +2% (337 d) | +1% (876 d) | +1% (1403 d) | -3% (157 d) | +3% (126 d) | +7% (274 d) |
| 5-plekken | -3% (199 d) | +3% (69 d) | +2% (163 d) | +19% (4 d) | +0% (341 d) | +1% (878 d) | +1% (1409 d) | -4% (149 d) | -2% (126 d) | +1% (274 d) |
| meer-per-aankoop | -9% (205 d) | +8% (69 d) | +16% (163 d) | +67% (4 d) | +6% (345 d) | +1% (881 d) | +4% (1410 d) | -2% (162 d) | +2% (126 d) | +9% (274 d) |
| veel-meer-per-aankoop | -1% (205 d) | +12% (69 d) | +18% (163 d) | +117% (4 d) | +4% (344 d) | +5% (881 d) | +5% (1410 d) | -1% (161 d) | +2% (126 d) | +5% (274 d) |
| rest-in-wereld-etf | +13% (205 d) | +12% (69 d) | +30% (163 d) | +134% (4 d) | +7% (345 d) | +5% (881 d) | +7% (1410 d) | -7% (162 d) | -2% (126 d) | +7% (274 d) |

## Trend-agent: lessen uit 10 jaar backtest (productie)

920 afgesloten trades, 37% winst, gemiddeld +0.16 R per trade (mediaan -0.38 R), totaal €10,188, gemiddeld 28 dagen vastgehouden.

### Bevindingen

- Geen overtuigende verschillen (minimaal 20 trades per groep, verschil ≥ 0.15 R en t ≥ 2.0).

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend | 644 | 36% | +0.09 | 4,852 |
| zijwaarts | 142 | 38% | +0.18 | 2,402 |
| dalend | 126 | 40% | +0.26 | 1,487 |
| onbekend (te weinig) | 8 | 75% | +3.64 | 1,446 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 458 | 39% | +0.24 | 7,827 |
| laag | 232 | 32% | +0.03 | 1,666 |
| hoog | 222 | 35% | -0.01 | -751 |
| onbekend (te weinig) | 8 | 75% | +3.64 | 1,446 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 60-70 | 404 | 38% | +0.23 | 6,831 |
| 70-80 | 237 | 33% | +0.00 | -60 |
| 50-60 | 235 | 40% | +0.24 | 3,736 |
| onder 50 | 44 | 30% | -0.13 | -319 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| positief | 474 | 37% | +0.15 | 4,249 |
| negatief | 446 | 36% | +0.16 | 5,938 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| hoger (>1,1) | 407 | 40% | +0.20 | 6,241 |
| normaal | 350 | 34% | +0.10 | 1,648 |
| lager (<0,9) | 163 | 37% | +0.17 | 2,299 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% | 478 | 36% | +0.14 | 4,442 |
| meer dan 25% | 312 | 39% | +0.15 | 3,787 |
| tot 10% | 130 | 35% | +0.23 | 1,958 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 499 | 35% | +0.16 | 6,045 |
| wild (>3%) | 240 | 40% | +0.11 | 2,108 |
| rustig (<1,5%) | 181 | 38% | +0.20 | 2,035 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt | 829 | 39% | +0.20 | 11,725 |
| trend gebroken (slot onder 50-daags gemiddelde) | 91 | 13% | -0.21 | -1,538 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| lang (>30 d) | 357 | 75% | +1.45 | 36,732 |
| middel | 306 | 23% | -0.42 | -9,477 |
| kort (<10 d) | 257 | 0% | -0.95 | -17,067 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-081d85 | 920 | 37% | +0.16 | 10,188 |

## Trend-agent: lessen uit het oefenen (nepgeld, live)

Live van 2026-10-13 t/m 2026-11-02 (15 handelsdagen): bot -0.70%, wereld-ETF -1.81%, verschil +1.11%.

Live pas 1 afgesloten trades (gemiddeld -0.96 R); vanaf 20 trades is een vergelijking met de backtest (+0.16 R) zinvol.

1 afgesloten trades, 0% winst, gemiddeld -0.96 R per trade (mediaan -0.96 R), totaal €-23, gemiddeld 23 dagen vastgehouden.

### Bevindingen

- Geen overtuigende verschillen (minimaal 20 trades per groep, verschil ≥ 0.15 R en t ≥ 2.0).

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| onbekend (te weinig) | 1 | 0% | -0.96 | -23 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| onbekend (te weinig) | 1 | 0% | -0.96 | -23 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| onbekend (te weinig) | 1 | 0% | -0.96 | -23 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| onbekend (te weinig) | 1 | 0% | -0.96 | -23 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| onbekend (te weinig) | 1 | 0% | -0.96 | -23 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| onbekend (te weinig) | 1 | 0% | -0.96 | -23 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| onbekend (te weinig) | 1 | 0% | -0.96 | -23 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt (te weinig) | 1 | 0% | -0.96 | -23 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| middel (te weinig) | 1 | 0% | -0.96 | -23 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| onbekend (te weinig) | 1 | 0% | -0.96 | -23 |

## Investeerder

Periode 2016-11-03 t/m 2026-11-03. Ontwikkeldeel 2016-11-03 t/m 2023-11-02, holdout 2023-11-03 t/m 2026-11-03. 6 varianten getest tegen productie.

### Uitkomst

- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.62 vs productie 1.68 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 1.00 vs 1.16
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -36.7% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.17 vs 1.30
- **satelliet-3-aandelen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.65 vs productie 1.68 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 1.18 vs 1.16
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -38.1% vs -36.7%
    - ✓ Dubbele kosten en slippage: Sharpe 1.31 vs 1.30
- **zonder-crypto: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.69 vs productie 1.68 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.92 vs 1.16
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -34.8% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.14 vs 1.30
- **minder-satelliet: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.71 vs productie 1.68 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 1.12 vs 1.16
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -35.3% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.26 vs 1.30
- **hooguit-1-per-sector: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.57 vs productie 1.68 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 1.15 vs 1.16
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -35.7% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.25 vs 1.30
- **voorzichtig: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.68 vs productie 1.68 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 1.02 vs 1.16
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -33.9% vs -36.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.18 vs 1.30

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +889.4% | +25.8% | -36.7% | 1.32 | 1.68 | 1.30 | 290 | 73% | 1.61 |
| regimefilter | +617.3% | +21.8% | -36.7% | 1.19 | 1.62 | 1.17 | 287 | 71% | 1.46 |
| satelliet-3-aandelen | +1073.2% | +27.9% | -38.1% | 1.33 | 1.65 | 1.31 | 243 | 75% | 1.38 |
| zonder-crypto | +601.4% | +21.5% | -34.8% | 1.16 | 1.69 | 1.14 | 242 | 74% | 1.56 |
| minder-satelliet | +617.4% | +21.8% | -35.3% | 1.28 | 1.71 | 1.26 | 265 | 71% | 2.12 |
| hooguit-1-per-sector | +669.6% | +22.6% | -35.7% | 1.27 | 1.57 | 1.25 | 333 | 71% | 1.39 |
| voorzichtig | +529.3% | +20.2% | -33.9% | 1.20 | 1.68 | 1.18 | 291 | 68% | 1.85 |

### Per periode (rendement)

| Variant | Nov 2016–Nov 2018 | Nov 2018–Oct 2020 | Nov 2020–Oct 2022 | Nov 2022–Oct 2024 | Oct 2024–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | +61.8% | +43.8% | +59.0% | +57.4% | +79.5% |
| regimefilter | +61.8% | +10.2% | +60.9% | +53.9% | +71.8% |
| satelliet-3-aandelen | +77.8% | +43.1% | +56.8% | +59.9% | +94.7% |
| zonder-crypto | +42.3% | +37.1% | +34.2% | +53.9% | +82.9% |
| minder-satelliet | +51.7% | +31.0% | +59.1% | +50.0% | +56.0% |
| hooguit-1-per-sector | +52.4% | +34.6% | +58.9% | +63.7% | +49.4% |
| voorzichtig | +44.1% | +30.3% | +46.8% | +47.9% | +58.9% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (satelliet-3-aandelen, satelliet-3-aandelen, satelliet-3-aandelen, hooguit-1-per-sector), was het resultaat over de laatste 4 periodes +436.1%, tegen +546.0% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +59% (147 d) | +18% (51 d) | +65% (117 d) | +228% (2 d) | +19% (251 d) | +21% (623 d) | +21% (1015 d) | -2% (118 d) | -5% (90 d) | +30% (194 d) |
| regimefilter | +43% (147 d) | +11% (51 d) | +41% (117 d) | +228% (2 d) | +19% (251 d) | +22% (623 d) | +21% (1015 d) | -5% (118 d) | -6% (90 d) | +14% (194 d) |
| satelliet-3-aandelen | +60% (147 d) | +20% (51 d) | +69% (117 d) | +285% (2 d) | +27% (251 d) | +22% (623 d) | +21% (1015 d) | +6% (118 d) | +0% (90 d) | +32% (194 d) |
| zonder-crypto | +63% (147 d) | +18% (51 d) | +70% (117 d) | +235% (2 d) | +15% (251 d) | +15% (623 d) | +18% (1015 d) | +6% (118 d) | -11% (90 d) | +16% (194 d) |
| minder-satelliet | +58% (147 d) | +20% (51 d) | +58% (117 d) | +207% (2 d) | +13% (251 d) | +20% (623 d) | +17% (1015 d) | -2% (118 d) | -9% (90 d) | +22% (194 d) |
| hooguit-1-per-sector | +59% (147 d) | +17% (51 d) | +56% (117 d) | +177% (2 d) | +19% (251 d) | +19% (623 d) | +17% (1015 d) | -6% (118 d) | -4% (90 d) | +29% (194 d) |
| voorzichtig | +59% (147 d) | +18% (51 d) | +61% (117 d) | +202% (2 d) | +14% (251 d) | +16% (623 d) | +16% (1015 d) | +3% (118 d) | -9% (90 d) | +16% (194 d) |

## Investeerder live (nepgeld)

Van 2026-10-13 t/m 2026-11-02: investeerder -6.06%, wereld-ETF -1.81%, verschil -4.26%.
