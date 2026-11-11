# Backtest investeerder

Periode **2016-11-11 t/m 2026-11-11** (ongeveer 10 jaar), startkapitaal €10.000 nepgeld, 131 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de investeerder het beter dan gewoon de wereld-ETF vasthouden (+855,7% tegen +232,9%).
- Zijn grootste daling was -36,7%, tegen -33,6% voor de ETF.
- In 68% van alle periodes van 4 weken stond de investeerder aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -36,5%, het beste +25,8%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Investeerder | +855,7% | +25,3% | -36,7% | 1,29 | €95.440 |
| MSCI World-ETF (IWDA) | +232,9% | +12,8% | -33,6% | 0,86 | €33.291 |
| S&P 500-ETF (SPY, in euro) | +304,2% | +15,0% | -33,1% | 0,81 | €40.425 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Investeerder | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2016 | +13,8% | +6,9% | +7,0% |
| 2017 | +32,9% | +7,5% | +7,8% |
| 2018 | -5,6% | -4,2% | -0,4% |
| 2019 | +34,7% | +29,6% | +34,0% |
| 2020 | +43,1% | +6,2% | +7,8% |
| 2021 | +41,3% | +32,5% | +39,8% |
| 2022 | -13,9% | -13,5% | -13,1% |
| 2023 | +23,8% | +19,9% | +21,5% |
| 2024 | +51,9% | +27,2% | +32,8% |
| 2025 | +18,6% | +7,1% | +4,3% |
| 2026 | +27,9% | +17,4% | +19,1% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Investeerder | 68% | +2,1% | -5,9% | -36,5% | +25,8% |
| MSCI World-ETF (IWDA) | 67% | +1,4% | -5,7% | -31,2% | +23,9% |
| S&P 500-ETF (SPY, in euro) | 66% | +1,5% | -5,7% | -31,0% | +24,3% |

## Trades

- Aankopen: 271, afgesloten: 289, waarvan winst: 73%
- Gemiddelde winst: €374, gemiddeld verlies: €-244, profit factor: 4,08
- Gemiddeld vastgehouden: 69 dagen; totale kosten: €670
- Kill switch aangegaan: 0 keer

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
