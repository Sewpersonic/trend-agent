# Backtest investeerder

Periode **2021-10-13 t/m 2026-10-13** (ongeveer 5 jaar), startkapitaal €10.000 nepgeld, 52 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de investeerder het beter dan gewoon de wereld-ETF vasthouden (+164,4% tegen +82,5%).
- Zijn grootste daling was -21,4%, tegen -21,6% voor de ETF.
- In 61% van alle periodes van 4 weken stond de investeerder aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -13,4%, het beste +16,3%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Investeerder | +164,4% | +21,5% | -21,4% | 1,23 | €26.399 |
| MSCI World-ETF (IWDA) | +82,5% | +12,8% | -21,6% | 0,91 | €18.249 |
| S&P 500-ETF (SPY, in euro) | +96,5% | +14,5% | -23,0% | 0,8 | €19.652 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Investeerder | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2021 | +3,5% | +9,4% | +11,5% |
| 2022 | -11,6% | -13,5% | -13,1% |
| 2023 | +31,0% | +19,9% | +21,5% |
| 2024 | +50,8% | +27,2% | +32,8% |
| 2025 | +10,4% | +7,1% | +4,3% |
| 2026 | +32,4% | +18,1% | +20,4% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Investeerder | 61% | +1,4% | -6,0% | -13,4% | +16,3% |
| MSCI World-ETF (IWDA) | 66% | +1,3% | -6,0% | -12,4% | +13,6% |
| S&P 500-ETF (SPY, in euro) | 65% | +1,3% | -6,6% | -14,9% | +17,9% |

## Trades

- Aankopen: 146, afgesloten: 152, waarvan winst: 66%
- Gemiddelde winst: €137, gemiddeld verlies: €-108, profit factor: 2,52
- Gemiddeld vastgehouden: 66 dagen; totale kosten: €300
- Kill switch aangegaan: 0 keer

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
