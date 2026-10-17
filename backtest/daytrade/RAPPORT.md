# Test daytrade-bot (nepgeld)

Periode: 2026-08-07 t/m 2026-10-16 (50 beursdagen; de eerste 10 dagen daarvoor dienden alleen om 'normaal volume' te leren). Startbedrag 10.000 nepgeld. Kosten: geen commissie, wel 0,05% slippage per kant.

Belangrijk: dit zijn maar ongeveer 2 maanden. Dat is te kort om iets te bewijzen; het zegt alleen of de regels in deze periode zinnig werkten. Het echte bewijs moet uit het oefenen komen.

## Uitkomst van de regels

| Variant | Rendement | Trades | Winst-% | Gem. R | Grootste daling |
|---|---|---|---|---|---|
| basis | +2,3% | 38 | 63% | 0,15 | -0,9% |
| alleen als de daggrafiek van het aandeel stijgt | +0,4% | 31 | 48% | -0,054 | -1,0% |
| niet als de daggrafiek van de markt daalt | +2,3% | 38 | 63% | 0,15 | -0,9% |
| zonder winstdoel (alleen stop of einde dag) | +2,3% | 37 | 62% | 0,157 | -0,9% |
| zonder marktfilter | -0,4% | 62 | 48% | -0,034 | -2,1% |
| openingsrange 15 minuten | +2,1% | 52 | 52% | -0,016 | -1,3% |
| minder streng op volume (1,0x) | +0,7% | 56 | 52% | 0,028 | -1,5% |

## Ter vergelijking

- S&P 500 (SPY) de hele periode vasthouden: -1,0%
- SPY elke dag bij de opening kopen en om 15:45 verkopen: -6,9%

## Hoe de basisregels eindigden

- Gestopt door stop-loss: 1
- Winstdoel gehaald: 1
- Verkocht aan het einde van de dag: 36
- Dagen met minstens één trade: 22 van 50

## Wat leert hij van de grafieken?

- Test op oude koersen: 38 trades, 63% met winst, gemiddeld +0,15 R per trade.
- Tijdstip van kopen (New York): bij '10:00-10:59' ging het duidelijk beter dan anders (25 trades, gemiddeld +0,27 R, +0,36 R verschil met de rest). Misschien een kans om op te letten.

Gem. R: gemiddelde winst of verlies per trade, gemeten in 'risico-eenheden' (1 R = het bedrag dat hij verliest als de stop-loss geraakt wordt). Boven 0 betekent: de winsten wogen zwaarder dan de verliezen.
