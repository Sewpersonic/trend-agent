# Backtest trend-agent

Periode **2021-10-26 t/m 2026-10-26** (ongeveer 5 jaar), startkapitaal €10.000 nepgeld, 52 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de trend-agent het slechter dan gewoon de wereld-ETF vasthouden (+7,4% tegen +72,7%).
- Zijn grootste daling was -4,5%, tegen -21,6% voor de ETF.
- In 54% van alle periodes van 4 weken stond de trend-agent aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -2,7%, het beste +2,5%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | +7,4% | +1,4% | -4,5% | 0,37 | €10.739 |
| MSCI World-ETF (IWDA) | +72,7% | +11,5% | -21,6% | 0,7 | €17.268 |
| S&P 500-ETF (SPY, in euro) | +86,5% | +13,3% | -23,0% | 0,63 | €18.645 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Trend-agent | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2021 | +0,0% | +4,5% | +7,2% |
| 2022 | -2,5% | -13,5% | -13,1% |
| 2023 | +2,2% | +19,9% | +21,5% |
| 2024 | +4,1% | +27,2% | +32,8% |
| 2025 | +1,9% | +7,1% | +4,3% |
| 2026 | +1,6% | +17,0% | +18,9% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | 54% | +0,1% | -1,1% | -2,7% | +2,5% |
| MSCI World-ETF (IWDA) | 63% | +1,0% | -5,2% | -14,0% | +12,3% |
| S&P 500-ETF (SPY, in euro) | 64% | +1,0% | -5,4% | -13,0% | +13,4% |

## Trades

- Aankopen: 196, afgesloten: 193, waarvan winst: 35%
- Gemiddelde winst: €42, gemiddeld verlies: €-18, profit factor: 1,26
- Gemiddeld vastgehouden: 26 dagen; totale kosten: €389
- Kill switch aangegaan: 25 keer (2021-12-06: 3 verliestrades op rij; 2022-01-20: 5 verliestrades op rij; 2022-06-17: 3 verliestrades op rij; 2022-08-01: 3 verliestrades op rij; 2022-09-06: 3 verliestrades op rij; 2022-09-21: 3 verliestrades op rij …)

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
