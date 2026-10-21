# Trend-agent rapport 2026-10-20

_Oefenportefeuille met nepgeld. Geen beleggingsadvies; resultaten uit het verleden zeggen niets over de toekomst._

**Status:** OK  
**Waarde:** €10,034.22  
**Kas:** €8,550.41  
**Marktregime:** stijgend-laag  
**Strategieversie:** trend-1.1-d373c7  
**Koersbronnen:** 0 bevestigd door 2 bronnen, 50 uit 1 bron, 0 afwijkend; wisselkoers bevestigd  
**Sinds start:** +0.34%  

## Analyse van vandaag

**Wat de bot zag**

- **Markt (IWDA.AS):** koers 130,47, 8,1% boven het 200-daags gemiddelde (120,75); de afgelopen maand +1,4%. Trend: **stijgend**.
- **Beweeglijkheid:** 8% op jaarbasis, tegen normaal 10% het afgelopen jaar: **laag**.
- **Breedte:** 33 van de 50 instrumenten staan boven hun 200-daags gemiddelde (66%; EU 12 van 23, US 21 van 27).
- **Bekeken:** 50 instrumenten.
- **Afgevallen** (een instrument kan op meer regels afvallen): geen stijgende trend (koers niet boven 50- en 200-daags gemiddelde): 32; niet gestegen over 1 of 3 maanden: 31; te weinig handel: 1.
- **Door de zeef:** 15. Koopbare trends: **15**.

**Wat de bot eruit haalt**

- De markt stijgt breed: goede omstandigheden voor trendvolgen.
- De markt is rustig: stops liggen dichterbij, posities kunnen iets groter.
- Amerika staat er duidelijk beter voor dan Europa (78% tegen 52% in een stijgende trend).
- 3 van de 5 sterkste staan al ver boven hun gemiddelde (SHELL.AS, WKL.AS, V): de trend is sterk, maar instappen op zo'n moment kost vaker een terugval.
- Alle plekken zijn bezet, dus de bot koopt niets bij, hoe sterk een trend ook is.

## Vandaag gedaan

- SAP.DE: stop omhoog van 185.25 naar 185.60

## Verlies en risico

| Ticker | Instap | Koers nu | Resultaat | Stop | Afstand tot stop | Als de stop geraakt wordt |
| --- | --- | --- | --- | --- | --- | --- |
| SHELL.AS | 45.06 EUR | 46.65 | €20,70 (+3,5%) | 44.25 | +5,4% | -€11,51 verlies |
| SAP.DE | 191.56 EUR | 201.80 | €20,49 (+5,3%) | 185.60 | +8,7% | -€12,92 verlies |
| MSFT | 535.34 USD | 532.13 | -€3,98 (-0,6%) | 509.90 | +4,4% | -€24,77 verlies |

Raken alle stops tegelijk, dan is het verlies hooguit ongeveer €49,20 (bij een koersgat 's ochtends kan het meer zijn).

**Remmen** (bij overschrijden gaat de kill switch aan en koopt de bot niets meer):

- Daling vanaf de top: -0,05% (grens -5%; top was €10.038,89)
- Vandaag: -0,01% (grens -1%)
- Verliestrades op rij: 0 van 3

## Kansen: wat de bot vandaag het sterkst vond

_Dit is wat de oefenbot met zijn nepgeld volgens zijn eigen regels zou doen. Geen advies voor echt geld; het instapmoment is een ongeteste vuistregel en wordt door de bot niet gebruikt._

### 1. SAP (SAP.DE): instapmoment **neutraal**

- **Waarom sterk:** SAP steeg +57,3% in 3 maanden en +10,4% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,8x het normale volume; beweegt gemiddeld 2,7% per dag.
- **Instapmoment:** de koers staat +4,9% van het 20-daags gemiddelde, RSI 69.
- **Status:** al in bezit.
- **Plan van de bot:** koop 2 stuks rond 201.90 EUR (inzet €403,80), stop-loss 191.10 EUR (-5,3%). Maximaal verlies als de stop wordt geraakt: ongeveer €23,60. Ter oriëntatie: 2x het risico winst ligt bij 223.50 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 2. Shell (SHELL.AS): instapmoment **opgelopen**

- **Waarom sterk:** Shell steeg +20,2% in 3 maanden en +14,4% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 2,0% per dag.
- **Instapmoment:** de koers staat +4,8% van het 20-daags gemiddelde (2,4x de normale dagbeweging) en RSI is 78; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** al in bezit.
- **Plan van de bot:** koop 13 stuks rond 46.67 EUR (inzet €606,75), stop-loss 44.82 EUR (-4,0%). Maximaal verlies als de stop wordt geraakt: ongeveer €26,06. Ter oriëntatie: 2x het risico winst ligt bij 50.37 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 3. Wolters Kluwer (WKL.AS): instapmoment **opgelopen**

- **Waarom sterk:** Wolters Kluwer steeg +42,5% in 3 maanden en +24,8% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 3,0% per dag.
- **Instapmoment:** de koers staat +11,4% van het 20-daags gemiddelde (3,9x de normale dagbeweging) en RSI is 80; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 5 stuks rond 84.00 EUR (inzet €420,01), stop-loss 79.05 EUR (-5,9%). Maximaal verlies als de stop wordt geraakt: ongeveer €26,76. Ter oriëntatie: 2x het risico winst ligt bij 93.90 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 4. Visa (V): instapmoment **opgelopen**

- **Waarom sterk:** Visa steeg +15,4% in 3 maanden en +10,0% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 1,8% per dag.
- **Instapmoment:** de koers staat +5,8% van het 20-daags gemiddelde (3,2x de normale dagbeweging) en RSI is 76; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 1 stuk rond 407.27 USD (inzet €362,60), stop-loss 392.73 USD (-3,6%). Maximaal verlies als de stop wordt geraakt: ongeveer €14,95. Ter oriëntatie: 2x het risico winst ligt bij 436.36 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 5. Energie-ETF (XLE): instapmoment **neutraal**

- **Waarom sterk:** Energie-ETF steeg +15,5% in 3 maanden en +8,8% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,1x het normale volume; beweegt gemiddeld 2,0% per dag.
- **Instapmoment:** de koers staat +3,9% van het 20-daags gemiddelde, RSI 67.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 10 stuks rond 67.99 USD (inzet €605,31), stop-loss 65.22 USD (-4,1%). Maximaal verlies als de stop wordt geraakt: ongeveer €26,62. Ter oriëntatie: 2x het risico winst ligt bij 73.52 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.


## Wat de bot tot nu toe geleerd heeft

- Nog geen afgesloten trades. Leren begint pas als trades zijn afgesloten: dan weet de bot of een instap goed of slecht uitpakte, en onder welke omstandigheden.

## Klaar voor echt geld?

**Trend-agent:** Nog niet klaar: de bot is nog bezig met bewijzen. Blijven oefenen.

| Eis | Stand | Nu |
| --- | --- | --- |
| Oefentijd | ⏳ | 7 van 63 handelsdagen (ongeveer 3 maanden) |
| Minstens zo goed als de wereld-ETF | ⏳ | verschil tot nu toe +1,55% |
| Grootste daling onder 5% | ✅ | grootste daling tot nu toe -0,10% |
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
| SHELL.AS | 13 | 45.06 EUR | 44.25 | 2026-10-10 |
| SAP.DE | 2 | 191.56 EUR | 185.60 | 2026-10-10 |
| MSFT | 1 | 535.34 USD | 509.90 | 2026-10-10 |

## Sterkste trends vandaag

| # | Ticker | Score | 3 mnd | 1 mnd |
| --- | --- | --- | --- | --- |
| 1 | SAP.DE | 0.157 | +57.3% | +10.4% |
| 2 | SHELL.AS | 0.155 | +20.2% | +14.4% |
| 3 | WKL.AS | 0.139 | +42.5% | +24.8% |
| 4 | V | 0.114 | +15.4% | +10.0% |
| 5 | XLE | 0.105 | +15.5% | +8.8% |
| 6 | MSFT | 0.100 | +36.6% | +6.1% |
| 7 | XOM | 0.097 | +15.9% | +12.4% |
| 8 | CRM | 0.081 | +49.0% | +2.6% |
| 9 | PLTR | 0.072 | +54.6% | +5.2% |
| 10 | OR.PA | 0.062 | +9.6% | +5.3% |
