# Test daytrade-bot (nepgeld)

Periode: 2026-08-18 t/m 2026-10-26 (49 beursdagen; de eerste 10 dagen daarvoor dienden alleen om 'normaal volume' te leren). Startbedrag 10.000 nepgeld. Kosten: geen commissie, wel 0,05% slippage per kant.

Belangrijk: dit zijn maar ongeveer 2 maanden. Dat is te kort om iets te bewijzen; het zegt alleen of de regels in deze periode zinnig werkten. Het echte bewijs moet uit het oefenen komen.

## Uitkomst van de regels

| Variant | Rendement | Trades | Winst-% | Gem. R | Grootste daling |
|---|---|---|---|---|---|
| basis | +2,1% | 39 | 62% | 0,132 | -0,8% |
| alleen als de daggrafiek van het aandeel stijgt | +0,2% | 32 | 47% | -0,063 | -1,0% |
| niet als de daggrafiek van de markt daalt | +2,1% | 39 | 62% | 0,132 | -0,8% |
| zonder winstdoel (alleen stop of einde dag) | +2,1% | 38 | 60% | 0,138 | -0,8% |
| zonder marktfilter | -0,4% | 63 | 48% | -0,039 | -1,7% |
| openingsrange 15 minuten | +0,1% | 60 | 45% | -0,115 | -1,9% |
| minder streng op volume (1,0x) | +1,8% | 60 | 52% | 0,057 | -1,4% |

## Ter vergelijking

- S&P 500 (SPY) de hele periode vasthouden: -0,4%
- SPY elke dag bij de opening kopen en om 15:45 verkopen: -5,5%

## Hoe de basisregels eindigden

- Gestopt door stop-loss: 1
- Winstdoel gehaald: 1
- Verkocht aan het einde van de dag: 37
- Dagen met minstens één trade: 23 van 49

## Indicatie per kans

Uit 73 uitbraken in de koersgeschiedenis (ook die de bot niet kocht). Toets op 10 latere dagen die de indicatie nooit zag: gunstig –, gemiddeld +0,19 R (36 uitbraken), ongunstig –. Nog geen duidelijk verschil: gebruik de indicatie voorlopig alleen als informatie.

## Wat leert hij van de grafieken?

- Test op oude koersen: 39 trades, 62% met winst, gemiddeld +0,13 R per trade.
- Beter: tijdstip van kopen (New York) 10:00-10:59 (27 trades, gemiddeld +0,25 R per trade).
- Slechter: tijdstip van kopen (New York) 11:00-11:59 (11 trades, gemiddeld −0,12 R per trade).

Gem. R: gemiddelde winst of verlies per trade, gemeten in 'risico-eenheden' (1 R = het bedrag dat hij verliest als de stop-loss geraakt wordt). Boven 0 betekent: de winsten wogen zwaarder dan de verliezen.
