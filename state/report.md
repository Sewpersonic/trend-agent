# Trend-agent rapport 2026-11-02

_Oefenportefeuille met nepgeld. Geen beleggingsadvies; resultaten uit het verleden zeggen niets over de toekomst._

**Status:** GESTOPT  
**Waarde:** €9,944.33  
**Kas:** €5,051.88  
**Marktregime:** stijgend-laag  
**Strategieversie:** trend-1.1-081d85  
**Koersbronnen:** 69 bevestigd door 2 bronnen, 60 uit 1 bron, 0 afwijkend; wisselkoers bevestigd  
**Sinds start:** -0.56%  

## Analyse van vandaag

**Wat de bot zag**

- **Markt (IWDA.AS):** koers 129,87, 6,9% boven het 200-daags gemiddelde (121,50); de afgelopen maand -0,1%. Trend: **stijgend**.
- **Beweeglijkheid:** 9% op jaarbasis, tegen normaal 10% het afgelopen jaar: **laag**.
- **Breedte:** 77 van de 129 instrumenten staan boven hun 200-daags gemiddelde (60%; EU 37 van 60, US 40 van 69).
- **Bekeken:** 129 instrumenten.
- **Afgevallen** (een instrument kan op meer regels afvallen): geen stijgende trend (koers niet boven 50- en 200-daags gemiddelde): 85; niet gestegen over 1 of 3 maanden: 79; te weinig handel: 2; verdachte dagsprong: 1.
- **Door de zeef:** 35. Koopbare trends: **35**.

**Wat de bot eruit haalt**

- De markt stijgt, maar gedragen door een minderheid van de aandelen: kwetsbaarder dan het lijkt.
- De markt is rustig: stops liggen dichterbij, posities kunnen iets groter.
- Sterk zonder ver weggelopen te zijn: SHELL.AS, ABBV, DB1.DE.
- Er waren trends, maar geen enkele paste binnen de risicoregels (zie Kansen voor de reden per ticker).

## Vandaag gedaan

- SAP.DE: stop omhoog van 199.31 naar 199.49
- SELL 1 x MSFT @ 511.25 (stop-loss geraakt, resultaat €-22.73)

## Waarom

- **SELL MSFT**: stop-loss geraakt. Omstandigheden: RSI 40, MACD-histogram -0.68%, ATR 2.5% per dag, +16.0% boven SMA200, markt stijgend-laag, R = -0.96 na 23 dagen

## Waarschuwingen

- Kill switch aangezet: dagverlies groter dan 1%. Zet hem zelf weer uit met 'resume'.

## Verlies en risico

| Ticker | Instap | Koers nu | Resultaat | Stop | Afstand tot stop | Als de stop geraakt wordt |
| --- | --- | --- | --- | --- | --- | --- |
| SHELL.AS | 45.06 EUR | 47.02 | €25,51 (+4,4%) | 45.99 | +2,2% | €11,07 winst vastgezet |
| SAP.DE | 191.56 EUR | 210.10 | €37,09 (+9,7%) | 199.49 | +5,3% | €14,87 winst vastgezet |
| DB1.DE | 314.96 EUR | 314.20 | -€0,76 (-0,2%) | 302.20 | +4,0% | -€13,76 verlies |
| ABBV | 290.94 USD | 288.84 | -€3,22 (-0,7%) | 277.38 | +4,1% | -€24,71 verlies |
| CVX | 235.64 USD | 227.77 | -€37,17 (-3,3%) | 226.17 | +0,7% | -€45,32 verlies |
| XLE | 70.03 USD | 67.25 | -€49,56 (-4,0%) | 67.18 | +0,1% | -€51,69 verlies |
| WKL.AS | 86.80 EUR | 87.02 | €2,17 (+0,2%) | 82.09 | +6,0% | -€48,09 verlies |

Raken alle stops tegelijk, dan is het verlies hooguit ongeveer €183,57 (bij een koersgat 's ochtends kan het meer zijn).

**Remmen** (bij overschrijden gaat de kill switch aan en koopt de bot niets meer):

- Daling vanaf de top: -1,33% (grens -10%; top was €10.078,53)
- Vandaag: -1,33% (grens -1%)
- Verliestrades op rij: 1 van 3

## Kansen: wat de bot vandaag het sterkst vond

_Dit is wat de oefenbot met zijn nepgeld volgens zijn eigen regels zou doen. Geen advies voor echt geld; het instapmoment is een ongeteste vuistregel en wordt door de bot niet gebruikt._

### 1. Shell (SHELL.AS): instapmoment **gunstig**

- **Waarom sterk:** Shell steeg +23,6% in 3 maanden en +10,9% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD negatief (de stijging vertraagt); handel 1,0x het normale volume; beweegt gemiddeld 2,2% per dag.
- **Instapmoment:** de trend is sterk maar de koers is niet ver weggelopen (+1,4% van het 20-daags gemiddelde, RSI 59).
- **Status:** al in bezit.
- **Plan van de bot:** koop 24 stuks rond 47.04 EUR (inzet €1.129,04), stop-loss 45.01 EUR (-4,3%). Maximaal verlies als de stop wordt geraakt: ongeveer €50,81. Ter oriëntatie: 2x het risico winst ligt bij 51.11 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 2. Mastercard (MA): instapmoment **opgelopen**

- **Waarom sterk:** Mastercard steeg +15,4% in 3 maanden en +19,3% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,1x het normale volume; beweegt gemiddeld 1,9% per dag.
- **Instapmoment:** de koers staat +7,3% van het 20-daags gemiddelde (3,8x de normale dagbeweging) en RSI is 76; na zo'n sprint volgt vaak eerst een terugval.
- **Status:** niet gekocht: de kill switch staat aan.
- **Plan van de bot:** koop 2 stuks rond 658.43 USD (inzet €1.177,14), stop-loss 633.09 USD (-3,9%). Maximaal verlies als de stop wordt geraakt: ongeveer €47,31. Ter oriëntatie: 2x het risico winst ligt bij 709.11 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 3. AbbVie (ABBV): instapmoment **gunstig**

- **Waarom sterk:** AbbVie steeg +19,2% in 3 maanden en +10,6% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,1x het normale volume; beweegt gemiddeld 2,4% per dag.
- **Instapmoment:** de trend is sterk maar de koers is niet ver weggelopen (+2,3% van het 20-daags gemiddelde, RSI 63).
- **Status:** al in bezit.
- **Plan van de bot:** koop 4 stuks rond 288.98 USD (inzet €1.033,29), stop-loss 275.18 USD (-4,8%). Maximaal verlies als de stop wordt geraakt: ongeveer €51,37. Ter oriëntatie: 2x het risico winst ligt bij 316.60 USD; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 4. Deutsche Börse (DB1.DE): instapmoment **gunstig**

- **Waarom sterk:** Deutsche Börse steeg +16,8% in 3 maanden en +9,4% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 1,1x het normale volume; beweegt gemiddeld 2,1% per dag.
- **Instapmoment:** de trend is sterk maar de koers is niet ver weggelopen (+2,3% van het 20-daags gemiddelde, RSI 64).
- **Status:** al in bezit.
- **Plan van de bot:** koop 3 stuks rond 314.36 EUR (inzet €943,07), stop-loss 301.10 EUR (-4,2%). Maximaal verlies als de stop wordt geraakt: ongeveer €41,77. Ter oriëntatie: 2x het risico winst ligt bij 340.87 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.

### 5. Wolters Kluwer (WKL.AS): instapmoment **neutraal**

- **Waarom sterk:** Wolters Kluwer steeg +25,7% in 3 maanden en +28,3% in 1 maand; koers boven het 50-daags en dat boven het 200-daags gemiddelde; MACD positief (de stijging versnelt); handel 0,9x het normale volume; beweegt gemiddeld 2,8% per dag.
- **Instapmoment:** de koers staat +6,5% van het 20-daags gemiddelde, RSI 71.
- **Status:** al in bezit.
- **Plan van de bot:** koop 10 stuks rond 87.06 EUR (inzet €870,64), stop-loss 82.27 EUR (-5,5%). Maximaal verlies als de stop wordt geraakt: ongeveer €49,91. Ter oriëntatie: 2x het risico winst ligt bij 96.65 EUR; de bot verkoopt daar niet vanzelf, hij laat de stop meeschuiven.


## Wat de bot tot nu toe geleerd heeft

- 1 afgesloten trades: 0 met winst (0%), gemiddeld -0,96 R per trade (R = winst of verlies gedeeld door het risico bij instap), totaal -€22,73.
- Pas vanaf 20 trades trekt de bot conclusies over welke omstandigheden goed of slecht uitpakken; met minder is het vooral toeval. Het wekelijkse onderzoek (zaterdag) doet dat.

## Klaar voor echt geld?

**Trend-agent:** Nog niet klaar: de bot is nog bezig met bewijzen. Blijven oefenen.

| Eis | Stand | Nu |
| --- | --- | --- |
| Oefentijd | ⏳ | 16 van 63 handelsdagen (ongeveer 3 maanden) |
| Minstens zo goed als de wereld-ETF | ⏳ | verschil tot nu toe +1,11% |
| Grootste daling onder 5% | ✅ | grootste daling tot nu toe -1,33% |
| Genoeg afgesloten trades | ⏳ | 1 van 20 |

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
| SAP.DE | 2 | 191.56 EUR | 199.49 | 2026-10-10 |
| DB1.DE | 1 | 314.96 EUR | 302.20 | 2026-10-29 |
| ABBV | 2 | 290.94 USD | 277.38 | 2026-10-29 |
| CVX | 5 | 235.64 USD | 226.17 | 2026-10-30 |
| XLE | 19 | 70.03 USD | 67.18 | 2026-10-30 |
| WKL.AS | 10 | 86.80 EUR | 82.09 | 2026-10-30 |

## Sterkste trends vandaag

| # | Ticker | Score | 3 mnd | 1 mnd |
| --- | --- | --- | --- | --- |
| 1 | SHELL.AS | 0.151 | +23.6% | +10.9% |
| 2 | MA | 0.142 | +15.4% | +19.3% |
| 3 | ABBV | 0.138 | +19.2% | +10.6% |
| 4 | DB1.DE | 0.138 | +16.8% | +9.4% |
| 5 | WKL.AS | 0.137 | +25.7% | +28.3% |
| 6 | LLY | 0.132 | +26.7% | +23.5% |
| 7 | V | 0.132 | +15.3% | +18.0% |
| 8 | OR.PA | 0.115 | +12.3% | +17.1% |
| 9 | KO | 0.114 | +11.4% | +11.9% |
| 10 | PG | 0.112 | +11.2% | +13.6% |

## Afgesloten trades

1 trades, 0 winst (0%), totaal €-22.73 na kosten.
