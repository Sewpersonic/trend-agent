# Test daytrade-bot (nepgeld)

Periode: 2026-08-14 t/m 2026-10-23 (50 beursdagen; de eerste 10 dagen daarvoor dienden alleen om 'normaal volume' te leren). Startbedrag 10.000 nepgeld. Kosten: geen commissie, wel 0,05% slippage per kant.

Belangrijk: dit zijn maar ongeveer 2 maanden. Dat is te kort om iets te bewijzen; het zegt alleen of de regels in deze periode zinnig werkten. Het echte bewijs moet uit het oefenen komen.

## Uitkomst van de regels

| Variant | Rendement | Trades | Winst-% | Gem. R | Grootste daling |
|---|---|---|---|---|---|
| basis | +2,5% | 37 | 68% | 0,166 | -0,8% |
| alleen als de daggrafiek van het aandeel stijgt | +0,3% | 31 | 48% | -0,061 | -1,0% |
| niet als de daggrafiek van de markt daalt | +2,5% | 37 | 68% | 0,166 | -0,8% |
| zonder winstdoel (alleen stop of einde dag) | +2,5% | 36 | 67% | 0,174 | -0,8% |
| zonder marktfilter | -0,5% | 62 | 50% | -0,038 | -2,0% |
| openingsrange 15 minuten | +0,5% | 58 | 48% | -0,096 | -1,8% |
| minder streng op volume (1,0x) | +2,4% | 56 | 57% | 0,091 | -1,2% |

## Ter vergelijking

- S&P 500 (SPY) de hele periode vasthouden: -2,4%
- SPY elke dag bij de opening kopen en om 15:45 verkopen: -6,7%

## Hoe de basisregels eindigden

- Gestopt door stop-loss: 1
- Winstdoel gehaald: 1
- Verkocht aan het einde van de dag: 35
- Dagen met minstens één trade: 22 van 50

## Indicatie per kans

Uit 69 uitbraken in de koersgeschiedenis (ook die de bot niet kocht). Toets op 9 latere dagen die de indicatie nooit zag: gunstig –, gemiddeld +0,28 R (32 uitbraken), ongunstig –. Nog geen duidelijk verschil: gebruik de indicatie voorlopig alleen als informatie.

## Wat leert hij van de grafieken?

- Test op oude koersen: 37 trades, 68% met winst, gemiddeld +0,17 R per trade.
- Tijdstip van kopen (New York): bij '10:00-10:59' ging het duidelijk beter dan anders (25 trades, gemiddeld +0,30 R, +0,43 R verschil met de rest). Misschien een kans om op te letten.
- Tijdstip van kopen (New York): bij '11:00-11:59' ging het duidelijk slechter dan anders (11 trades, gemiddeld −0,12 R, −0,40 R verschil met de rest). Misschien een situatie om over te slaan.

Gem. R: gemiddelde winst of verlies per trade, gemeten in 'risico-eenheden' (1 R = het bedrag dat hij verliest als de stop-loss geraakt wordt). Boven 0 betekent: de winsten wogen zwaarder dan de verliezen.
