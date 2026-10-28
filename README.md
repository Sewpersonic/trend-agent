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
| **Daytrade-bot** | Koopt en verkoopt op dezelfde dag op de Amerikaanse beurs: alleen bij een sterke uitbraak in de ochtend, met stop-loss, daglimiet en hooguit 3 aankopen per dag. Verkoopt alles om 15:45 New Yorkse tijd. Eigen boekhouding, nog geen broker. | $10.000 nepgeld |
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
| **Onderzoek** | Bovenaan de conclusie van het wekelijkse onderzoek (huidige regels blijven, of: er staat een voorstel klaar). Dan wat €10.000 in 5 jaar werd voor beide bots en de wereld-ETF, wat goed is om te weten, en alle geteste regels met het verschil tegenover nu; tik op een regel voor de toetsen in gewone taal. |
| **Risico** | Bovenaan "Klaar voor echt geld?" per bot (ook het oefenaccount); het menu toont een stip (oranje = nog niet klaar, groen = klaar). Daarna verlies en risico per positie, de remmen en alle eisen. |
| **Controles** | Bovenaan in één woord hoe de laatste ronde ging (Alles in orde / In orde / Er ging iets mis). Per bot een vaste lijst vragen ("Zijn alle koersen binnengekomen?") met ✓ goed, ! let op, ✕ fout of i informatie, en een uitleg in gewone taal; tik op een vraag voor het technische detail. Daarnaast alle trades met reden. |
| **GitHub** | Welke runs op GitHub goed gingen en welke niet, en waarom, in gewone taal. |
| **Oefenaccount** | De stand bij Trading 212, of het gelijkloopt met de trend-agent, de orders, en knoppen om te kopen en verkopen. |
| **Daytrader** | De daytrade-bot: waarde, wat er nu open staat (met stop en doel), resultaat per beursdag, alle trades en wat hij in de laatste ronde deed. |
| **Systeem** | De systeemkaart: hoe de bots samenwerken (bronnen, starters, bots, onderzoek, opslag, jij) en de knelpunten van nu. Na elke run op GitHub opnieuw berekend uit de bestanden van de bots (`systeem.py`); klopt er iets niet, dan wordt het vanzelf een knelpunt met uitleg. |

Bijwerken: elke werkdag rond 07:41 alles, en tijdens beurstijden elk uur (rond :25) het oefenaccount en het
GitHub-overzicht. Dat doen twee geplande taken van Claude die de bestanden uit `dashboard/` naar de pagina
kopiëren. De pagina zelf staat in `dashboard/index.html`. Omdat het dashboard per bestand hooguit 256 KB
accepteert, gaat de pagina in delen online: `python scripts/pagina_splitsen.py` maakt `index.html`, `stijl.css` en
`app-01.js`, `app-02.js`, ... in `dashboard/pagina/` (die map staat niet in git).

## Wanneer gebeurt wat

| Wanneer (Nederlandse zomertijd; in de wintertijd een uur eerder) | Workflow | Wat |
| --- | --- | --- |
| Werkdagen ± 00:17 | `practice` | De ronde van beide bots met de slotkoersen van die dag, daarna het oefenaccount gelijkzetten, rapporten en dashboardcijfers maken, opslaan, en de gezondheidscontrole. |
| Werkdagen elk uur rond :25 | `broker` (gestart door een geplande taak van Claude) | Alleen kijken in het oefenaccount (geen orders) en de volglijst bijwerken, voor een verse stand op het dashboard. |
| Werkdagen, ruim vóór de opening (drie GitHub-starts plus de uurtaak van Claude) | `daytrade-sessie` | De beursdag van de daytrade-bot, zoals een mens die handelt: hij wacht tot 10:00 New Yorkse tijd en kijkt dan elk kwartier, tot 12:30 om te kopen (koopdeel) en daarna tot 15:45 om zijn posities te bewaken (middagdeel, door het koopdeel zelf gestart). Een te vroege start wacht; een dubbele start doet niets. |
| Werkdagen elk uur van 15:25 tot 22:25 (gestart door de uurlijkse taak van Claude; het schema van GitHub zelf komt vaak uren te laat) | `daytrade` | Eén ronde van de daytrade-bot: verkopen bewaken (gemiste kijkmomenten worden met de echte koersen nagespeeld). Loopt de sessie van de koopuren, dan slaat hij over. |
| Zaterdag ± 08:41 | `daytrade` | Onderzoek van de daytrade-bot: regels (ook uit de grafiekanalyse) opnieuw testen en lessen bijwerken. |
| Na elke run | `status` | Zet de lijst van de laatste GitHub-runs en open voorstellen klaar voor het dashboard. |
| Zaterdag ± 07:17 | `onderzoek` | Test varianten van de regels op 5 jaar koersen en zet een voorstel klaar als er een bewezen betere is. |
| Na elke codewijziging | `tests` | Alle tests en een controle op fouten in de code. |
| Als de regels van de bots veranderen | `backtest` | De backtest over 5 jaar. |
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

## De daytrade-bot

Oefent met $10.000 nepgeld op de Amerikaanse beurs (meestal 15:30-22:00 Nederlandse tijd) en houdt nooit iets 's nachts vast.

1. Het eerste half uur kijkt hij alleen: wat is de hoogste en laagste koers (de *openingsrange*)?
2. Daarna, tot 12:30 New Yorkse tijd, koopt hij een aandeel dat boven die hoogste koers uitbreekt, met veel meer handel dan normaal, boven de gemiddelde prijs van de dag (VWAP), terwijl de hele markt (SPY) boven de opening staat.
3. Stop-loss op de onderkant van de openingsrange (hooguit 2% lager), winstdoel twee keer het risico.
4. Om 15:45 verkoopt hij alles.

| Rem | Standaard |
| --- | --- |
| Risico per aankoop | 0,5% van het vermogen |
| Max gewicht per aandeel | 25% |
| Max aankopen per dag / tegelijk | 3 / 2 |
| Dagverlies 1,5% | die dag niets meer kopen |
| Koersen te oud of verdacht | niets kopen |
| Kill switch aan of `config/daytrader.json` "aan": false | alleen nog verkopen |

**Leren van de grafieken.** Elke ochtend bekijkt hij de daggrafiek van elk aandeel en van de markt, met dezelfde regels als de patronen van de trend-agent: trend (slot boven of onder het 50- en 200-daags gemiddelde), plek in het bereik van 3 maanden, terugval binnen een stijgende trend. Bij elke aankoop legt hij dat vast, samen met het tijdstip, de extra handel, de breedte van de openingsrange en of het aandeel met een gat opende (`daytrade_leren.py`). Het tabblad Daytrader laat per situatie zien hoe de trades uitpakten, en welke situaties duidelijk beter of slechter waren (alleen met genoeg trades). Elke zaterdag test het onderzoek ook regels uit de grafiekanalyse ("alleen als de daggrafiek stijgt", "niet als de markt daalt"). Werkt er een duidelijk beter, dan verschijnt een voorstel; aanzetten doe jij in `config/daytrader.json` onder `"regels"` (bijv. `{"dagtrend_filter": true}`). De bot past zijn regels nooit zelf aan, en de remmen zijn via dat bestand niet te versoepelen.

**Indicatie per kans (geen voorspelling).** Het onderzoek speelt ook álle uitbraken na die aan de koopregels voldeden, ook die de bot niet kocht (honderden voorbeelden: zo reageerde de markt, en dus andere handelaren, op zulke situaties). Die uitbraken worden bewaard (`backtest/daytrade/uitbraken.json`), dus de ervaring groeit elke week, ook al geeft Yahoo maar ~60 dagen 5-minutenkoersen. Per situatie (tijdstip, extra handel, daggrafiek, markt, ...) telt hij hoe vaak het goed afliep (`daytrade_indicatie.py`, `backtest/daytrade/indicatie.json`). Bij elke nieuwe kans geeft hij daaruit een label: gunstig, gemiddeld of ongunstig, met de cijfers erbij; je ziet het bij de open posities en trades. Of het label iets zegt wordt eerlijk getoetst: tabel uit de eerste 60% van de dagen, beoordeeld op de latere dagen die hij nooit zag. Ongunstige kansen overslaan staat uit; aanzetten doe jij met `{"indicatie_filter": true}` onder `"regels"`.

De regels zijn getest op de 5-minutenkoersen van de afgelopen ~60 beursdagen (`backtest/daytrade/RAPPORT.md`; opnieuw via Actions → daytrade → `test`). Dat is te kort om iets te bewijzen; daarom oefent hij eerst in zijn eigen boekhouding. Daarna kan hij naar een oefenaccount bij een broker (Alpaca paper trading). De test en het echte oefenen gebruiken dezelfde rekenkern (`daytrader.DayEngine`), zodat ze niet van elkaar kunnen afwijken.

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
- **Elke zaterdag** zoekt het onderzoek ook alle eerdere **koopsignalen** van de trend-agent op (elke keer dat een
  aandeel aan zijn koopregels voldeed, ook zonder vrije plek) en kijkt hoe die afliepen met zijn gewone stop-loss
  (`trend_indicatie.py`, `onderzoek/trend_indicatie.json`). Daaruit krijgt elke kans op het tabblad **Kansen** (en
  elk aandeel op de volglijst dat bij zijn regels past) een label: gunstig, gemiddeld of ongunstig. Het label wordt
  eerlijk getoetst (gemaakt uit de oudere jaren, gecontroleerd op de latere). Het is alleen informatie: de bot koopt
  hierdoor niet anders. Pas als de toets een duidelijk verschil laat zien, kan het een regel worden, en alleen met
  jouw ja. Het oefenaccount volgt de trend-agent en krijgt zo dezelfde labels.
- **Elke zaterdag** test het onderzoek ook of de trend-agent beter werkt met **4 of 5 plekken** in plaats van 3
  (zelfde risico per aankoop). Nu staat het meeste geld stil zodra 3 plekken bezet zijn. Alleen als dat bewezen
  beter is, komt er een voorstel; jij beslist.
- **5-minutenkoersen bewaren:** het daytrade-onderzoek slaat elke week de 5-minutenkoersen op
  (`backtest/daytrade/koersen/`, één bestand per week). Yahoo geeft er maar ~60 dagen van; met het archief kijkt
  het onderzoek steeds verder terug (tot 250 beursdagen).
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
python -m trendagent daytrade               # één ronde van de daytrade-bot (doet buiten beurstijd niets)
python -m trendagent daytrade-test          # daytrade-regels testen op 5-minutenkoersen (~60 beursdagen)
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
