# Backtest trend-agent (eerlijke test: grootste bedrijven van 2016)

Periode **2016-11-11 t/m 2026-11-11** (ongeveer 10 jaar), startkapitaal €10.000 nepgeld, 90 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de trend-agent (eerlijke test: grootste bedrijven van 2016) het slechter dan gewoon de wereld-ETF vasthouden (+31,8% tegen +232,9%).
- Zijn grootste daling was -16,6%, tegen -33,6% voor de ETF.
- In 52% van alle periodes van 4 weken stond de trend-agent (eerlijke test: grootste bedrijven van 2016) aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -9,7%, het beste +8,7%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Trend-agent (eerlijke test: grootste bedrijven van 2016) | +31,8% | +2,8% | -16,6% | 0,25 | €13.174 |
| MSCI World-ETF (IWDA) | +232,9% | +12,8% | -33,6% | 0,73 | €33.291 |
| S&P 500-ETF (SPY, in euro) | +304,7% | +15,0% | -33,1% | 0,68 | €40.473 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Trend-agent (eerlijke test: grootste bedrijven van 2016) | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2016 | +8,3% | +6,9% | +7,0% |
| 2017 | -3,6% | +7,5% | +7,8% |
| 2018 | +0,2% | -4,2% | -0,4% |
| 2019 | +11,1% | +29,6% | +34,0% |
| 2020 | -7,9% | +6,2% | +7,8% |
| 2021 | +6,7% | +32,5% | +39,8% |
| 2022 | -7,3% | -13,5% | -13,1% |
| 2023 | +5,1% | +19,9% | +21,5% |
| 2024 | +8,6% | +27,2% | +32,8% |
| 2025 | +6,6% | +7,1% | +4,3% |
| 2026 | +2,4% | +17,4% | +19,3% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Trend-agent (eerlijke test: grootste bedrijven van 2016) | 52% | +0,1% | -3,6% | -9,7% | +8,7% |
| MSCI World-ETF (IWDA) | 65% | +1,1% | -4,8% | -27,7% | +21,1% |
| S&P 500-ETF (SPY, in euro) | 65% | +1,2% | -5,1% | -28,7% | +22,1% |

## Trades

- Aankopen: 1008, afgesloten: 1000, waarvan winst: 34%
- Gemiddelde winst: €79, gemiddeld verlies: €-38, profit factor: 1,09
- Gemiddeld vastgehouden: 25 dagen; totale kosten: €2.030
- Kill switch aangegaan: 123 keer (2017-01-31: 3 verliestrades op rij; 2017-03-23: 3 verliestrades op rij; 2017-04-26: 3 verliestrades op rij; 2017-05-17: dagverlies groter dan 2%; 2017-06-09: 3 verliestrades op rij; 2017-06-29: 4 verliestrades op rij …)

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
