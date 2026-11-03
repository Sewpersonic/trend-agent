# Backtest investeerder (eerlijke test: grootste bedrijven van 2016)

Periode **2016-11-03 t/m 2026-11-03** (ongeveer 10 jaar), startkapitaal €10.000 nepgeld, 90 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de investeerder (eerlijke test: grootste bedrijven van 2016) het beter dan gewoon de wereld-ETF vasthouden (+370,9% tegen +239,0%).
- Zijn grootste daling was -33,2%, tegen -33,6% voor de ETF.
- In 67% van alle periodes van 4 weken stond de investeerder (eerlijke test: grootste bedrijven van 2016) aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -33,0%, het beste +21,0%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Investeerder (eerlijke test: grootste bedrijven van 2016) | +370,9% | +16,8% | -33,2% | 1,04 | €47.027 |
| MSCI World-ETF (IWDA) | +239,0% | +13,0% | -33,6% | 0,87 | €33.905 |
| S&P 500-ETF (SPY, in euro) | +317,9% | +15,4% | -33,1% | 0,83 | €41.794 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Investeerder (eerlijke test: grootste bedrijven van 2016) | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2016 | +10,4% | +11,0% | +13,0% |
| 2017 | +21,3% | +7,5% | +7,8% |
| 2018 | -4,5% | -4,2% | -0,4% |
| 2019 | +28,9% | +29,6% | +34,0% |
| 2020 | +17,4% | +6,2% | +7,8% |
| 2021 | +34,4% | +32,5% | +39,8% |
| 2022 | -4,4% | -13,5% | -13,1% |
| 2023 | +17,8% | +19,9% | +21,5% |
| 2024 | +34,6% | +27,2% | +32,8% |
| 2025 | +4,7% | +7,1% | +4,3% |
| 2026 | +13,9% | +15,1% | +16,6% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Investeerder (eerlijke test: grootste bedrijven van 2016) | 67% | +1,5% | -5,3% | -33,0% | +21,0% |
| MSCI World-ETF (IWDA) | 67% | +1,4% | -5,7% | -31,2% | +23,9% |
| S&P 500-ETF (SPY, in euro) | 67% | +1,6% | -5,7% | -31,0% | +24,3% |

## Trades

- Aankopen: 301, afgesloten: 321, waarvan winst: 61%
- Gemiddelde winst: €182, gemiddeld verlies: €-110, profit factor: 2,57
- Gemiddeld vastgehouden: 66 dagen; totale kosten: €643
- Kill switch aangegaan: 0 keer

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
