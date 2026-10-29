# Backtest investeerder

Periode **2016-10-31 t/m 2026-10-29** (ongeveer 10 jaar), startkapitaal €10.000 nepgeld, 131 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de investeerder het beter dan gewoon de wereld-ETF vasthouden (+904,9% tegen +238,0%).
- Zijn grootste daling was -36,7%, tegen -33,6% voor de ETF.
- In 69% van alle periodes van 4 weken stond de investeerder aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -36,5%, het beste +25,8%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Investeerder | +904,9% | +26,0% | -36,7% | 1,33 | €100.351 |
| MSCI World-ETF (IWDA) | +238,0% | +13,0% | -33,6% | 0,87 | €33.803 |
| S&P 500-ETF (SPY, in euro) | +316,5% | +15,3% | -33,1% | 0,83 | €41.647 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Investeerder | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2016 | +15,7% | +8,0% | +9,9% |
| 2017 | +33,1% | +7,5% | +7,8% |
| 2018 | -5,6% | -4,2% | -0,4% |
| 2019 | +34,9% | +29,6% | +34,0% |
| 2020 | +43,0% | +6,2% | +7,8% |
| 2021 | +41,1% | +32,5% | +39,8% |
| 2022 | -14,0% | -13,5% | -13,1% |
| 2023 | +23,8% | +19,9% | +21,5% |
| 2024 | +52,1% | +27,2% | +32,8% |
| 2025 | +18,6% | +7,1% | +4,3% |
| 2026 | +32,1% | +17,9% | +19,5% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Investeerder | 69% | +2,1% | -5,8% | -36,5% | +25,8% |
| MSCI World-ETF (IWDA) | 67% | +1,4% | -5,7% | -31,2% | +23,9% |
| S&P 500-ETF (SPY, in euro) | 67% | +1,6% | -5,7% | -31,0% | +24,3% |

## Trades

- Aankopen: 271, afgesloten: 287, waarvan winst: 73%
- Gemiddelde winst: €372, gemiddeld verlies: €-224, profit factor: 4,45
- Gemiddeld vastgehouden: 68 dagen; totale kosten: €661
- Kill switch aangegaan: 0 keer

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
