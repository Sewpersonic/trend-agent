# Trend-agent rapport 2026-11-19

_Oefenportefeuille met nepgeld. Geen beleggingsadvies; resultaten uit het verleden zeggen niets over de toekomst._

**Status:** OK  
**Waarde:** €9,820.63  
**Kas:** €2,525.68  
**Marktregime:** stijgend-hoog  
**Strategieversie:** trend-1.1-eaf4f8  
**Koersbronnen:** 69 bevestigd door 2 bronnen, 60 uit 1 bron, 0 afwijkend; wisselkoers bevestigd  
**Sinds start:** -1.79%  

## Analyse van vandaag

**Wat de bot zag**

- **Markt (IWDA.AS):** koers 126,70, 3,4% boven het 200-daags gemiddelde (122,57); de afgelopen maand -3,4%. Trend: **stijgend**.
- **Beweeglijkheid:** 16% op jaarbasis, tegen normaal 10% het afgelopen jaar: **hoog**.
- **Breedte:** 65 van de 129 instrumenten staan boven hun 200-daags gemiddelde (50%; EU 36 van 60, US 29 van 69).
- **Bekeken:** 129 instrumenten.
- **Afgevallen** (een instrument kan op meer regels afvallen): geen stijgende trend (koers niet boven 50- en 200-daags gemiddelde): 92; niet gestegen over 1 of 3 maanden: 87; te weinig handel: 2; verdachte dagsprong: 1.
- **Door de zeef:** 27. Koopbare trends: **27**.

**Wat de bot eruit haalt**

- De markt stijgt, maar gedragen door een minderheid van de aandelen: kwetsbaarder dan het lijkt.
- De markt beweegt meer dan normaal: stops worden sneller geraakt. Het risico per trade blijft gelijk, dus de posities worden vanzelf kleiner.
- Sterk zonder ver weggelopen te zijn: BRK-B, BAYN.DE.
- Gekocht vandaag: PHIA.AS.

## Vandaag gedaan

- SELL 2 x MA @ 630.84 (stop-loss geraakt, resultaat €-4.11)
- PG: stop omhoog van 162.72 naar 163.02
- BUY 35 x PHIA.AS @ 26.85 (trend OK: 3m +13.7%, 1m +14.7%, volume x1.29)

## Waarom

- **SELL MA**: stop-loss geraakt. Omstandigheden: RSI 46, MACD-histogram -0.74%, ATR 2.6% per dag, +15.5% boven SMA200, markt stijgend-hoog, R = -0.09 na 16 dagen
- **BUY PHIA.AS**: trend OK: 3m +13.7%, 1m +14.7%, volume x1.29. Omstandigheden: RSI 68, MACD-histogram -0.24%, ATR 2.6% per dag, +14.7% boven SMA200, markt stijgend-hoog

## Verlies en risico

| Ticker | Instap | Koers nu | Resultaat | Stop | Afstand tot stop | Als de stop geraakt wordt |
| --- | --- | --- | --- | --- | --- | --- |
| DB1.DE | 314.96 EUR | 320.50 | €5,54 (+1,8%) | 311.69 | +2,8% | -€4,27 verlies |
| ABBV | 290.94 USD | 283.51 | -€3,00 (-2,5%) | 277.38 | +2,2% | -€15,17 verlies |
| WKL.AS | 86.80 EUR | 86.30 | -€5,03 (-0,6%) | 84.28 | +2,4% | -€26,28 verlies |
| OR.PA | 446.42 EUR | 437.70 | -€17,45 (-1,9%) | 428.45 | +2,2% | -€36,94 verlies |
| PG | 167.40 USD | 167.85 | €33,39 (+0,3%) | 163.02 | +3,0% | -€2,84 verlies |
| BRK-B | 574.91 USD | 572.04 | -€6,72 (-0,5%) | 551.07 | +3,8% | -€45,93 verlies |
| AI.PA | 189.91 EUR | 189.28 | -€5,08 (-0,3%) | 184.03 | +2,9% | -€48,11 verlies |
| PHIA.AS | 26.85 EUR | 26.84 | -€0,47 (-0,1%) | 25.46 | +5,4% | -€49,70 verlies |

Raken alle stops tegelijk, dan is het verlies hooguit ongeveer €229,24 (bij een koersgat 's ochtends kan het meer zijn).

**Remmen** (bij overschrijden gaat de kill switch aan en koopt de bot niets meer):

- Daling vanaf de top: -2,65% (grens -10%; top was €10.087,85)
- Vandaag: -0,71% (grens -2%)
- Verliestrades op rij: 1 van 3

## Kansen: wat de bot vandaag het sterkst vond

_Dit is wat de oefenbot met zijn nepgeld volgens zijn eigen regels zou doen. Geen advies voor echt geld; het instapmoment is een ongeteste vuistregel en wordt door de bot niet gebruikt._

### 1. Berkshire Hathaway (BRK-B): instapmoment **gunstig**

- **Waarom sterk:** Berkshire Hathaway steeg +15,4% in 3 maanden en +6,1% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD negatief (de stijging vertraagt); handel 1,1x het normale volume; beweegt gemiddeld 2,1% per dag.
- **Instapmoment:** de trend is sterk maar de koers is niet ver weggelopen (+0,7% van het 20-daags gemiddelde, RSI 58).
- **Status:** al in bezit.
- **Plan van de bot:** koop 2 stuks rond 572.33 USD (inzet €1.042,89), stop-loss 548.42 USD (-4,2%). Maximaal verlies als de stop wordt geraakt: ongeveer €45,57. Ter oriëntatie: 2x het risico winst ligt bij 620.15 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 2. Philips (PHIA.AS): instapmoment **neutraal**

- **Waarom sterk:** Philips steeg +13,7% in 3 maanden en +14,7% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD negatief (de stijging vertraagt); handel 1,3x het normale volume; beweegt gemiddeld 2,6% per dag.
- **Instapmoment:** de koers staat +2,7% van het 20-daags gemiddelde, RSI 68.
- **Status:** vandaag gekocht door de bot.
- **Plan van de bot:** koop 35 stuks rond 26.85 EUR (inzet €939,87), stop-loss 25.46 EUR (-5,2%). Maximaal verlies als de stop wordt geraakt: ongeveer €50,70. Ter oriëntatie: 2x het risico winst ligt bij 29.64 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 3. Air Liquide (AI.PA): instapmoment **neutraal**

- **Waarom sterk:** Air Liquide steeg +12,9% in 3 maanden en +9,0% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD negatief (de stijging vertraagt); handel 1,1x het normale volume; beweegt gemiddeld 1,5% per dag.
- **Instapmoment:** de koers staat +1,8% van het 20-daags gemiddelde, RSI 66.
- **Status:** al in bezit.
- **Plan van de bot:** koop 8 stuks rond 189.37 EUR (inzet €1.515,00), stop-loss 183.78 EUR (-2,9%). Maximaal verlies als de stop wordt geraakt: ongeveer €46,75. Ter oriëntatie: 2x het risico winst ligt bij 200.56 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 4. Costco (COST): instapmoment **neutraal**

- **Waarom sterk:** Costco steeg +15,6% in 3 maanden en +9,7% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,1x het normale volume; beweegt gemiddeld 1,9% per dag.
- **Instapmoment:** de koers staat +3,3% van het 20-daags gemiddelde, RSI 68.
- **Status:** niet gekocht: alle 8 plekken zijn bezet.
- **Plan van de bot:** koop 1 stuk rond 1094.38 USD (inzet €997,09), stop-loss 1052.44 USD (-3,8%). Maximaal verlies als de stop wordt geraakt: ongeveer €40,21. Ter oriëntatie: 2x het risico winst ligt bij 1178.25 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 5. Bayer (BAYN.DE): instapmoment **gunstig**

- **Waarom sterk:** Bayer steeg +13,4% in 3 maanden en +23,2% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,2x het normale volume; beweegt gemiddeld 3,1% per dag.
- **Instapmoment:** de trend is sterk maar de koers is niet ver weggelopen (+3,0% van het 20-daags gemiddelde, RSI 63).
- **Status:** niet gekocht: alle 8 plekken zijn bezet.
- **Plan van de bot:** koop 14 stuks rond 55.01 EUR (inzet €770,10), stop-loss 51.62 EUR (-6,2%). Maximaal verlies als de stop wordt geraakt: ongeveer €49,42. Ter oriëntatie: 2x het risico winst ligt bij 61.78 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.


## Wat de bot tot nu toe geleerd heeft

- 8 afgesloten trades: 3 met winst (38%), gemiddeld -0,46 R per trade (R = winst of verlies gedeeld door het risico bij instap), totaal -€172,54.
- Pas vanaf 20 trades trekt de bot conclusies over welke omstandigheden goed of slecht uitpakken; met minder is het vooral toeval. Het wekelijkse onderzoek (zaterdag) doet dat.

## Klaar voor echt geld?

**Trend-agent:** Nog niet klaar: de bot is nog bezig met bewijzen. Blijven oefenen.

| Eis | Stand | Nu |
| --- | --- | --- |
| Oefentijd | ⏳ | 29 van 63 handelsdagen (ongeveer 3 maanden) |
| Minstens zo goed als de wereld-ETF | ⏳ | verschil tot nu toe +2,27% |
| Grootste daling onder 5% | ✅ | grootste daling tot nu toe -2,65% |
| Genoeg afgesloten trades | ⏳ | 8 van 20 |

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
| DB1.DE | 1 | 314.96 EUR | 311.69 | 2026-10-29 |
| ABBV | 2 | 290.94 USD | 277.38 | 2026-10-29 |
| WKL.AS | 10 | 86.80 EUR | 84.28 | 2026-10-30 |
| OR.PA | 2 | 446.42 EUR | 428.45 | 2026-11-04 |
| PG | 8 | 167.40 USD | 163.02 | 2026-11-04 |
| BRK-B | 2 | 574.91 USD | 551.07 | 2026-11-18 |
| AI.PA | 8 | 189.91 EUR | 184.03 | 2026-11-18 |
| PHIA.AS | 35 | 26.85 EUR | 25.46 | 2026-11-19 |

## Sterkste trends vandaag

| # | Ticker | Score | 3 mnd | 1 mnd |
| --- | --- | --- | --- | --- |
| 1 | BRK-B | 0.131 | +15.4% | +6.1% |
| 2 | PHIA.AS | 0.125 | +13.7% | +14.7% |
| 3 | AI.PA | 0.121 | +12.9% | +9.0% |
| 4 | COST | 0.113 | +15.6% | +9.7% |
| 5 | BAYN.DE | 0.106 | +13.4% | +23.2% |
| 6 | PG | 0.103 | +16.8% | +7.7% |
| 7 | HEIA.AS | 0.103 | +12.7% | +8.1% |
| 8 | ASRNL.AS | 0.100 | +12.6% | +4.3% |
| 9 | IBE.MC | 0.098 | +12.5% | +4.6% |
| 10 | OR.PA | 0.093 | +11.5% | +7.9% |

## Afgesloten trades

8 trades, 3 winst (38%), totaal €-172.54 na kosten.
