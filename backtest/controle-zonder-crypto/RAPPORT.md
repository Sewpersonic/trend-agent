# Backtest investeerder (zonder crypto)

Periode **2021-10-29 t/m 2026-10-29** (ongeveer 5 jaar), startkapitaal €10.000 nepgeld, 52 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de investeerder (zonder crypto) het beter dan gewoon de wereld-ETF vasthouden (+152,8% tegen +73,6%).
- Zijn grootste daling was -21,4%, tegen -21,6% voor de ETF.
- In 62% van alle periodes van 4 weken stond de investeerder (zonder crypto) aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -13,2%, het beste +16,9%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Investeerder (zonder crypto) | +152,8% | +20,4% | -21,4% | 1,15 | €25.245 |
| MSCI World-ETF (IWDA) | +73,6% | +11,7% | -21,6% | 0,84 | €17.362 |
| S&P 500-ETF (SPY, in euro) | +87,1% | +13,4% | -23,0% | 0,75 | €18.711 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Investeerder (zonder crypto) | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2021 | -1,0% | +4,3% | +7,1% |
| 2022 | -12,1% | -13,5% | -13,1% |
| 2023 | +29,8% | +19,9% | +21,5% |
| 2024 | +47,6% | +27,2% | +32,8% |
| 2025 | +14,7% | +7,1% | +4,3% |
| 2026 | +32,2% | +17,9% | +19,4% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Investeerder (zonder crypto) | 62% | +1,6% | -6,3% | -13,2% | +16,9% |
| MSCI World-ETF (IWDA) | 66% | +1,3% | -6,0% | -12,4% | +13,6% |
| S&P 500-ETF (SPY, in euro) | 65% | +1,3% | -6,6% | -14,9% | +17,9% |

## Trades

- Aankopen: 130, afgesloten: 133, waarvan winst: 65%
- Gemiddelde winst: €140, gemiddeld verlies: €-94, profit factor: 2,73
- Gemiddeld vastgehouden: 59 dagen; totale kosten: €266
- Kill switch aangegaan: 0 keer

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
