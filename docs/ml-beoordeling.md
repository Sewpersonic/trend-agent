# Machine learning en reinforcement learning: nu nog niet

## Conclusie

Voor deze bots is machine learning (ML) op dit moment **niet zinvol**, en reinforcement learning (RL) al helemaal niet.
De eenvoudige regels plus het meten van uitkomsten (`learning.py`, `evaluation.py`) leveren nu meer op, met veel minder risico.

## Waarom niet

- **Te weinig voorbeelden.** De trend-agent sluit in 5 jaar backtest zo'n 200 trades af, de investeerder herverdeelt
  ongeveer 60 keer. Een ML-model met een handvol kenmerken heeft er honderden tot duizenden nodig om iets betrouwbaars
  te leren. Met minder leert het vooral toeval (overfitting).
- **Markten veranderen.** Een patroon uit 2021-2023 kan in 2026 weg zijn. Hoe flexibeler het model, hoe beter het zich
  aan het verleden aanpast, en hoe slechter dat vaak in de toekomst uitpakt.
- **Uitleg.** Bij elke beslissing moet de bot kunnen zeggen waarom. Bij vaste regels lukt dat, bij de meeste ML-modellen veel minder.
- **RL** leert door te proberen. In een markt kun je niet miljoenen keren proberen, en een simulatie is nooit echt genoeg.
  RL is hier daarom ongeschikt.

## Wanneer het opnieuw beoordelen

Pas als alle drie de voorwaarden waar zijn:

1. Er zijn minstens 300 afgesloten trades met volledig journaal (omstandigheden bij in- en uitstap).
2. Het leerrapport toont een bevinding die in meerdere weken achter elkaar terugkomt (niet één keer).
3. Een eenvoudige regel op basis van die bevinding (via de evaluatie) is aantoonbaar beter, en er is reden om te
   denken dat een model meer haalt dan die regel.

## Als het zover is: de eerste stap

Geen model dat zelf koopt of verkoopt, maar een **filter**: een eenvoudige logistische regressie die op basis van het
journaal (RSI, MACD, regime, beweeglijkheid) schat of een signaal van de bestaande regels de moeite waard is. Dat model
moet dezelfde acceptatiepoort halen als elke andere variant: holdout, alle periodes, dubbele kosten.
