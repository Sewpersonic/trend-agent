# Backtest trend-agent (eerlijke test: grootste bedrijven van 2016)

Periode **2016-10-30 t/m 2026-10-30** (ongeveer 10 jaar), startkapitaal €10.000 nepgeld, 90 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de trend-agent (eerlijke test: grootste bedrijven van 2016) het slechter dan gewoon de wereld-ETF vasthouden (+15,9% tegen +231,7%).
- Zijn grootste daling was -27,4%, tegen -33,6% voor de ETF.
- In 51% van alle periodes van 4 weken stond de trend-agent (eerlijke test: grootste bedrijven van 2016) aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -13,7%, het beste +8,5%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Trend-agent (eerlijke test: grootste bedrijven van 2016) | +15,9% | +1,5% | -27,4% | 0,16 | €11.590 |
| MSCI World-ETF (IWDA) | +231,7% | +12,7% | -33,6% | 0,72 | €33.167 |
| S&P 500-ETF (SPY, in euro) | +306,8% | +15,1% | -33,1% | 0,69 | €40.677 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Trend-agent (eerlijke test: grootste bedrijven van 2016) | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2016 | +5,2% | +7,5% | +9,0% |
| 2017 | -3,7% | +7,5% | +7,8% |
| 2018 | +0,4% | -4,2% | -0,4% |
| 2019 | +17,0% | +29,6% | +34,0% |
| 2020 | -9,9% | +6,2% | +7,8% |
| 2021 | +2,5% | +32,5% | +39,8% |
| 2022 | -15,3% | -13,5% | -13,1% |
| 2023 | +6,9% | +19,9% | +21,5% |
| 2024 | -3,1% | +27,2% | +32,8% |
| 2025 | +4,8% | +7,1% | +4,3% |
| 2026 | +14,7% | +16,3% | +17,6% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Trend-agent (eerlijke test: grootste bedrijven van 2016) | 51% | +0,1% | -3,7% | -13,7% | +8,5% |
| MSCI World-ETF (IWDA) | 65% | +1,1% | -4,8% | -27,7% | +21,1% |
| S&P 500-ETF (SPY, in euro) | 66% | +1,2% | -5,1% | -28,7% | +22,1% |

## Trades

- Aankopen: 965, afgesloten: 957, waarvan winst: 35%
- Gemiddelde winst: €69, gemiddeld verlies: €-36, profit factor: 1,03
- Gemiddeld vastgehouden: 27 dagen; totale kosten: €1.936
- Kill switch aangegaan: 201 keer (2016-11-01: dagverlies groter dan 1%; 2016-11-10: 3 verliestrades op rij; 2016-11-16: dagverlies groter dan 1%; 2016-11-28: dagverlies groter dan 1%; 2017-01-17: dagverlies groter dan 1%; 2017-01-30: dagverlies groter dan 1% …)

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
