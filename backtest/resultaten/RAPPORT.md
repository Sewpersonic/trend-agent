# Backtest trend-agent

Periode **2016-11-03 t/m 2026-11-03** (ongeveer 10 jaar), startkapitaal €10.000 nepgeld, 131 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de trend-agent het slechter dan gewoon de wereld-ETF vasthouden (+112,8% tegen +240,7%).
- Zijn grootste daling was -17,0%, tegen -33,6% voor de ETF.
- In 55% van alle periodes van 4 weken stond de trend-agent aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -11,9%, het beste +11,0%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | +112,8% | +7,8% | -17,0% | 0,57 | €21.251 |
| MSCI World-ETF (IWDA) | +240,7% | +13,0% | -33,6% | 0,74 | €34.069 |
| S&P 500-ETF (SPY, in euro) | +320,3% | +15,4% | -33,1% | 0,7 | €42.027 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Trend-agent | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2016 | +16,5% | +11,0% | +13,0% |
| 2017 | +1,2% | +7,5% | +7,8% |
| 2018 | +1,9% | -4,2% | -0,4% |
| 2019 | +15,1% | +29,6% | +34,0% |
| 2020 | +7,0% | +6,2% | +7,8% |
| 2021 | +17,5% | +32,5% | +39,8% |
| 2022 | -13,5% | -13,5% | -13,1% |
| 2023 | +14,9% | +19,9% | +21,5% |
| 2024 | +13,4% | +27,2% | +32,8% |
| 2025 | +9,4% | +7,1% | +4,3% |
| 2026 | -0,7% | +15,6% | +17,2% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | 55% | +0,4% | -3,6% | -11,9% | +11,0% |
| MSCI World-ETF (IWDA) | 65% | +1,1% | -4,8% | -27,7% | +21,1% |
| S&P 500-ETF (SPY, in euro) | 65% | +1,2% | -5,1% | -28,7% | +22,1% |

## Trades

- Aankopen: 927, afgesloten: 920, waarvan winst: 37%
- Gemiddelde winst: €124, gemiddeld verlies: €-55, profit factor: 1,32
- Gemiddeld vastgehouden: 28 dagen; totale kosten: €2.036
- Kill switch aangegaan: 207 keer (2016-11-14: 3 verliestrades op rij; 2016-11-28: dagverlies groter dan 1%; 2017-01-05: dagverlies groter dan 1%; 2017-01-17: dagverlies groter dan 1%; 2017-01-30: dagverlies groter dan 1%; 2017-03-06: dagverlies groter dan 1% …)

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
