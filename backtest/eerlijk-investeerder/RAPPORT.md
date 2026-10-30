# Backtest investeerder (eerlijke test: grootste bedrijven van 2016)

Periode **2016-10-31 t/m 2026-10-30** (ongeveer 10 jaar), startkapitaal €10.000 nepgeld, 90 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de investeerder (eerlijke test: grootste bedrijven van 2016) het beter dan gewoon de wereld-ETF vasthouden (+367,7% tegen +233,4%).
- Zijn grootste daling was -33,2%, tegen -33,6% voor de ETF.
- In 67% van alle periodes van 4 weken stond de investeerder (eerlijke test: grootste bedrijven van 2016) aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -33,0%, het beste +21,0%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Investeerder (eerlijke test: grootste bedrijven van 2016) | +367,7% | +16,7% | -33,2% | 1,04 | €46.708 |
| MSCI World-ETF (IWDA) | +233,4% | +12,8% | -33,6% | 0,86 | €33.338 |
| S&P 500-ETF (SPY, in euro) | +309,9% | +15,2% | -33,1% | 0,82 | €40.990 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Investeerder (eerlijke test: grootste bedrijven van 2016) | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2016 | +7,1% | +8,0% | +9,9% |
| 2017 | +21,4% | +7,5% | +7,8% |
| 2018 | -4,4% | -4,2% | -0,4% |
| 2019 | +28,9% | +29,6% | +34,0% |
| 2020 | +17,7% | +6,2% | +7,8% |
| 2021 | +34,4% | +32,5% | +39,8% |
| 2022 | -4,4% | -13,5% | -13,1% |
| 2023 | +17,8% | +19,9% | +21,5% |
| 2024 | +35,4% | +27,2% | +32,8% |
| 2025 | +4,8% | +7,1% | +4,3% |
| 2026 | +15,5% | +16,3% | +17,6% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Investeerder (eerlijke test: grootste bedrijven van 2016) | 67% | +1,6% | -5,3% | -33,0% | +21,0% |
| MSCI World-ETF (IWDA) | 67% | +1,4% | -5,7% | -31,2% | +23,9% |
| S&P 500-ETF (SPY, in euro) | 67% | +1,6% | -5,7% | -31,0% | +24,3% |

## Trades

- Aankopen: 299, afgesloten: 320, waarvan winst: 60%
- Gemiddelde winst: €178, gemiddeld verlies: €-95, profit factor: 2,81
- Gemiddeld vastgehouden: 64 dagen; totale kosten: €637
- Kill switch aangegaan: 0 keer

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
