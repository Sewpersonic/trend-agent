# Trend-agent rapport 2026-11-05

_Oefenportefeuille met nepgeld. Geen beleggingsadvies; resultaten uit het verleden zeggen niets over de toekomst._

**Status:** OK  
**Waarde:** €9,961.07  
**Kas:** €3,362.61  
**Marktregime:** stijgend-hoog  
**Strategieversie:** trend-1.1-f132c3  
**Koersbronnen:** 69 bevestigd door 2 bronnen, 60 uit 1 bron, 0 afwijkend; wisselkoers bevestigd  
**Sinds start:** -0.39%  

## Analyse van vandaag

**Wat de bot zag**

- **Markt (IWDA.AS):** koers 127,65, 4,9% boven het 200-daags gemiddelde (121,75); de afgelopen maand -2,9%. Trend: **stijgend**.
- **Beweeglijkheid:** 13% op jaarbasis, tegen normaal 10% het afgelopen jaar: **hoog**.
- **Breedte:** 75 van de 129 instrumenten staan boven hun 200-daags gemiddelde (58%; EU 39 van 60, US 36 van 69).
- **Bekeken:** 129 instrumenten.
- **Afgevallen** (een instrument kan op meer regels afvallen): geen stijgende trend (koers niet boven 50- en 200-daags gemiddelde): 86; niet gestegen over 1 of 3 maanden: 73; te weinig handel: 2; verdachte dagsprong: 1.
- **Door de zeef:** 36. Koopbare trends: **36**.

**Wat de bot eruit haalt**

- De markt stijgt, maar gedragen door een minderheid van de aandelen: kwetsbaarder dan het lijkt.
- De markt beweegt meer dan normaal: stops worden sneller geraakt. Het risico per trade blijft gelijk, dus de posities worden vanzelf kleiner.
- De sterkste trends zijn vooral Europese instrumenten.
- 3 van de 5 sterkste staan al ver boven hun gemiddelde (WKL.AS, MUV2.DE, OR.PA): de trend is sterk, maar instappen op zo'n moment kost vaker een terugval.
- Alle plekken zijn bezet, dus de bot koopt niets bij, hoe sterk een trend ook is.

## Vandaag gedaan

- DB1.DE: stop omhoog van 302.20 naar 306.40
- WKL.AS: stop omhoog van 82.85 naar 84.13

## Verlies en risico

| Ticker | Instap | Koers nu | Resultaat | Stop | Afstand tot stop | Als de stop geraakt wordt |
| --- | --- | --- | --- | --- | --- | --- |
| SAP.DE | 191.56 EUR | 216.75 | €50,39 (+13,2%) | 199.49 | +8,6% | €14,87 winst vastgezet |
| DB1.DE | 314.96 EUR | 327.20 | €12,24 (+3,9%) | 306.40 | +6,8% | -€9,55 verlies |
| ABBV | 290.94 USD | 288.24 | -€5,51 (-0,9%) | 277.38 | +3,9% | -€25,87 verlies |
| WKL.AS | 86.80 EUR | 92.44 | €56,37 (+6,5%) | 84.13 | +9,9% | -€27,73 verlies |
| MA | 647.63 USD | 655.92 | €18,28 (+1,3%) | 631.15 | +3,9% | -€26,90 verlies |
| V | 420.59 USD | 422.59 | €8,76 (+0,5%) | 412.07 | +2,5% | -€20,39 verlies |
| OR.PA | 446.42 EUR | 453.30 | €13,75 (+1,5%) | 428.34 | +5,8% | -€37,16 verlies |
| PG | 167.40 USD | 167.10 | €2,12 (-0,2%) | 160.52 | +4,1% | -€45,79 verlies |

Raken alle stops tegelijk, dan is het verlies hooguit ongeveer €193,39 (bij een koersgat 's ochtends kan het meer zijn).

**Remmen** (bij overschrijden gaat de kill switch aan en koopt de bot niets meer):

- Daling vanaf de top: -0,26% (grens -10%; top was €9.987,03)
- Vandaag: -0,26% (grens -2%)
- Verliestrades op rij: 1 van 3

## Kansen: wat de bot vandaag het sterkst vond

_Dit is wat de oefenbot met zijn nepgeld volgens zijn eigen regels zou doen. Geen advies voor echt geld; het instapmoment is een ongeteste vuistregel en wordt door de bot niet gebruikt._

### 1. Deutsche Börse (DB1.DE): instapmoment **neutraal**

- **Waarom sterk:** Deutsche Börse steeg +18,7% in 3 maanden en +12,0% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,1x het normale volume; beweegt gemiddeld 2,1% per dag.
- **Instapmoment:** de koers staat +5,3% van het 20-daags gemiddelde, RSI 74.
- **Status:** al in bezit.
- **Plan van de bot:** koop 3 stuks rond 327.36 EUR (inzet €982,09), stop-loss 313.50 EUR (-4,2%). Maximaal verlies als de stop wordt geraakt: ongeveer €43,59. Ter oriëntatie: 2x het risico winst ligt bij 355.09 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 2. Wolters Kluwer (WKL.AS): instapmoment **opgelopen**

- **Waarom sterk:** Wolters Kluwer steeg +33,2% in 3 maanden en +30,4% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 3,0% per dag.
- **Instapmoment:** de koers staat +10,2% van het 20-daags gemiddelde (3,4x de normale dagbeweging) en RSI is 74; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** al in bezit.
- **Plan van de bot:** koop 8 stuks rond 92.49 EUR (inzet €739,89), stop-loss 86.95 EUR (-6,0%). Maximaal verlies als de stop wordt geraakt: ongeveer €46,32. Ter oriëntatie: 2x het risico winst ligt bij 103.57 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 3. Munich Re (MUV2.DE): instapmoment **opgelopen**

- **Waarom sterk:** Munich Re steeg +15,2% in 3 maanden en +15,4% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 1,7% per dag.
- **Instapmoment:** de koers staat +7,2% van het 20-daags gemiddelde (4,3x de normale dagbeweging) en RSI is 86; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: RSI 86 boven de grens 75.
- **Plan van de bot:** koop 2 stuks rond 596.30 EUR (inzet €1.192,60), stop-loss 576.33 EUR (-3,4%). Maximaal verlies als de stop wordt geraakt: ongeveer €41,94. Ter oriëntatie: 2x het risico winst ligt bij 636.24 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 4. L'Oreal (OR.PA): instapmoment **opgelopen**

- **Waarom sterk:** L'Oreal steeg +16,7% in 3 maanden en +21,1% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,2x het normale volume; beweegt gemiddeld 2,1% per dag.
- **Instapmoment:** de koers staat +7,7% van het 20-daags gemiddelde (3,7x de normale dagbeweging) en RSI is 76; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** al in bezit.
- **Plan van de bot:** koop 2 stuks rond 453.53 EUR (inzet €907,05), stop-loss 434.39 EUR (-4,2%). Maximaal verlies als de stop wordt geraakt: ongeveer €40,27. Ter oriëntatie: 2x het risico winst ligt bij 491.80 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 5. Mastercard (MA): instapmoment **neutraal**

- **Waarom sterk:** Mastercard steeg +16,7% in 3 maanden en +15,2% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,2x het normale volume; beweegt gemiddeld 2,3% per dag.
- **Instapmoment:** de koers staat +4,9% van het 20-daags gemiddelde, RSI 66.
- **Status:** al in bezit.
- **Plan van de bot:** koop 1 stuk rond 656.25 USD (inzet €585,24), stop-loss 625.85 USD (-4,6%). Maximaal verlies als de stop wordt geraakt: ongeveer €29,11. Ter oriëntatie: 2x het risico winst ligt bij 717.04 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.


## Wat de bot tot nu toe geleerd heeft

- 5 afgesloten trades: 1 met winst (20%), gemiddeld -0,87 R per trade (R = winst of verlies gedeeld door het risico bij instap), totaal -€187,32.
- Pas vanaf 20 trades trekt de bot conclusies over welke omstandigheden goed of slecht uitpakken; met minder is het vooral toeval. Het wekelijkse onderzoek (zaterdag) doet dat.

## Klaar voor echt geld?

**Trend-agent:** Nog niet klaar: de bot is nog bezig met bewijzen. Blijven oefenen.

| Eis | Stand | Nu |
| --- | --- | --- |
| Oefentijd | ⏳ | 19 van 63 handelsdagen (ongeveer 3 maanden) |
| Minstens zo goed als de wereld-ETF | ⏳ | verschil tot nu toe +2,95% |
| Grootste daling onder 5% | ✅ | grootste daling tot nu toe -2,18% |
| Genoeg afgesloten trades | ⏳ | 5 van 20 |

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
| SAP.DE | 2 | 191.56 EUR | 199.49 | 2026-10-10 |
| DB1.DE | 1 | 314.96 EUR | 306.40 | 2026-10-29 |
| ABBV | 2 | 290.94 USD | 277.38 | 2026-10-29 |
| WKL.AS | 10 | 86.80 EUR | 84.13 | 2026-10-30 |
| MA | 2 | 647.63 USD | 631.15 | 2026-11-03 |
| V | 3 | 420.59 USD | 412.07 | 2026-11-03 |
| OR.PA | 2 | 446.42 EUR | 428.34 | 2026-11-04 |
| PG | 8 | 167.40 USD | 160.52 | 2026-11-04 |

## Sterkste trends vandaag

| # | Ticker | Score | 3 mnd | 1 mnd |
| --- | --- | --- | --- | --- |
| 1 | DB1.DE | 0.158 | +18.7% | +12.0% |
| 2 | WKL.AS | 0.150 | +33.2% | +30.4% |
| 3 | MUV2.DE | 0.149 | +15.2% | +15.4% |
| 4 | OR.PA | 0.146 | +16.7% | +21.1% |
| 5 | MA | 0.132 | +16.7% | +15.2% |
| 6 | PG | 0.128 | +15.4% | +13.8% |
| 7 | IBE.MC | 0.123 | +10.7% | +8.8% |
| 8 | HEIA.AS | 0.122 | +9.6% | +19.1% |
| 9 | V | 0.122 | +16.8% | +13.6% |
| 10 | BRK-B | 0.118 | +9.7% | +13.1% |

## Afgesloten trades

5 trades, 1 winst (20%), totaal €-187.32 na kosten.
