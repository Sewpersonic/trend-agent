"""Koopuren van de daytrader op tijd draaien: één GitHub-run die van 10:00 tot 12:30 (New York) bij elk kijkmoment
van de bot een ronde doet, precies zoals in de test op oude koersen (elk kwartier).

Waarom: het GitHub-schema komt vaak uren te laat en de uurlijkse rondes kwamen te laat voor een uitbraak (de bot mag
alleen kopen op het laatste kijkmoment). Verkopen is daar geen probleem: een latere ronde speelt alle gemiste
kijkmomenten na met de echte koersen (stop-loss, winstdoel, 15:45). Daarom draait deze sessie alleen de koopuren.

De regels van de bot veranderen niet; dit bepaalt alleen wanneer hij kijkt. Alleen nepgeld.
"""

from __future__ import annotations

import time as _time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from .daytrader import NY, Params, check_times

WACHT_NA = timedelta(seconds=90)   # na een kijkmoment even wachten tot het laatste 5-minutenblok binnen is
MAX_DUUR = timedelta(hours=4)      # nooit langer (GitHub stopt een run na 6 uur)


def _ny(t: datetime) -> datetime:
    return t.astimezone(NY).replace(tzinfo=None)


def momenten(dag: date, p: Params = Params()) -> list[datetime]:
    """Rondetijden (New York) voor de koopuren: elk kijkmoment tot en met het laatste moment om te kopen."""
    return [t + WACHT_NA for t in check_times(dag, p) if t.time() <= p.entry_until]


def sessie(state_dir: Path, config_path: Path = Path("config/daytrader.json"), *, nu=None, slaap=None,
           ronde=None, na_ronde=None, p: Params | None = None) -> list[str]:
    """Draait de rondes van de koopuren. Geeft per ronde een korte regel terug.

    nu() -> datetime met tijdzone (standaard de echte tijd), slaap(seconden), ronde(state_dir, config_path, now) -> stand,
    na_ronde(stand) wordt na elke ronde aangeroepen (in GitHub: dashboardcijfers maken en opslaan).
    """
    from . import daytrade_live
    nu = nu or (lambda: datetime.now(timezone.utc))
    slaap = slaap or _time.sleep
    ronde = ronde or (lambda sd, cp, now: daytrade_live.run(sd, cp, now=now))
    p = p or daytrade_live.params_from(daytrade_live.load(config_path))
    begin = nu()
    dag = _ny(begin).date()
    uit: list[str] = []
    if dag.weekday() >= 5:
        return ["Weekend: geen sessie."]
    tijden = momenten(dag, p)
    if _ny(begin) > tijden[-1] + timedelta(minutes=10):
        # Te laat gestart (bijvoorbeeld een uitgesteld GitHub-schema): één gewone ronde, dan stoppen.
        st = ronde(state_dir, config_path, nu())
        if na_ronde:
            na_ronde(st)
        return ["Na de koopuren gestart: één gewone ronde gedaan."]
    for t in tijden:
        nu_ny = _ny(nu())
        if nu_ny - t > timedelta(minutes=10):
            continue                      # dit kijkmoment is al voorbij; de volgende ronde speelt het na
        if nu() - begin > MAX_DUUR:
            uit.append("Gestopt: de sessie duurde te lang.")
            break
        if nu_ny < t:
            slaap((t - nu_ny).total_seconds())
        st = ronde(state_dir, config_path, nu())
        lr = st.get("laatste_ronde") or {}
        uit.append(f"{lr.get('ny', '')[11:]} {lr.get('status', '')}: " + "; ".join(lr.get("log", [])[-2:]))
        if na_ronde:
            na_ronde(st)
        if (st.get("vandaag") or {}).get("klaar") or lr.get("status", "").startswith("beurs dicht"):
            break
    return uit
