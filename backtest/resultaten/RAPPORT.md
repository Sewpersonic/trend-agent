# Backtest trend-agent

Periode **2016-10-29 t/m 2026-10-29** (ongeveer 10 jaar), startkapitaal €10.000 nepgeld, 131 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de trend-agent het slechter dan gewoon de wereld-ETF vasthouden (+13,3% tegen +236,3%).
- Zijn grootste daling was -10,4%, tegen -33,6% voor de ETF.
- In 54% van alle periodes van 4 weken stond de trend-agent aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -4,0%, het beste +3,2%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | +13,3% | +1,3% | -10,4% | 0,25 | €11.326 |
| MSCI World-ETF (IWDA) | +236,3% | +12,9% | -33,6% | 0,73 | €33.630 |
| S&P 500-ETF (SPY, in euro) | +313,3% | +15,2% | -33,1% | 0,69 | €41.329 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Trend-agent | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2016 | +1,7% | +7,5% | +9,0% |
| 2017 | +0,1% | +7,5% | +7,8% |
| 2018 | -0,5% | -4,2% | -0,4% |
| 2019 | +2,7% | +29,6% | +34,0% |
| 2020 | +2,7% | +6,2% | +7,8% |
| 2021 | +2,8% | +32,5% | +39,8% |
| 2022 | -6,9% | -13,5% | -13,1% |
| 2023 | +5,3% | +19,9% | +21,5% |
| 2024 | +3,1% | +27,2% | +32,8% |
| 2025 | +1,6% | +7,1% | +4,3% |
| 2026 | +0,5% | +17,9% | +19,5% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | 54% | +0,1% | -1,6% | -4,0% | +3,2% |
| MSCI World-ETF (IWDA) | 65% | +1,1% | -4,8% | -27,7% | +21,1% |
| S&P 500-ETF (SPY, in euro) | 66% | +1,2% | -5,1% | -28,7% | +22,1% |

## Trades

- Aankopen: 625, afgesloten: 620, waarvan winst: 35%
- Gemiddelde winst: €42, gemiddeld verlies: €-20, profit factor: 1,12
- Gemiddeld vastgehouden: 27 dagen; totale kosten: €1.245
- Kill switch aangegaan: 75 keer (2016-11-02: 3 verliestrades op rij; 2016-12-01: 3 verliestrades op rij; 2017-03-03: 3 verliestrades op rij; 2017-05-17: dagverlies groter dan 1%; 2017-07-24: 3 verliestrades op rij; 2017-09-20: 3 verliestrades op rij …)

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
