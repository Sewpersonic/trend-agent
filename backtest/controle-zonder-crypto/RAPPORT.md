# Backtest investeerder (zonder crypto)

Periode **2016-10-31 t/m 2026-10-30** (ongeveer 10 jaar), startkapitaal €10.000 nepgeld, 131 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de investeerder (zonder crypto) het beter dan gewoon de wereld-ETF vasthouden (+603,4% tegen +234,6%).
- Zijn grootste daling was -34,6%, tegen -33,6% voor de ETF.
- In 68% van alle periodes van 4 weken stond de investeerder (zonder crypto) aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -34,5%, het beste +28,1%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Investeerder (zonder crypto) | +603,4% | +21,6% | -34,6% | 1,16 | €70.247 |
| MSCI World-ETF (IWDA) | +234,6% | +12,8% | -33,6% | 0,86 | €33.461 |
| S&P 500-ETF (SPY, in euro) | +315,8% | +15,3% | -33,1% | 0,82 | €41.577 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Investeerder (zonder crypto) | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2016 | +14,3% | +8,0% | +9,9% |
| 2017 | +14,2% | +7,5% | +7,8% |
| 2018 | -3,4% | -4,2% | -0,4% |
| 2019 | +34,1% | +29,6% | +34,0% |
| 2020 | +30,2% | +6,2% | +7,8% |
| 2021 | +26,6% | +32,5% | +39,8% |
| 2022 | -14,2% | -13,5% | -13,1% |
| 2023 | +24,0% | +19,9% | +21,5% |
| 2024 | +47,5% | +27,2% | +32,8% |
| 2025 | +21,4% | +7,1% | +4,3% |
| 2026 | +32,4% | +16,7% | +19,3% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Investeerder (zonder crypto) | 68% | +2,0% | -6,0% | -34,5% | +28,1% |
| MSCI World-ETF (IWDA) | 67% | +1,4% | -5,7% | -31,2% | +23,9% |
| S&P 500-ETF (SPY, in euro) | 67% | +1,6% | -5,7% | -31,0% | +24,3% |

## Trades

- Aankopen: 241, afgesloten: 244, waarvan winst: 73%
- Gemiddelde winst: €265, gemiddeld verlies: €-163, profit factor: 4,3
- Gemiddeld vastgehouden: 67 dagen; totale kosten: €517
- Kill switch aangegaan: 0 keer

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
