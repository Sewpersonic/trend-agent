# Onderzoeksrapport 2026-10-24

Dit rapport test varianten van beide strategieën op echte koersen en kijkt wat de bots leren van hun eigen trades. **Er wordt niets automatisch aangepast.** Een aanbevolen variant gaat pas in productie als jij (of iemand die je vertrouwt) de instelling in de code aanpast; daarna draait de backtest opnieuw en loopt de nieuwe versie eerst weken mee op papier.

> Resultaten uit het verleden zijn geen garantie. De aandelenlijst is in 2026 gekozen (survivorship bias).

## Trend-agent

Periode 2021-10-24 t/m 2026-10-24. Ontwikkeldeel 2021-10-24 t/m 2025-04-28, holdout 2025-04-29 t/m 2026-10-24. 6 varianten getest tegen productie.

### Uitkomst

- **rem-pas-na-5-verliezen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.34 vs productie 0.58 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.27 vs 0.29
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.1% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.07 vs 0.10
    - ✓ Genoeg trades: 200 afgesloten trades (nodig: 30)
- **regimefilter: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.89 vs productie 0.58 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.24 vs 0.29
    - ✗ Consistent over periodes: beter in 1 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.9% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe -0.18 vs 0.10
    - ✓ Genoeg trades: 170 afgesloten trades (nodig: 30)
- **niet-kopen-boven-rsi-75: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.46 vs productie 0.58 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.13 vs 0.29
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -4.8% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.03 vs 0.10
    - ✓ Genoeg trades: 197 afgesloten trades (nodig: 30)
- **koop-na-terugval: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 0.80 vs productie 0.58 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.12 vs 0.29
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -5.6% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe -0.21 vs 0.10
    - ✓ Genoeg trades: 197 afgesloten trades (nodig: 30)
- **koop-bij-nieuwe-top: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 0.49 vs productie 0.58 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.22 vs 0.29
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -4.8% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe 0.04 vs 0.10
    - ✓ Genoeg trades: 174 afgesloten trades (nodig: 30)
- **verkoop-na-2-rode-trendkaarsen: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe -0.29 vs productie 0.58 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe -0.87 vs 0.29
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -13.8% vs -4.5%
    - ✗ Dubbele kosten en slippage: Sharpe -1.80 vs 0.10
    - ✓ Genoeg trades: 587 afgesloten trades (nodig: 30)

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +7.4% | +1.4% | -4.5% | 0.37 | 0.58 | 0.10 | 193 | 35% | 2.31 |
| rem-pas-na-5-verliezen | +5.7% | +1.1% | -5.1% | 0.29 | 0.34 | 0.07 | 200 | 36% | 2.04 |
| regimefilter | +2.0% | +0.4% | -5.9% | 0.12 | 0.89 | -0.18 | 170 | 29% | 2.52 |
| niet-kopen-boven-rsi-75 | +4.3% | +0.8% | -4.8% | 0.23 | 0.46 | 0.03 | 197 | 36% | 2.03 |
| koop-na-terugval | +2.5% | +0.5% | -5.6% | 0.16 | 0.80 | -0.21 | 197 | 32% | 2.19 |
| koop-bij-nieuwe-top | +5.5% | +1.1% | -4.8% | 0.31 | 0.49 | 0.04 | 174 | 38% | 2.00 |
| verkoop-na-2-rode-trendkaarsen | -11.8% | -2.5% | -13.8% | -0.69 | -0.29 | -1.80 | 587 | 31% | 1.58 |

### Per periode (rendement)

| Variant | Oct 2021–Oct 2022 | Oct 2022–Oct 2023 | Oct 2023–Oct 2024 | Oct 2024–Oct 2025 | Oct 2025–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | -1.4% | +1.1% | +0.8% | +4.6% | +1.6% |
| rem-pas-na-5-verliezen | -1.6% | +2.9% | +1.0% | +1.4% | +1.3% |
| regimefilter | -2.5% | +0.5% | -2.9% | +3.6% | +3.0% |
| niet-kopen-boven-rsi-75 | -2.1% | -1.2% | +1.7% | +1.7% | +3.7% |
| koop-na-terugval | -3.9% | -0.0% | +2.9% | +0.6% | +2.6% |
| koop-bij-nieuwe-top | -2.2% | -0.1% | +4.5% | -0.1% | +2.7% |
| verkoop-na-2-rode-trendkaarsen | -3.6% | -5.3% | -2.5% | +0.3% | -1.7% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (productie, rem-pas-na-5-verliezen, rem-pas-na-5-verliezen, productie), was het resultaat over de laatste 4 periodes +5.2%, tegen +8.3% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +5% (92 d) | -0% (69 d) | -2% (100 d) | -5% (3 d) | +1% (226 d) | +1% (394 d) | +2% (616 d) | -2% (77 d) | -2% (93 d) | -1% (142 d) |
| rem-pas-na-5-verliezen | +6% (92 d) | -1% (69 d) | -1% (100 d) | -5% (3 d) | +1% (226 d) | +2% (394 d) | +1% (616 d) | -3% (73 d) | -0% (93 d) | -1% (142 d) |
| regimefilter | +0% (92 d) | +1% (69 d) | -1% (98 d) | -5% (3 d) | -1% (221 d) | +1% (394 d) | +1% (611 d) | -3% (77 d) | -3% (93 d) | +1% (139 d) |
| niet-kopen-boven-rsi-75 | +5% (92 d) | -1% (69 d) | -2% (100 d) | -15% (3 d) | +2% (221 d) | +0% (392 d) | +2% (614 d) | -3% (77 d) | -5% (93 d) | -2% (142 d) |
| koop-na-terugval | +4% (92 d) | -1% (69 d) | +2% (100 d) | -6% (3 d) | -1% (218 d) | +2% (394 d) | +0% (611 d) | -1% (76 d) | -3% (90 d) | +1% (142 d) |
| koop-bij-nieuwe-top | +0% (92 d) | +2% (69 d) | +1% (100 d) | -5% (3 d) | +3% (221 d) | -0% (394 d) | +2% (613 d) | -1% (77 d) | -6% (88 d) | +1% (142 d) |
| verkoop-na-2-rode-trendkaarsen | +1% (92 d) | -5% (67 d) | -2% (90 d) | -5% (3 d) | +1% (202 d) | -0% (364 d) | -2% (592 d) | -5% (74 d) | -10% (84 d) | -2% (135 d) |

## Trend-agent: lessen uit 5 jaar backtest (productie)

193 afgesloten trades, 35% winst, gemiddeld +0.14 R per trade (mediaan -0.42 R), totaal €586, gemiddeld 26 dagen vastgehouden.

### Bevindingen

- Sterkte: RSI bij instap = 70-80: gemiddeld +0.65 R over 52 trades (+0.70 R t.o.v. de rest, t = 2.3). Te testen via instelling `max_rsi_entry`.
- Zwakte: RSI bij instap = 60-70: gemiddeld -0.21 R over 55 trades (-0.49 R t.o.v. de rest, t = -2.3). Te testen via instelling `max_rsi_entry`.
- Sterkte: Marktbeweeglijkheid bij instap = normaal: gemiddeld +0.40 R over 92 trades (+0.50 R t.o.v. de rest, t = 2.0). Te testen via instelling `regime_filter`.

_Dit zijn hypotheses. Een regel verandert pas na een test op ongeziene data (zie het onderzoeksrapport)._

### Markttrend bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stijgend | 129 | 33% | +0.14 | 452 |
| zijwaarts | 36 | 42% | +0.15 | 132 |
| dalend | 25 | 36% | +0.14 | 34 |
| onbekend (te weinig) | 3 | 33% | -0.33 | -31 |

### Marktbeweeglijkheid bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 92 | 37% | +0.40 | 880 |
| laag | 51 | 35% | -0.01 | -54 |
| hoog | 47 | 32% | -0.19 | -209 |
| onbekend (te weinig) | 3 | 33% | -0.33 | -31 |

### RSI bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 50-60 | 61 | 33% | +0.16 | 191 |
| 60-70 | 55 | 27% | -0.21 | -257 |
| 70-80 | 52 | 50% | +0.65 | 803 |
| 80 of hoger (te weinig) | 15 | 27% | -0.14 | -67 |
| onder 50 (te weinig) | 10 | 30% | -0.33 | -84 |

### MACD-histogram bij instap

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| positief | 113 | 36% | +0.23 | 586 |
| negatief | 80 | 34% | +0.00 | -1 |

### Volume t.o.v. normaal

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| hoger (>1,1) | 80 | 36% | +0.03 | 81 |
| normaal | 74 | 36% | +0.31 | 519 |
| lager (<0,9) | 39 | 31% | +0.01 | -15 |

### Afstand tot SMA200

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| 10-25% | 91 | 29% | -0.09 | -220 |
| meer dan 25% | 82 | 39% | +0.34 | 652 |
| tot 10% | 20 | 50% | +0.31 | 154 |

### Beweeglijkheid aandeel (ATR%)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| normaal | 113 | 32% | -0.00 | -100 |
| wild (>3%) | 56 | 43% | +0.42 | 612 |
| rustig (<1,5%) | 24 | 33% | +0.13 | 74 |

### Uitstapreden (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| stop-loss geraakt | 175 | 38% | +0.18 | 719 |
| trend gebroken (slot onder 50-daags gemiddelde) (te weinig) | 18 | 11% | -0.32 | -133 |

### Houdduur (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| middel | 75 | 15% | -0.49 | -854 |
| lang (>30 d) | 66 | 85% | +1.72 | 2,646 |
| kort (<10 d) | 52 | 2% | -0.96 | -1,206 |

### Strategieversie (uitkomst, ter informatie)

| Groep | Trades | Winst | Gem. R | Totaal € |
| --- | --- | --- | --- | --- |
| trend-1.1-d373c7 | 193 | 35% | +0.14 | 586 |

## Trend-agent: lessen uit het oefenen (nepgeld, live)

Live van 2026-10-13 t/m 2026-10-23 (9 handelsdagen): bot +0.61%, wereld-ETF -1.84%, verschil +2.46%.

Nog geen afgesloten trades om van te leren.

## Investeerder

Periode 2021-10-25 t/m 2026-10-23. Ontwikkeldeel 2021-10-25 t/m 2025-04-23, holdout 2025-04-24 t/m 2026-10-23. 2 varianten getest tegen productie.

### Uitkomst

- **regimefilter: NIET AANBEVOLEN**
    - ✗ Holdout (ongeziene laatste 30%): Sharpe 1.69 vs productie 1.73 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.81 vs 0.87
    - ✗ Consistent over periodes: beter in 0 van 5 periodes (nodig: 60%)
    - ✓ Grootste daling: -20.2% vs -21.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.05 vs 1.10
- **satelliet-3-aandelen: NIET AANBEVOLEN**
    - ✓ Holdout (ongeziene laatste 30%): Sharpe 1.85 vs productie 1.73 (nodig: +0.10)
    - ✗ Ontwikkeldeel (eerste 70%): Sharpe 0.70 vs 0.87
    - ✗ Consistent over periodes: beter in 2 van 5 periodes (nodig: 60%)
    - ✗ Grootste daling: -24.1% vs -21.7%
    - ✗ Dubbele kosten en slippage: Sharpe 1.04 vs 1.10

Geen enkele variant is aantoonbaar beter. Productie blijft zoals hij is.

### Cijfers per variant (hele periode, na kosten)

| Variant | Totaal | Per jaar | Grootste daling | Sharpe | Sharpe holdout | Sharpe 2x kosten | Trades | Winst % | Winst/verlies |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +146.5% | +19.8% | -21.7% | 1.13 | 1.73 | 1.10 | 148 | 66% | 1.32 |
| regimefilter | +127.1% | +17.8% | -20.2% | 1.09 | 1.69 | 1.05 | 153 | 64% | 1.28 |
| satelliet-3-aandelen | +144.3% | +19.6% | -24.1% | 1.06 | 1.85 | 1.04 | 124 | 66% | 1.27 |

### Per periode (rendement)

| Variant | Oct 2021–Oct 2022 | Oct 2022–Oct 2023 | Oct 2023–Oct 2024 | Oct 2024–Oct 2025 | Oct 2025–Oct 2026 |
| --- | --- | --- | --- | --- | --- |
| productie | -10.8% | +11.9% | +54.9% | +25.8% | +25.8% |
| regimefilter | -10.2% | +4.5% | +54.8% | +23.2% | +25.8% |
| satelliet-3-aandelen | -14.3% | +10.7% | +47.0% | +31.1% | +32.6% |

### Zelf bijsturen op basis van het verleden?

Als de bot elke periode de variant had gekozen die tot dan toe het best was (productie, productie, productie, productie), was het resultaat over de laatste 4 periodes +174.3%, tegen +174.3% voor gewoon productie houden. Automatisch bijsturen voegde hier dus niets toe.

### Per marktregime (gemiddeld rendement op jaarbasis)

| Variant | dalend-hoog | dalend-laag | dalend-normaal | onbekend-onbekend | stijgend-hoog | stijgend-laag | stijgend-normaal | zijwaarts-hoog | zijwaarts-laag | zijwaarts-normaal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| productie | +66% (66 d) | +14% (51 d) | +30% (74 d) | +36% (2 d) | +37% (162 d) | +24% (279 d) | +4% (447 d) | +36% (56 d) | -22% (67 d) | +21% (100 d) |
| regimefilter | +61% (66 d) | +10% (51 d) | +28% (74 d) | +36% (2 d) | +37% (162 d) | +23% (279 d) | +4% (447 d) | +30% (56 d) | -27% (67 d) | +15% (100 d) |
| satelliet-3-aandelen | +57% (66 d) | +17% (51 d) | +33% (74 d) | +113% (2 d) | +33% (162 d) | +24% (279 d) | +6% (447 d) | +48% (56 d) | -25% (67 d) | +16% (100 d) |

## Investeerder live (nepgeld)

Van 2026-10-13 t/m 2026-10-23: investeerder -5.09%, wereld-ETF -1.84%, verschil -3.24%.
