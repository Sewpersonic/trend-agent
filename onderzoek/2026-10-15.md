# Onderzoeksrapport 2026-10-15

Dit rapport test varianten van beide strategieën op echte koersen en kijkt wat de bots leren van hun eigen trades. **Er wordt niets automatisch aangepast.** Een aanbevolen variant gaat pas in productie als jij (of iemand die je vertrouwt) de instelling in de code aanpast; daarna draait de backtest opnieuw en loopt de nieuwe versie eerst weken mee op papier.

> Resultaten uit het verleden zijn geen garantie. De aandelenlijst is in 2026 gekozen (survivorship bias).

## Trend-agent

Periode 2021-10-15 t/m 2026-10-15. Ontwikkeldeel 2021-10-15 t/m 2025-04-19, holdout 2025-04-20 t/m 2026-10-15. 6 varianten getest tegen productie.

### Uitkomst

- **rem-pas-na-5-verliezen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.27 vs productie 0.56 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.22 vs 0.25
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.2% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe -0.07 vs 0.05
    - ✓ Genoeg trades: 203 afgesloten trades (nodig: 30)
- **regimefilter: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.81 vs productie 0.56 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.25 vs 0.25
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.6% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe -0.21 vs 0.05
    - ✓ Genoeg trades: 170 afgesloten trades (nodig: 30)
- **niet-kopen-boven-rsi-75: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.42 vs productie 0.56 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.12 vs 0.25
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -4.8% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.02 vs 0.05
    - ✓ Genoeg trades: 197 afgesloten trades (nodig: 30)
- **koop-na-terugval: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.70 vs productie 0.56 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.05 vs 0.25
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -3.9% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe -0.10 vs 0.05
    - ✓ Genoeg trades: 197 afgesloten trades (nodig: 30)
- **koop-bij-nieuwe-top: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.34 vs productie 0.56 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.26 vs 0.25
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.0% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.04 vs 0.05
    - ✓ Genoeg trades: 173 afgesloten trades (nodig: 30)
- **verkoop-na-2-rode-trendkaarsen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe -0.42 vs productie 0.56 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.80 vs 0.25
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -14.0% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe -1.77 vs 0.05
    - ✓ Genoeg trades: 589 afgesloten trades (nodig: 30)

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +6.8% | +1.3% | -4.5% | 0.34 | 0.56 | 0.05 | 195 | 34% | 2.38 |
| rem-pas-na-5-verliezen | +4.6% | +0.9% | -5.2% | 0.24 | 0.27 | -0.07 | 203 | 35% | 2.13 |
| regimefilter | +1.2% | +0.2% | -5.6% | 0.08 | 0.81 | -0.21 | 170 | 28% | 2.63 |
| niet-kopen-boven-rsi-75 | +4.1% | +0.8% | -4.8% | 0.22 | 0.42 | 0.02 | 197 | 36% | 2.04 |
| koop-na-terugval | +4.0% | +0.8% | -3.9% | 0.24 | 0.70 | -0.10 | 197 | 34% | 2.26 |
| koop-bij-nieuwe-top | +5.1% | +1.0% | -5.0% | 0.29 | 0.34 | 0.04 | 173 | 38% | 2.01 |
| verkoop-na-2-rode-trendkaarsen | -11.7% | -2.5% | -14.0% | -0.68 | -0.42 | -1.77 | 589 | 31% | 1.62 |

### Per periode (rendement)

| Variant | Oct 2021–Oct 2022 | Oct 2022–Oct 2023 | Oct 2023–Oct 2024 | Oct 2024–Oct 2025 | Oct 2025–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | -2.3% | +2.1% | +0.4% | +4.9% | +1.0% |
| rem-pas-na-5-verliezen | -2.7% | +4.0% | +0.3% | +1.8% | +0.7% |
| regimefilter | -3.3% | +1.4% | -2.6% | +3.3% | +2.2% |
| niet-kopen-boven-rsi-75 | -2.5% | -0.2% | +1.3% | +1.7% | +3.5% |
| koop-na-terugval | -2.2% | +1.1% | +2.1% | +0.4% | +2.4% |
| koop-bij-nieuwe-top | -2.3% | +1.5% | +3.2% | -0.3% | +2.8% |
| verkoop-na-2-rode-trendkaarsen | -3.3% | -4.5% | -2.1% | +0.0% | -2.7% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (productie, rem-pas-na-5-verliezen, koop-bij-nieuwe-top, productie), was het resultaat over de laatste 4 periodes +3.1%, tegen +8.6% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +5% (92 d) | -0% (69 d) | -2% (100 d) | +5% (4 d) | +1% (234 d) | +1% (385 d) | +2% (616 d) | -2% (77 d) | -2% (93 d) | -1% (142 d) |
| rem-pas-na-5-verliezen | +6% (92 d) | -1% (69 d) | -1% (100 d) | +5% (4 d) | +1% (234 d) | +1% (385 d) | +1% (616 d) | -3% (73 d) | -0% (93 d) | -1% (142 d) |
| regimefilter | +0% (92 d) | +1% (69 d) | -1% (98 d) | +5% (4 d) | -1% (224 d) | +1% (385 d) | +1% (611 d) | -3% (77 d) | -3% (93 d) | +1% (139 d) |
| niet-kopen-boven-rsi-75 | +5% (92 d) | -1% (69 d) | -2% (100 d) | +7% (4 d) | +2% (229 d) | -0% (383 d) | +2% (614 d) | -3% (77 d) | -5% (93 d) | -2% (142 d) |
| koop-na-terugval | +4% (92 d) | -1% (69 d) | +2% (100 d) | +7% (4 d) | -0% (225 d) | +2% (385 d) | +0% (612 d) | +0% (77 d) | -3% (90 d) | +1% (142 d) |
| koop-bij-nieuwe-top | +0% (92 d) | +2% (69 d) | +2% (100 d) | +5% (4 d) | +4% (229 d) | -1% (385 d) | +2% (613 d) | -1% (77 d) | -6% (88 d) | +1% (142 d) |
| verkoop-na-2-rode-trendkaarsen | +0% (92 d) | -4% (67 d) | -2% (90 d) | +5% (4 d) | +2% (210 d) | -1% (355 d) | -2% (592 d) | -5% (74 d) | -9% (84 d) | -2% (135 d) |

## Trend-agent: lessen uit 5 jaar backtest (productie)

195 afgesloten trades, 34% winst, gemiddeld +0.12 R per trade (mediaan -0.44 R), totaal €559, gemiddeld 26 dagen vastgehouden.

### Bevindingen

- Sterkte: Marktbeweeglijkheid bij instap = normaal: gemiddeld +0.42 R over 91 trades (+0.56 R t.o.v. de rest, t = 2.2). Te testen via instelling `regime_filter`.
- Zwakte: RSI bij instap = 60-70: gemiddeld -0.21 R over 55 trades (-0.47 R t.o.v. de rest, t = -2.2). Te testen via instelling `max_rsi_entry`.
- Sterkte: RSI bij instap = 70-80: gemiddeld +0.58 R over 54 trades (+0.63 R t.o.v. de rest, t = 2.1). Te testen via instelling `max_rsi_entry`.

_Dit zijn hypotheses. Een regel verandert pas na een test op ongeziene data (zie het onderzoeksrapport)._

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend | 131 | 33% | +0.13 | 437 |
| zijwaarts | 36 | 42% | +0.15 | 132 |
| dalend | 25 | 36% | +0.14 | 50 |
| onbekend (te weinig) | 3 | 0% | -0.78 | -60 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 91 | 37% | +0.42 | 930 |
| laag | 52 | 33% | -0.05 | -84 |
| hoog | 49 | 33% | -0.20 | -226 |
| onbekend (te weinig) | 3 | 0% | -0.78 | -60 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 50-60 | 62 | 34% | +0.16 | 198 |
| 60-70 | 55 | 27% | -0.21 | -255 |
| 70-80 | 54 | 46% | +0.58 | 750 |
| 80 of hoger (te weinig) | 14 | 21% | -0.16 | -50 |
| onder 50 (te weinig) | 10 | 30% | -0.33 | -84 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| positief | 114 | 35% | +0.22 | 582 |
| negatief | 81 | 33% | -0.01 | -23 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| hoger (>1,1) | 82 | 34% | +0.01 | 35 |
| normaal | 74 | 36% | +0.31 | 524 |
| lager (<0,9) | 39 | 31% | +0.01 | 1 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% | 91 | 29% | -0.09 | -223 |
| meer dan 25% | 84 | 37% | +0.31 | 628 |
| tot 10% | 20 | 50% | +0.31 | 154 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 114 | 32% | -0.01 | -111 |
| wild (>3%) | 57 | 40% | +0.39 | 596 |
| rustig (<1,5%) | 24 | 33% | +0.13 | 74 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt | 177 | 37% | +0.17 | 692 |
| trend gebroken (slot onder 50-daags gemiddelde) (te weinig) | 18 | 11% | -0.32 | -133 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| middel | 76 | 13% | -0.51 | -882 |
| lang (>30 d) | 67 | 84% | +1.69 | 2,628 |
| kort (<10 d) | 52 | 2% | -0.96 | -1,186 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-d373c7 | 195 | 34% | +0.12 | 559 |

## Trend-agent: lessen uit het oefenen (nepgeld, live)

Live van 2026-10-13 t/m 2026-10-14 (2 handelsdagen): bot +0.10%, wereld-ETF -0.36%, verschil +0.46%.

Nog geen afgesloten trades om van te leren.

## Investeerder

Periode 2021-10-15 t/m 2026-10-15. Ontwikkeldeel 2021-10-15 t/m 2025-04-15, holdout 2025-04-16 t/m 2026-10-15. 2 varianten getest tegen productie.

### Uitkomst

- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.84 vs productie 1.88 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.84 vs 0.90
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -20.2% vs -21.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.09 vs 1.14
- **satelliet-3-aandelen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.97 vs productie 1.88 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.74 vs 0.90
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -24.4% vs -21.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.08 vs 1.14

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +154.1% | +20.5% | -21.7% | 1.17 | 1.88 | 1.14 | 148 | 66% | 1.36 |
| regimefilter | +134.0% | +18.5% | -20.2% | 1.13 | 1.84 | 1.09 | 153 | 65% | 1.24 |
| satelliet-3-aandelen | +153.0% | +20.4% | -24.4% | 1.10 | 1.97 | 1.08 | 125 | 67% | 1.24 |

### Per periode (rendement)

| Variant | Oct 2021–Oct 2022 | Oct 2022–Oct 2023 | Oct 2023–Oct 2024 | Oct 2024–Oct 2025 | Oct 2025–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | -11.3% | +18.5% | +47.9% | +27.4% | +28.1% |
| regimefilter | -10.6% | +10.7% | +47.9% | +24.5% | +28.2% |
| satelliet-3-aandelen | -15.1% | +17.4% | +40.7% | +31.7% | +36.2% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (productie, productie, productie, productie), was het resultaat over de laatste 4 periodes +186.0%, tegen +186.0% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +66% (66 d) | +14% (51 d) | +30% (74 d) | +85% (2 d) | +38% (168 d) | +25% (273 d) | +4% (447 d) | +36% (56 d) | -22% (67 d) | +21% (100 d) |
| regimefilter | +61% (66 d) | +10% (51 d) | +28% (74 d) | +85% (2 d) | +38% (168 d) | +24% (273 d) | +4% (447 d) | +30% (56 d) | -27% (67 d) | +14% (100 d) |
| satelliet-3-aandelen | +57% (66 d) | +17% (51 d) | +32% (74 d) | +85% (2 d) | +36% (168 d) | +25% (273 d) | +6% (447 d) | +48% (56 d) | -25% (67 d) | +16% (100 d) |

## Investeerder live (nepgeld)

Van 2026-10-13 t/m 2026-10-14: investeerder -1.87%, wereld-ETF -0.36%, verschil -1.50%.
