# Backtest trend-agent

Periode **2021-10-11 t/m 2026-10-09** (ongeveer 5 jaar), startkapitaal €10.000 nepgeld, 50 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de agent het slechter dan gewoon de wereld-ETF vasthouden (+5,2% tegen +79,8%).
- Zijn grootste daling was -5,0%, tegen -21,6% voor de ETF.
- In 50% van alle periodes van 4 weken stond de agent aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -2,1%, het beste +2,4%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | +5,2% | +1,0% | -5,0% | 0.33 | €10.517 |
| MSCI World-ETF (IWDA) | +79,8% | +12,5% | -21,6% | 0.89 | €17.979 |
| S&P 500-ETF (SPY, in euro) | +97,7% | +14,6% | -23,0% | 0.81 | €19.766 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Trend-agent | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2021 | -0,2% | +8,4% | +12,0% |
| 2022 | -3,1% | -13,5% | -13,1% |
| 2023 | +1,6% | +19,9% | +21,5% |
| 2024 | +3,8% | +27,2% | +32,8% |
| 2025 | +2,1% | +7,1% | +4,3% |
| 2026 | +1,0% | +17,4% | +20,6% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Trend-agent | 50% | +0,0% | -1,2% | -2,1% | +2,4% |
| MSCI World-ETF (IWDA) | 66% | +1,4% | -6,0% | -12,4% | +13,6% |
| S&P 500-ETF (SPY, in euro) | 65% | +1,3% | -6,7% | -14,0% | +17,9% |

## Trades

- Aankopen: 196, afgesloten: 193, waarvan winst: 32%
- Gemiddelde winst: €43, gemiddeld verlies: €-17, profit factor: 1,2
- Gemiddeld vastgehouden: 26 dagen; totale kosten: €389
- Kill switch aangegaan: 26 keer (2021-11-09: 3 verliestrades op rij; 2021-12-06: 4 verliestrades op rij; 2022-01-20: 5 verliestrades op rij; 2022-06-17: 3 verliestrades op rij; 2022-08-01: 3 verliestrades op rij; 2022-09-06: 3 verliestrades op rij …)

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
