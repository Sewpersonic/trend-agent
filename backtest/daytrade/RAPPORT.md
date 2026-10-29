# Test daytrade-bot (nepgeld)

Periode: 2026-08-18 t/m 2026-10-29 (52 beursdagen; de eerste 10 dagen daarvoor dienden alleen om 'normaal volume' te leren). Startbedrag 10.000 nepgeld. Kosten: geen commissie, wel 0,05% slippage per kant.

Belangrijk: dit zijn maar ongeveer 2 maanden. Dat is te kort om iets te bewijzen; het zegt alleen of de regels in deze periode zinnig werkten. Het echte bewijs moet uit het oefenen komen.

## Uitkomst van de regels

| Variant | Rendement | Trades | Winst-% | Gem. R | Grootste daling |
|---|---|---|---|---|---|
| basis | +1,7% | 42 | 62% | 0,079 | -0,8% |
| alleen als de daggrafiek van het aandeel stijgt | -0,3% | 34 | 44% | -0,122 | -1,0% |
| niet als de daggrafiek van de markt daalt | +1,7% | 42 | 62% | 0,079 | -0,8% |
| zonder winstdoel (alleen stop of einde dag) | +1,7% | 41 | 61% | 0,083 | -0,8% |
| zonder marktfilter | -0,8% | 66 | 48% | -0,063 | -1,8% |
| openingsrange 15 minuten | +0,2% | 64 | 47% | -0,11 | -1,9% |
| minder streng op volume (1,0x) | +2,2% | 62 | 55% | 0,062 | -1,2% |
| elke 5 minuten kijken | +0,6% | 47 | 51% | -0,023 | -1,3% |
| alleen kopen tot 11:00 | +2,3% | 30 | 67% | 0,161 | -0,4% |

## Ter vergelijking

- S&P 500 (SPY) de hele periode vasthouden: +0,1%
- SPY elke dag bij de opening kopen en om 15:45 verkopen: -5,5%

## Hoe de basisregels eindigden

- Gestopt door stop-loss: 3
- Winstdoel gehaald: 1
- Verkocht aan het einde van de dag: 38
- Dagen met minstens één trade: 25 van 52

## Indicatie per kans

Uit 76 uitbraken in de koersgeschiedenis (ook die de bot niet kocht). Toets op 10 latere dagen die de indicatie nooit zag: gunstig –, gemiddeld +0,12 R (37 uitbraken), ongunstig –. Nog geen duidelijk verschil: gebruik de indicatie voorlopig alleen als informatie.

## Wat leert hij van de grafieken?

- Test op oude koersen: 42 trades, 62% met winst, gemiddeld +0,08 R per trade.
- Geen situatie die duidelijk beter of slechter was dan de rest.

Gem. R: gemiddelde winst of verlies per trade, gemeten in 'risico-eenheden' (1 R = het bedrag dat hij verliest als de stop-loss geraakt wordt). Boven 0 betekent: de winsten wogen zwaarder dan de verliezen.
