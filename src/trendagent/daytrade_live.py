"""De daytrade-bot echt laten oefenen (alleen nepgeld, eigen boekhouding in dollars).

Draait elk kwartier tijdens de Amerikaanse beurs (GitHub Actions). Elke ronde:
1. Is de beurs open? Zo niet: niets doen (alleen een eerder open gebleven dag afsluiten).
2. Koersen per 5 minuten ophalen (Yahoo) en controleren: vers genoeg, geen rare sprongen.
   Klopt iets niet, dan koopt hij niets (NO TRADE op onbevestigde data); verkopen om risico te beperken mag wel.
3. De kijkmomenten sinds de vorige ronde afwerken met dezelfde rekenkern als de test (daytrader.DayEngine).
   Een gemist kijkmoment (GitHub te laat) telt alleen voor stop-loss, winstdoel en einde van de dag, nooit voor kopen.
4. Om 15:45 New Yorkse tijd alles verkopen. Nooit iets mee de nacht in.

Kill switch aan of config/daytrader.json "aan": false: niets kopen (wat open staat wordt nog wel netjes verkocht).
Schrijft state/daytrader.json (stand + geschiedenis) en state/daytrader_audit.jsonl (wat hij deed en waarom).
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

from .daytrader import (
    CLOSE,
    NY,
    OPEN,
    Bar5,
    DayEngine,
    Params,
    avg_or_volumes,
    check_times,
    split_days,
)

START = 10_000.0
MAX_JUMP = 0.15          # een sprong van meer dan 15% tussen twee blokken van 5 minuten = verdacht
MAX_STALE_MIN = 20       # laatste blok van de markt (SPY) mag hooguit zo oud zijn


def tickers() -> list[str]:
    from .universe import UNIVERSE
    return [i.ticker for i in UNIVERSE if i.region == "US"]


def fetch(tks: list[str], period: str) -> dict[str, list[Bar5]]:
    """Alle koersen in één verzoek (minder kans op blokkeren door Yahoo)."""
    import yfinance as yf
    df = yf.download(tks, period=period, interval="5m", group_by="ticker", prepost=False, auto_adjust=False,
                     threads=True, progress=False)
    out: dict[str, list[Bar5]] = {}
    if df is None or df.empty:
        return out
    for tk in tks:
        try:
            sub = df[tk]
        except KeyError:
            continue
        bars = []
        for idx, r in sub.iterrows():
            if r["Close"] != r["Close"]:
                continue
            t = idx.to_pydatetime()
            t = t.astimezone(NY) if t.tzinfo is not None else t
            bars.append(Bar5(t, float(r["Open"]), float(r["High"]), float(r["Low"]), float(r["Close"]), float(r["Volume"])))
        if bars:
            out[tk] = bars
    return out


def fetch_daily(tks: list[str]) -> dict:
    """Dagkoersen van ongeveer een jaar (voor de daggrafiek), in één verzoek."""
    import yfinance as yf

    from .data import Bar
    df = yf.download(tks, period="1y", interval="1d", group_by="ticker", auto_adjust=True, threads=True, progress=False)
    out: dict = {}
    if df is None or df.empty:
        return out
    for tk in tks:
        try:
            sub = df[tk]
        except KeyError:
            continue
        bars = [Bar(idx.date(), float(r["Open"]), float(r["High"]), float(r["Low"]), float(r["Close"]), float(r["Volume"]))
                for idx, r in sub.iterrows() if r["Close"] == r["Close"]]
        if bars:
            out[tk] = bars
    return out


# Regels die jij in config/daytrader.json onder "regels" mag aan- of uitzetten (na het onderzoek). Alles erbuiten
# wordt genegeerd: de remmen (risico, daglimiet, aantal trades) zijn niet via dit bestand te versoepelen.
REGELS = {"dagtrend_filter": bool, "markt_trend_filter": bool, "indicatie_filter": bool, "kopen_tot_11": bool}


def params_from(cfg: dict, base: Params = Params()) -> Params:
    """Regels die de gebruiker aanzet in config/daytrader.json onder "regels" (alleen deze, alleen true/false)."""
    from dataclasses import replace
    kies = {k: bool(v) for k, v in (cfg.get("regels") or {}).items() if k in REGELS and isinstance(v, bool)}
    if kies.pop("kopen_tot_11", False):
        kies["entry_until"] = time(11, 0)    # alleen kopen tot 11:00 New Yorkse tijd (uit het onderzoek)
    return replace(base, **kies) if kies else base


def beoordelaar(pad: Path):
    """Functie die bij een kans de indicatie geeft (uit het laatste onderzoek), of None als die er nog niet is."""
    from .daytrade_indicatie import indicatie
    t = load(pad).get("tabel")
    if not t:
        return None
    return lambda ctx: indicatie(ctx, t)


def suspicious(bars: list[Bar5]) -> str | None:
    for a, b in zip(bars, bars[1:]):
        if min(b.o, b.h, b.l, b.c) <= 0:
            return "koers van 0 of lager"
        if abs(b.c / a.c - 1) > MAX_JUMP:
            return f"sprong van {b.c / a.c - 1:+.0%} binnen 5 minuten"
    return None


def _naive(t: datetime) -> datetime:
    return t.replace(tzinfo=None)


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def run(state_dir: Path, config_path: Path = Path("config/daytrader.json"), now: datetime | None = None,
        provider=None, p: Params | None = None, daily_provider=None,
        indicatie_pad: Path = Path("backtest/daytrade/indicatie.json")) -> dict:
    """Eén ronde. provider(tickers, period) -> {ticker: [Bar5]} (standaard Yahoo; in tests verzonnen koersen).
    daily_provider(tickers) -> {ticker: [Bar]}: dagkoersen voor de daggrafiek (één keer per dag)."""
    from .core.kill_switch import KillSwitch
    path = state_dir / "daytrader.json"
    st = load(path) or {"start": START, "equity": START, "dagen": [], "trades": [], "vandaag": None}
    cfg = load(config_path)
    p = p or params_from(cfg)
    aan = cfg.get("aan", True)
    kill = KillSwitch(state_dir / "kill_switch.json").is_active()
    now = now or datetime.now(timezone.utc)
    ny = _naive(now.astimezone(NY)) if NY else now
    today = ny.date()
    if daily_provider is None:
        daily_provider = fetch_daily if provider is None else (lambda _tks: {})
    provider = provider or fetch
    log: list[str] = []
    ronde = {"tijd": now.isoformat(timespec="seconds"), "ny": ny.strftime("%Y-%m-%d %H:%M"), "status": "ok", "log": log}

    try:
        v = st.get("vandaag")
        in_session = today.weekday() < 5 and OPEN <= ny.time() < time_plus(CLOSE, 30)
        # Een dag die nog openstaat afsluiten: een eerdere dag, of vandaag als de beurs al dicht is
        # (bijvoorbeeld omdat de laatste ronde van GitHub pas na sluitingstijd kwam).
        open_day = bool(v and not v.get("klaar") and (v.get("dag") != today.isoformat()
                                                      or ny.time() >= time_plus(CLOSE, 30)))
        if not open_day and not in_session:
            ronde["status"] = "beurs dicht"
            return _save(path, st, ronde)
        vandaag_klaar = v and v.get("dag") == today.isoformat() and v.get("klaar")
        eerste = check_times(today, p)[0]
        if not open_day and (vandaag_klaar or ny < eerste + timedelta(minutes=1)):
            ronde["status"] = "klaar voor vandaag" if vandaag_klaar else "wacht op de openingsrange"
            return _save(path, st, ronde)

        need_avg = not (v and v.get("dag") == today.isoformat() and st.get("gem_vol"))
        data = provider(tickers(), "15d" if (need_avg or open_day) else "1d")
        per = {tk: split_days(bs) for tk, bs in data.items()}

        # Een vorige dag die nog openstond (rondes gemist): afsluiten met de koersen van die dag.
        if open_day:
            d = date.fromisoformat(v["dag"])
            e = DayEngine.from_dict(v, p)
            bars_d = {tk: x[d] for tk, x in per.items() if d in x}
            for t in [t for t in check_times(d, p) if not e.prev or t > e.prev]:
                log += e.step(t, bars_d, {}, allow_entries=False)
                if e.klaar:
                    break
            for tk in list(e.open):
                e._close(e.open[tk], e.open[tk].entry, datetime.combine(d, CLOSE), "einde van de dag (geen koers)")
            e.klaar = True
            _finish_day(st, e)
            log.append(f"{d}: dag afgesloten (de laatste ronde kwam na sluitingstijd)")
            st["vandaag"] = {**e.to_dict(), "klaar": True}
            if not in_session:
                return _save(path, st, ronde)

        bars = {tk: x[today] for tk, x in per.items() if today in x}
        if p.market not in bars:
            ronde["status"] = "beurs dicht"   # feestdag: geen koersen van vandaag
            log.append("Geen koersen van vandaag: de beurs is dicht (feestdag) of Yahoo heeft nog niets.")
            return _save(path, st, ronde)

        # Nieuwe dag?
        if not st.get("vandaag") or st["vandaag"].get("dag") != today.isoformat():
            st["vandaag"] = DayEngine(today, float(st["equity"]), p).to_dict()
            st["gem_vol"] = avg_or_volumes(per, today, p)
            st["uitgesloten"] = {}
            # Daggrafiek van elk aandeel (zelfde regels als de patronen van de trend-agent), één keer per dag.
            from .daytrade_leren import dag_context
            try:
                st["dagcontext"] = dag_context(daily_provider(tickers()), today)
            except Exception as exc:  # noqa: BLE001 - zonder daggrafiek handelt hij gewoon, maar leert hij minder
                st["dagcontext"] = {}
                log.append(f"Daggrafieken niet opgehaald ({type(exc).__name__}); vandaag zonder grafiekanalyse.")
            if (p.dagtrend_filter or p.markt_trend_filter) and not st["dagcontext"]:
                log.append("Regel uit de grafiekanalyse staat aan, maar de daggrafieken ontbreken: vandaag niets kopen.")
                st["geen_context"] = True
            else:
                st["geen_context"] = False
        e = DayEngine.from_dict(st["vandaag"], p)
        avg = st.get("gem_vol") or {}

        # Controle van de koersen (NO TRADE op onbevestigde data).
        uitgesloten = dict(st.get("uitgesloten") or {})
        for tk, bs in bars.items():
            why = suspicious(bs)
            if why and tk not in uitgesloten:
                uitgesloten[tk] = why
                log.append(f"{tk}: vandaag niet kopen ({why})")
        st["uitgesloten"] = uitgesloten
        mkt_last = _naive(bars[p.market][-1].t)
        vers = (ny - mkt_last) <= timedelta(minutes=MAX_STALE_MIN)
        if not vers:
            log.append(f"Koersen niet vers (laatste blok {mkt_last:%H:%M}): niets kopen deze ronde.")

        due = [t for t in check_times(today, p) if t <= ny - timedelta(minutes=1) and (not e.prev or t > e.prev)]
        live_bars = {tk: bs for tk, bs in bars.items() if tk not in uitgesloten or tk in e.open}

        def live_price(tk, _t):
            bs = bars.get(tk) or []
            return bs[-1].c if bs else None

        beoordeel = beoordelaar(indicatie_pad)
        for i, t in enumerate(due):
            laatste = i == len(due) - 1
            mag_kopen = (laatste and aan and not kill and vers and (ny - t) <= timedelta(minutes=14)
                         and not st.get("geen_context"))
            stap = e.step(t, live_bars if mag_kopen else bars, avg, fill_at=live_price if laatste else None,
                          allow_entries=mag_kopen, context=st.get("dagcontext") or {}, beoordeel=beoordeel)
            log += [f"{t:%H:%M} {x}" for x in stap]
            if e.klaar:
                break
        # Vroege sluiting (bijvoorbeeld de dag na Thanksgiving en kerstavond: de beurs sluit om 13:00):
        # komen er na 13:00 al 20 minuten geen nieuwe koersen meer, dan alles verkopen tegen de laatste koers.
        if not e.klaar and e.open and ny.time() >= time(13, 5) and mkt_last.time() < time(15, 0) \
                and ny - mkt_last > timedelta(minutes=20):
            for tk in list(e.open):
                prijs = live_price(tk, ny) or e.open[tk].entry
                e._close(e.open[tk], prijs, ny, "beurs vroeg dicht")
                log.append(f"{tk}: verkocht (de beurs sloot vandaag vroeg)")
            e.klaar = True
        if due and not any("gekocht" in x for x in log):
            t_last = due[-1]
            if e.klaar:
                pass
            elif kill or not aan:
                log.append("Niets gekocht: de bot mag nu alleen verkopen.")
            elif t_last.time() > p.entry_until:
                log.append(f"Na {p.entry_until:%H:%M} (New York) koopt hij niets meer; wat open staat volgt hij tot {p.exit_at:%H:%M}.")
            elif len(e.res.trades) + len(e.open) >= p.max_trades:
                log.append(f"Vandaag al {p.max_trades} aankopen gedaan: het maximum.")
            elif vers:
                top = sorted(e.redenen.items(), key=lambda x: -x[1])[:3]
                waarom = "; ".join(f"{k} ({n}x)" for k, n in top)
                log.append("Bekeken: geen aandeel voldeed nu aan alle regels." + (f" Meestal: {waarom}." if waarom else ""))
        if kill:
            ronde["status"] = "alleen verkopen (kill switch aan)"
        elif not aan:
            ronde["status"] = "alleen verkopen (bot staat uit)"
        if e.klaar:
            _finish_day(st, e)
            st["vandaag"] = {**e.to_dict(), "klaar": True}
            log.append(f"Dag klaar: {len(e.res.trades)} trades, resultaat {e.realized:+.2f} dollar.")
        else:
            st["vandaag"] = e.to_dict()
        # Huidige waarde van open posities (voor het dashboard).
        st["open_nu"] = [{**{k: v for k, v in asdict(x).items() if k != "t_in"}, "t_in": x.t_in.strftime("%H:%M"),
                          "koers": (bars.get(x.ticker) or [None])[-1].c if bars.get(x.ticker) else None}
                         for x in e.open.values()]
    except Exception as exc:  # noqa: BLE001 - nooit half handelen: fout vastleggen, niets meer doen
        ronde["status"] = "fout"
        log.append(f"Fout: {type(exc).__name__}: {exc}"[:300])
    return _save(path, st, ronde)


def time_plus(t, minutes: int):
    return (datetime.combine(date(2000, 1, 1), t) + timedelta(minutes=minutes)).time()


def _finish_day(st: dict, e: DayEngine) -> None:
    if any(d.get("dag") == e.res.dag for d in st["dagen"]):
        return
    st["equity"] = round(float(st["equity"]) + e.realized, 2)
    st["dagen"].append({"dag": e.res.dag, "begin": round(e.res.begin, 2), "eind": round(st["equity"], 2),
                        "resultaat": round(e.realized, 2), "trades": len(e.res.trades),
                        "daglimiet": "daglimiet" in e.res.notities})
    st["dagen"] = st["dagen"][-400:]
    st["trades"] = (st.get("trades", []) + [asdict(t) for t in e.res.trades])[-500:]


def _save(path: Path, st: dict, ronde: dict) -> dict:
    st["laatste_ronde"] = {k: v for k, v in ronde.items() if k != "log"} | {"log": ronde["log"][-30:]}
    if ronde["log"] or ronde["status"] not in ("beurs dicht",):
        rondes = st.get("rondes", [])
        rondes.append(st["laatste_ronde"])
        st["rondes"] = rondes[-60:]
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(st, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    tmp.replace(path)
    with (path.parent / "daytrader_audit.jsonl").open("a", encoding="utf-8") as f:
        if ronde["log"]:
            f.write(json.dumps(st["laatste_ronde"], ensure_ascii=False) + "\n")
    return st
