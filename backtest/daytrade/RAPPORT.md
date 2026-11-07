# Test daytrade-bot (nepgeld)

Periode: 2026-08-18 t/m 2026-11-06 (58 beursdagen; de eerste 10 dagen daarvoor dienden alleen om 'normaal volume' te leren). Startbedrag 10.000 nepgeld. Kosten: geen commissie, wel 0,05% slippage per kant.

Belangrijk: dit zijn maar ongeveer 2 maanden. Dat is te kort om iets te bewijzen; het zegt alleen of de regels in deze periode zinnig werkten. Het echte bewijs moet uit het oefenen komen.

## Uitkomst van de regels

| Variant | Rendement | Trades | Winst-% | Gem. R | Grootste daling |
|---|---|---|---|---|---|
| basis | +0,8% | 49 | 55% | 0,03 | -1,6% |
| alleen als de daggrafiek van het aandeel stijgt | +0,2% | 37 | 49% | -0,087 | -1,0% |
| niet als de daggrafiek van de markt daalt | +0,8% | 49 | 55% | 0,03 | -1,6% |
| zonder winstdoel (alleen stop of einde dag) | +0,8% | 48 | 54% | 0,033 | -1,6% |
| zonder marktfilter | -3,5% | 78 | 42% | -0,139 | -4,4% |
| openingsrange 15 minuten | -1,3% | 72 | 43% | -0,158 | -3,2% |
| minder streng op volume (1,0x) | +1,1% | 72 | 50% | -0,011 | -1,2% |
| elke 5 minuten kijken | -1,1% | 56 | 46% | -0,081 | -3,1% |
| alleen kopen tot 11:00 | +1,1% | 37 | 57% | 0,059 | -1,6% |

## Ter vergelijking

- S&P 500 (SPY) de hele periode vasthouden: -4,3%
- SPY elke dag bij de opening kopen en om 15:45 verkopen: -10,7%

## Hoe de basisregels eindigden

- Gestopt door stop-loss: 4
- Winstdoel gehaald: 1
- Verkocht aan het einde van de dag: 44
- Dagen met minstens één trade: 29 van 58

## Indicatie per kans

Uit 97 uitbraken in de koersgeschiedenis (ook die de bot niet kocht). Toets op 12 latere dagen die de indicatie nooit zag: gunstig –, gemiddeld −0,02 R (50 uitbraken), ongunstig –. Nog geen duidelijk verschil: gebruik de indicatie voorlopig alleen als informatie.

## Wat leert hij van de grafieken?

- Test op oude koersen: 49 trades, 55% met winst, gemiddeld +0,03 R per trade.
- Beter: daggrafiek van de markt (SPY) markt in stijgende trend (35 trades, gemiddeld +0,17 R per trade).
- Slechter: daggrafiek van de markt (SPY) markt zonder richting (14 trades, gemiddeld −0,32 R per trade).

Gem. R: gemiddelde winst of verlies per trade, gemeten in 'risico-eenheden' (1 R = het bedrag dat hij verliest als de stop-loss geraakt wordt). Boven 0 betekent: de winsten wogen zwaarder dan de verliezen.
