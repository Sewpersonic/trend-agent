# Backtest trend-agent

Periode **2021-10-15 t/m 2026-10-15** (ongeveer 5 jaar), startkapitaal €10.000 nepgeld, 52 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de trend-agent het slechter dan gewoon de wereld-ETF vasthouden (+6,8% tegen +76,8%).
- Zijn grootste daling was -4,5%, tegen -21,6% voor de ETF.
- In 53% van alle periodes van 4 weken stond de trend-agent aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -2,7%, het beste +2,4%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | +6,8% | +1,3% | -4,5% | 0,34 | €10.673 |
| MSCI World-ETF (IWDA) | +76,8% | +12,1% | -21,6% | 0,73 | €17.680 |
| S&P 500-ETF (SPY, in euro) | +91,2% | +13,8% | -23,0% | 0,65 | €19.116 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Trend-agent | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2021 | -0,4% | +6,8% | +9,4% |
| 2022 | -2,5% | -13,5% | -13,1% |
| 2023 | +2,2% | +19,9% | +21,5% |
| 2024 | +4,2% | +27,2% | +32,8% |
| 2025 | +2,0% | +7,1% | +4,3% |
| 2026 | +1,2% | +17,2% | +19,4% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | 53% | +0,0% | -1,1% | -2,7% | +2,4% |
| MSCI World-ETF (IWDA) | 63% | +1,1% | -5,2% | -14,0% | +12,3% |
| S&P 500-ETF (SPY, in euro) | 65% | +1,0% | -5,4% | -13,0% | +13,4% |

## Trades

- Aankopen: 198, afgesloten: 195, waarvan winst: 34%
- Gemiddelde winst: €42, gemiddeld verlies: €-18, profit factor: 1,25
- Gemiddeld vastgehouden: 26 dagen; totale kosten: €393
- Kill switch aangegaan: 26 keer (2021-11-09: 3 verliestrades op rij; 2021-12-06: 4 verliestrades op rij; 2022-01-20: 5 verliestrades op rij; 2022-06-17: 3 verliestrades op rij; 2022-08-01: 3 verliestrades op rij; 2022-09-06: 3 verliestrades op rij …)

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
