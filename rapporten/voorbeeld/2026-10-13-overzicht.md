# Dagoverzicht 2026-10-13

_Twee oefenbots met elk €10.000 nepgeld. Geen beleggingsadvies._

## Stand

| Bot | Waarde | Vandaag | Sinds start | Tegenover wereld-ETF |
| --- | --- | --- | --- | --- |
| Investeerder | €9.918,81 | – | -0,81% | nog te kort |
| Trend-agent | €10.038,91 | €42,63 (+0,43%) | +0,39% | nog te kort |

## Vandaag gedaan

- Investeerder kocht IWDA.AS voor €5.997,00 (doelgewicht 60%)
- Investeerder kocht MU voor €599,00 (doelgewicht 6%)
- Investeerder kocht SMH voor €599,00 (doelgewicht 6%)
- Investeerder kocht ASML.AS voor €599,00 (doelgewicht 6%)
- Investeerder kocht IFX.DE voor €599,00 (doelgewicht 6%)
- Investeerder kocht AMD voor €599,00 (doelgewicht 6%)
- Investeerder kocht ETH-USD voor €499,00 (doelgewicht 5%)
- Investeerder kocht BTC-USD voor €499,00 (doelgewicht 5%)

## Wat de bots uit de analyse halen

**Investeerder**

- De markt stijgt: de kern (wereld-ETF) doet zijn werk, de sterkste aandelen lopen mee.
- Uit de top gevallen: ASML.AS, IFX.DE, SMH. Blijft dat zo, dan worden ze bij de volgende herverdeling (eerste handelsdag van 2026-11) vervangen door CRWD, PANW, INGA.AS.

**Trend-agent**

- De markt stijgt breed: goede omstandigheden voor trendvolgen.
- De markt is rustig: stops liggen dichterbij, posities kunnen iets groter.
- Amerika staat er duidelijk beter voor dan Europa (81% tegen 57% in een stijgende trend).
- 23 van de 50 instrumenten zijn een koopbare trend: veel keus, de bot neemt alleen de rustigste, sterkste.
- Alle plekken zijn bezet, dus de bot koopt niets bij, hoe sterk een trend ook is.

## Verlies en risico

- Trend-agent SHELL.AS: €18,88 (+3,2%), +6,2% boven de stop; raakt hij de stop, dan €17,51 verlies.
- Trend-agent SAP.DE: €13,41 (+3,5%), +8,8% boven de stop; raakt hij de stop, dan €19,72 verlies.
- Trend-agent MSFT: €9,61 (+1,2%), +6,3% boven de stop; raakt hij de stop, dan €20,29 verlies.
- Trend-agent remmen: +0,0% vanaf de top (grens -5%), 0 van 3 verliestrades op rij.
- Investeerder: -€81,19 op de beleggingen; grootste verlies IFX.DE -€30,19 (-5,0%).

## Beste kansen volgens de trend-agent

_Wat de oefenbot met nepgeld zou doen; geen advies. Uitleg per ticker in het trend-rapport._

| Ticker | Instapmoment | Plan van de bot | Max verlies | Status |
| --- | --- | --- | --- | --- |
| Shell (SHELL.AS) | opgelopen | 13 x rond 46.53 EUR, stop 44.72 | €25,59 | al in bezit |
| SAP (SAP.DE) | neutraal | 2 x rond 198.36 EUR, stop 187.65 | €23,42 | al in bezit |
| Wolters Kluwer (WKL.AS) | opgelopen | 5 x rond 78.44 EUR, stop 74.02 | €24,10 | niet gekocht: alle 3 plekken zijn bezet |
| Microsoft (MSFT) | neutraal | 1 x rond 542.31 USD, stop 519.16 | €22,81 | al in bezit |
| Energie-ETF (XLE) | neutraal | 11 x rond 67.40 USD, stop 64.97 | €26,09 | niet gekocht: alle 3 plekken zijn bezet |

## Klaar voor echt geld?

_Eerst bewijzen, dan pas een oefenaccount bij een echte broker, dan een klein bedrag met jouw goedkeuring per order._

**Investeerder:** Nog niet klaar: de bot is nog bezig met bewijzen. Blijven oefenen.

| Eis | Stand | Nu |
| --- | --- | --- |
| Oefentijd | ⏳ | 1 van 63 handelsdagen (ongeveer 3 maanden) |
| Minstens zo goed als de wereld-ETF | ⏳ | nog te weinig dagen |
| Daling niet veel dieper dan de ETF | ✅ | bot -0,81%, ETF +0,00% |

**Trend-agent:** Nog niet klaar: de bot is nog bezig met bewijzen. Blijven oefenen.

| Eis | Stand | Nu |
| --- | --- | --- |
| Oefentijd | ⏳ | 2 van 63 handelsdagen (ongeveer 3 maanden) |
| Minstens zo goed als de wereld-ETF | ⏳ | nog te weinig dagen |
| Grootste daling onder 5% | ✅ | grootste daling tot nu toe -0,04% |
| Genoeg afgesloten trades | ⏳ | 0 van 20 |

## Controles

- Investeerder: status **OK**, 52 van 52 koersen opgehaald, marktregime stijgend-laag.
- Koersbronnen: 0 bevestigd door twee bronnen, 52 uit één bron, 0 afwijkend. Wisselkoers: bevestigd. Tweede bron overgeslagen na herhaalde fouten (GOOGL: Stooq gaf geen koersen ('<!DOCTYPE html><html><head><meta charset')).
- Trend-agent: status **OK**, 50 van 50 koersen opgehaald, marktregime stijgend-laag.
- Koersbronnen: 0 bevestigd door twee bronnen, 50 uit één bron, 0 afwijkend. Wisselkoers: bevestigd. Tweede bron overgeslagen na herhaalde fouten (GOOGL: Stooq gaf geen koersen ('<!DOCTYPE html><html><head><meta charset')).

_GitHub startte deze ronde 16 uur later dan gepland. De koersen zijn die van de slotkoers van deze handelsdag; de vertraging verandert daar niets aan._

## Details

- Investeerder: [2026-10-13-investeerder.md](2026-10-13-investeerder.md)
- Trend-agent: [2026-10-13.md](2026-10-13.md)
- Excel: `investeerder.xlsx` en `trend-agent.xlsx` (met tabblad Grafieken)
