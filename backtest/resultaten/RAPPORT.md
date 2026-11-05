# Backtest trend-agent

Periode **2016-11-05 t/m 2026-11-05** (ongeveer 10 jaar), startkapitaal €10.000 nepgeld, 130 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de trend-agent het slechter dan gewoon de wereld-ETF vasthouden (+63,1% tegen +241,8%).
- Zijn grootste daling was -21,3%, tegen -33,6% voor de ETF.
- In 55% van alle periodes van 4 weken stond de trend-agent aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -10,3%, het beste +9,3%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | +63,1% | +5,0% | -21,3% | 0,39 | €16.310 |
| MSCI World-ETF (IWDA) | +241,8% | +13,1% | -33,6% | 0,74 | €34.182 |
| S&P 500-ETF (SPY, in euro) | +325,2% | +15,6% | -33,1% | 0,71 | €42.519 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Trend-agent | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2016 | +13,5% | +11,4% | +13,2% |
| 2017 | -0,1% | +7,5% | +7,8% |
| 2018 | -6,7% | -4,2% | -0,4% |
| 2019 | +10,9% | +29,6% | +34,0% |
| 2020 | +13,7% | +6,2% | +7,8% |
| 2021 | +17,9% | +32,5% | +39,8% |
| 2022 | -18,1% | -13,5% | -13,1% |
| 2023 | +7,5% | +19,9% | +21,5% |
| 2024 | +7,8% | +27,2% | +32,8% |
| 2025 | +7,2% | +7,1% | +4,3% |
| 2026 | +2,1% | +15,6% | +18,4% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | 55% | +0,4% | -4,2% | -10,3% | +9,3% |
| MSCI World-ETF (IWDA) | 65% | +1,1% | -4,8% | -27,7% | +21,1% |
| S&P 500-ETF (SPY, in euro) | 65% | +1,2% | -5,1% | -28,7% | +22,1% |

## Trades

- Aankopen: 984, afgesloten: 976, waarvan winst: 35%
- Gemiddelde winst: €101, gemiddeld verlies: €-46, profit factor: 1,19
- Gemiddeld vastgehouden: 27 dagen; totale kosten: €2.031
- Kill switch aangegaan: 120 keer (2016-11-10: 3 verliestrades op rij; 2017-01-05: 3 verliestrades op rij; 2017-02-24: 3 verliestrades op rij; 2017-03-14: 3 verliestrades op rij; 2017-04-11: 3 verliestrades op rij; 2017-06-16: 4 verliestrades op rij …)

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
