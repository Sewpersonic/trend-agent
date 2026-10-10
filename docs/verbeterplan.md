# Verbeterplan: wat de bots kunnen, wat ontbrak, wat er is gedaan

Stand: oktober 2026. Beide bots handelen alleen met nepgeld.

## Inventaris

| Onderdeel | Was er al | Ontbrak | Nu gedaan |
| --- | --- | --- | --- |
| Marktanalyse | SMA50/200, ATR, rendement 1 en 3 maanden, beweeglijkheid, relatief volume, 12-maands momentum | RSI, MACD, EMA; herkennen van het marktregime | RSI, MACD, EMA, ATR%, afstand tot SMA200 (`features.py`); regime = trend (stijgend/dalend/zijwaarts) × beweeglijkheid (laag/normaal/hoog) |
| Leren van historie | Backtest over 5 jaar zonder look-ahead, met kosten; vergelijking met ETF | Scheiding in ongezien deel, periodes, kostenstress, regime-uitsplitsing | Evaluatiekader (`evaluation.py`): 70/30 holdout, 5 periodes, dubbele kosten, per regime, walk-forward-selectietest |
| Leren van trades | Trades met reden en resultaat | Marktomstandigheden bij in- en uitstap, R-multiple, houdduur, strategieversie; analyse van winst vs. verlies | Tradejournaal in `portfolio.py`; leeranalyse (`learning.py`) per regime, RSI, MACD, volume, ATR, uitstapreden, versie; driftmelding live vs. backtest |
| Strategie optimaliseren | Twee losse controles op de investeerder | Varianten eerlijk vergelijken; acceptatiepoort | Klein vast setje varianten per bot; alleen "AANBEVOLEN" als alle 6 toetsen slagen |
| Risicobeheer | Risico per trade 0,25%, max 1% open, max 3 posities, ATR-stop, meeschuivende stop, kill switch, kosten en slippage | Herkennen van te onzekere markten; datakwaliteit per instrument | Regimefilter (standaard uit, eerst bewijzen); verdachte data (bevroren koers, sprong, geen volume) wordt niet gekocht |
| Verbeterlus | Geen | Vaste cyclus van meten, testen, aanbevelen; versies bijhouden | Wekelijkse Action `onderzoek`; strategieversie op elke trade; `onderzoek/historie.csv` |
| Betrouwbaarheid | Controle op oude/kapotte koersen, wisselkoers, auditlog | Signaal bij fouten; uitleg per beslissing | `state/health.json`; Action wordt rood bij problemen (GitHub mailt je); "Waarom"-sectie per trade in het dagrapport |

## Hoe de verbeterlus werkt

1. **Elke werkdag** handelen beide bots met nepgeld en leggen ze elke beslissing vast, met omstandigheden en versie.
2. **Elke zaterdag** draait de Action `onderzoek`:
   - test een paar varianten tegen productie op 5 jaar echte koersen;
   - analyseert de trades uit de backtest én uit het oefenen: welke omstandigheden gaan samen met winst of verlies?
   - vergelijkt live met de backtest (drift: werkt de strategie nog zoals getest?);
   - schrijft `onderzoek/LAATSTE.md` en een regel per variant in `onderzoek/historie.csv`.
3. **Een mens beslist.** Staat een variant op AANBEVOLEN, dan kun je die instelling in de code aanpassen. Daardoor
   verandert de strategieversie vanzelf, en draait de backtest opnieuw. De Action `onderzoek` mag technisch alleen
   bestanden in `onderzoek/` opslaan.

## Waarom de bot zichzelf niet automatisch aanpast

- Met een handvol varianten en 5 jaar data is de kans groot dat een "winnaar" toevallig goed uitkomt.
- Het rapport meet dit ook: in de sectie "Zelf bijsturen op basis van het verleden?" staat of het steeds kiezen van
  de tot dan toe beste variant beter had gewerkt dan productie houden.
- Een fout in een automatische aanpassing kan ongemerkt veel schade doen. Een mens die het rapport leest is een goede rem.

## Bekende beperkingen

- **Survivorship bias**: de aandelenlijst is in 2026 gekozen. De controle met alleen ETF's in `backtest/` geeft een eerlijker beeld.
- **Gratis data** (Yahoo Finance) kan gaten of fouten bevatten; verdachte reeksen worden overgeslagen.
- **De investeerder** herverdeelt maandelijks; zijn trades zijn herverdelingen, geen losse ideeën. Daarom wordt hij
  vooral beoordeeld op rendement tegenover de wereld-ETF, niet per trade.
- **Spread** is niet apart gemodelleerd; die zit in de slippage (0,05%) en wordt in de stresstest verdubbeld.
