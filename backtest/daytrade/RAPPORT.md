# Test daytrade-bot (nepgeld)

Periode: 2026-08-18 t/m 2026-11-20 (68 beursdagen; de eerste 10 dagen daarvoor dienden alleen om 'normaal volume' te leren). Startbedrag 10.000 nepgeld. Kosten: geen commissie, wel 0,05% slippage per kant.

Belangrijk: dit zijn maar ongeveer 2 maanden. Dat is te kort om iets te bewijzen; het zegt alleen of de regels in deze periode zinnig werkten. Het echte bewijs moet uit het oefenen komen.

## Uitkomst van de regels

| Variant | Rendement | Trades | Winst-% | Gem. R | Grootste daling |
|---|---|---|---|---|---|
| basis | +0,3% | 55 | 55% | -0,012 | -2,2% |
| alleen als de daggrafiek van het aandeel stijgt | -0,3% | 39 | 46% | -0,133 | -1,0% |
| niet als de daggrafiek van de markt daalt | +0,3% | 55 | 55% | -0,012 | -2,2% |
| zonder winstdoel (alleen stop of einde dag) | +0,3% | 54 | 54% | -0,011 | -2,2% |
| zonder marktfilter | -3,7% | 86 | 43% | -0,143 | -4,6% |
| openingsrange 15 minuten | -2,9% | 81 | 42% | -0,199 | -5,0% |
| minder streng op volume (1,0x) | +2,0% | 78 | 51% | 0,003 | -1,3% |
| elke 5 minuten kijken | -2,0% | 62 | 45% | -0,109 | -4,0% |
| alleen kopen tot 11:00 | +1,0% | 42 | 57% | 0,025 | -1,8% |

## Ter vergelijking

- S&P 500 (SPY) de hele periode vasthouden: -10,1%
- SPY elke dag bij de opening kopen en om 15:45 verkopen: -17,8%

## Hoe de basisregels eindigden

- Gestopt door stop-loss: 6
- Winstdoel gehaald: 1
- Verkocht aan het einde van de dag: 48
- Dagen met minstens één trade: 33 van 68

## Indicatie per kans

Uit 104 uitbraken in de koersgeschiedenis (ook die de bot niet kocht). Toets op 14 latere dagen die de indicatie nooit zag: gunstig –, gemiddeld −0,14 R (49 uitbraken), ongunstig –. Nog geen duidelijk verschil: gebruik de indicatie voorlopig alleen als informatie.

## Wat leert hij van de grafieken?

- Test op oude koersen: 55 trades, 55% met winst, gemiddeld −0,01 R per trade.
- Beter: daggrafiek van de markt (SPY) markt in stijgende trend (35 trades, gemiddeld +0,17 R per trade).
- Slechter: daggrafiek van de markt (SPY) markt zonder richting (20 trades, gemiddeld −0,34 R per trade).

Gem. R: gemiddelde winst of verlies per trade, gemeten in 'risico-eenheden' (1 R = het bedrag dat hij verliest als de stop-loss geraakt wordt). Boven 0 betekent: de winsten wogen zwaarder dan de verliezen.
