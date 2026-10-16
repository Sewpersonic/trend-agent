# Trend-agent rapport 2026-10-15

_Oefenportefeuille met nepgeld. Geen beleggingsadvies; resultaten uit het verleden zeggen niets over de toekomst._

**Status:** OK  
**Waarde:** €10,038.89  
**Kas:** €8,550.41  
**Marktregime:** stijgend-laag  
**Strategieversie:** trend-1.1-d373c7  
**Koersbronnen:** 0 bevestigd door 2 bronnen, 50 uit 1 bron, 0 afwijkend; wisselkoers bevestigd  
**Sinds start:** +0.39%  

## Analyse van vandaag

**Wat de bot zag**

- **Markt (IWDA.AS):** koers 130,82, 8,6% boven het 200-daags gemiddelde (120,48); de afgelopen maand +3,4%. Trend: **stijgend**.
- **Beweeglijkheid:** 9% op jaarbasis, tegen normaal 10% het afgelopen jaar: **laag**.
- **Breedte:** 34 van de 50 instrumenten staan boven hun 200-daags gemiddelde (68%; EU 12 van 23, US 22 van 27).
- **Bekeken:** 50 instrumenten.
- **Afgevallen** (een instrument kan op meer regels afvallen): geen stijgende trend (koers niet boven 50- en 200-daags gemiddelde): 29; niet gestegen over 1 of 3 maanden: 23; te weinig handel: 1.
- **Door de zeef:** 18. Koopbare trends: **18**.

**Wat de bot eruit haalt**

- De markt stijgt breed: goede omstandigheden voor trendvolgen.
- De markt is rustig: stops liggen dichterbij, posities kunnen iets groter.
- Amerika staat er duidelijk beter voor dan Europa (81% tegen 52% in een stijgende trend).
- Alle plekken zijn bezet, dus de bot koopt niets bij, hoe sterk een trend ook is.

## Vandaag gedaan

- SHELL.AS: stop omhoog van 43.70 naar 43.77
- SAP.DE: stop omhoog van 181.20 naar 184.62

## Verlies en risico

| Ticker | Instap | Koers nu | Resultaat | Stop | Afstand tot stop | Als de stop geraakt wordt |
| --- | --- | --- | --- | --- | --- | --- |
| SHELL.AS | 45.06 EUR | 46.47 | €18,36 (+3,1%) | 43.77 | +6,2% | -€17,72 verlies |
| SAP.DE | 191.56 EUR | 201.70 | €20,29 (+5,3%) | 184.62 | +9,2% | -€14,87 verlies |
| MSFT | 535.34 USD | 539.33 | €3,24 (+0,8%) | 509.90 | +5,8% | -€24,01 verlies |

Raken alle stops tegelijk, dan is het verlies hooguit ongeveer €56,60 (bij een koersgat 's ochtends kan het meer zijn).

**Remmen** (bij overschrijden gaat de kill switch aan en koopt de bot niets meer):

- Daling vanaf de top: +0,00% (grens -5%; top was €10.038,89)
- Vandaag: +0,15% (grens -1%)
- Verliestrades op rij: 0 van 3

## Kansen: wat de bot vandaag het sterkst vond

_Dit is wat de oefenbot met zijn nepgeld volgens zijn eigen regels zou doen. Geen advies voor echt geld; het instapmoment is een ongeteste vuistregel en wordt door de bot niet gebruikt._

### 1. Shell (SHELL.AS): instapmoment **opgelopen**

- **Waarom sterk:** Shell steeg +23,8% in 3 maanden en +11,1% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,0x het normale volume; beweegt gemiddeld 1,9% per dag.
- **Instapmoment:** de koers staat +6,3% van het 20-daags gemiddelde (3,3x de normale dagbeweging) en RSI is 81; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** al in bezit.
- **Plan van de bot:** koop 13 stuks rond 46.49 EUR (inzet €604,41), stop-loss 44.69 EUR (-3,9%). Maximaal verlies als de stop wordt geraakt: ongeveer €25,39. Ter oriëntatie: 2x het risico winst ligt bij 50.09 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 2. Wolters Kluwer (WKL.AS): instapmoment **opgelopen**

- **Waarom sterk:** Wolters Kluwer steeg +34,1% in 3 maanden en +17,9% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,2x het normale volume; beweegt gemiddeld 2,9% per dag.
- **Instapmoment:** de koers staat +11,8% van het 20-daags gemiddelde (4,0x de normale dagbeweging) en RSI is 77; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 5 stuks rond 81.20 EUR (inzet €406,00), stop-loss 76.44 EUR (-5,9%). Maximaal verlies als de stop wordt geraakt: ongeveer €25,80. Ter oriëntatie: 2x het risico winst ligt bij 90.72 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 3. SAP (SAP.DE): instapmoment **neutraal**

- **Waarom sterk:** SAP steeg +45,9% in 3 maanden en +8,1% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,8x het normale volume; beweegt gemiddeld 2,8% per dag.
- **Instapmoment:** de koers staat +6,4% van het 20-daags gemiddelde, RSI 70.
- **Status:** al in bezit.
- **Plan van de bot:** koop 2 stuks rond 201.80 EUR (inzet €403,60), stop-loss 190.42 EUR (-5,6%). Maximaal verlies als de stop wordt geraakt: ongeveer €24,77. Ter oriëntatie: 2x het risico winst ligt bij 224.57 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 4. Microsoft (MSFT): instapmoment **neutraal**

- **Waarom sterk:** Microsoft steeg +37,2% in 3 maanden en +10,0% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 2,1% per dag.
- **Instapmoment:** de koers staat +3,4% van het 20-daags gemiddelde, RSI 65.
- **Status:** al in bezit.
- **Plan van de bot:** koop 1 stuk rond 539.60 USD (inzet €481,22), stop-loss 516.89 USD (-4,2%). Maximaal verlies als de stop wordt geraakt: ongeveer €22,25. Ter oriëntatie: 2x het risico winst ligt bij 585.01 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 5. ExxonMobil (XOM): instapmoment **neutraal**

- **Waarom sterk:** ExxonMobil steeg +19,3% in 3 maanden en +6,9% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,0x het normale volume; beweegt gemiddeld 1,9% per dag.
- **Instapmoment:** de koers staat +4,3% van het 20-daags gemiddelde, RSI 68.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 4 stuks rond 174.74 USD (inzet €623,32), stop-loss 167.92 USD (-3,9%). Maximaal verlies als de stop wordt geraakt: ongeveer €26,31. Ter oriëntatie: 2x het risico winst ligt bij 188.37 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.


## Wat de bot tot nu toe geleerd heeft

- Nog geen afgesloten trades. Leren begint pas als trades zijn afgesloten: dan weet de bot of een instap goed of slecht uitpakte, en onder welke omstandigheden.

## Klaar voor echt geld?

**Trend-agent:** Nog niet klaar: de bot is nog bezig met bewijzen. Blijven oefenen.

| Eis | Stand | Nu |
| --- | --- | --- |
| Oefentijd | ⏳ | 4 van 63 handelsdagen (ongeveer 3 maanden) |
| Minstens zo goed als de wereld-ETF | ⏳ | verschil tot nu toe +1,33% |
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
| SHELL.AS | 13 | 45.06 EUR | 43.77 | 2026-10-10 |
| SAP.DE | 2 | 191.56 EUR | 184.62 | 2026-10-10 |
| MSFT | 1 | 535.34 USD | 509.90 | 2026-10-10 |

## Sterkste trends vandaag

| # | Ticker | Score | 3 mnd | 1 mnd |
| --- | --- | --- | --- | --- |
| 1 | SHELL.AS | 0.164 | +23.8% | +11.1% |
| 2 | WKL.AS | 0.124 | +34.1% | +17.9% |
| 3 | SAP.DE | 0.121 | +45.9% | +8.1% |
| 4 | MSFT | 0.107 | +37.2% | +10.0% |
| 5 | XOM | 0.095 | +19.3% | +6.9% |
| 6 | XLE | 0.094 | +16.1% | +4.6% |
| 7 | V | 0.087 | +11.7% | +7.7% |
| 8 | TTE.PA | 0.079 | +14.3% | +1.6% |
| 9 | QQQ | 0.078 | +4.8% | +3.4% |
| 10 | PLTR | 0.077 | +51.5% | +15.0% |
