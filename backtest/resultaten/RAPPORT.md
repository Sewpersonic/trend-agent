# Backtest trend-agent

Periode **2021-10-29 t/m 2026-10-29** (ongeveer 5 jaar), startkapitaal €10.000 nepgeld, 52 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de trend-agent het slechter dan gewoon de wereld-ETF vasthouden (+18,8% tegen +73,8%).
- Zijn grootste daling was -5,6%, tegen -21,6% voor de ETF.
- In 59% van alle periodes van 4 weken stond de trend-agent aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -2,8%, het beste +3,3%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | +18,8% | +3,5% | -5,6% | 0,64 | €11.877 |
| MSCI World-ETF (IWDA) | +73,8% | +11,7% | -21,6% | 0,71 | €17.377 |
| S&P 500-ETF (SPY, in euro) | +88,5% | +13,5% | -23,0% | 0,64 | €18.854 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Trend-agent | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2021 | -0,7% | +4,3% | +7,1% |
| 2022 | -2,5% | -13,5% | -13,1% |
| 2023 | +5,3% | +19,9% | +21,5% |
| 2024 | +8,2% | +27,2% | +32,8% |
| 2025 | +2,3% | +7,1% | +4,3% |
| 2026 | +5,4% | +18,0% | +20,3% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | 59% | +0,2% | -1,5% | -2,8% | +3,3% |
| MSCI World-ETF (IWDA) | 63% | +1,0% | -5,2% | -14,0% | +12,3% |
| S&P 500-ETF (SPY, in euro) | 64% | +1,0% | -5,4% | -13,0% | +13,4% |

## Trades

- Aankopen: 309, afgesloten: 304, waarvan winst: 38%
- Gemiddelde winst: €45, gemiddeld verlies: €-19, profit factor: 1,46
- Gemiddeld vastgehouden: 27 dagen; totale kosten: €613
- Kill switch aangegaan: 35 keer (2021-11-19: 3 verliestrades op rij; 2021-12-03: 3 verliestrades op rij; 2022-01-06: 3 verliestrades op rij; 2022-01-20: 4 verliestrades op rij; 2022-05-09: 3 verliestrades op rij; 2022-06-17: 4 verliestrades op rij …)

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
