# Backtest investeerder (alleen etf's)

Periode **2016-11-11 t/m 2026-11-11** (ongeveer 10 jaar), startkapitaal €10.000 nepgeld, 131 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de investeerder (alleen etf's) het beter dan gewoon de wereld-ETF vasthouden (+475,5% tegen +232,9%).
- Zijn grootste daling was -31,6%, tegen -33,6% voor de ETF.
- In 69% van alle periodes van 4 weken stond de investeerder (alleen etf's) aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -31,6%, het beste +17,9%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Investeerder (alleen ETF's) | +475,5% | +19,1% | -31,6% | 1,22 | €57.484 |
| MSCI World-ETF (IWDA) | +232,9% | +12,8% | -33,6% | 0,86 | €33.291 |
| S&P 500-ETF (SPY, in euro) | +304,7% | +15,0% | -33,1% | 0,81 | €40.467 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Investeerder (alleen ETF's) | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2016 | +8,8% | +6,9% | +7,0% |
| 2017 | +26,2% | +7,5% | +7,8% |
| 2018 | -5,4% | -4,2% | -0,4% |
| 2019 | +31,7% | +29,6% | +34,0% |
| 2020 | +21,3% | +6,2% | +7,8% |
| 2021 | +47,5% | +32,5% | +39,8% |
| 2022 | -7,5% | -13,5% | -13,1% |
| 2023 | +19,5% | +19,9% | +21,5% |
| 2024 | +35,6% | +27,2% | +32,8% |
| 2025 | +7,9% | +7,1% | +4,3% |
| 2026 | +16,2% | +17,4% | +19,2% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Investeerder (alleen ETF's) | 69% | +1,7% | -5,3% | -31,6% | +17,9% |
| MSCI World-ETF (IWDA) | 67% | +1,4% | -5,7% | -31,2% | +23,9% |
| S&P 500-ETF (SPY, in euro) | 66% | +1,5% | -5,7% | -31,0% | +24,3% |

## Trades

- Aankopen: 123, afgesloten: 137, waarvan winst: 80%
- Gemiddelde winst: €332, gemiddeld verlies: €-130, profit factor: 10,44
- Gemiddeld vastgehouden: 80 dagen; totale kosten: €335
- Kill switch aangegaan: 0 keer

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
