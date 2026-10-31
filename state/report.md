# Trend-agent rapport 2026-10-30

_Oefenportefeuille met nepgeld. Geen beleggingsadvies; resultaten uit het verleden zeggen niets over de toekomst._

**Status:** OK  
**Waarde:** €10,078.53  
**Kas:** €4,595.88  
**Marktregime:** stijgend-normaal  
**Strategieversie:** trend-1.1-081d85  
**Koersbronnen:** 69 bevestigd door 2 bronnen, 60 uit 1 bron, 0 afwijkend; wisselkoers bevestigd  
**Sinds start:** +0.79%  

## Analyse van vandaag

**Wat de bot zag**

- **Markt (IWDA.AS):** koers 129,70, 6,8% boven het 200-daags gemiddelde (121,41); de afgelopen maand +0,7%. Trend: **stijgend**.
- **Beweeglijkheid:** 9% op jaarbasis, tegen normaal 10% het afgelopen jaar: **normaal**.
- **Breedte:** 73 van de 129 instrumenten staan boven hun 200-daags gemiddelde (57%; EU 34 van 60, US 39 van 69).
- **Bekeken:** 129 instrumenten.
- **Afgevallen** (een instrument kan op meer regels afvallen): geen stijgende trend (koers niet boven 50- en 200-daags gemiddelde): 86; niet gestegen over 1 of 3 maanden: 79; te weinig handel: 2; verdachte dagsprong: 1.
- **Door de zeef:** 35. Koopbare trends: **35**.

**Wat de bot eruit haalt**

- De markt stijgt, maar gedragen door een minderheid van de aandelen: kwetsbaarder dan het lijkt.
- Gekocht vandaag: CVX, XLE, WKL.AS.

## Vandaag gedaan

- Niets

## Waarom

- **BUY CVX**: trend OK: 3m +23.0%, 1m +13.7%, volume x0.89. Omstandigheden: RSI 73, MACD-histogram +0.34%, ATR 2.0% per dag, +23.1% boven SMA200, markt stijgend-normaal
- **BUY XLE**: trend OK: 3m +19.8%, 1m +11.6%, volume x1.05. Omstandigheden: RSI 68, MACD-histogram +0.15%, ATR 2.0% per dag, +20.4% boven SMA200, markt stijgend-normaal
- **BUY WKL.AS**: trend OK: 3m +22.9%, 1m +26.4%, volume x0.86. Omstandigheden: RSI 71, MACD-histogram +0.14%, ATR 2.7% per dag, +31.8% boven SMA200, markt stijgend-normaal

## Verlies en risico

| Ticker | Instap | Koers nu | Resultaat | Stop | Afstand tot stop | Als de stop geraakt wordt |
| --- | --- | --- | --- | --- | --- | --- |
| SHELL.AS | 45.06 EUR | 48.80 | €48,59 (+8,3%) | 45.99 | +6,1% | €11,07 winst vastgezet |
| SAP.DE | 191.56 EUR | 211.75 | €40,39 (+10,5%) | 199.31 | +6,2% | €14,50 winst vastgezet |
| MSFT | 535.34 USD | 521.91 | -€11,03 (-2,5%) | 511.50 | +2,0% | -€21,33 verlies |
| DB1.DE | 314.96 EUR | 320.40 | €5,44 (+1,7%) | 302.20 | +6,0% | -€13,76 verlies |
| ABBV | 290.94 USD | 294.89 | €7,79 (+1,4%) | 277.38 | +6,3% | -€24,53 verlies |
| CVX | 235.64 USD | 235.52 | -€2,14 (-0,1%) | 226.17 | +4,1% | -€44,94 verlies |
| XLE | 70.03 USD | 70.02 | -€2,08 (-0,0%) | 67.18 | +4,2% | -€51,27 verlies |
| WKL.AS | 86.80 EUR | 86.76 | -€0,43 (-0,1%) | 82.09 | +5,7% | -€48,09 verlies |

Raken alle stops tegelijk, dan is het verlies hooguit ongeveer €203,92 (bij een koersgat 's ochtends kan het meer zijn).

**Remmen** (bij overschrijden gaat de kill switch aan en koopt de bot niets meer):

- Daling vanaf de top: -0,05% (grens -10%; top was €10.083,15)
- Vandaag: +0,11% (grens -1%)
- Verliestrades op rij: 0 van 3

## Kansen: wat de bot vandaag het sterkst vond

_Dit is wat de oefenbot met zijn nepgeld volgens zijn eigen regels zou doen. Geen advies voor echt geld; het instapmoment is een ongeteste vuistregel en wordt door de bot niet gebruikt._

### 1. Shell (SHELL.AS): instapmoment **neutraal**

- **Waarom sterk:** Shell steeg +26,8% in 3 maanden en +15,5% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,0x het normale volume; beweegt gemiddeld 1,9% per dag.
- **Instapmoment:** de koers staat +5,4% van het 20-daags gemiddelde, RSI 74.
- **Status:** al in bezit.
- **Plan van de bot:** koop 26 stuks rond 48.82 EUR (inzet €1.269,30), stop-loss 46.95 EUR (-3,8%). Maximaal verlies als de stop wordt geraakt: ongeveer €50,69. Ter oriëntatie: 2x het risico winst ligt bij 52.57 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 2. Deutsche Börse (DB1.DE): instapmoment **opgelopen**

- **Waarom sterk:** Deutsche Börse steeg +21,1% in 3 maanden en +11,8% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,1x het normale volume; beweegt gemiddeld 2,0% per dag.
- **Instapmoment:** de koers staat +4,5% van het 20-daags gemiddelde (2,3x de normale dagbeweging) en RSI is 77; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** al in bezit.
- **Plan van de bot:** koop 3 stuks rond 320.56 EUR (inzet €961,68), stop-loss 307.66 EUR (-4,0%). Maximaal verlies als de stop wordt geraakt: ongeveer €40,70. Ter oriëntatie: 2x het risico winst ligt bij 346.36 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 3. AbbVie (ABBV): instapmoment **neutraal**

- **Waarom sterk:** AbbVie steeg +21,1% in 3 maanden en +14,1% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,1x het normale volume; beweegt gemiddeld 2,4% per dag.
- **Instapmoment:** de koers staat +4,7% van het 20-daags gemiddelde, RSI 73.
- **Status:** al in bezit.
- **Plan van de bot:** koop 4 stuks rond 295.04 USD (inzet €1.055,33), stop-loss 281.10 USD (-4,7%). Maximaal verlies als de stop wordt geraakt: ongeveer €51,86. Ter oriëntatie: 2x het risico winst ligt bij 322.92 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 4. Chevron (CVX): instapmoment **neutraal**

- **Waarom sterk:** Chevron steeg +23,0% in 3 maanden en +13,7% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 2,0% per dag.
- **Instapmoment:** de koers staat +5,3% van het 20-daags gemiddelde, RSI 73.
- **Status:** vandaag gekocht door de bot.
- **Plan van de bot:** koop 5 stuks rond 235.64 USD (inzet €1.053,57), stop-loss 226.17 USD (-4,0%). Maximaal verlies als de stop wordt geraakt: ongeveer €44,34. Ter oriëntatie: 2x het risico winst ligt bij 254.58 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 5. Eli Lilly (LLY): instapmoment **opgelopen**

- **Waarom sterk:** Eli Lilly steeg +26,6% in 3 maanden en +23,3% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,0x het normale volume; beweegt gemiddeld 3,4% per dag.
- **Instapmoment:** de koers staat +11,9% van het 20-daags gemiddelde (3,5x de normale dagbeweging) en RSI is 78; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: RSI 78 boven de grens 75.
- **Plan van de bot:** instap rond 1418.25 USD, stop 1321.77 USD (-6,8%). Met een risicobudget van €50,39 past er geen heel stuk in.


## Wat de bot tot nu toe geleerd heeft

- Nog geen afgesloten trades. Leren begint pas als trades zijn afgesloten: dan weet de bot of een instap goed of slecht uitpakte, en onder welke omstandigheden.

## Klaar voor echt geld?

**Trend-agent:** Nog niet klaar: de bot is nog bezig met bewijzen. Blijven oefenen.

| Eis | Stand | Nu |
| --- | --- | --- |
| Oefentijd | ⏳ | 15 van 63 handelsdagen (ongeveer 3 maanden) |
| Minstens zo goed als de wereld-ETF | ⏳ | verschil tot nu toe +2,58% |
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
| SHELL.AS | 13 | 45.06 EUR | 45.99 | 2026-10-10 |
| SAP.DE | 2 | 191.56 EUR | 199.31 | 2026-10-10 |
| MSFT | 1 | 535.34 USD | 511.50 | 2026-10-10 |
| DB1.DE | 1 | 314.96 EUR | 302.20 | 2026-10-29 |
| ABBV | 2 | 290.94 USD | 277.38 | 2026-10-29 |
| CVX | 5 | 235.64 USD | 226.17 | 2026-10-30 |
| XLE | 19 | 70.03 USD | 67.18 | 2026-10-30 |
| WKL.AS | 10 | 86.80 EUR | 82.09 | 2026-10-30 |

## Sterkste trends vandaag

| # | Ticker | Score | 3 mnd | 1 mnd |
| --- | --- | --- | --- | --- |
| 1 | SHELL.AS | 0.193 | +26.8% | +15.5% |
| 2 | DB1.DE | 0.173 | +21.1% | +11.8% |
| 3 | ABBV | 0.162 | +21.1% | +14.1% |
| 4 | CVX | 0.135 | +23.0% | +13.7% |
| 5 | LLY | 0.129 | +26.6% | +23.3% |
| 6 | XLE | 0.125 | +19.8% | +11.7% |
| 7 | WKL.AS | 0.123 | +22.9% | +26.4% |
| 8 | XOM | 0.122 | +21.5% | +14.3% |
| 9 | TTE.PA | 0.122 | +16.3% | +14.6% |
| 10 | MA | 0.119 | +11.9% | +16.2% |
