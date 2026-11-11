# Backtest trend-agent

Periode **2016-11-11 t/m 2026-11-11** (ongeveer 10 jaar), startkapitaal €10.000 nepgeld, 131 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de trend-agent het slechter dan gewoon de wereld-ETF vasthouden (+82,4% tegen +232,9%).
- Zijn grootste daling was -13,8%, tegen -33,6% voor de ETF.
- In 57% van alle periodes van 4 weken stond de trend-agent aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -9,7%, het beste +7,8%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | +82,4% | +6,2% | -13,8% | 0,47 | €18.228 |
| MSCI World-ETF (IWDA) | +232,9% | +12,8% | -33,6% | 0,73 | €33.291 |
| S&P 500-ETF (SPY, in euro) | +304,2% | +15,0% | -33,1% | 0,68 | €40.425 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Trend-agent | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2016 | +8,8% | +6,9% | +7,0% |
| 2017 | -1,6% | +7,5% | +7,8% |
| 2018 | +4,3% | -4,2% | -0,4% |
| 2019 | +16,1% | +29,6% | +34,0% |
| 2020 | +7,1% | +6,2% | +7,8% |
| 2021 | +9,7% | +32,5% | +39,8% |
| 2022 | -10,4% | -13,5% | -13,1% |
| 2023 | +4,8% | +19,9% | +21,5% |
| 2024 | +8,1% | +27,2% | +32,8% |
| 2025 | +13,4% | +7,1% | +4,3% |
| 2026 | +4,0% | +17,4% | +19,1% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | 57% | +0,4% | -3,8% | -9,7% | +7,8% |
| MSCI World-ETF (IWDA) | 65% | +1,1% | -4,8% | -27,7% | +21,1% |
| S&P 500-ETF (SPY, in euro) | 65% | +1,2% | -5,1% | -28,7% | +22,1% |

## Trades

- Aankopen: 1004, afgesloten: 997, waarvan winst: 37%
- Gemiddelde winst: €99, gemiddeld verlies: €-47, profit factor: 1,25
- Gemiddeld vastgehouden: 26 dagen; totale kosten: €2.095
- Kill switch aangegaan: 125 keer (2016-12-02: 3 verliestrades op rij; 2017-02-06: 3 verliestrades op rij; 2017-03-21: 3 verliestrades op rij; 2017-04-11: 4 verliestrades op rij; 2017-05-17: dagverlies groter dan 2%; 2017-07-11: 3 verliestrades op rij …)

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
