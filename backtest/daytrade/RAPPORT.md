# Test daytrade-bot (nepgeld)

Periode: 2026-08-18 t/m 2026-10-30 (53 beursdagen; de eerste 10 dagen daarvoor dienden alleen om 'normaal volume' te leren). Startbedrag 10.000 nepgeld. Kosten: geen commissie, wel 0,05% slippage per kant.

Belangrijk: dit zijn maar ongeveer 2 maanden. Dat is te kort om iets te bewijzen; het zegt alleen of de regels in deze periode zinnig werkten. Het echte bewijs moet uit het oefenen komen.

## Uitkomst van de regels

| Variant | Rendement | Trades | Winst-% | Gem. R | Grootste daling |
|---|---|---|---|---|---|
| basis | +2,2% | 41 | 63% | 0,106 | -0,8% |
| alleen als de daggrafiek van het aandeel stijgt | +0,1% | 33 | 46% | -0,094 | -1,0% |
| niet als de daggrafiek van de markt daalt | +2,2% | 41 | 63% | 0,106 | -0,8% |
| zonder winstdoel (alleen stop of einde dag) | +2,2% | 40 | 62% | 0,111 | -0,8% |
| zonder marktfilter | -1,4% | 68 | 47% | -0,092 | -2,4% |
| openingsrange 15 minuten | +0,2% | 64 | 47% | -0,11 | -1,9% |
| minder streng op volume (1,0x) | +2,3% | 62 | 55% | 0,058 | -1,2% |
| elke 5 minuten kijken | +0,6% | 47 | 51% | -0,023 | -1,3% |
| alleen kopen tot 11:00 | +2,3% | 30 | 67% | 0,161 | -0,4% |

## Ter vergelijking

- S&P 500 (SPY) de hele periode vasthouden: -1,7%
- SPY elke dag bij de opening kopen en om 15:45 verkopen: -6,6%

## Hoe de basisregels eindigden

- Gestopt door stop-loss: 2
- Winstdoel gehaald: 1
- Verkocht aan het einde van de dag: 38
- Dagen met minstens één trade: 25 van 53

## Indicatie per kans

Uit 76 uitbraken in de koersgeschiedenis (ook die de bot niet kocht). Toets op 10 latere dagen die de indicatie nooit zag: gunstig –, gemiddeld +0,12 R (37 uitbraken), ongunstig –. Nog geen duidelijk verschil: gebruik de indicatie voorlopig alleen als informatie.

## Wat leert hij van de grafieken?

- Test op oude koersen: 41 trades, 63% met winst, gemiddeld +0,11 R per trade.
- Geen situatie die duidelijk beter of slechter was dan de rest.

Gem. R: gemiddelde winst of verlies per trade, gemeten in 'risico-eenheden' (1 R = het bedrag dat hij verliest als de stop-loss geraakt wordt). Boven 0 betekent: de winsten wogen zwaarder dan de verliezen.
