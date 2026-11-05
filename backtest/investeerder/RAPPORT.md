# Backtest investeerder

Periode **2016-11-07 t/m 2026-11-05** (ongeveer 10 jaar), startkapitaal €10.000 nepgeld, 130 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de investeerder het beter dan gewoon de wereld-ETF vasthouden (+924,8% tegen +235,6%).
- Zijn grootste daling was -36,8%, tegen -33,6% voor de ETF.
- In 69% van alle periodes van 4 weken stond de investeerder aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -36,6%, het beste +25,8%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Investeerder | +924,8% | +26,2% | -36,8% | 1,33 | €102.337 |
| MSCI World-ETF (IWDA) | +235,6% | +12,9% | -33,6% | 0,87 | €33.559 |
| S&P 500-ETF (SPY, in euro) | +316,0% | +15,3% | -33,1% | 0,83 | €41.597 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Investeerder | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2016 | +17,7% | +9,4% | +10,7% |
| 2017 | +33,1% | +7,5% | +7,8% |
| 2018 | -5,4% | -4,2% | -0,4% |
| 2019 | +34,8% | +29,6% | +34,0% |
| 2020 | +42,9% | +6,2% | +7,8% |
| 2021 | +40,4% | +32,5% | +39,8% |
| 2022 | -13,8% | -13,5% | -13,1% |
| 2023 | +26,6% | +19,9% | +21,5% |
| 2024 | +56,0% | +27,2% | +32,8% |
| 2025 | +18,6% | +7,1% | +4,3% |
| 2026 | +26,5% | +15,6% | +18,4% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Investeerder | 69% | +2,2% | -5,9% | -36,6% | +25,8% |
| MSCI World-ETF (IWDA) | 67% | +1,4% | -5,7% | -31,2% | +23,9% |
| S&P 500-ETF (SPY, in euro) | 66% | +1,5% | -5,7% | -31,0% | +24,3% |

## Trades

- Aankopen: 279, afgesloten: 298, waarvan winst: 74%
- Gemiddelde winst: €391, gemiddeld verlies: €-271, profit factor: 4,21
- Gemiddeld vastgehouden: 65 dagen; totale kosten: €711
- Kill switch aangegaan: 0 keer

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
