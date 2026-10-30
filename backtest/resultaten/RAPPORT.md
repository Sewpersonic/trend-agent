# Backtest trend-agent

Periode **2016-10-30 t/m 2026-10-30** (ongeveer 10 jaar), startkapitaal €10.000 nepgeld, 131 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de trend-agent het slechter dan gewoon de wereld-ETF vasthouden (+116,0% tegen +233,3%).
- Zijn grootste daling was -17,5%, tegen -33,6% voor de ETF.
- In 56% van alle periodes van 4 weken stond de trend-agent aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -12,3%, het beste +8,0%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | +116,0% | +8,0% | -17,5% | 0,58 | €21.603 |
| MSCI World-ETF (IWDA) | +233,3% | +12,8% | -33,6% | 0,73 | €33.326 |
| S&P 500-ETF (SPY, in euro) | +312,5% | +15,2% | -33,1% | 0,69 | €41.250 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Trend-agent | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2016 | +7,0% | +7,5% | +9,0% |
| 2017 | +2,4% | +7,5% | +7,8% |
| 2018 | +3,4% | -4,2% | -0,4% |
| 2019 | +15,6% | +29,6% | +34,0% |
| 2020 | +7,9% | +6,2% | +7,8% |
| 2021 | +17,2% | +32,5% | +39,8% |
| 2022 | -13,8% | -13,5% | -13,1% |
| 2023 | +15,2% | +19,9% | +21,5% |
| 2024 | +12,7% | +27,2% | +32,8% |
| 2025 | +13,5% | +7,1% | +4,3% |
| 2026 | +2,8% | +16,8% | +19,3% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | 56% | +0,4% | -3,6% | -12,3% | +8,0% |
| MSCI World-ETF (IWDA) | 65% | +1,1% | -4,8% | -27,7% | +21,1% |
| S&P 500-ETF (SPY, in euro) | 66% | +1,2% | -5,1% | -28,7% | +22,1% |

## Trades

- Aankopen: 935, afgesloten: 927, waarvan winst: 36%
- Gemiddelde winst: €123, gemiddeld verlies: €-52, profit factor: 1,33
- Gemiddeld vastgehouden: 28 dagen; totale kosten: €2.034
- Kill switch aangegaan: 208 keer (2016-11-02: 4 verliestrades op rij; 2016-11-10: 3 verliestrades op rij; 2016-11-16: dagverlies groter dan 1%; 2016-11-28: dagverlies groter dan 1%; 2016-12-20: 3 verliestrades op rij; 2017-01-05: dagverlies groter dan 1% …)

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
