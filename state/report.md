# Trend-agent rapport 2026-10-21

_Oefenportefeuille met nepgeld. Geen beleggingsadvies; resultaten uit het verleden zeggen niets over de toekomst._

**Status:** OK  
**Waarde:** €10,050.37  
**Kas:** €8,550.41  
**Marktregime:** stijgend-laag  
**Strategieversie:** trend-1.1-d373c7  
**Koersbronnen:** 0 bevestigd door 2 bronnen, 50 uit 1 bron, 0 afwijkend; wisselkoers bevestigd  
**Sinds start:** +0.50%  

## Analyse van vandaag

**Wat de bot zag**

- **Markt (IWDA.AS):** koers 131,17, 8,6% boven het 200-daags gemiddelde (120,83); de afgelopen maand +1,4%. Trend: **stijgend**.
- **Beweeglijkheid:** 8% op jaarbasis, tegen normaal 10% het afgelopen jaar: **laag**.
- **Breedte:** 33 van de 50 instrumenten staan boven hun 200-daags gemiddelde (66%; EU 12 van 23, US 21 van 27).
- **Bekeken:** 50 instrumenten.
- **Afgevallen** (een instrument kan op meer regels afvallen): geen stijgende trend (koers niet boven 50- en 200-daags gemiddelde): 28; niet gestegen over 1 of 3 maanden: 30; te weinig handel: 1.
- **Door de zeef:** 16. Koopbare trends: **16**.

**Wat de bot eruit haalt**

- De markt stijgt breed: goede omstandigheden voor trendvolgen.
- De markt is rustig: stops liggen dichterbij, posities kunnen iets groter.
- Amerika staat er duidelijk beter voor dan Europa (78% tegen 52% in een stijgende trend).
- 3 van de 5 sterkste staan al ver boven hun gemiddelde (SHELL.AS, WKL.AS, V): de trend is sterk, maar instappen op zo'n moment kost vaker een terugval.
- Sterk zonder ver weggelopen te zijn: MSFT.
- Alle plekken zijn bezet, dus de bot koopt niets bij, hoe sterk een trend ook is.

## Vandaag gedaan

- SAP.DE: stop omhoog van 185.60 naar 192.41
- MSFT: stop omhoog van 509.90 naar 510.08

## Verlies en risico

| Ticker | Instap | Koers nu | Resultaat | Stop | Afstand tot stop | Als de stop geraakt wordt |
| --- | --- | --- | --- | --- | --- | --- |
| SHELL.AS | 45.06 EUR | 46.82 | €22,91 (+3,9%) | 44.25 | +5,8% | -€11,51 verlies |
| SAP.DE | 191.56 EUR | 208.55 | €33,99 (+8,9%) | 192.41 | +8,4% | €0,70 winst vastgezet |
| MSFT | 535.34 USD | 532.81 | -€3,53 (-0,5%) | 510.08 | +4,5% | -€24,76 verlies |

Raken alle stops tegelijk, dan is het verlies hooguit ongeveer €36,27 (bij een koersgat 's ochtends kan het meer zijn).

**Remmen** (bij overschrijden gaat de kill switch aan en koopt de bot niets meer):

- Daling vanaf de top: +0,00% (grens -5%; top was €10.050,37)
- Vandaag: +0,16% (grens -1%)
- Verliestrades op rij: 0 van 3

## Kansen: wat de bot vandaag het sterkst vond

_Dit is wat de oefenbot met zijn nepgeld volgens zijn eigen regels zou doen. Geen advies voor echt geld; het instapmoment is een ongeteste vuistregel en wordt door de bot niet gebruikt._

### 1. Shell (SHELL.AS): instapmoment **opgelopen**

- **Waarom sterk:** Shell steeg +22,0% in 3 maanden en +14,2% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 1,9% per dag.
- **Instapmoment:** de koers staat +4,7% van het 20-daags gemiddelde (2,5x de normale dagbeweging) en RSI is 78; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** al in bezit.
- **Plan van de bot:** koop 14 stuks rond 46.84 EUR (inzet €655,81), stop-loss 45.08 EUR (-3,8%). Maximaal verlies als de stop wordt geraakt: ongeveer €26,65. Ter oriëntatie: 2x het risico winst ligt bij 50.36 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 2. SAP (SAP.DE): instapmoment **neutraal**

- **Waarom sterk:** SAP steeg +48,8% in 3 maanden en +14,4% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,8x het normale volume; beweegt gemiddeld 2,6% per dag.
- **Instapmoment:** de koers staat +7,6% van het 20-daags gemiddelde, RSI 74.
- **Status:** al in bezit.
- **Plan van de bot:** koop 2 stuks rond 208.65 EUR (inzet €417,31), stop-loss 197.89 EUR (-5,2%). Maximaal verlies als de stop wordt geraakt: ongeveer €23,53. Ter oriëntatie: 2x het risico winst ligt bij 230.18 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 3. Wolters Kluwer (WKL.AS): instapmoment **opgelopen**

- **Waarom sterk:** Wolters Kluwer steeg +38,1% in 3 maanden en +27,2% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 2,8% per dag.
- **Instapmoment:** de koers staat +11,5% van het 20-daags gemiddelde (4,2x de normale dagbeweging) en RSI is 80; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 5 stuks rond 85.04 EUR (inzet €425,21), stop-loss 80.35 EUR (-5,5%). Maximaal verlies als de stop wordt geraakt: ongeveer €25,49. Ter oriëntatie: 2x het risico winst ligt bij 94.44 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 4. Visa (V): instapmoment **opgelopen**

- **Waarom sterk:** Visa steeg +16,3% in 3 maanden en +12,7% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 1,8% per dag.
- **Instapmoment:** de koers staat +5,4% van het 20-daags gemiddelde (3,0x de normale dagbeweging) en RSI is 76; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 1 stuk rond 408.22 USD (inzet €363,32), stop-loss 393.74 USD (-3,5%). Maximaal verlies als de stop wordt geraakt: ongeveer €14,89. Ter oriëntatie: 2x het risico winst ligt bij 437.20 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 5. Microsoft (MSFT): instapmoment **gunstig**

- **Waarom sterk:** Microsoft steeg +39,9% in 3 maanden en +7,0% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD negatief (de stijging vertraagt); handel 0,8x het normale volume; beweegt gemiddeld 2,1% per dag.
- **Instapmoment:** de trend is sterk maar de koers is niet ver weggelopen (+1,4% van het 20-daags gemiddelde, RSI 59).
- **Status:** al in bezit.
- **Plan van de bot:** koop 1 stuk rond 533.08 USD (inzet €474,44), stop-loss 510.83 USD (-4,2%). Maximaal verlies als de stop wordt geraakt: ongeveer €21,80. Ter oriëntatie: 2x het risico winst ligt bij 577.57 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.


## Wat de bot tot nu toe geleerd heeft

- Nog geen afgesloten trades. Leren begint pas als trades zijn afgesloten: dan weet de bot of een instap goed of slecht uitpakte, en onder welke omstandigheden.

## Klaar voor echt geld?

**Trend-agent:** Nog niet klaar: de bot is nog bezig met bewijzen. Blijven oefenen.

| Eis | Stand | Nu |
| --- | --- | --- |
| Oefentijd | ⏳ | 8 van 63 handelsdagen (ongeveer 3 maanden) |
| Minstens zo goed als de wereld-ETF | ⏳ | verschil tot nu toe +1,18% |
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
| SAP.DE | 2 | 191.56 EUR | 192.41 | 2026-10-10 |
| MSFT | 1 | 535.34 USD | 510.08 | 2026-10-10 |

## Sterkste trends vandaag

| # | Ticker | Score | 3 mnd | 1 mnd |
| --- | --- | --- | --- | --- |
| 1 | SHELL.AS | 0.165 | +22.0% | +14.2% |
| 2 | SAP.DE | 0.157 | +48.8% | +14.4% |
| 3 | WKL.AS | 0.134 | +38.1% | +27.2% |
| 4 | V | 0.128 | +16.3% | +12.7% |
| 5 | MSFT | 0.110 | +39.9% | +7.0% |
| 6 | XLE | 0.106 | +15.5% | +10.3% |
| 7 | CRM | 0.092 | +54.3% | +3.6% |
| 8 | XOM | 0.090 | +14.2% | +12.2% |
| 9 | PLTR | 0.086 | +63.4% | +9.0% |
| 10 | OR.PA | 0.053 | +8.4% | +4.3% |
