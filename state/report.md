# Trend-agent rapport 2026-11-06

_Oefenportefeuille met nepgeld. Geen beleggingsadvies; resultaten uit het verleden zeggen niets over de toekomst._

**Status:** OK  
**Waarde:** €9,891.50  
**Kas:** €3,362.61  
**Marktregime:** stijgend-hoog  
**Strategieversie:** trend-1.1-f132c3  
**Koersbronnen:** 69 bevestigd door 2 bronnen, 60 uit 1 bron, 0 afwijkend; wisselkoers bevestigd  
**Sinds start:** -1.09%  

## Analyse van vandaag

**Wat de bot zag**

- **Markt (IWDA.AS):** koers 127,23, 4,4% boven het 200-daags gemiddelde (121,82); de afgelopen maand -2,9%. Trend: **stijgend**.
- **Beweeglijkheid:** 13% op jaarbasis, tegen normaal 10% het afgelopen jaar: **hoog**.
- **Breedte:** 75 van de 129 instrumenten staan boven hun 200-daags gemiddelde (58%; EU 38 van 60, US 37 van 69).
- **Bekeken:** 129 instrumenten.
- **Afgevallen** (een instrument kan op meer regels afvallen): geen stijgende trend (koers niet boven 50- en 200-daags gemiddelde): 89; niet gestegen over 1 of 3 maanden: 78; te weinig handel: 2; verdachte dagsprong: 1.
- **Door de zeef:** 33. Koopbare trends: **33**.

**Wat de bot eruit haalt**

- De markt stijgt, maar gedragen door een minderheid van de aandelen: kwetsbaarder dan het lijkt.
- De markt beweegt meer dan normaal: stops worden sneller geraakt. Het risico per trade blijft gelijk, dus de posities worden vanzelf kleiner.
- De sterkste trends zijn vooral Europese instrumenten.
- Sterk zonder ver weggelopen te zijn: DB1.DE.
- Alle plekken zijn bezet, dus de bot koopt niets bij, hoe sterk een trend ook is.

## Vandaag gedaan

- Niets

## Verlies en risico

| Ticker | Instap | Koers nu | Resultaat | Stop | Afstand tot stop | Als de stop geraakt wordt |
| --- | --- | --- | --- | --- | --- | --- |
| SAP.DE | 191.56 EUR | 210.40 | €37,69 (+9,8%) | 199.49 | +5,5% | €14,87 winst vastgezet |
| DB1.DE | 314.96 EUR | 320.30 | €5,34 (+1,7%) | 306.40 | +4,5% | -€9,55 verlies |
| ABBV | 290.94 USD | 291.31 | -€0,72 (+0,1%) | 277.38 | +5,0% | -€26,53 verlies |
| WKL.AS | 86.80 EUR | 89.90 | €30,97 (+3,6%) | 84.13 | +6,9% | -€27,73 verlies |
| MA | 647.63 USD | 652.70 | €10,98 (+0,8%) | 631.15 | +3,4% | -€28,40 verlies |
| V | 420.59 USD | 422.65 | €7,41 (+0,5%) | 412.07 | +2,6% | -€21,86 verlies |
| OR.PA | 446.42 EUR | 449.80 | €6,75 (+0,8%) | 428.34 | +5,0% | -€37,16 verlies |
| PG | 167.40 USD | 165.40 | -€11,58 (-1,2%) | 160.52 | +3,0% | -€47,32 verlies |

Raken alle stops tegelijk, dan is het verlies hooguit ongeveer €198,55 (bij een koersgat 's ochtends kan het meer zijn).

**Remmen** (bij overschrijden gaat de kill switch aan en koopt de bot niets meer):

- Daling vanaf de top: -0,96% (grens -10%; top was €9.987,03)
- Vandaag: -0,70% (grens -2%)
- Verliestrades op rij: 1 van 3

## Kansen: wat de bot vandaag het sterkst vond

_Dit is wat de oefenbot met zijn nepgeld volgens zijn eigen regels zou doen. Geen advies voor echt geld; het instapmoment is een ongeteste vuistregel en wordt door de bot niet gebruikt._

### 1. L'Oreal (OR.PA): instapmoment **neutraal**

- **Waarom sterk:** L'Oreal steeg +17,2% in 3 maanden en +20,3% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,2x het normale volume; beweegt gemiddeld 2,2% per dag.
- **Instapmoment:** de koers staat +6,1% van het 20-daags gemiddelde, RSI 72.
- **Status:** al in bezit.
- **Plan van de bot:** koop 2 stuks rond 450.02 EUR (inzet €900,05), stop-loss 430.22 EUR (-4,4%). Maximaal verlies als de stop wordt geraakt: ongeveer €41,61. Ter oriëntatie: 2x het risico winst ligt bij 489.64 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 2. Deutsche Börse (DB1.DE): instapmoment **gunstig**

- **Waarom sterk:** Deutsche Börse steeg +16,9% in 3 maanden en +9,5% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,2x het normale volume; beweegt gemiddeld 2,2% per dag.
- **Instapmoment:** de trend is sterk maar de koers is niet ver weggelopen (+2,8% van het 20-daags gemiddelde, RSI 63).
- **Status:** al in bezit.
- **Plan van de bot:** koop 3 stuks rond 320.46 EUR (inzet €961,38), stop-loss 306.33 EUR (-4,4%). Maximaal verlies als de stop wordt geraakt: ongeveer €44,39. Ter oriëntatie: 2x het risico winst ligt bij 348.72 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 3. Heineken (HEIA.AS): instapmoment **opgelopen**

- **Waarom sterk:** Heineken steeg +11,3% in 3 maanden en +17,7% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,1x het normale volume; beweegt gemiddeld 2,0% per dag.
- **Instapmoment:** de koers staat +6,3% van het 20-daags gemiddelde (3,1x de normale dagbeweging) en RSI is 77; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: RSI 77 boven de grens 75.
- **Plan van de bot:** koop 14 stuks rond 83.36 EUR (inzet €1.167,06), stop-loss 79.95 EUR (-4,1%). Maximaal verlies als de stop wordt geraakt: ongeveer €49,72. Ter oriëntatie: 2x het risico winst ligt bij 90.18 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 4. Wolters Kluwer (WKL.AS): instapmoment **neutraal**

- **Waarom sterk:** Wolters Kluwer steeg +28,6% in 3 maanden en +25,2% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 3,2% per dag.
- **Instapmoment:** de koers staat +6,4% van het 20-daags gemiddelde, RSI 67.
- **Status:** al in bezit.
- **Plan van de bot:** koop 8 stuks rond 89.94 EUR (inzet €719,56), stop-loss 84.25 EUR (-6,3%). Maximaal verlies als de stop wordt geraakt: ongeveer €47,55. Ter oriëntatie: 2x het risico winst ligt bij 101.33 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 5. Mastercard (MA): instapmoment **neutraal**

- **Waarom sterk:** Mastercard steeg +16,1% in 3 maanden en +13,7% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,2x het normale volume; beweegt gemiddeld 2,5% per dag.
- **Instapmoment:** de koers staat +4,0% van het 20-daags gemiddelde, RSI 64.
- **Status:** al in bezit.
- **Plan van de bot:** koop 1 stuk rond 653.03 USD (inzet €581,59), stop-loss 620.89 USD (-4,9%). Maximaal verlies als de stop wordt geraakt: ongeveer €30,62. Ter oriëntatie: 2x het risico winst ligt bij 717.29 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.


## Wat de bot tot nu toe geleerd heeft

- 5 afgesloten trades: 1 met winst (20%), gemiddeld -0,87 R per trade (R = winst of verlies gedeeld door het risico bij instap), totaal -€187,32.
- Pas vanaf 20 trades trekt de bot conclusies over welke omstandigheden goed of slecht uitpakken; met minder is het vooral toeval. Het wekelijkse onderzoek (zaterdag) doet dat.

## Klaar voor echt geld?

**Trend-agent:** Nog niet klaar: de bot is nog bezig met bewijzen. Blijven oefenen.

| Eis | Stand | Nu |
| --- | --- | --- |
| Oefentijd | ⏳ | 20 van 63 handelsdagen (ongeveer 3 maanden) |
| Minstens zo goed als de wereld-ETF | ⏳ | verschil tot nu toe +2,58% |
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
| 1 | OR.PA | 0.147 | +17.2% | +20.3% |
| 2 | DB1.DE | 0.136 | +16.9% | +9.5% |
| 3 | HEIA.AS | 0.135 | +11.3% | +17.7% |
| 4 | WKL.AS | 0.125 | +28.6% | +25.2% |
| 5 | MA | 0.125 | +16.1% | +13.7% |
| 6 | V | 0.123 | +17.2% | +12.7% |
| 7 | ABBV | 0.120 | +18.2% | +7.6% |
| 8 | BAYN.DE | 0.114 | +12.8% | +29.7% |
| 9 | AI.PA | 0.111 | +9.6% | +12.0% |
| 10 | PG | 0.110 | +13.7% | +10.6% |

## Afgesloten trades

5 trades, 1 winst (20%), totaal €-187.32 na kosten.
