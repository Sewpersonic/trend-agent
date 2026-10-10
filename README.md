# Trend-agent (oefenen met nepgeld)

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

Zelf een ronde starten of de agent stoppen: tab **Actions**, kies **practice**, klik **Run workflow**
en kies `run`, `kill` of `resume`.

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
pytest -v
```

Instellingen staan in `.env.example`.

## Later: echt geld?

Pas na maanden oefenen met een stabiel resultaat dat beter is dan gewoon een wereldwijde ETF vasthouden.
Dan kan er een koppeling met een broker (bijvoorbeeld het paper-account van Interactive Brokers) worden
toegevoegd, met jouw goedkeuring per order. Broker-sleutels horen dan in GitHub Secrets of een `.env`-bestand,
nooit in de code.
