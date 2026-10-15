# Trend-agent rapport 2026-10-14

_Oefenportefeuille met nepgeld. Geen beleggingsadvies; resultaten uit het verleden zeggen niets over de toekomst._

**Status:** OK  
**Waarde:** €10,029.19  
**Kas:** €8,550.41  
**Marktregime:** stijgend-normaal  
**Strategieversie:** trend-1.1-d373c7  
**Koersbronnen:** 0 bevestigd door 2 bronnen, 50 uit 1 bron, 0 afwijkend; wisselkoers bevestigd  
**Sinds start:** +0.29%  

## Analyse van vandaag

**Wat de bot zag**

- **Markt (IWDA.AS):** koers 130,18, 8,1% boven het 200-daags gemiddelde (120,38); de afgelopen maand +3,5%. Trend: **stijgend**.
- **Beweeglijkheid:** 10% op jaarbasis, tegen normaal 10% het afgelopen jaar: **normaal**.
- **Breedte:** 34 van de 50 instrumenten staan boven hun 200-daags gemiddelde (68%; EU 12 van 23, US 22 van 27).
- **Bekeken:** 50 instrumenten.
- **Afgevallen** (een instrument kan op meer regels afvallen): geen stijgende trend (koers niet boven 50- en 200-daags gemiddelde): 28; niet gestegen over 1 of 3 maanden: 26; te weinig handel: 1.
- **Door de zeef:** 17. Koopbare trends: **17**.

**Wat de bot eruit haalt**

- De markt stijgt breed: goede omstandigheden voor trendvolgen.
- Amerika staat er duidelijk beter voor dan Europa (81% tegen 52% in een stijgende trend).
- 3 van de 5 sterkste staan al ver boven hun gemiddelde (SHELL.AS, WKL.AS, XOM): de trend is sterk, maar instappen op zo'n moment kost vaker een terugval.
- Alle plekken zijn bezet, dus de bot koopt niets bij, hoe sterk een trend ook is.

## Vandaag gedaan

- SHELL.AS: stop omhoog van 43.24 naar 43.59
- SAP.DE: stop omhoog van 181.02 naar 184.37

## Verlies en risico

| Ticker | Instap | Koers nu | Resultaat | Stop | Afstand tot stop | Als de stop geraakt wordt |
| --- | --- | --- | --- | --- | --- | --- |
| SHELL.AS | 45.06 EUR | 46.30 | €16,09 (+2,8%) | 43.59 | +6,2% | -€20,08 verlies |
| SAP.DE | 191.56 EUR | 200.50 | €17,89 (+4,7%) | 184.37 | +8,8% | -€15,37 verlies |
| MSFT | 535.34 USD | 533.69 | -€1,79 (-0,3%) | 509.90 | +4,7% | -€24,01 verlies |

Raken alle stops tegelijk, dan is het verlies hooguit ongeveer €59,46 (bij een koersgat 's ochtends kan het meer zijn).

**Remmen** (bij overschrijden gaat de kill switch aan en koopt de bot niets meer):

- Daling vanaf de top: +0,00% (grens -5%; top was €10.029,19)
- Vandaag: +0,15% (grens -1%)
- Verliestrades op rij: 0 van 3

## Kansen: wat de bot vandaag het sterkst vond

_Dit is wat de oefenbot met zijn nepgeld volgens zijn eigen regels zou doen. Geen advies voor echt geld; het instapmoment is een ongeteste vuistregel en wordt door de bot niet gebruikt._

### 1. Shell (SHELL.AS): instapmoment **opgelopen**

- **Waarom sterk:** Shell steeg +22,9% in 3 maanden en +8,4% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,0x het normale volume; beweegt gemiddeld 1,9% per dag.
- **Instapmoment:** de koers staat +6,7% van het 20-daags gemiddelde (3,4x de normale dagbeweging) en RSI is 80; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** al in bezit.
- **Plan van de bot:** koop 13 stuks rond 46.32 EUR (inzet €602,14), stop-loss 44.51 EUR (-3,9%). Maximaal verlies als de stop wordt geraakt: ongeveer €25,45. Ter oriëntatie: 2x het risico winst ligt bij 49.93 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 2. SAP (SAP.DE): instapmoment **neutraal**

- **Waarom sterk:** SAP steeg +45,4% in 3 maanden en +7,2% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,8x het normale volume; beweegt gemiddeld 2,7% per dag.
- **Instapmoment:** de koers staat +6,3% van het 20-daags gemiddelde, RSI 70.
- **Status:** al in bezit.
- **Plan van de bot:** koop 2 stuks rond 200.60 EUR (inzet €401,20), stop-loss 189.85 EUR (-5,4%). Maximaal verlies als de stop wordt geraakt: ongeveer €23,51. Ter oriëntatie: 2x het risico winst ligt bij 222.11 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 3. Wolters Kluwer (WKL.AS): instapmoment **opgelopen**

- **Waarom sterk:** Wolters Kluwer steeg +31,3% in 3 maanden en +16,5% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,2x het normale volume; beweegt gemiddeld 2,7% per dag.
- **Instapmoment:** de koers staat +11,3% van het 20-daags gemiddelde (4,1x de normale dagbeweging) en RSI is 78; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 5 stuks rond 80.02 EUR (inzet €400,10), stop-loss 75.63 EUR (-5,5%). Maximaal verlies als de stop wordt geraakt: ongeveer €23,94. Ter oriëntatie: 2x het risico winst ligt bij 88.80 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 4. Energie-ETF (XLE): instapmoment **neutraal**

- **Waarom sterk:** Energie-ETF steeg +19,3% in 3 maanden en +3,2% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,1x het normale volume; beweegt gemiddeld 1,8% per dag.
- **Instapmoment:** de koers staat +5,2% van het 20-daags gemiddelde, RSI 72.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 11 stuks rond 67.66 USD (inzet €663,77), stop-loss 65.22 USD (-3,6%). Maximaal verlies als de stop wordt geraakt: ongeveer €25,98. Ter oriëntatie: 2x het risico winst ligt bij 72.55 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 5. ExxonMobil (XOM): instapmoment **opgelopen**

- **Waarom sterk:** ExxonMobil steeg +22,1% in 3 maanden en +4,5% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 1,8% per dag.
- **Instapmoment:** de koers staat +6,2% van het 20-daags gemiddelde (3,4x de normale dagbeweging) en RSI is 75; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 4 stuks rond 177.10 USD (inzet €631,75), stop-loss 170.67 USD (-3,6%). Maximaal verlies als de stop wordt geraakt: ongeveer €24,92. Ter oriëntatie: 2x het risico winst ligt bij 189.95 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.


## Wat de bot tot nu toe geleerd heeft

- Nog geen afgesloten trades. Leren begint pas als trades zijn afgesloten: dan weet de bot of een instap goed of slecht uitpakte, en onder welke omstandigheden.

## Klaar voor echt geld?

**Trend-agent:** Nog niet klaar: de bot is nog bezig met bewijzen. Blijven oefenen.

| Eis | Stand | Nu |
| --- | --- | --- |
| Oefentijd | ⏳ | 3 van 63 handelsdagen (ongeveer 3 maanden) |
| Minstens zo goed als de wereld-ETF | ⏳ | verschil tot nu toe +1,72% |
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
| SHELL.AS | 13 | 45.06 EUR | 43.59 | 2026-10-10 |
| SAP.DE | 2 | 191.56 EUR | 184.37 | 2026-10-10 |
| MSFT | 1 | 535.34 USD | 509.90 | 2026-10-10 |

## Sterkste trends vandaag

| # | Ticker | Score | 3 mnd | 1 mnd |
| --- | --- | --- | --- | --- |
| 1 | SHELL.AS | 0.148 | +22.9% | +8.4% |
| 2 | SAP.DE | 0.119 | +45.4% | +7.2% |
| 3 | WKL.AS | 0.116 | +31.3% | +16.5% |
| 4 | XLE | 0.106 | +19.3% | +3.2% |
| 5 | XOM | 0.101 | +22.1% | +4.5% |
| 6 | MSFT | 0.093 | +33.3% | +7.4% |
| 7 | TTE.PA | 0.082 | +15.7% | +1.4% |
| 8 | PLTR | 0.076 | +49.5% | +16.5% |
| 9 | META | 0.053 | +11.1% | +10.1% |
| 10 | V | 0.052 | +7.4% | +4.2% |
