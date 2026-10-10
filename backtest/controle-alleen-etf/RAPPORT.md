# Backtest investeerder (alleen etf's)

Periode **2021-10-11 t/m 2026-10-09** (ongeveer 5 jaar), startkapitaal €10.000 nepgeld, 52 instrumenten met koersdata. Zelfde regels, kosten en slippage als bij het dagelijks oefenen.

> Dit is geen voorspelling. Het laat zien hoe deze regels het in het verleden hadden gedaan.

## In het kort

- Over de hele periode deed de investeerder (alleen etf's) het beter dan gewoon de wereld-ETF vasthouden (+108,8% tegen +80,7%).
- Zijn grootste daling was -19,0%, tegen -21,6% voor de ETF.
- In 64% van alle periodes van 4 weken stond de investeerder (alleen etf's) aan het eind hoger dan aan het begin. Het slechtste blok van 4 weken was -10,7%, het beste +11,2%.

## Totaal

| | Totaal | Per jaar | Grootste daling | Sharpe | Eindwaarde |
| --- | --- | --- | --- | --- | --- |
| Investeerder (alleen ETF's) | +108,8% | +15,9% | -19,0% | 1,14 | €20.852 |
| MSCI World-ETF (IWDA) | +80,7% | +12,6% | -21,6% | 0,89 | €18.074 |
| S&P 500-ETF (SPY, in euro) | +97,7% | +14,6% | -23,0% | 0,81 | €19.766 |

_Sharpe: rendement gedeeld door beweeglijkheid. Boven 1 is goed, onder 0,5 matig._

## Per kalenderjaar

| Jaar | Investeerder (alleen ETF's) | MSCI World-ETF (IWDA) | S&P 500-ETF (SPY, in euro) |
| --- | --- | --- | --- |
| 2021 | +7,5% | +8,4% | +12,0% |
| 2022 | -7,4% | -13,5% | -13,1% |
| 2023 | +18,4% | +19,9% | +21,5% |
| 2024 | +35,4% | +27,2% | +32,8% |
| 2025 | +8,3% | +7,1% | +4,3% |
| 2026 | +20,7% | +18,1% | +20,6% |

## Periodes van 4 weken (20 handelsdagen)

Dit beantwoordt de vraag "wat kan er in een paar weken gebeuren?": elk mogelijk blok van 4 weken in de periode.

| | Hoger geëindigd | Normaal (mediaan) | Slecht (1 op 20) | Slechtste | Beste |
| --- | --- | --- | --- | --- | --- |
| Investeerder (alleen ETF's) | 64% | +1,3% | -5,5% | -10,7% | +11,2% |
| MSCI World-ETF (IWDA) | 66% | +1,3% | -6,0% | -12,4% | +13,6% |
| S&P 500-ETF (SPY, in euro) | 65% | +1,3% | -6,6% | -14,9% | +17,9% |

## Trades

- Aankopen: 56, afgesloten: 62, waarvan winst: 69%
- Gemiddelde winst: €131, gemiddeld verlies: €-55, profit factor: 5,41
- Gemiddeld vastgehouden: 91 dagen; totale kosten: €123
- Kill switch aangegaan: 0 keer

## Belangrijke kanttekeningen

- **Survivorship bias.** De lijst instrumenten is in 2026 gekozen. Aandelen die de afgelopen jaren groot zijn geworden (Nvidia, Palantir, Rheinmetall) staan er daardoor in, en verliezers die uit de indexen zijn verdwenen niet. De echte uitkomst was waarschijnlijk minder goed.
- **Klein risico per trade.** Met 0,25% risico per trade is de agent vaak maar voor een deel belegd. Daardoor zijn zowel winst als verlies kleiner dan bij de ETF.
- **Gratis koersdata** van Yahoo Finance kan fouten of gaten bevatten.
- **Na de kill switch** doet de backtest alsof jij na 5 handelsdagen 'resume' doet.
- Een goed resultaat in het verleden is geen toestemming om met echt geld te handelen.

![Waardeverloop](waardeverloop.png)
