"""De beursdag van de daytrader, zoals een mens die handelt: op tijd aanwezig en elk kwartier kijken.

Twee delen, elk één GitHub-run (een run mag hooguit 6 uur duren, een beursdag is 6,5 uur):
  koop    vóór de opening starten, wachten tot 10:00 (New York) en dan bij elk kijkmoment tot 12:30 een ronde:
          het enige moment waarop hij koopt, precies zoals in de test op oude koersen;
  middag  daarna elk kwartier zijn posities bewaken (stop-loss, winstdoel) tot hij om 15:45 alles verkoopt.
Het koopdeel start het middagdeel zelf als het klaar is.

Starten mag vroeg: komt de start (GitHub-schema of de uurtaak van Claude) tot ruim 3 uur vóór 10:00, dan wacht de run.
Een tweede start op dezelfde dag doet niets (er loopt al een sessie, of het deel is vandaag al gedaan).
De regels van de bot veranderen niet; dit bepaalt alleen wanneer hij kijkt. Alleen nepgeld.
"""

from __future__ import annotations

import time as _time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from .daytrader import NY, Params, check_times

WACHT_NA = timedelta(seconds=90)    # na een kijkmoment even wachten tot het laatste 5-minutenblok binnen is
VROEGST = timedelta(hours=3, minutes=15)   # zo lang mag een run vóór het eerste kijkmoment al wachten
MAX_DUUR = timedelta(hours=5, minutes=40)  # nooit langer (GitHub stopt een run na 6 uur)
DELEN = ("koop", "middag")


def _ny(t: datetime) -> datetime:
    return t.astimezone(NY).replace(tzinfo=None)


def momenten(dag: date, p: Params = Params(), deel: str = "koop") -> list[datetime]:
    """Rondetijden (New York). koop: elk kijkmoment tot het laatste moment om te kopen.
    middag: elk kijkmoment daarna tot en met het verkoopmoment (15:45)."""
    alle = check_times(dag, p)
    if deel == "koop":
        gekozen = [t for t in alle if t.time() <= p.entry_until]
    else:
        gekozen = [t for t in alle if p.entry_until < t.time() <= p.exit_at]
    return [t + WACHT_NA for t in gekozen]


def al_gedaan(st: dict, dag: date, p: Params, deel: str) -> bool:
    """Is dit deel vandaag al gedraaid (bijvoorbeeld door een eerdere start)?"""
    v = st.get("vandaag") or {}
    if v.get("dag") == dag.isoformat() and v.get("klaar"):
        return True
    laatste = momenten(dag, p, deel)[-1]
    tijden = [str(r.get("ny", "")) for r in st.get("rondes", [])]
    return any(x.startswith(dag.isoformat()) and x[11:16] >= laatste.strftime("%H:%M") for x in tijden)


def sessie(state_dir: Path, config_path: Path = Path("config/daytrader.json"), *, deel: str = "koop", nu=None,
           slaap=None, ronde=None, na_ronde=None, p: Params | None = None) -> list[str]:
    """Draait één deel van de beursdag. Geeft per ronde een korte regel terug.

    nu() -> datetime met tijdzone (standaard de echte tijd), slaap(seconden), ronde(state_dir, config_path, now) -> stand,
    na_ronde(stand) wordt na elke ronde aangeroepen (in GitHub: dashboardcijfers maken en opslaan).
    """
    from . import daytrade_live
    if deel not in DELEN:
        raise ValueError(f"onbekend deel: {deel}")
    nu = nu or (lambda: datetime.now(timezone.utc))
    slaap = slaap or _time.sleep
    ronde = ronde or (lambda sd, cp, now: daytrade_live.run(sd, cp, now=now))
    p = p or daytrade_live.params_from(daytrade_live.load(config_path))
    begin = nu()
    dag = _ny(begin).date()
    if dag.weekday() >= 5:
        return ["Weekend: geen sessie."]
    tijden = momenten(dag, p, deel)
    if al_gedaan(daytrade_live.load(state_dir / "daytrader.json"), dag, p, deel):
        return [f"Het {deel}deel is vandaag al gedaan: niets te doen."]
    if tijden[0] - _ny(begin) > VROEGST:
        return ["Te vroeg gestart: een latere start doet dit deel."]
    if _ny(begin) > tijden[-1] + timedelta(minutes=10):
        # Te laat gestart (bijvoorbeeld een uitgesteld GitHub-schema): één gewone ronde, dan stoppen.
        st = ronde(state_dir, config_path, nu())
        if na_ronde:
            na_ronde(st)
        return [f"Na het {deel}deel gestart: één gewone ronde gedaan."]
    uit: list[str] = []
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
