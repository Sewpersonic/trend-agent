# Backtest trend-agent

Periode **2021-10-29 t/m 2026-10-29** (ongeveer 5 jaar), startkapitaal €10.000 nepgeld, 52 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de trend-agent het slechter dan gewoon de wereld-ETF vasthouden (+16,1% tegen +73,6%).
- Zijn grootste daling was -6,8%, tegen -21,6% voor de ETF.
- In 55% van alle periodes van 4 weken stond de trend-agent aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -2,6%, het beste +3,3%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | +16,1% | +3,0% | -6,8% | 0,61 | €11.600 |
| MSCI World-ETF (IWDA) | +73,6% | +11,7% | -21,6% | 0,71 | €17.362 |
| S&P 500-ETF (SPY, in euro) | +87,1% | +13,4% | -23,0% | 0,63 | €18.713 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Trend-agent | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2021 | +0,2% | +4,3% | +7,1% |
| 2022 | -5,1% | -13,5% | -13,1% |
| 2023 | +3,0% | +19,9% | +21,5% |
| 2024 | +9,8% | +27,2% | +32,8% |
| 2025 | +2,7% | +7,1% | +4,3% |
| 2026 | +5,2% | +17,9% | +19,4% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | 55% | +0,2% | -1,4% | -2,6% | +3,3% |
| MSCI World-ETF (IWDA) | 63% | +1,0% | -5,2% | -14,0% | +12,3% |
| S&P 500-ETF (SPY, in euro) | 64% | +1,0% | -5,4% | -13,0% | +13,4% |

## Trades

- Aankopen: 313, afgesloten: 308, waarvan winst: 36%
- Gemiddelde winst: €44, gemiddeld verlies: €-18, profit factor: 1,34
- Gemiddeld vastgehouden: 27 dagen; totale kosten: €621
- Kill switch aangegaan: 41 keer (2021-12-06: 4 verliestrades op rij; 2022-01-06: 4 verliestrades op rij; 2022-01-20: 4 verliestrades op rij; 2022-02-07: 3 verliestrades op rij; 2022-02-17: 3 verliestrades op rij; 2022-03-03: 3 verliestrades op rij …)

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
