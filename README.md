# Trend-agent en investeerder (oefenen met nepgeld)

Twee bots die beleggen met **nepgeld**, plus een **oefenaccount bij Trading 212** (ook nepgeld) dat de
trend-agent volgt. Alles draait vanzelf op GitHub; de uitkomst zie je op het online dashboard, in Excel en in
dagnotities.

> Geen beleggingsadvies. Resultaten op papier en in een oefenaccount zeggen niets over toekomstige resultaten
> met echt geld.

| | Wat | Startbedrag |
| --- | --- | --- |
| **Investeerder** | Lange termijn: 60% wereldwijde ETF, 30% de 5 sterkste aandelen/ETF's van het afgelopen jaar, 10% Bitcoin/Ethereum (alleen in een stijgende trend). Herverdeelt één keer per maand. | €10.000 nepgeld |
| **Trend-agent** | Korte trends in grote Europese en Amerikaanse aandelen, maximaal 3 posities, met een stop-loss op elke positie en een heel klein risico per trade. | €10.000 nepgeld |
| **Oefenaccount** | Het demo-account van Trading 212. Volgt elke aankoop en verkoop van de trend-agent bij een echte broker. Je kunt er ook zelf kopen en verkopen. | €5.000 nepgeld (van Trading 212) |

**Onderzoek over 5 jaar** (okt 2021 – okt 2026, €10.000, na kosten, gemeten op 15 okt 2026):
investeerder €25.201, gewoon de wereld-ETF vasthouden €17.613, trend-agent €10.666.
De aandelenlijst is achteraf gekozen (bedrijven die groot zijn geworden zitten erin), dus de echte uitkomst zou
waarschijnlijk minder goed zijn geweest.

## Het dashboard

Het dashboard is een privé webpagina op claude.ai (in de zijbalk vastgezet). Het werkt op de computer en op de
telefoon (daar met een menu linksboven en een opbouw zoals een beurs-app).

| Tabblad | Wat je ziet |
| --- | --- |
| **Overzicht** | *Begin hier*: per bot wat hij nu doet, wat hij als laatste deed en wat er straks gebeurt. Dan *Klaar voor echt geld?*: per bot een ring met de oefentijd, hoeveel eisen gehaald zijn en wanneer hij op zijn vroegst klaar kan zijn. Daaronder de drie kaarten (investeerder, trend-agent, oefenaccount), wat de grafieken vandaag laten zien, een koersgrafiek per aandeel en de laatste trades. |
| **Weekoverzicht** | Per week: wat de bots kochten en verkochten (met reden), het resultaat tegenover de wereld-ETF, en *Wat heeft hij geleerd?* in gewone zinnen (afgesloten trades, onderzoek, patronen uit oude trades). |
| **Grafieken** | Kaarsgrafieken per aandeel (rustige trendkaarsen of gewone kaarsen). |
| **Patronen** | Per aandeel de trend, week/maand/3 maanden en opvallende patronen. Beschrijft alleen, voorspelt niets. |
| **Kansen** | De sterkste trends, met een stoplicht voor het instapmoment en wat de bot zou doen. Daaronder de **volglijst**: extra beleggingen die alleen bekeken worden (trend, rendement, of de trend-agent ze zou kopen, of ze bij Trading 212 te koop zijn). |
| **Analyse** | Wat de bots in de markt zagen en wat ze eruit concluderen. |
| **Onderzoek** | Het wekelijkse onderzoek: wat €10.000 na 5 jaar werd en welke nieuwe regels zijn getest. Staat er een voorstel klaar, dan zie je dat hier bovenaan. |
| **Risico** | Bovenaan "Klaar voor echt geld?" per bot (ook het oefenaccount); het menu toont een stip (oranje = nog niet klaar, groen = klaar). Daarna verlies en risico per positie, de remmen en alle eisen. |
| **Controles** | Koersbronnen, waarschuwingen en alle trades met reden. |
| **GitHub** | Welke runs op GitHub goed gingen en welke niet, en waarom, in gewone taal. |
| **Oefenaccount** | De stand bij Trading 212, of het gelijkloopt met de trend-agent, de orders, en knoppen om te kopen en verkopen. |

Bijwerken: elke werkdag rond 07:41 alles, en tijdens beurstijden elk uur (rond :25) het oefenaccount en het
GitHub-overzicht. Dat doen twee geplande taken van Claude die de bestanden uit `dashboard/` naar de pagina
kopiëren. De pagina zelf staat in `dashboard/index.html`.

## Wanneer gebeurt wat

| Wanneer (Nederlandse zomertijd; in de wintertijd een uur eerder) | Workflow | Wat |
| --- | --- | --- |
| Werkdagen ± 00:17 | `practice` | De ronde van beide bots met de slotkoersen van die dag, daarna het oefenaccount gelijkzetten, rapporten en dashboardcijfers maken, opslaan, en de gezondheidscontrole. |
| Werkdagen elk uur rond :25 | `broker` (gestart door een geplande taak van Claude) | Alleen kijken in het oefenaccount (geen orders) en de volglijst bijwerken, voor een verse stand op het dashboard. |
| Na elke run | `status` | Zet de lijst van de laatste GitHub-runs en open voorstellen klaar voor het dashboard. |
| Zaterdag ± 07:17 | `onderzoek` | Test varianten van de regels op 5 jaar koersen en zet een voorstel klaar als er een bewezen betere is. |
| Na elke codewijziging | `tests`, `backtest` | Alle tests, en de backtest over 5 jaar. |
| Met de hand | `diagnose` | Test of de koersbron werkt. |

Een run die misgaat wordt rood en GitHub mailt je. Op het dashboard (tabblad **GitHub**) staat in gewone taal
wat er misging en of een latere run het weer goed deed.

## De trend-agent

1. **Koersen ophalen** van ongeveer 50 grote aandelen en ETF's in Amerika en Europa (zie
   `src/trendagent/universe.py`), bij twee bronnen (zie *Koersen*).
2. **Trending bepalen** met vaste regels: slot boven het 50-daags gemiddelde en dat boven het 200-daagse,
   gestegen over 1 en 3 maanden, genoeg handel, geen verdachte sprong. Rangschikken op rendement gedeeld door
   beweeglijkheid.
3. **Verkopen** als de stop-loss wordt geraakt of de koers onder het 50-daags gemiddelde zakt. Gaat het goed,
   dan schuift de stop mee omhoog.
4. **Kopen**: de sterkste trends, maximaal 3 posities.
5. **Kosten meetellen**: 0,05% slippage plus 0,05% kosten (minimaal €1) per order.

### Ingebouwde remmen

| Rem | Standaard |
| --- | --- |
| Max verlies per trade (als de stop wordt geraakt) | 0,25% van het vermogen (± €25) |
| Max opgeteld risico van alle posities | 1% |
| Max posities tegelijk | 3 |
| Max gewicht per positie | 25% |
| Dagverlies groter dan 1% | kill switch aan |
| Daling van 5% vanaf de top | kill switch aan |
| 3 verliestrades op rij | kill switch aan |
| Wisselkoers of te veel koersdata ontbreekt | die dag geen handel |

De kill switch gaat **alleen** weer uit als jij `resume` doet. Bijkopen in een verliezende positie, short gaan en
hefboom bestaan niet in de code.

## Koersen uit meerdere bronnen

De bot haalt de koersen bij **Yahoo Finance** en controleert ze bij **Stooq**; de euro/dollar-koers controleert
hij bij de **Europese Centrale Bank**.

- Wijken de bronnen meer dan 2% af, dan koopt hij dat aandeel die dag niet.
- **Geen trade op een koers die niet klopt:** spreken de bronnen elkaar tegen of loopt de koers achter, dan
  verkoopt of herverdeelt hij die belegging ook niet, hooguit 3 handelsdagen achter elkaar. Daarna gaat de
  stop-loss weer voor, want verlies beperken wint.
- Wijkt de wisselkoers meer dan 1% af, dan handelt hij die dag helemaal niet.
- Yahoo publiceert slotkoersen soms laat; een ontbrekende dag wordt aangevuld uit uurkoersen, en een half
  afgemaakte dag (tijdens de handel) wordt genegeerd.

## Het oefenaccount bij Trading 212

Het oefenaccount is het **demo-account** (Invest) van Trading 212: een echte broker, maar met nepgeld.

**Hoe het werkt**
- Na elke ronde zet de bot het oefenaccount gelijk met wat de trend-agent volgens zijn eigen boekhouding bezit:
  hij koopt wat ontbreekt en verkoopt wat de trend-agent niet meer heeft. Verkopen gaan voor kopen.
- Orders die buiten beurstijd worden geplaatst, voert Trading 212 uit zodra de beurs opengaat. Zolang een order
  nog open staat, plaatst de bot voor dat aandeel niets nieuws (geen dubbele aankopen). Wil de bot het aandeel
  niet meer, dan trekt hij de openstaande koop in.
- Crypto kan niet in het Invest-account; Bitcoin/Ethereum en de investeerder blijven daarom alleen op papier.

**Veiligheid (vast in de code, `src/trendagent/broker_t212.py`)**
- Alleen het demo-adres `https://demo.trading212.com` werkt; het echte account weigert de code.
- Alleen als `PAPER_TRADING=true`.
- Nooit short: verkopen alleen wat echt in het account staat. Geen hefboom.
- Hooguit 6 orders per ronde en hooguit €3.000 per order.
- Staat de kill switch aan, dan plaatst hij niets (handmatig verkopen mag wel).
- Krijgt hij een onduidelijk antwoord van Trading 212 (time-out, storing), dan stopt hij die ronde; de volgende
  ronde kijkt eerst wat er echt in het account staat.
- Onverwacht antwoord of fout: niets doen, de reden staat in `state/broker.json` en de run wordt rood.

**Bedienen** (tab **Actions** → **broker** → **Run workflow**, of via de knoppen op het dashboard)

| Keuze | Wat er gebeurt |
| --- | --- |
| `kijken` | Verbinding testen en de stand ophalen. Geen orders. |
| `orders uit` / `orders aan` | Het gelijkzetten uit- of aanzetten (`config/broker.json`). Uit = alleen kijken. |
| `nu gelijkzetten` | Nu meteen gelijkzetten in plaats van 's nachts. |
| `handmatig kopen` / `handmatig verkopen` | Zelf een order geven: vul ook **aandeel** (bijv. ASML, Shell, MSFT) en **aantal** in. Alleen aandelen die de bots kennen of die op de volglijst staan, hooguit €3.000. De bot draait je handmatige order niet terug. |

**Sleutels:** de API-sleutel staat alleen in GitHub Secrets (`T212_DEMO_KEY` en `T212_DEMO_SECRET`), nooit in
de code, de chat of het dashboard. De sleutel heeft alleen de rechten Account data, History - Orders,
Metadata, Orders - Execute, Orders - Read en Portfolio.

## Hoe de bots leren

- **Elke ronde** leggen de bots elke trade vast met reden, marktregime, indicatoren en strategieversie.
- **Elke zaterdag** test het onderzoek varianten van de regels (ook patronen uit de grafieken, zoals "koop na een
  terugval" of "verkoop na 2 rode trendkaarsen") tegen de huidige regels: op 5 jaar koersen, met een ongezien
  deel, 5 periodes, dubbele kosten en per marktregime. Rapport: `onderzoek/LAATSTE.md`.
- **Elke week** zet het dashboard (tabblad **Weekoverzicht**) op een rij wat de bots kochten en verkochten en wat
  ze ervan leerden, zodat je per week kunt nalezen welke orders er waren en waarom.
- **Jij beslist.** Haalt een variant alle toetsen, dan zet het onderzoek een **voorstel** (pull request) klaar
  dat alleen `config/productie.json` wijzigt. Je ziet het op het dashboard en krijgt een e-mail. **Merge** =
  overnemen, **Close** = laten zoals het is. Na een merge gebruikt de trend-agent de nieuwe regel en volgt het
  oefenaccount vanzelf.

## De volglijst (alleen kijken)

In `config/volglijst.json` staan extra aandelen en fondsen (Walmart, Coca-Cola, Philips, Unilever, Sanofi,
een S&P 500-ETF in euro, obligaties en meer). Elke werkdag en elk uur bij het kijken in het oefenaccount bekijkt
`python -m trendagent volglijst` ze: koers, rendement over een week, maand en 3 maanden, de trend, of de
trend-agent ze volgens zijn eigen regels zou kopen, en of ze bij Trading 212 te koop zijn (uit de
instrumentenlijst van het oefenaccount). De bots kopen ze **nooit vanzelf**. Wil je er een in het oefenaccount,
gebruik dan de knop Kopen. De koersen komen van Yahoo, omdat Trading 212 geen koersgeschiedenis geeft. Je mag de
lijst zelf aanpassen.

## Rapporten

- `rapporten/dagrapport.xlsx`: één Excel-bestand, elke dag bijgewerkt, met Overzicht, Grafieken (kaarsgrafieken),
  Patronen, Analyse, Verlies en risico, Kansen, Klaar voor echt geld, Waarde per dag, Trades, Controles en Uitleg.
- `rapporten/OVERZICHT.md`: het dagoverzicht van beide bots.
- `rapporten/JJJJ-MM-DD.md`: een notitie per dag; grafieken in `rapporten/grafieken/`.
- `state/`: de nep-portefeuilles, het auditlog (`audit.jsonl`), de gezondheid en het oefenaccount (`broker.json`).
- `backtest/` en `onderzoek/`: de uitkomsten van de backtest en het wekelijkse onderzoek.

## Lokaal draaien

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

python -m trendagent run --simulated        # proefronde trend-agent met verzonnen koersen
python -m trendagent run                    # ronde met echte (gratis) koersen
python -m trendagent invest                 # ronde van de investeerder
python -m trendagent overzicht              # dagoverzicht en dagrapport.xlsx
python -m trendagent dashboard              # cijfers voor het dashboard (map dashboard/)
python -m trendagent health                 # gezondheid van de laatste rondes
python -m trendagent volglijst              # volglijst bekijken (alleen kijken, nooit kopen)
python -m trendagent kill "even stoppen"    # kill switch aan
python -m trendagent resume                 # kill switch uit (alleen jij)
python -m trendagent backtest --simulated   # backtest-proef zonder internet
python -m trendagent onderzoek --simulated  # onderzoek-proef (duurt een paar minuten)

# Oefenaccount (alleen met T212_DEMO_KEY en T212_DEMO_SECRET in je omgeving)
python -m trendagent broker --check                                       # alleen kijken
python -m trendagent broker                                               # gelijkzetten
python -m trendagent broker --handmatig koop --aandeel ASML --aantal 1    # handmatige order

PYTHONPATH=src python -m unittest discover -s tests -t .   # alle tests
```

Instellingen staan in `.env.example` en `config/`. Alle workflows slaan hun resultaat op via
`scripts/opslaan.sh`, dat een botsing met een andere workflow netjes oplost en de run rood maakt als opslaan
niet lukt.

## Later: echt geld?

Op het dashboard (tabblad **Risico** → *Klaar voor echt geld?*) staan de eisen: minstens 3 maanden oefenen,
minstens zo goed als de wereld-ETF, beperkte daling, genoeg trades met gemiddeld winst. Pas als alles groen is
én het oefenaccount maanden betrouwbaar meeloopt, is een volgende stap zinvol: een klein bedrag, met **jouw
goedkeuring per order**. Die beslissing neem jij, niet de bot. Tot die tijd bestaat er geen code die met echt
geld handelt.
