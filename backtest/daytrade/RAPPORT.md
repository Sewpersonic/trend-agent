# Test daytrade-bot (nepgeld)

Periode: 2026-08-18 t/m 2026-11-25 (71 beursdagen; de eerste 10 dagen daarvoor dienden alleen om 'normaal volume' te leren). Startbedrag 10.000 nepgeld. Kosten: geen commissie, wel 0,05% slippage per kant.

Belangrijk: dit zijn maar ongeveer 2 maanden. Dat is te kort om iets te bewijzen; het zegt alleen of de regels in deze periode zinnig werkten. Het echte bewijs moet uit het oefenen komen.

## Uitkomst van de regels

| Variant | Rendement | Trades | Winst-% | Gem. R | Grootste daling |
|---|---|---|---|---|---|
| basis | +0,4% | 59 | 52% | -0,01 | -2,8% |
| alleen als de daggrafiek van het aandeel stijgt | -0,3% | 40 | 45% | -0,129 | -1,0% |
| niet als de daggrafiek van de markt daalt | +0,4% | 59 | 52% | -0,01 | -2,8% |
| zonder winstdoel (alleen stop of einde dag) | +0,4% | 58 | 52% | -0,009 | -2,8% |
| zonder marktfilter | -3,4% | 91 | 43% | -0,128 | -5,0% |
| openingsrange 15 minuten | -3,2% | 87 | 40% | -0,187 | -5,7% |
| minder streng op volume (1,0x) | +1,6% | 83 | 51% | -0,01 | -1,5% |
| elke 5 minuten kijken | -1,5% | 67 | 46% | -0,084 | -4,2% |
| alleen kopen tot 11:00 | +0,4% | 44 | 52% | -0,007 | -2,3% |

## Ter vergelijking

- S&P 500 (SPY) de hele periode vasthouden: -6,8%
- SPY elke dag bij de opening kopen en om 15:45 verkopen: -16,4%

## Hoe de basisregels eindigden

- Gestopt door stop-loss: 7
- Winstdoel gehaald: 1
- Verkocht aan het einde van de dag: 51
- Dagen met minstens één trade: 35 van 71

## Indicatie per kans

Uit 112 uitbraken in de koersgeschiedenis (ook die de bot niet kocht). Toets op 14 latere dagen die de indicatie nooit zag: gunstig +0,17 R (7 uitbraken), gemiddeld −0,34 R (37 uitbraken), ongunstig –. Nog geen duidelijk verschil: gebruik de indicatie voorlopig alleen als informatie.

## Wat leert hij van de grafieken?

- Test op oude koersen: 59 trades, 52% met winst, gemiddeld −0,01 R per trade.
- Beter: daggrafiek van de markt (SPY) markt in stijgende trend (35 trades, gemiddeld +0,17 R per trade).
- Slechter: daggrafiek van de markt (SPY) markt zonder richting (24 trades, gemiddeld −0,27 R per trade).
- Beter: opening t.o.v. gisteren lager geopend (16 trades, gemiddeld +0,31 R per trade).

Gem. R: gemiddelde winst of verlies per trade, gemeten in 'risico-eenheden' (1 R = het bedrag dat hij verliest als de stop-loss geraakt wordt). Boven 0 betekent: de winsten wogen zwaarder dan de verliezen.
