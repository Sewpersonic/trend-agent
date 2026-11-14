# Test daytrade-bot (nepgeld)

Periode: 2026-08-18 t/m 2026-11-13 (63 beursdagen; de eerste 10 dagen daarvoor dienden alleen om 'normaal volume' te leren). Startbedrag 10.000 nepgeld. Kosten: geen commissie, wel 0,05% slippage per kant.

Belangrijk: dit zijn maar ongeveer 2 maanden. Dat is te kort om iets te bewijzen; het zegt alleen of de regels in deze periode zinnig werkten. Het echte bewijs moet uit het oefenen komen.

## Uitkomst van de regels

| Variant | Rendement | Trades | Winst-% | Gem. R | Grootste daling |
|---|---|---|---|---|---|
| basis | +0,6% | 53 | 55% | 0,021 | -1,8% |
| alleen als de daggrafiek van het aandeel stijgt | +0,2% | 37 | 49% | -0,087 | -1,0% |
| niet als de daggrafiek van de markt daalt | +0,6% | 53 | 55% | 0,021 | -1,8% |
| zonder winstdoel (alleen stop of einde dag) | +0,6% | 52 | 54% | 0,023 | -1,8% |
| zonder marktfilter | -3,7% | 82 | 43% | -0,137 | -4,6% |
| openingsrange 15 minuten | -1,9% | 77 | 43% | -0,163 | -3,8% |
| minder streng op volume (1,0x) | +1,9% | 77 | 52% | 0,011 | -1,2% |
| elke 5 minuten kijken | -1,2% | 60 | 47% | -0,079 | -3,2% |
| alleen kopen tot 11:00 | +1,3% | 40 | 57% | 0,07 | -1,6% |

## Ter vergelijking

- S&P 500 (SPY) de hele periode vasthouden: -1,9%
- SPY elke dag bij de opening kopen en om 15:45 verkopen: -9,5%

## Hoe de basisregels eindigden

- Gestopt door stop-loss: 5
- Winstdoel gehaald: 1
- Verkocht aan het einde van de dag: 47
- Dagen met minstens één trade: 32 van 63

## Indicatie per kans

Uit 102 uitbraken in de koersgeschiedenis (ook die de bot niet kocht). Toets op 13 latere dagen die de indicatie nooit zag: gunstig –, gemiddeld −0,10 R (47 uitbraken), ongunstig –. Nog geen duidelijk verschil: gebruik de indicatie voorlopig alleen als informatie.

## Wat leert hij van de grafieken?

- Test op oude koersen: 53 trades, 55% met winst, gemiddeld +0,02 R per trade.
- Beter: daggrafiek van de markt (SPY) markt in stijgende trend (35 trades, gemiddeld +0,17 R per trade).
- Slechter: daggrafiek van de markt (SPY) markt zonder richting (18 trades, gemiddeld −0,27 R per trade).

Gem. R: gemiddelde winst of verlies per trade, gemeten in 'risico-eenheden' (1 R = het bedrag dat hij verliest als de stop-loss geraakt wordt). Boven 0 betekent: de winsten wogen zwaarder dan de verliezen.
