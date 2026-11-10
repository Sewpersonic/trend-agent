# Trend-agent rapport 2026-11-09

_Oefenportefeuille met nepgeld. Geen beleggingsadvies; resultaten uit het verleden zeggen niets over de toekomst._

**Status:** OK  
**Waarde:** €9,901.14  
**Kas:** €3,362.61  
**Marktregime:** stijgend-hoog  
**Strategieversie:** trend-1.1-f132c3  
**Koersbronnen:** 69 bevestigd door 2 bronnen, 60 uit 1 bron, 0 afwijkend; wisselkoers bevestigd  
**Sinds start:** -0.99%  

## Analyse van vandaag

**Wat de bot zag**

- **Markt (IWDA.AS):** koers 128,45, 5,4% boven het 200-daags gemiddelde (121,90); de afgelopen maand -2,5%. Trend: **stijgend**.
- **Beweeglijkheid:** 13% op jaarbasis, tegen normaal 10% het afgelopen jaar: **hoog**.
- **Breedte:** 82 van de 129 instrumenten staan boven hun 200-daags gemiddelde (64%; EU 40 van 60, US 42 van 69).
- **Bekeken:** 129 instrumenten.
- **Afgevallen** (een instrument kan op meer regels afvallen): geen stijgende trend (koers niet boven 50- en 200-daags gemiddelde): 82; niet gestegen over 1 of 3 maanden: 74; te weinig handel: 2; verdachte dagsprong: 1.
- **Door de zeef:** 36. Koopbare trends: **36**.

**Wat de bot eruit haalt**

- De markt stijgt breed: goede omstandigheden voor trendvolgen.
- De markt beweegt meer dan normaal: stops worden sneller geraakt. Het risico per trade blijft gelijk, dus de posities worden vanzelf kleiner.
- 3 van de 5 sterkste staan al ver boven hun gemiddelde (HEIA.AS, BRK-B, BAYN.DE): de trend is sterk, maar instappen op zo'n moment kost vaker een terugval.
- Alle plekken zijn bezet, dus de bot koopt niets bij, hoe sterk een trend ook is.

## Vandaag gedaan

- Niets

## Verlies en risico

| Ticker | Instap | Koers nu | Resultaat | Stop | Afstand tot stop | Als de stop geraakt wordt |
| --- | --- | --- | --- | --- | --- | --- |
| SAP.DE | 191.56 EUR | 211.65 | €40,19 (+10,5%) | 199.49 | +6,1% | €14,87 winst vastgezet |
| DB1.DE | 314.96 EUR | 315.20 | €0,24 (+0,1%) | 306.40 | +2,9% | -€9,55 verlies |
| ABBV | 290.94 USD | 293.30 | €2,93 (+0,8%) | 277.38 | +5,7% | -€26,43 verlies |
| WKL.AS | 86.80 EUR | 88.86 | €20,57 (+2,4%) | 84.13 | +5,6% | -€27,73 verlies |
| MA | 647.63 USD | 655.81 | €16,77 (+1,3%) | 631.15 | +3,9% | -€28,16 verlies |
| V | 420.59 USD | 422.16 | €6,34 (+0,4%) | 412.07 | +2,5% | -€21,63 verlies |
| OR.PA | 446.42 EUR | 446.40 | -€0,05 (-0,0%) | 428.34 | +4,2% | -€37,16 verlies |
| PG | 167.40 USD | 168.32 | €9,48 (+0,5%) | 160.52 | +4,9% | -€47,08 verlies |

Raken alle stops tegelijk, dan is het verlies hooguit ongeveer €197,74 (bij een koersgat 's ochtends kan het meer zijn).

**Remmen** (bij overschrijden gaat de kill switch aan en koopt de bot niets meer):

- Daling vanaf de top: -0,86% (grens -10%; top was €9.987,03)
- Vandaag: +0,10% (grens -2%)
- Verliestrades op rij: 1 van 3

## Kansen: wat de bot vandaag het sterkst vond

_Dit is wat de oefenbot met zijn nepgeld volgens zijn eigen regels zou doen. Geen advies voor echt geld; het instapmoment is een ongeteste vuistregel en wordt door de bot niet gebruikt._

### 1. Heineken (HEIA.AS): instapmoment **opgelopen**

- **Waarom sterk:** Heineken steeg +12,7% in 3 maanden en +17,1% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,1x het normale volume; beweegt gemiddeld 2,0% per dag.
- **Instapmoment:** de koers staat +5,6% van het 20-daags gemiddelde (2,7x de normale dagbeweging) en RSI is 76; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: RSI 76 boven de grens 75.
- **Plan van de bot:** koop 14 stuks rond 83.34 EUR (inzet €1.166,78), stop-loss 79.94 EUR (-4,1%). Maximaal verlies als de stop wordt geraakt: ongeveer €49,60. Ter oriëntatie: 2x het risico winst ligt bij 90.14 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 2. L'Oreal (OR.PA): instapmoment **neutraal**

- **Waarom sterk:** L'Oreal steeg +17,3% in 3 maanden en +17,1% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,3x het normale volume; beweegt gemiddeld 2,2% per dag.
- **Instapmoment:** de koers staat +4,8% van het 20-daags gemiddelde, RSI 68.
- **Status:** al in bezit.
- **Plan van de bot:** koop 2 stuks rond 446.62 EUR (inzet €893,25), stop-loss 426.67 EUR (-4,5%). Maximaal verlies als de stop wordt geraakt: ongeveer €41,90. Ter oriëntatie: 2x het risico winst ligt bij 486.52 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 3. Berkshire Hathaway (BRK-B): instapmoment **opgelopen**

- **Waarom sterk:** Berkshire Hathaway steeg +11,4% in 3 maanden en +11,6% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,1x het normale volume; beweegt gemiddeld 1,9% per dag.
- **Instapmoment:** de koers staat +4,8% van het 20-daags gemiddelde (2,6x de normale dagbeweging) en RSI is 75; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: RSI 75 boven de grens 75.
- **Plan van de bot:** koop 2 stuks rond 575.54 USD (inzet €1.025,38), stop-loss 554.05 USD (-3,7%). Maximaal verlies als de stop wordt geraakt: ongeveer €40,28. Ter oriëntatie: 2x het risico winst ligt bij 618.51 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 4. Bayer (BAYN.DE): instapmoment **opgelopen**

- **Waarom sterk:** Bayer steeg +17,6% in 3 maanden en +29,0% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,2x het normale volume; beweegt gemiddeld 3,3% per dag.
- **Instapmoment:** de koers staat +13,4% van het 20-daags gemiddelde (4,0x de normale dagbeweging) en RSI is 77; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: RSI 77 boven de grens 75.
- **Plan van de bot:** koop 13 stuks rond 56.49 EUR (inzet €734,35), stop-loss 52.75 EUR (-6,6%). Maximaal verlies als de stop wordt geraakt: ongeveer €50,60. Ter oriëntatie: 2x het risico winst ligt bij 63.97 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 5. Procter & Gamble (PG): instapmoment **neutraal**

- **Waarom sterk:** Procter & Gamble steeg +16,7% in 3 maanden en +12,0% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,2x het normale volume; beweegt gemiddeld 2,3% per dag.
- **Instapmoment:** de koers staat +4,8% van het 20-daags gemiddelde, RSI 69.
- **Status:** al in bezit.
- **Plan van de bot:** koop 7 stuks rond 168.40 USD (inzet €1.050,10), stop-loss 160.71 USD (-4,6%). Maximaal verlies als de stop wordt geraakt: ongeveer €49,98. Ter oriëntatie: 2x het risico winst ligt bij 183.79 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.


## Wat de bot tot nu toe geleerd heeft

- 5 afgesloten trades: 1 met winst (20%), gemiddeld -0,87 R per trade (R = winst of verlies gedeeld door het risico bij instap), totaal -€187,32.
- Pas vanaf 20 trades trekt de bot conclusies over welke omstandigheden goed of slecht uitpakken; met minder is het vooral toeval. Het wekelijkse onderzoek (zaterdag) doet dat.

## Klaar voor echt geld?

**Trend-agent:** Nog niet klaar: de bot is nog bezig met bewijzen. Blijven oefenen.

| Eis | Stand | Nu |
| --- | --- | --- |
| Oefentijd | ⏳ | 21 van 63 handelsdagen (ongeveer 3 maanden) |
| Minstens zo goed als de wereld-ETF | ⏳ | verschil tot nu toe +1,75% |
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
| 1 | HEIA.AS | 0.145 | +12.7% | +17.1% |
| 2 | OR.PA | 0.141 | +17.3% | +17.1% |
| 3 | BRK-B | 0.134 | +11.4% | +11.6% |
| 4 | BAYN.DE | 0.131 | +17.6% | +29.0% |
| 5 | PG | 0.129 | +16.7% | +12.0% |
| 6 | ASRNL.AS | 0.123 | +13.4% | +9.3% |
| 7 | MA | 0.122 | +17.0% | +11.3% |
| 8 | IBE.MC | 0.122 | +11.7% | +8.2% |
| 9 | DB1.DE | 0.122 | +15.8% | +6.5% |
| 10 | AI.PA | 0.121 | +11.2% | +11.6% |

## Afgesloten trades

5 trades, 1 winst (20%), totaal €-187.32 na kosten.
