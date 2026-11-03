# Backtest trend-agent (eerlijke test: grootste bedrijven van 2016)

Periode **2016-11-03 t/m 2026-11-03** (ongeveer 10 jaar), startkapitaal €10.000 nepgeld, 90 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de trend-agent (eerlijke test: grootste bedrijven van 2016) het slechter dan gewoon de wereld-ETF vasthouden (+32,0% tegen +239,0%).
- Zijn grootste daling was -23,6%, tegen -33,6% voor de ETF.
- In 51% van alle periodes van 4 weken stond de trend-agent (eerlijke test: grootste bedrijven van 2016) aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -8,2%, het beste +10,0%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Trend-agent (eerlijke test: grootste bedrijven van 2016) | +32,0% | +2,8% | -23,6% | 0,25 | €13.183 |
| MSCI World-ETF (IWDA) | +239,0% | +13,0% | -33,6% | 0,74 | €33.905 |
| S&P 500-ETF (SPY, in euro) | +317,9% | +15,4% | -33,1% | 0,7 | €41.794 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Trend-agent (eerlijke test: grootste bedrijven van 2016) | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2016 | +14,3% | +11,0% | +13,0% |
| 2017 | -1,1% | +7,5% | +7,8% |
| 2018 | -0,6% | -4,2% | -0,4% |
| 2019 | +17,1% | +29,6% | +34,0% |
| 2020 | -3,4% | +6,2% | +7,8% |
| 2021 | +0,6% | +32,5% | +39,8% |
| 2022 | -15,0% | -13,5% | -13,1% |
| 2023 | +9,5% | +19,9% | +21,5% |
| 2024 | -5,3% | +27,2% | +32,8% |
| 2025 | +4,4% | +7,1% | +4,3% |
| 2026 | +12,4% | +15,1% | +16,6% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Trend-agent (eerlijke test: grootste bedrijven van 2016) | 51% | +0,1% | -3,6% | -8,2% | +10,0% |
| MSCI World-ETF (IWDA) | 65% | +1,1% | -4,8% | -27,7% | +21,1% |
| S&P 500-ETF (SPY, in euro) | 65% | +1,2% | -5,1% | -28,7% | +22,1% |

## Trades

- Aankopen: 954, afgesloten: 947, waarvan winst: 36%
- Gemiddelde winst: €79, gemiddeld verlies: €-40, profit factor: 1,1
- Gemiddeld vastgehouden: 27 dagen; totale kosten: €1.937
- Kill switch aangegaan: 194 keer (2016-11-14: 3 verliestrades op rij; 2016-11-28: dagverlies groter dan 1%; 2017-01-17: dagverlies groter dan 1%; 2017-01-30: dagverlies groter dan 1%; 2017-03-06: dagverlies groter dan 1%; 2017-03-21: dagverlies groter dan 1% …)

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
