# Backtest investeerder (eerlijke test: grootste bedrijven van 2016)

Periode **2016-11-07 t/m 2026-11-05** (ongeveer 10 jaar), startkapitaal €10.000 nepgeld, 90 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de investeerder (eerlijke test: grootste bedrijven van 2016) het beter dan gewoon de wereld-ETF vasthouden (+374,6% tegen +235,6%).
- Zijn grootste daling was -33,2%, tegen -33,6% voor de ETF.
- In 67% van alle periodes van 4 weken stond de investeerder (eerlijke test: grootste bedrijven van 2016) aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -33,0%, het beste +21,0%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Investeerder (eerlijke test: grootste bedrijven van 2016) | +374,6% | +16,9% | -33,2% | 1,05 | €47.399 |
| MSCI World-ETF (IWDA) | +235,6% | +12,9% | -33,6% | 0,87 | €33.559 |
| S&P 500-ETF (SPY, in euro) | +315,7% | +15,3% | -33,1% | 0,82 | €41.574 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Investeerder (eerlijke test: grootste bedrijven van 2016) | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2016 | +8,5% | +9,4% | +10,7% |
| 2017 | +21,5% | +7,5% | +7,8% |
| 2018 | -4,3% | -4,2% | -0,4% |
| 2019 | +28,9% | +29,6% | +34,0% |
| 2020 | +17,9% | +6,2% | +7,8% |
| 2021 | +34,4% | +32,5% | +39,8% |
| 2022 | -4,4% | -13,5% | -13,1% |
| 2023 | +17,8% | +19,9% | +21,5% |
| 2024 | +35,1% | +27,2% | +32,8% |
| 2025 | +5,1% | +7,1% | +4,3% |
| 2026 | +15,2% | +15,6% | +18,4% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Investeerder (eerlijke test: grootste bedrijven van 2016) | 67% | +1,6% | -5,3% | -33,0% | +21,0% |
| MSCI World-ETF (IWDA) | 67% | +1,4% | -5,7% | -31,2% | +23,9% |
| S&P 500-ETF (SPY, in euro) | 66% | +1,5% | -5,7% | -31,0% | +24,3% |

## Trades

- Aankopen: 298, afgesloten: 319, waarvan winst: 60%
- Gemiddelde winst: €185, gemiddeld verlies: €-106, profit factor: 2,62
- Gemiddeld vastgehouden: 67 dagen; totale kosten: €638
- Kill switch aangegaan: 0 keer

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
