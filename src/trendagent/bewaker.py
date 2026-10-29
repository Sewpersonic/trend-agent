"""De bewaker: de hele beursdag (09:00-22:00 Nederlandse tijd) elk kwartier de stop-losses bewaken.

De trend-agent beslist 's nachts op slotkoersen. Zakt een aandeel overdag onder zijn stop-loss, dan verkoopt hij dat
in zijn eigen boekhouding 's nachts tegen de stopprijs. Maar het oefenaccount bij Trading 212 verkocht pas de volgende
ochtend, vaak tegen een slechtere prijs. De bewaker kijkt daarom de hele dag mee, zoals een handelaar:

  - per aandeel van de trend-agent dat ook in het oefenaccount staat: de koers bij Trading 212 én bij Yahoo;
  - twee bronnen: beide koersen moeten het eens zijn (hooguit 2% verschil), anders doet hij niets (geen trade op
    onbevestigde koersen);
  - staat de koers op of onder de stop-loss van de trend-agent: het oefenaccount verkoopt dat aandeel meteen.

Verder verandert hij niets: geen aankopen, geen andere verkopen, geen regels. Alleen het oefenaccount (nepgeld),
alleen als orders aan staan en de kill switch uit is.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

MAX_VERSCHIL = 0.02     # Trading 212 en Yahoo mogen hooguit zoveel verschillen
BESTAND = "bewaker.json"


def _load(p: Path, default):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def yahoo_koers(ticker: str) -> float | None:
    """Laatste koers bij Yahoo (5-minutenblokken van vandaag)."""
    try:
        import yfinance as yf
        df = yf.Ticker(ticker).history(period="1d", interval="5m", auto_adjust=False, prepost=False)
        return float(df["Close"].dropna().iloc[-1]) if not df.empty else None
    except Exception:  # noqa: BLE001 - geen koers = niets doen
        return None


def ronde(state_dir: Path, config_path: Path = Path("config/broker.json"), client=None, yahoo=yahoo_koers,
          nu: datetime | None = None) -> dict:
    """Eén controle. Schrijft state/bewaker.json en geeft het verslag terug."""
    from .broker_t212 import BrokerError, T212Demo, _tq
    from .core.kill_switch import KillSwitch
    nu = nu or datetime.now(timezone.utc)
    vorig = _load(state_dir / BESTAND, {})
    verslag = {"tijd": nu.isoformat(timespec="seconds"), "status": "ok", "posities": [], "verkocht": [], "log": []}
    log = verslag["log"]
    try:
        port = _load(state_dir / "portfolio.json", {}).get("positions", {})
        koppeling = _load(state_dir / "broker.json", {}).get("koppeling", {})
        cfg = _load(config_path, {})
        mag_orders = bool(cfg.get("orders_aan")) and not KillSwitch(state_dir / "kill_switch.json").is_active()
        client = client or T212Demo()
        posities = {}
        for p in client.positions():
            t, q = _tq(p, "positie")
            posities[t] = {"qty": q, "koers": p.get("currentPrice")}
        open_orders = {_tq(o, "order")[0] for o in client.open_orders()}
        for y, p in port.items():
            t = koppeling.get(y)
            stop = float(p.get("stop") or 0)
            rij = {"ticker": y, "t212": t, "stop": round(stop, 4), "actie": ""}
            verslag["posities"].append(rij)
            if not t or t not in posities or posities[t]["qty"] <= 0:
                rij["actie"] = "niet in het oefenaccount"
                continue
            k212 = posities[t]["koers"]
            ky = yahoo(y)
            rij.update(koers_t212=k212, koers_yahoo=None if ky is None else round(ky, 4))
            if k212 is None or ky is None:
                rij["actie"] = "geen tweede koers: niets gedaan"
                continue
            k212 = float(k212)
            if abs(k212 / ky - 1) > MAX_VERSCHIL:
                rij["actie"] = f"bronnen verschillen {abs(k212 / ky - 1):.1%}: niets gedaan"
                log.append(f"{y}: Trading 212 ({k212:.2f}) en Yahoo ({ky:.2f}) zijn het niet eens; voor de zekerheid niets gedaan.")
                continue
            koers = max(k212, ky)          # beide bronnen moeten onder de stop staan (bevestigd)
            rij["afstand_pct"] = round(koers / stop - 1, 4) if stop else None
            if stop <= 0 or koers > stop:
                rij["actie"] = "boven de stop-loss"
                continue
            if t in open_orders:
                rij["actie"] = "er staat al een order open"
                continue
            if not mag_orders:
                rij["actie"] = "onder de stop-loss, maar orders staan uit of de kill switch staat aan"
                log.append(f"{y}: koers {koers:.2f} onder de stop-loss {stop:.2f}; geen order (orders uit of kill switch).")
                continue
            qty = posities[t]["qty"]
            try:
                antwoord = client.market_order(t, -qty)
                rij["actie"] = f"verkocht ({qty:g} stuks): koers {koers:.2f} onder de stop-loss {stop:.2f}"
                verslag["verkocht"].append({"ticker": y, "t212": t, "aantal": qty, "koers": koers, "stop": stop,
                                            "antwoord": antwoord})
                log.append(f"{y}: verkocht in het oefenaccount, koers {koers:.2f} onder de stop-loss {stop:.2f}.")
            except BrokerError as e:
                rij["actie"] = f"verkopen mislukt: {e}"[:200]
                verslag["status"] = "deels mislukt"
                if e.onzeker:
                    log.append("Onzeker of de order aankwam; de volgende ronde kijkt eerst wat er echt staat.")
                    break
        if not log:
            dichtst = min((r for r in verslag["posities"] if r.get("afstand_pct") is not None),
                          key=lambda r: r["afstand_pct"], default=None)
            log.append("Alles boven de stop-loss." + (f" Dichtst bij: {dichtst['ticker']} ({dichtst['afstand_pct']:+.1%})."
                                                       if dichtst else ""))
    except Exception as e:  # noqa: BLE001 - nooit half handelen: fout vastleggen, niets meer doen
        verslag["status"] = "fout"
        log.append(f"Fout: {type(e).__name__}: {e}"[:300])
    hist = vorig.get("geschiedenis", [])
    if verslag["verkocht"] or verslag["status"] != "ok":
        hist.append({k: verslag[k] for k in ("tijd", "status", "verkocht", "log")})
    verslag["geschiedenis"] = hist[-60:]
    verslag["rondes_vandaag"] = (vorig.get("rondes_vandaag", 0) + 1
                                 if str(vorig.get("tijd", ""))[:10] == verslag["tijd"][:10] else 1)
    (state_dir / BESTAND).write_text(json.dumps(verslag, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return verslag


def sessie(state_dir: Path, *, nu=None, slaap=None, ronde_fn=None, na_ronde=None, elke_min: int = 15,
           eind_uur: int = 22, max_duur_min: int = 330) -> tuple[list[str], bool]:
    """Elk kwartier een ronde tot 22:00 Nederlandse tijd of tot de run te lang duurt.
    Geeft (regels, verder) terug: verder=True betekent dat een volgende run het moet overnemen."""
    import time as _time
    from datetime import timedelta
    from zoneinfo import ZoneInfo
    nl = ZoneInfo("Europe/Amsterdam")
    nu = nu or (lambda: datetime.now(timezone.utc))
    slaap = slaap or _time.sleep
    ronde_fn = ronde_fn or (lambda: ronde(state_dir))
    begin = nu()
    if begin.astimezone(nl).weekday() >= 5:
        return ["Weekend: de beurs is dicht."], False
    uit = []
    while True:
        t = nu().astimezone(nl)
        if t.hour >= eind_uur:
            return uit + ["Klaar voor vandaag."], False
        if (nu() - begin) >= timedelta(minutes=max_duur_min):
            return uit + ["Deze run stopt; een volgende neemt het over."], True
        if t.hour >= 9:
            v = ronde_fn()
            uit.append(f"{t:%H:%M} {v['status']}: " + "; ".join(v.get("log", [])[-2:]))
            if na_ronde:
                na_ronde(v)
        t = nu().astimezone(nl)
        volgende = (t + timedelta(minutes=elke_min - t.minute % elke_min)).replace(second=30, microsecond=0)
        if volgende.hour < 9:
            volgende = volgende.replace(hour=9, minute=0)
        slaap(max(5.0, (volgende - t).total_seconds()))
