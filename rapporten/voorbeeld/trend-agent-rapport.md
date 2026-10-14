# Trend-agent rapport 2026-10-14

_Oefenportefeuille met nepgeld. Geen beleggingsadvies; resultaten uit het verleden zeggen niets over de toekomst._

**Status:** OK  
**Waarde:** €10,026.44  
**Kas:** €8,550.41  
**Marktregime:** stijgend-laag  
**Strategieversie:** trend-1.1-d373c7  
**Koersbronnen:** 0 bevestigd door 2 bronnen, 50 uit 1 bron, 0 afwijkend; wisselkoers bevestigd  
**Sinds start:** +0.26%  

## Analyse van vandaag

**Wat de bot zag**

- **Markt (IWDA.AS):** koers 131,81, 9,6% boven het 200-daags gemiddelde (120,29); de afgelopen maand +4,3%. Trend: **stijgend**.
- **Beweeglijkheid:** 8% op jaarbasis, tegen normaal 10% het afgelopen jaar: **laag**.
- **Breedte:** 35 van de 50 instrumenten staan boven hun 200-daags gemiddelde (70%; EU 13 van 23, US 22 van 27).
- **Bekeken:** 50 instrumenten.
- **Afgevallen** (een instrument kan op meer regels afvallen): geen stijgende trend (koers niet boven 50- en 200-daags gemiddelde): 26; niet gestegen over 1 of 3 maanden: 27; te weinig handel: 1.
- **Door de zeef:** 18. Koopbare trends: **18**.

**Wat de bot eruit haalt**

- De markt stijgt breed: goede omstandigheden voor trendvolgen.
- De markt is rustig: stops liggen dichterbij, posities kunnen iets groter.
- Amerika staat er duidelijk beter voor dan Europa (81% tegen 57% in een stijgende trend).
- 3 van de 5 sterkste staan al ver boven hun gemiddelde (SHELL.AS, WKL.AS, XOM): de trend is sterk, maar instappen op zo'n moment kost vaker een terugval.
- Alle plekken zijn bezet, dus de bot koopt niets bij, hoe sterk een trend ook is.

## Vandaag gedaan

- SHELL.AS: stop omhoog van 43.24 naar 43.73
- SAP.DE: stop omhoog van 180.83 naar 181.04

## Verlies en risico

| Ticker | Instap | Koers nu | Resultaat | Stop | Afstand tot stop | Als de stop geraakt wordt |
| --- | --- | --- | --- | --- | --- | --- |
| SHELL.AS | 45.06 EUR | 46.45 | €18,17 (+3,1%) | 43.73 | +6,2% | -€18,23 verlies |
| SAP.DE | 191.56 EUR | 196.94 | €10,77 (+2,8%) | 181.04 | +8,8% | -€22,04 verlies |
| MSFT | 535.34 USD | 533.69 | €0,50 (-0,3%) | 509.90 | +4,7% | -€21,81 verlies |

Raken alle stops tegelijk, dan is het verlies hooguit ongeveer €62,08 (bij een koersgat 's ochtends kan het meer zijn).

**Remmen** (bij overschrijden gaat de kill switch aan en koopt de bot niets meer):

- Daling vanaf de top: +0,00% (grens -5%; top was €10.026,44)
- Vandaag: +0,12% (grens -1%)
- Verliestrades op rij: 0 van 3

## Kansen: wat de bot vandaag het sterkst vond

_Dit is wat de oefenbot met zijn nepgeld volgens zijn eigen regels zou doen. Geen advies voor echt geld; het instapmoment is een ongeteste vuistregel en wordt door de bot niet gebruikt._

### 1. Shell (SHELL.AS): instapmoment **opgelopen**

- **Waarom sterk:** Shell steeg +23,4% in 3 maanden en +8,8% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,0x het normale volume; beweegt gemiddeld 1,9% per dag.
- **Instapmoment:** de koers staat +7,0% van het 20-daags gemiddelde (3,6x de normale dagbeweging) en RSI is 81; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** al in bezit.
- **Plan van de bot:** koop 13 stuks rond 46.48 EUR (inzet €604,22), stop-loss 44.66 EUR (-3,9%). Maximaal verlies als de stop wordt geraakt: ongeveer €25,59. Ter oriëntatie: 2x het risico winst ligt bij 50.11 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 2. SAP (SAP.DE): instapmoment **neutraal**

- **Waarom sterk:** SAP steeg +42,8% in 3 maanden en +5,3% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,8x het normale volume; beweegt gemiddeld 2,8% per dag.
- **Instapmoment:** de koers staat +4,6% van het 20-daags gemiddelde, RSI 66.
- **Status:** al in bezit.
- **Plan van de bot:** koop 2 stuks rond 197.04 EUR (inzet €394,08), stop-loss 186.21 EUR (-5,5%). Maximaal verlies als de stop wordt geraakt: ongeveer €23,66. Ter oriëntatie: 2x het risico winst ligt bij 218.70 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 3. Wolters Kluwer (WKL.AS): instapmoment **opgelopen**

- **Waarom sterk:** Wolters Kluwer steeg +28,2% in 3 maanden en +13,7% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,2x het normale volume; beweegt gemiddeld 2,8% per dag.
- **Instapmoment:** de koers staat +8,9% van het 20-daags gemiddelde (3,2x de normale dagbeweging) en RSI is 73; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 5 stuks rond 78.10 EUR (inzet €390,50), stop-loss 73.68 EUR (-5,7%). Maximaal verlies als de stop wordt geraakt: ongeveer €24,10. Ter oriëntatie: 2x het risico winst ligt bij 86.94 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 4. Energie-ETF (XLE): instapmoment **neutraal**

- **Waarom sterk:** Energie-ETF steeg +19,3% in 3 maanden en +3,2% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,1x het normale volume; beweegt gemiddeld 1,8% per dag.
- **Instapmoment:** de koers staat +5,2% van het 20-daags gemiddelde, RSI 72.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 11 stuks rond 67.66 USD (inzet €666,97), stop-loss 65.22 USD (-3,6%). Maximaal verlies als de stop wordt geraakt: ongeveer €26,10. Ter oriëntatie: 2x het risico winst ligt bij 72.55 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 5. ExxonMobil (XOM): instapmoment **opgelopen**

- **Waarom sterk:** ExxonMobil steeg +22,1% in 3 maanden en +4,5% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 1,8% per dag.
- **Instapmoment:** de koers staat +6,2% van het 20-daags gemiddelde (3,4x de normale dagbeweging) en RSI is 75; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 4 stuks rond 177.10 USD (inzet €634,79), stop-loss 170.67 USD (-3,6%). Maximaal verlies als de stop wordt geraakt: ongeveer €25,03. Ter oriëntatie: 2x het risico winst ligt bij 189.95 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.


## Wat de bot tot nu toe geleerd heeft

- Nog geen afgesloten trades. Leren begint pas als trades zijn afgesloten: dan weet de bot of een instap goed of slecht uitpakte, en onder welke omstandigheden.

## Klaar voor echt geld?

**Trend-agent:** Nog niet klaar: de bot is nog bezig met bewijzen. Blijven oefenen.

| Eis | Stand | Nu |
| --- | --- | --- |
| Oefentijd | ⏳ | 3 van 63 handelsdagen (ongeveer 3 maanden) |
| Minstens zo goed als de wereld-ETF | ⏳ | verschil tot nu toe +0,46% |
| Grootste daling onder 5% | ✅ | grootste daling tot nu toe -0,04% |
| Genoeg afgesloten trades | ⏳ | 0 van 20 |

<details><summary>Zo analyseert de trend-agent (klik om te openen)</summary>

1. **Data controleren.** Koersen van Yahoo, gecontroleerd bij een tweede bron en de wisselkoers bij de ECB.
   Bevroren koersen, rare sprongen of achterlopende markten: dat instrument wordt die dag niet gekocht.
2. **De markt als geheel.** Aan de hand van de wereld-ETF (IWDA) of de S&P 500: staat de koers boven het
   200-daags gemiddelde (stijgend), eronder (dalend) of ertussenin (zijwaarts)? En beweegt de markt meer of
   minder dan normaal vergeleken met het afgelopen jaar? Plus: hoeveel aandelen staan boven hun 200-daags gemiddelde (de breedte).
3. **Elk instrument door de zeef.** Een trend telt alleen als ALLES klopt: koers boven het 50-daags gemiddelde en
   dat boven het 200-daags, plus over 1 en 3 maanden gestegen, genoeg handel en geen verdachte sprong.
4. **Rangschikken.** Score = stijging (60% 3 maanden, 40% 1 maand) gedeeld door de beweeglijkheid. Een rustige,
   stevige stijger wint van een wilde.
5. **Risico bepalen.** Stop-loss op 2x de gemiddelde dagbeweging (ATR) onder de instap. Het aantal stuks wordt zo
   gekozen dat de stop hooguit 0,25% van het vermogen kost.
6. **Beheren.** De stop schuift mee omhoog (3x ATR onder de hoogste slotkoers). Verkopen bij stop of als de koers
   onder het 50-daags gemiddelde sluit.

</details>

## Open posities

| Ticker | Aantal | Instap | Stop | Sinds |
| --- | --- | --- | --- | --- |
| SHELL.AS | 13 | 45.06 EUR | 43.73 | 2026-10-10 |
| SAP.DE | 2 | 191.56 EUR | 181.04 | 2026-10-10 |
| MSFT | 1 | 535.34 USD | 509.90 | 2026-10-10 |

## Sterkste trends vandaag

| # | Ticker | Score | 3 mnd | 1 mnd |
| --- | --- | --- | --- | --- |
| 1 | SHELL.AS | 0.155 | +23.4% | +8.8% |
| 2 | SAP.DE | 0.110 | +42.8% | +5.3% |
| 3 | WKL.AS | 0.106 | +28.2% | +13.7% |
| 4 | XLE | 0.106 | +19.3% | +3.2% |
| 5 | XOM | 0.101 | +22.1% | +4.5% |
| 6 | MSFT | 0.093 | +33.3% | +7.4% |
| 7 | TTE.PA | 0.080 | +15.0% | +0.8% |
| 8 | PLTR | 0.076 | +49.5% | +16.5% |
| 9 | META | 0.053 | +11.1% | +10.1% |
| 10 | V | 0.052 | +7.4% | +4.2% |
