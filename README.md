# Trend-agent en investeerder (oefenen met nepgeld)

Er draaien twee bots naast elkaar, elk met hun eigen €10.000 nepgeld:

- **Investeerder** (`python -m trendagent invest`): 60% wereldwijde ETF, 30% de 5 sterkste aandelen/ETF's
  van het afgelopen jaar, 10% Bitcoin/Ethereum alleen in een stijgende trend. Eén keer per maand herverdelen.
  Rapport: `rapporten/investeerder.xlsx`.
- **Trend-agent** (`python -m trendagent run`): handelt korter op trends met een zeer klein risico per trade.
  Rapport: `rapporten/trend-agent.xlsx`.

Backtest over 5 jaar (okt 2021 tot okt 2026, €10.000, na kosten): investeerder €27.400, investeerder met alleen
ETF's €20.800, gewoon de wereld-ETF vasthouden €18.000, trend-agent €10.600. Zie `backtest/`. Het verleden is
geen garantie, en de aandelenlijst is achteraf gekozen.

## Candle-grafieken

Elke dag maakt de bot per positie een candle-grafiek van de laatste 3 maanden, met het 50- en 200-daags
gemiddelde, de instapprijs, de stop-loss en het volume. Je ziet ze onderaan de dagnotities in `rapporten/`
en in het tabblad **Grafieken** van `trend-agent.xlsx` en `investeerder.xlsx`. De afbeeldingen staan in
`rapporten/grafieken/` en worden 20 handelsdagen bewaard.

## Verlies, risico en kansen in het rapport

Elk dagrapport (en `rapporten/OVERZICHT.md`) laat zien:

- **Verlies en risico:** per open positie het resultaat nu, hoe ver de koers boven de stop-loss staat en wat je
  verliest (of al vastzet) als de stop wordt geraakt; plus hoe dicht de bot bij zijn remmen zit (daling vanaf de
  top, dagverlies, verliestrades op rij). Bij de investeerder: winst of verlies per belegging.
- **Kansen:** de 5 sterkste trends met uitleg waarom, een inschatting van het instapmoment (gunstig, neutraal of
  opgelopen) en het precieze plan van de bot: instapprijs, stop-loss, aantal, inzet in euro en maximaal verlies.

Dit is wat de oefenbot met nepgeld zou doen, geen advies voor echt geld. Het instapmoment is een ongeteste
vuistregel; de bot gebruikt hem niet bij het kopen.

## Koersen uit meerdere bronnen

Elke dag haalt de bot de koersen bij **Yahoo Finance** (hoofdbron) en controleert hij ze bij **Stooq**. De
wisselkoers euro/dollar controleert hij bij de **Europese Centrale Bank**. Wijken de bronnen meer dan 2% af,
dan koopt de bot dat aandeel die dag niet. Wijkt de wisselkoers meer dan 1% af, dan handelt hij die dag
helemaal niet. Valt Yahoo uit, dan gebruikt hij Stooq of de ECB. Lopen de koersen van een hele markt
achter (bijvoorbeeld alle Europese aandelen), dan koopt hij daar die dag niets. In het dagrapport en de gezondheidscontrole
staat hoeveel koersen door twee bronnen zijn bevestigd. Google Finance heeft geen API en mag niet automatisch
worden uitgelezen, dus die zit er niet bij. De backtest gebruikt alleen Yahoo.

## Hoe de bots leren en verbeteren

- **Elke werkdag** (Action `practice`): beide bots handelen met nepgeld en leggen elke trade vast met reden,
  marktregime, indicatoren (RSI, MACD, EMA, ATR) en strategieversie. Het dagrapport legt per trade uit waarom.
  Gaat er iets mis met de data of de bot, dan wordt de run rood en mailt GitHub je.
- **Elke zaterdag** (Action `onderzoek`): varianten worden getest tegen productie op 5 jaar echte koersen, met
  een ongezien deel, 5 periodes, dubbele kosten en een uitsplitsing per marktregime. Daarna volgt een analyse van
  welke omstandigheden samengaan met winst of verlies, en of de bot live nog presteert zoals in de test.
  Rapport: `onderzoek/LAATSTE.md`; verloop: `onderzoek/historie.csv`.
- **Een mens beslist.** Haalt een variant alle toetsen, dan zet het onderzoek een **voorstel** (pull request)
  klaar dat alleen `config/productie.json` wijzigt. Je krijgt een e-mail van GitHub. **Merge** = overnemen,
  **Close** = laten zoals het is. Na een merge draait de backtest opnieuw met de nieuwe instellingen.
  Eenmalig nodig: Settings → Actions → General → "Allow GitHub Actions to create and approve pull requests" aanvinken.

Zie `docs/verbeterplan.md` voor de inventaris en `docs/ml-beoordeling.md` voor waarom er (nog) geen machine learning is.

## Trend-agent

Een agent die **zelfstandig** handelt in wat op dit moment trending is in Europa en Amerika,
maar alleen in een **nep-portefeuille** van €10.000. Er gaat nooit echt geld om: er bestaat
geen code die met een broker praat, en de agent weigert te starten als `PAPER_TRADING` niet `true` is.

> Geen beleggingsadvies. Resultaten op papier zeggen niets over toekomstige resultaten met echt geld.

## Wat de agent elke werkdag doet

1. **Koersen ophalen** van ongeveer 50 grote aandelen en ETF's: VS (Apple, Nvidia, S&P 500-ETF, ...) en
   eurozone (ASML, SAP, LVMH, Shell, ...). Zie `src/trendagent/universe.py`.
2. **Trending bepalen** met vaste regels:
   - slotkoers boven het 50-daags gemiddelde, en dat boven het 200-daags gemiddelde;
   - positief rendement over 1 en 3 maanden;
   - genoeg handel (gemiddelde dagomzet minstens 20 miljoen);
   - geen verdachte dagsprong van meer dan 25% (pump-and-dump-filter).
   Daarna rangschikt hij op rendement gedeeld door beweeglijkheid: een rustige, stevige stijger wint van een wilde.
3. **Verkopen** als de stop-loss wordt geraakt of de koers onder het 50-daags gemiddelde zakt.
   Gaat een positie goed, dan schuift de stop mee omhoog.
4. **Kopen**: de sterkste trends, maximaal 3 posities tegelijk.
5. **Kosten meetellen**: 0,05% slippage plus 0,05% kosten (minimaal €1) per order.

## Ingebouwde remmen

| Rem | Standaard |
| --- | --- |
| Max verlies per trade (als de stop wordt geraakt) | 0,25% van het vermogen |
| Max opgeteld risico van alle posities | 1% |
| Max posities tegelijk | 3 |
| Max gewicht per positie | 25% |
| Dagverlies groter dan 1% | kill switch aan |
| Daling van 5% vanaf de top | kill switch aan |
| 3 verliestrades op rij | kill switch aan |
| Wisselkoers of te veel koersdata ontbreekt | die dag geen handel |

De kill switch gaat **alleen** weer uit als jij `resume` doet. Bijkopen in een verliezende positie,
short gaan en hefboom bestaan niet in de code.

Omdat het risico per trade klein is (0,25% van €10.000 = €25), koopt de agent vaak maar 1 of 2 aandelen
per positie, en slaat hij dure aandelen soms over. Dat is bewust: eerst leren, dan pas opschalen.

## Oefenen op GitHub (automatisch)

De workflow `.github/workflows/practice.yml` draait elke werkdag om 21:30 UTC, na het sluiten van de
Amerikaanse beurs. Je resultaten staan daarna in de map `state/`:

- `state/report.md`: het dagrapport (wat gekocht en verkocht, open posities, sterkste trends);
- `state/portfolio.json`: de nep-portefeuille;
- `state/audit.jsonl`: elke beslissing, beveiligd tegen achteraf wijzigen.

Daarnaast komt er elke ronde iets bij in de map **`rapporten/`**:

- `rapporten/2026-10-12.md` (één notitie per dag, blijft bewaard);
- `rapporten/trend-agent.xlsx`: één Excel-bestand dat elke dag wordt bijgewerkt, met de tabbladen
  Overzicht (waarde per dag), Posities, Trades, Trends en Uitleg.
  Downloaden: open het bestand op GitHub en klik op het download-icoon.

Zelf een ronde starten of de agent stoppen: tab **Actions**, kies **practice**, klik **Run workflow**
en kies `run`, `kill` of `resume`.

## Backtest: hoe had het de afgelopen jaren gewerkt?

`.github/workflows/backtest.yml` laat de agent de afgelopen 5 jaar opnieuw doorlopen op echte koersen,
dag voor dag, met dezelfde regels en kosten. Hij vergelijkt het resultaat met gewoon een MSCI World-ETF of
de S&P 500 vasthouden. De uitkomst staat in `backtest/resultaten/`: `RAPPORT.md`, `backtest.xlsx` en een grafiek.
Hij draait vanzelf als de code verandert, of handmatig via **Actions** → **backtest** → **Run workflow**.

Let op: de lijst instrumenten is vandaag gekozen, dus bedrijven die groot zijn geworden zitten erin
(survivorship bias). De echte uitkomst zou waarschijnlijk minder goed zijn geweest.

## Lokaal draaien

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

python -m trendagent run --simulated   # proefronde met verzonnen koersen
python -m trendagent run               # ronde met echte (gratis) koersen van Yahoo Finance
python -m trendagent status
python -m trendagent kill "even stoppen"
python -m trendagent resume
python -m trendagent backtest --simulated   # backtest-proef zonder internet
python -m trendagent invest --simulated     # investeerder-proef
python -m trendagent onderzoek --simulated  # onderzoek-proef (duurt een paar minuten)
python -m trendagent health                 # gezondheid van de laatste rondes
pytest -v
```

Instellingen staan in `.env.example`.

## Later: echt geld?

Pas na maanden oefenen met een stabiel resultaat dat beter is dan gewoon een wereldwijde ETF vasthouden.
Dan kan er een koppeling met een broker (bijvoorbeeld het paper-account van Interactive Brokers) worden
toegevoegd, met jouw goedkeuring per order. Broker-sleutels horen dan in GitHub Secrets of een `.env`-bestand,
nooit in de code.
