# Test daytrade-bot (nepgeld)

Periode: 2026-08-18 t/m 2026-10-30 (53 beursdagen; de eerste 10 dagen daarvoor dienden alleen om 'normaal volume' te leren). Startbedrag 10.000 nepgeld. Kosten: geen commissie, wel 0,05% slippage per kant.

Belangrijk: dit zijn maar ongeveer 2 maanden. Dat is te kort om iets te bewijzen; het zegt alleen of de regels in deze periode zinnig werkten. Het echte bewijs moet uit het oefenen komen.

## Uitkomst van de regels

| Variant | Rendement | Trades | Winst-% | Gem. R | Grootste daling |
|---|---|---|---|---|---|
| basis | +2,2% | 41 | 61% | 0,104 | -0,8% |
| alleen als de daggrafiek van het aandeel stijgt | +0,1% | 33 | 46% | -0,095 | -1,0% |
| niet als de daggrafiek van de markt daalt | +2,2% | 41 | 61% | 0,104 | -0,8% |
| zonder winstdoel (alleen stop of einde dag) | +2,2% | 40 | 60% | 0,109 | -0,8% |
| zonder marktfilter | -1,4% | 68 | 46% | -0,092 | -2,4% |
| openingsrange 15 minuten | +0,1% | 64 | 45% | -0,118 | -1,9% |
| minder streng op volume (1,0x) | +2,0% | 64 | 52% | 0,045 | -1,4% |
| elke 5 minuten kijken | +0,7% | 47 | 49% | -0,018 | -1,3% |
| alleen kopen tot 11:00 | +2,3% | 30 | 63% | 0,159 | -0,4% |

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

- Test op oude koersen: 41 trades, 61% met winst, gemiddeld +0,10 R per trade.
- Slechter: opening t.o.v. gisteren rond gisteren (11 trades, gemiddeld −0,22 R per trade).

Gem. R: gemiddelde winst of verlies per trade, gemeten in 'risico-eenheden' (1 R = het bedrag dat hij verliest als de stop-loss geraakt wordt). Boven 0 betekent: de winsten wogen zwaarder dan de verliezen.
