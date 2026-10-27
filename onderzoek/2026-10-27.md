# Onderzoeksrapport 2026-10-27

Dit rapport test varianten van beide strategieën op echte koersen en kijkt wat de bots leren van hun eigen trades. **Er wordt niets automatisch aangepast.** Een aanbevolen variant gaat pas in productie als jij (of iemand die je vertrouwt) de instelling in de code aanpast; daarna draait de backtest opnieuw en loopt de nieuwe versie eerst weken mee op papier.

> Resultaten uit het verleden zijn geen garantie. De aandelenlijst is in 2026 gekozen (survivorship bias).

## Trend-agent

Periode 2021-10-27 t/m 2026-10-27. Ontwikkeldeel 2021-10-27 t/m 2025-05-01, holdout 2025-05-02 t/m 2026-10-27. 8 varianten getest tegen productie.

### Uitkomst

- **rem-pas-na-5-verliezen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.32 vs productie 0.57 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.26 vs 0.28
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.1% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.07 vs 0.10
    - ✓ Genoeg trades: 200 afgesloten trades (nodig: 30)
- **regimefilter: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.87 vs productie 0.57 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.24 vs 0.28
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.9% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe -0.18 vs 0.10
    - ✓ Genoeg trades: 170 afgesloten trades (nodig: 30)
- **niet-kopen-boven-rsi-75: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.45 vs productie 0.57 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.15 vs 0.28
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -4.8% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.05 vs 0.10
    - ✓ Genoeg trades: 197 afgesloten trades (nodig: 30)
- **koop-na-terugval: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.78 vs productie 0.57 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.18 vs 0.28
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.7% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe -0.29 vs 0.10
    - ✓ Genoeg trades: 202 afgesloten trades (nodig: 30)
- **koop-bij-nieuwe-top: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.40 vs productie 0.57 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.37 vs 0.28
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.1% vs -4.5%
    - ✓ Dubbele kosten en slippage: Sharpe 0.17 vs 0.10
    - ✓ Genoeg trades: 169 afgesloten trades (nodig: 30)
- **verkoop-na-2-rode-trendkaarsen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe -0.35 vs productie 0.57 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.87 vs 0.28
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -13.8% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe -1.81 vs 0.10
    - ✓ Genoeg trades: 587 afgesloten trades (nodig: 30)
- **4-plekken: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.88 vs productie 0.57 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.24 vs 0.28
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.6% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.09 vs 0.10
    - ✓ Genoeg trades: 254 afgesloten trades (nodig: 30)
- **5-plekken: AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.93 vs productie 0.57 (nodig: +0.10)
    - ✓ Ontwikkeldeel (eerste 70%): Sharpe 0.46 vs 0.28
    - ✓ Consistent over periodes: beter in 3 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.5% vs -4.5%
    - ✓ Dubbele kosten en slippage: Sharpe 0.20 vs 0.10
    - ✓ Genoeg trades: 305 afgesloten trades (nodig: 30)

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +7.3% | +1.4% | -4.5% | 0.37 | 0.57 | 0.10 | 193 | 35% | 2.32 |
| rem-pas-na-5-verliezen | +5.6% | +1.1% | -5.1% | 0.28 | 0.32 | 0.07 | 200 | 36% | 2.04 |
| regimefilter | +1.9% | +0.4% | -5.9% | 0.11 | 0.87 | -0.18 | 170 | 29% | 2.52 |
| niet-kopen-boven-rsi-75 | +4.6% | +0.9% | -4.8% | 0.24 | 0.45 | 0.05 | 197 | 36% | 2.01 |
| koop-na-terugval | +1.9% | +0.4% | -5.7% | 0.12 | 0.78 | -0.29 | 202 | 31% | 2.33 |
| koop-bij-nieuwe-top | +6.9% | +1.3% | -5.1% | 0.39 | 0.40 | 0.17 | 169 | 41% | 1.90 |
| verkoop-na-2-rode-trendkaarsen | -12.0% | -2.5% | -13.8% | -0.71 | -0.35 | -1.81 | 587 | 31% | 1.58 |
| 4-plekken | +10.8% | +2.1% | -5.6% | 0.44 | 0.88 | 0.09 | 254 | 38% | 2.12 |
| 5-plekken | +17.7% | +3.3% | -5.5% | 0.61 | 0.93 | 0.20 | 305 | 38% | 2.36 |

### Per periode (rendement)

| Variant | Oct 2021–Oct 2022 | Nov 2022–Oct 2023 | Oct 2023–Oct 2024 | Oct 2024–Oct 2025 | Oct 2025–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | -1.3% | +1.1% | +1.1% | +4.5% | +1.9% |
| rem-pas-na-5-verliezen | -1.5% | +2.9% | +1.2% | +1.4% | +1.6% |
| regimefilter | -2.4% | +0.4% | -2.5% | +3.4% | +3.2% |
| niet-kopen-boven-rsi-75 | -1.6% | -1.3% | +2.0% | +1.8% | +3.7% |
| koop-na-terugval | -4.4% | -0.0% | +3.2% | +0.7% | +2.6% |
| koop-bij-nieuwe-top | +0.2% | -0.3% | +4.4% | -0.3% | +3.1% |
| verkoop-na-2-rode-trendkaarsen | -3.5% | -5.7% | -2.1% | +0.1% | -1.3% |
| 4-plekken | -2.1% | +1.3% | +3.3% | +2.8% | +5.4% |
| 5-plekken | -2.5% | +2.3% | +6.3% | +4.9% | +6.1% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (koop-bij-nieuwe-top, rem-pas-na-5-verliezen, koop-bij-nieuwe-top, 5-plekken), was het resultaat over de laatste 4 periodes +6.7%, tegen +8.8% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +5% (92 d) | -0% (69 d) | -2% (100 d) | +47% (2 d) | +1% (226 d) | +1% (397 d) | +2% (614 d) | -2% (77 d) | -2% (93 d) | -1% (142 d) |
| rem-pas-na-5-verliezen | +6% (92 d) | -1% (69 d) | -1% (100 d) | +47% (2 d) | +1% (226 d) | +2% (397 d) | +1% (614 d) | -3% (73 d) | -0% (93 d) | -1% (142 d) |
| regimefilter | +0% (92 d) | +1% (69 d) | -1% (98 d) | +47% (2 d) | -1% (221 d) | +1% (397 d) | +1% (609 d) | -3% (77 d) | -3% (93 d) | +1% (139 d) |
| niet-kopen-boven-rsi-75 | +5% (92 d) | -1% (69 d) | -2% (100 d) | -13% (2 d) | +2% (221 d) | +0% (395 d) | +2% (614 d) | -3% (77 d) | -5% (93 d) | -2% (142 d) |
| koop-na-terugval | +4% (92 d) | -1% (69 d) | +2% (100 d) | -57% (2 d) | +0% (221 d) | +1% (394 d) | -0% (609 d) | -1% (76 d) | -3% (90 d) | +1% (142 d) |
| koop-bij-nieuwe-top | +0% (92 d) | +1% (69 d) | +1% (100 d) | +63% (2 d) | +4% (221 d) | -0% (397 d) | +2% (611 d) | -1% (77 d) | -6% (88 d) | +1% (142 d) |
| verkoop-na-2-rode-trendkaarsen | +1% (92 d) | -5% (67 d) | -2% (90 d) | +44% (2 d) | +1% (202 d) | -0% (367 d) | -2% (590 d) | -5% (74 d) | -10% (84 d) | -2% (135 d) |
| 4-plekken | +5% (92 d) | -1% (69 d) | -1% (100 d) | +29% (2 d) | +3% (221 d) | +2% (397 d) | +2% (614 d) | -3% (77 d) | -3% (93 d) | +0% (142 d) |
| 5-plekken | +7% (92 d) | -1% (69 d) | +2% (100 d) | +23% (2 d) | +4% (226 d) | +3% (397 d) | +2% (611 d) | -1% (73 d) | -1% (93 d) | -1% (142 d) |

## Trend-agent: lessen uit 5 jaar backtest (productie)

193 afgesloten trades, 35% winst, gemiddeld +0.13 R per trade (mediaan -0.42 R), totaal €586, gemiddeld 26 dagen vastgehouden.

### Bevindingen

- Sterkte: RSI bij instap = 70-80: gemiddeld +0.68 R over 51 trades (+0.74 R t.o.v. de rest, t = 2.4). Te testen via instelling `max_rsi_entry`.
- Zwakte: RSI bij instap = 60-70: gemiddeld -0.22 R over 56 trades (-0.50 R t.o.v. de rest, t = -2.3). Te testen via instelling `max_rsi_entry`.
- Sterkte: Marktbeweeglijkheid bij instap = normaal: gemiddeld +0.40 R over 92 trades (+0.50 R t.o.v. de rest, t = 2.0). Te testen via instelling `regime_filter`.

_Dit zijn hypotheses. Een regel verandert pas na een test op ongeziene data (zie het onderzoeksrapport)._

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend | 129 | 33% | +0.14 | 452 |
| zijwaarts | 36 | 42% | +0.15 | 132 |
| dalend | 25 | 36% | +0.14 | 34 |
| onbekend (te weinig) | 3 | 33% | -0.40 | -32 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 92 | 37% | +0.40 | 880 |
| laag | 51 | 35% | -0.01 | -54 |
| hoog | 47 | 32% | -0.19 | -209 |
| onbekend (te weinig) | 3 | 33% | -0.40 | -32 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 50-60 | 61 | 33% | +0.16 | 191 |
| 60-70 | 56 | 27% | -0.22 | -273 |
| 70-80 | 51 | 51% | +0.68 | 823 |
| 80 of hoger (te weinig) | 15 | 27% | -0.16 | -72 |
| onder 50 (te weinig) | 10 | 30% | -0.33 | -84 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| positief | 112 | 37% | +0.24 | 610 |
| negatief | 81 | 33% | -0.01 | -25 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| hoger (>1,1) | 80 | 36% | +0.03 | 81 |
| normaal | 74 | 36% | +0.31 | 519 |
| lager (<0,9) | 39 | 31% | +0.01 | -15 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% | 91 | 29% | -0.08 | -215 |
| meer dan 25% | 82 | 39% | +0.34 | 647 |
| tot 10% | 20 | 50% | +0.31 | 154 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 112 | 31% | -0.01 | -109 |
| wild (>3%) | 57 | 44% | +0.42 | 620 |
| rustig (<1,5%) | 24 | 33% | +0.13 | 74 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt | 175 | 38% | +0.18 | 719 |
| trend gebroken (slot onder 50-daags gemiddelde) (te weinig) | 18 | 11% | -0.32 | -133 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| middel | 75 | 15% | -0.50 | -855 |
| lang (>30 d) | 66 | 85% | +1.72 | 2,646 |
| kort (<10 d) | 52 | 2% | -0.96 | -1,206 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-d373c7 | 193 | 35% | +0.13 | 586 |

## Trend-agent: lessen uit het oefenen (nepgeld, live)

Live van 2026-10-13 t/m 2026-10-26 (10 handelsdagen): bot +0.62%, wereld-ETF -1.29%, verschil +1.91%.

Nog geen afgesloten trades om van te leren.

## Investeerder

Periode 2021-10-27 t/m 2026-10-27. Ontwikkeldeel 2021-10-27 t/m 2025-04-25, holdout 2025-04-28 t/m 2026-10-27. 2 varianten getest tegen productie.

### Uitkomst

- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.76 vs productie 1.81 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.83 vs 0.89
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -20.2% vs -21.9%
    - ✗ Dubbele kosten en slippage: Sharpe 1.08 vs 1.12
- **satelliet-3-aandelen: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 1.93 vs productie 1.81 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.71 vs 0.89
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -24.5% vs -21.9%
    - ✗ Dubbele kosten en slippage: Sharpe 1.06 vs 1.12

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +152.7% | +20.4% | -21.9% | 1.16 | 1.81 | 1.12 | 147 | 65% | 1.43 |
| regimefilter | +132.7% | +18.4% | -20.2% | 1.12 | 1.76 | 1.08 | 152 | 62% | 1.38 |
| satelliet-3-aandelen | +149.5% | +20.1% | -24.5% | 1.08 | 1.93 | 1.06 | 122 | 64% | 1.41 |

### Per periode (rendement)

| Variant | Oct 2021–Oct 2022 | Oct 2022–Oct 2023 | Oct 2023–Oct 2024 | Oct 2024–Oct 2025 | Oct 2025–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | -10.3% | +9.9% | +56.7% | +28.1% | +27.7% |
| regimefilter | -9.7% | +2.7% | +56.7% | +25.4% | +27.7% |
| satelliet-3-aandelen | -14.2% | +10.0% | +47.4% | +34.1% | +34.6% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (productie, productie, productie, productie), was het resultaat over de laatste 4 periodes +181.6%, tegen +181.6% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +66% (66 d) | +14% (51 d) | +30% (74 d) | +259% (2 d) | +37% (162 d) | +26% (281 d) | +3% (445 d) | +36% (56 d) | -22% (67 d) | +21% (100 d) |
| regimefilter | +61% (66 d) | +10% (51 d) | +28% (74 d) | +259% (2 d) | +37% (162 d) | +25% (281 d) | +3% (445 d) | +30% (56 d) | -27% (67 d) | +15% (100 d) |
| satelliet-3-aandelen | +57% (66 d) | +17% (51 d) | +33% (74 d) | +253% (2 d) | +33% (162 d) | +26% (281 d) | +5% (445 d) | +47% (56 d) | -25% (67 d) | +17% (100 d) |

## Investeerder live (nepgeld)

Van 2026-10-13 t/m 2026-10-26: investeerder -4.12%, wereld-ETF -1.29%, verschil -2.82%.
