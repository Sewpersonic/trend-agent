# Trend-agent rapport 2026-10-22

_Oefenportefeuille met nepgeld. Geen beleggingsadvies; resultaten uit het verleden zeggen niets over de toekomst._

**Status:** OK  
**Waarde:** €10,053.90  
**Kas:** €8,550.41  
**Marktregime:** stijgend-laag  
**Strategieversie:** trend-1.1-d373c7  
**Koersbronnen:** 0 bevestigd door 2 bronnen, 50 uit 1 bron, 0 afwijkend; wisselkoers bevestigd  
**Sinds start:** +0.54%  

## Analyse van vandaag

**Wat de bot zag**

- **Markt (IWDA.AS):** koers 129,93, 7,5% boven het 200-daags gemiddelde (120,91); de afgelopen maand +0,6%. Trend: **stijgend**.
- **Beweeglijkheid:** 8% op jaarbasis, tegen normaal 10% het afgelopen jaar: **laag**.
- **Breedte:** 32 van de 50 instrumenten staan boven hun 200-daags gemiddelde (64%; EU 11 van 23, US 21 van 27).
- **Bekeken:** 50 instrumenten.
- **Afgevallen** (een instrument kan op meer regels afvallen): geen stijgende trend (koers niet boven 50- en 200-daags gemiddelde): 34; niet gestegen over 1 of 3 maanden: 31; te weinig handel: 1.
- **Door de zeef:** 14. Koopbare trends: **14**.

**Wat de bot eruit haalt**

- De markt stijgt breed: goede omstandigheden voor trendvolgen.
- De markt is rustig: stops liggen dichterbij, posities kunnen iets groter.
- Amerika staat er duidelijk beter voor dan Europa (78% tegen 48% in een stijgende trend).
- 3 van de 5 sterkste staan al ver boven hun gemiddelde (SAP.DE, V, WKL.AS): de trend is sterk, maar instappen op zo'n moment kost vaker een terugval.
- Sterk zonder ver weggelopen te zijn: MSFT.
- Alle plekken zijn bezet, dus de bot koopt niets bij, hoe sterk een trend ook is.

## Vandaag gedaan

- SAP.DE: stop omhoog van 192.41 naar 198.88

## Verlies en risico

| Ticker | Instap | Koers nu | Resultaat | Stop | Afstand tot stop | Als de stop geraakt wordt |
| --- | --- | --- | --- | --- | --- | --- |
| SHELL.AS | 45.06 EUR | 46.62 | €20,38 (+3,5%) | 44.25 | +5,4% | -€11,51 verlies |
| SAP.DE | 191.56 EUR | 216.45 | €49,79 (+13,0%) | 198.88 | +8,8% | €13,66 winst vastgezet |
| MSFT | 535.34 USD | 521.58 | -€13,27 (-2,6%) | 510.08 | +2,2% | -€24,51 verlies |

Raken alle stops tegelijk, dan is het verlies hooguit ongeveer €36,02 (bij een koersgat 's ochtends kan het meer zijn).

**Remmen** (bij overschrijden gaat de kill switch aan en koopt de bot niets meer):

- Daling vanaf de top: +0,00% (grens -5%; top was €10.053,90)
- Vandaag: +0,04% (grens -1%)
- Verliestrades op rij: 0 van 3

## Kansen: wat de bot vandaag het sterkst vond

_Dit is wat de oefenbot met zijn nepgeld volgens zijn eigen regels zou doen. Geen advies voor echt geld; het instapmoment is een ongeteste vuistregel en wordt door de bot niet gebruikt._

### 1. Shell (SHELL.AS): instapmoment **neutraal**

- **Waarom sterk:** Shell steeg +22,9% in 3 maanden en +11,8% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,0x het normale volume; beweegt gemiddeld 1,9% per dag.
- **Instapmoment:** de koers staat +3,9% van het 20-daags gemiddelde, RSI 75.
- **Status:** al in bezit.
- **Plan van de bot:** koop 13 stuks rond 46.65 EUR (inzet €606,43), stop-loss 44.85 EUR (-3,9%). Maximaal verlies als de stop wordt geraakt: ongeveer €25,35. Ter oriëntatie: 2x het risico winst ligt bij 50.24 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 2. SAP (SAP.DE): instapmoment **opgelopen**

- **Waarom sterk:** SAP steeg +43,1% in 3 maanden en +16,1% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,8x het normale volume; beweegt gemiddeld 2,7% per dag.
- **Instapmoment:** de koers staat +10,4% van het 20-daags gemiddelde (3,8x de normale dagbeweging) en RSI is 79; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** al in bezit.
- **Plan van de bot:** koop 2 stuks rond 216.56 EUR (inzet €433,12), stop-loss 204.85 EUR (-5,4%). Maximaal verlies als de stop wordt geraakt: ongeveer €25,42. Ter oriëntatie: 2x het risico winst ligt bij 239.98 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 3. Visa (V): instapmoment **opgelopen**

- **Waarom sterk:** Visa steeg +16,7% in 3 maanden en +14,6% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,0x het normale volume; beweegt gemiddeld 1,8% per dag.
- **Instapmoment:** de koers staat +6,3% van het 20-daags gemiddelde (3,5x de normale dagbeweging) en RSI is 79; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 1 stuk rond 414.52 USD (inzet €369,13), stop-loss 399.64 USD (-3,6%). Maximaal verlies als de stop wordt geraakt: ongeveer €15,24. Ter oriëntatie: 2x het risico winst ligt bij 444.26 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 4. Wolters Kluwer (WKL.AS): instapmoment **opgelopen**

- **Waarom sterk:** Wolters Kluwer steeg +30,7% in 3 maanden en +28,6% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 2,7% per dag.
- **Instapmoment:** de koers staat +12,3% van het 20-daags gemiddelde (4,6x de normale dagbeweging) en RSI is 82; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: alle 3 plekken zijn bezet.
- **Plan van de bot:** koop 5 stuks rond 86.84 EUR (inzet €434,22), stop-loss 82.15 EUR (-5,4%). Maximaal verlies als de stop wordt geraakt: ongeveer €25,44. Ter oriëntatie: 2x het risico winst ligt bij 96.22 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 5. Microsoft (MSFT): instapmoment **gunstig**

- **Waarom sterk:** Microsoft steeg +36,9% in 3 maanden en +4,2% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD negatief (de stijging vertraagt); handel 0,8x het normale volume; beweegt gemiddeld 2,2% per dag.
- **Instapmoment:** de trend is sterk maar de koers is niet ver weggelopen (-0,6% van het 20-daags gemiddelde, RSI 51).
- **Status:** al in bezit.
- **Plan van de bot:** koop 1 stuk rond 521.84 USD (inzet €464,70), stop-loss 499.08 USD (-4,4%). Maximaal verlies als de stop wordt geraakt: ongeveer €22,27. Ter oriëntatie: 2x het risico winst ligt bij 567.36 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.


## Wat de bot tot nu toe geleerd heeft

- Nog geen afgesloten trades. Leren begint pas als trades zijn afgesloten: dan weet de bot of een instap goed of slecht uitpakte, en onder welke omstandigheden.

## Klaar voor echt geld?

**Trend-agent:** Nog niet klaar: de bot is nog bezig met bewijzen. Blijven oefenen.

| Eis | Stand | Nu |
| --- | --- | --- |
| Oefentijd | ⏳ | 9 van 63 handelsdagen (ongeveer 3 maanden) |
| Minstens zo goed als de wereld-ETF | ⏳ | verschil tot nu toe +2,16% |
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
| SAP.DE | 2 | 191.56 EUR | 198.88 | 2026-10-10 |
| MSFT | 1 | 535.34 USD | 510.08 | 2026-10-10 |

## Sterkste trends vandaag

| # | Ticker | Score | 3 mnd | 1 mnd |
| --- | --- | --- | --- | --- |
| 1 | SHELL.AS | 0.163 | +22.9% | +11.8% |
| 2 | SAP.DE | 0.157 | +43.1% | +16.1% |
| 3 | V | 0.136 | +16.7% | +14.6% |
| 4 | WKL.AS | 0.128 | +30.7% | +28.6% |
| 5 | MSFT | 0.097 | +36.9% | +4.2% |
| 6 | XLE | 0.092 | +14.0% | +8.4% |
| 7 | CRM | 0.092 | +53.2% | +5.3% |
| 8 | XOM | 0.086 | +14.3% | +10.5% |
| 9 | PLTR | 0.076 | +59.7% | +2.3% |
| 10 | OR.PA | 0.074 | +10.0% | +8.6% |
