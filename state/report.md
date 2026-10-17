# Trend-agent rapport 2026-10-16

_Oefenportefeuille met nepgeld. Geen beleggingsadvies; resultaten uit het verleden zeggen niets over de toekomst._

**Status:** OK  
**Waarde:** €10,028.47  
**Kas:** €8,550.41  
**Marktregime:** stijgend-laag  
**Strategieversie:** trend-1.1-d373c7  
**Koersbronnen:** 0 bevestigd door 2 bronnen, 50 uit 1 bron, 0 afwijkend; wisselkoers bevestigd  
**Sinds start:** +0.28%  

## Analyse van vandaag

**Wat de bot zag**

- **Markt (IWDA.AS):** koers 130,45, 8,2% boven het 200-daags gemiddelde (120,57); de afgelopen maand +2,4%. Trend: **stijgend**.
- **Beweeglijkheid:** 9% op jaarbasis, tegen normaal 10% het afgelopen jaar: **laag**.
- **Breedte:** 34 van de 50 instrumenten staan boven hun 200-daags gemiddelde (68%; EU 12 van 23, US 22 van 27).
- **Bekeken:** 50 instrumenten.
- **Afgevallen** (een instrument kan op meer regels afvallen): geen stijgende trend (koers niet boven 50- en 200-daags gemiddelde): 33; niet gestegen over 1 of 3 maanden: 30; te weinig handel: 1.
- **Door de zeef:** 14. Koopbare trends: **14**.

**Wat de bot eruit haalt**

- De markt stijgt breed: goede omstandigheden voor trendvolgen.
- De markt is rustig: stops liggen dichterbij, posities kunnen iets groter.
- Amerika staat er duidelijk beter voor dan Europa (81% tegen 52% in een stijgende trend).
- 3 van de 5 sterkste staan al ver boven hun gemiddelde (SHELL.AS, WKL.AS, XOM): de trend is sterk, maar instappen op zo'n moment kost vaker een terugval.
- Alle plekken zijn bezet, dus de bot koopt niets bij, hoe sterk een trend ook is.

## Vandaag gedaan

- SHELL.AS: stop omhoog van 43.77 naar 44.19
- SAP.DE: stop omhoog van 184.62 naar 185.13

## Verlies en risico

| Ticker | Instap | Koers nu | Resultaat | Stop | Afstand tot stop | Als de stop geraakt wordt |
| --- | --- | --- | --- | --- | --- | --- |
| SHELL.AS | 45.06 EUR | 46.89 | €23,82 (+4,1%) | 44.19 | +6,1% | -€12,31 verlies |
| SAP.DE | 191.56 EUR | 199.02 | €14,93 (+3,9%) | 185.13 | +7,5% | -€13,86 verlies |
| MSFT | 535.34 USD | 528.95 | -€7,29 (-1,2%) | 509.90 | +3,7% | -€25,23 verlies |

Raken alle stops tegelijk, dan is het verlies hooguit ongeveer €51,40 (bij een koersgat 's ochtends kan het meer zijn).

**Remmen** (bij overschrijden gaat de kill switch aan en koopt de bot niets meer):

- Daling vanaf de top: -0,10% (grens -5%; top was €10.038,89)
- Vandaag: -0,10% (grens -1%)
- Verliestrades op rij: 0 van 3

## Kansen: wat de bot vandaag het sterkst vond

_Dit is wat de oefenbot met zijn nepgeld volgens zijn eigen regels zou doen. Geen advies voor echt geld; het instapmoment is een ongeteste vuistregel en wordt door de bot niet gebruikt._

### 1. Shell (SHELL.AS): instapmoment **opgelopen**

- **Waarom sterk:** Shell steeg +24,0% in 3 maanden en +12,8% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 1,9% per dag.
- **Instapmoment:** de koers staat +6,6% van het 20-daags gemiddelde (3,4x de normale dagbeweging) en RSI is 81; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** al in bezit.
- **Plan van de bot:** koop 13 stuks rond 46.91 EUR (inzet €609,87), stop-loss 45.11 EUR (-3,8%). Maximaal verlies als de stop wordt geraakt: ongeveer €25,42. Ter oriëntatie: 2x het risico winst ligt bij 50.52 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 2. SAP (SAP.DE): instapmoment **neutraal**

- **Waarom sterk:** SAP steeg +45,9% in 3 maanden en +5,9% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,8x het normale volume; beweegt gemiddeld 2,8% per dag.
- **Instapmoment:** de koers staat +4,5% van het 20-daags gemiddelde, RSI 66.
- **Status:** al in bezit.
- **Plan van de bot:** koop 2 stuks rond 199.12 EUR (inzet €398,24), stop-loss 188.07 EUR (-5,5%). Maximaal verlies als de stop wordt geraakt: ongeveer €24,10. Ter oriëntatie: 2x het risico winst ligt bij 221.22 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 3. Wolters Kluwer (WKL.AS): instapmoment **opgelopen**

- **Waarom sterk:** Wolters Kluwer steeg +38,2% in 3 maanden en +16,6% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 2,9% per dag.
- **Instapmoment:** de koers staat +11,2% van het 20-daags gemiddelde (3,9x de normale dagbeweging) en RSI is 78; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 5 stuks rond 81.76 EUR (inzet €408,80), stop-loss 77.10 EUR (-5,7%). Maximaal verlies als de stop wordt geraakt: ongeveer €25,33. Ter oriëntatie: 2x het risico winst ligt bij 91.09 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 4. Energie-ETF (XLE): instapmoment **neutraal**

- **Waarom sterk:** Energie-ETF steeg +18,5% in 3 maanden en +6,4% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,1x het normale volume; beweegt gemiddeld 1,9% per dag.
- **Instapmoment:** de koers staat +5,2% van het 20-daags gemiddelde, RSI 70.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 10 stuks rond 68.26 USD (inzet €607,14), stop-loss 65.60 USD (-3,9%). Maximaal verlies als de stop wordt geraakt: ongeveer €25,72. Ter oriëntatie: 2x het risico winst ligt bij 73.60 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 5. ExxonMobil (XOM): instapmoment **opgelopen**

- **Waarom sterk:** ExxonMobil steeg +21,4% in 3 maanden en +9,6% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 2,0% per dag.
- **Instapmoment:** de koers staat +6,2% van het 20-daags gemiddelde (3,2x de normale dagbeweging) en RSI is 73; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 4 stuks rond 179.07 USD (inzet €637,06), stop-loss 172.04 USD (-3,9%). Maximaal verlies als de stop wordt geraakt: ongeveer €27,03. Ter oriëntatie: 2x het risico winst ligt bij 193.14 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.


## Wat de bot tot nu toe geleerd heeft

- Nog geen afgesloten trades. Leren begint pas als trades zijn afgesloten: dan weet de bot of een instap goed of slecht uitpakte, en onder welke omstandigheden.

## Klaar voor echt geld?

**Trend-agent:** Nog niet klaar: de bot is nog bezig met bewijzen. Blijven oefenen.

| Eis | Stand | Nu |
| --- | --- | --- |
| Oefentijd | ⏳ | 5 van 63 handelsdagen (ongeveer 3 maanden) |
| Minstens zo goed als de wereld-ETF | ⏳ | verschil tot nu toe +1,51% |
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
| SHELL.AS | 13 | 45.06 EUR | 44.19 | 2026-10-10 |
| SAP.DE | 2 | 191.56 EUR | 185.13 | 2026-10-10 |
| MSFT | 1 | 535.34 USD | 509.90 | 2026-10-10 |

## Sterkste trends vandaag

| # | Ticker | Score | 3 mnd | 1 mnd |
| --- | --- | --- | --- | --- |
| 1 | SHELL.AS | 0.168 | +24.0% | +12.8% |
| 2 | SAP.DE | 0.118 | +45.9% | +5.9% |
| 3 | WKL.AS | 0.117 | +38.2% | +16.6% |
| 4 | XLE | 0.112 | +18.5% | +6.4% |
| 5 | XOM | 0.109 | +21.4% | +9.6% |
| 6 | V | 0.090 | +11.9% | +8.8% |
| 7 | MSFT | 0.087 | +31.7% | +6.3% |
| 8 | TTE.PA | 0.060 | +11.8% | +2.2% |
| 9 | OR.PA | 0.054 | +7.3% | +6.9% |
| 10 | PLTR | 0.051 | +38.0% | +5.6% |
