# Backtest trend-agent

Periode **2021-10-13 t/m 2026-10-13** (ongeveer 5 jaar), startkapitaal €10.000 nepgeld, 51 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de trend-agent het slechter dan gewoon de wereld-ETF vasthouden (+6,0% tegen +83,1%).
- Zijn grootste daling was -4,5%, tegen -21,6% voor de ETF.
- In 52% van alle periodes van 4 weken stond de trend-agent aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -2,7%, het beste +3,1%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | +6,0% | +1,2% | -4,5% | 0,31 | €10.597 |
| MSCI World-ETF (IWDA) | +83,1% | +12,9% | -21,6% | 0,77 | €18.307 |
| S&P 500-ETF (SPY, in euro) | +97,0% | +14,5% | -23,0% | 0,68 | €19.699 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Trend-agent | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2021 | +0,1% | +9,4% | +11,5% |
| 2022 | -2,5% | -13,5% | -13,1% |
| 2023 | +2,1% | +19,9% | +21,5% |
| 2024 | +4,8% | +27,2% | +32,8% |
| 2025 | +0,7% | +7,1% | +4,3% |
| 2026 | +0,8% | +18,5% | +20,7% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | 52% | +0,0% | -1,1% | -2,7% | +3,1% |
| MSCI World-ETF (IWDA) | 63% | +1,1% | -5,2% | -14,0% | +12,3% |
| S&P 500-ETF (SPY, in euro) | 65% | +1,0% | -5,4% | -13,0% | +13,4% |

## Trades

- Aankopen: 202, afgesloten: 199, waarvan winst: 34%
- Gemiddelde winst: €42, gemiddeld verlies: €-18, profit factor: 1,22
- Gemiddeld vastgehouden: 26 dagen; totale kosten: €401
- Kill switch aangegaan: 28 keer (2021-11-09: 3 verliestrades op rij; 2021-12-06: 3 verliestrades op rij; 2022-01-20: 5 verliestrades op rij; 2022-06-17: 3 verliestrades op rij; 2022-08-01: 3 verliestrades op rij; 2022-09-06: 3 verliestrades op rij …)

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
