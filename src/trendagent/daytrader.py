"""Daytrade-bot (alleen nepgeld): koopt en verkoopt op dezelfde beursdag, nooit iets 's nachts vasthouden.

Regels (openingsrange-uitbraak, alleen kopen, geen hefboom, nooit short):
1. Openingsrange: hoogste en laagste koers in de eerste OR_MIN minuten na de opening van de Amerikaanse beurs.
2. Kopen mag alleen tussen het einde van de openingsrange en ENTRY_UNTIL (New Yorkse tijd), op een vast
   kijkmoment (elk kwartier: zo vaak draait de bot ook echt).
   - het laatste afgesloten 5-minutenblok sloot boven de top van de openingsrange (uitbraak),
   - maar niet meer dan MAX_CHASE erboven (niet achter een raket aanrennen),
   - de koers staat boven de VWAP (gemiddelde prijs van vandaag, gewogen naar volume),
   - het volume in de openingsrange is minstens MIN_RVOL keer zo groot als normaal (er gebeurt echt iets),
   - de hele markt (SPY) staat boven zijn openingskoers (alleen kopen als de markt meewerkt),
   - de openingsrange is niet te wild (hooguit MAX_OR_PCT van de koers).
3. Stop-loss: onderkant van de openingsrange (maar hooguit MAX_RISK_PCT onder de instap).
   Winstdoel: TARGET_R keer het risico. Raakt een blok beide, dan rekenen we voorzichtig met de stop.
4. Om EXIT_AT wordt alles verkocht. Nooit iets mee de nacht in.
5. Remmen: hooguit MAX_TRADES aankopen per dag, MAX_OPEN tegelijk, elk aandeel één keer per dag;
   risico per aankoop RISK_PER_TRADE van het vermogen, hooguit MAX_WEIGHT van het vermogen in één aandeel;
   is het verlies van vandaag DAY_STOP of meer, dan koopt hij die dag niets meer.

Kosten: geen commissie (zoals bij Alpaca), wel SLIPPAGE per kant (de prijs is altijd iets slechter dan op het scherm).
Dezelfde functies worden gebruikt voor de test op oude koersen en voor het echte oefenen, zodat die niet van
elkaar kunnen verschillen.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field, replace
from datetime import date, datetime, time, timedelta

try:
    from zoneinfo import ZoneInfo
    NY = ZoneInfo("America/New_York")
except Exception:  # noqa: BLE001
    NY = None

OPEN = time(9, 30)
CLOSE = time(16, 0)


@dataclass(frozen=True)
class Params:
    or_min: int = 30               # openingsrange in minuten
    entry_until: time = time(12, 30)
    exit_at: time = time(15, 45)   # vanaf dit kijkmoment alles verkopen
    check_every: int = 15          # minuten tussen kijkmomenten
    min_rvol: float = 1.2
    max_chase: float = 0.015
    max_or_pct: float = 0.04
    max_risk_pct: float = 0.02
    target_r: float = 2.0
    risk_per_trade: float = 0.005
    max_weight: float = 0.25
    max_trades: int = 3
    max_open: int = 2
    day_stop: float = -0.015
    slippage: float = 0.0005
    market_filter: bool = True
    vwap_filter: bool = True
    use_target: bool = True
    rvol_days: int = 10
    market: str = "SPY"
    # Regels uit de grafiekanalyse (standaard uit; alleen aan na onderzoek en jouw ja):
    dagtrend_filter: bool = False      # alleen kopen als de daggrafiek van het aandeel stijgt (slot > 50d > 200d)
    markt_trend_filter: bool = False   # niet kopen als de daggrafiek van de markt (SPY) daalt


@dataclass
class Bar5:
    t: datetime        # begin van het blok, New Yorkse tijd
    o: float
    h: float
    l: float  # noqa: E741
    c: float
    v: float


@dataclass
class Pos:
    ticker: str
    qty: int
    entry: float
    stop: float
    target: float | None
    t_in: datetime
    risk: float
    ctx: dict = field(default_factory=dict)   # hoe de situatie eruitzag bij het kopen (om van te leren)


@dataclass
class DayTrade:
    dag: str
    ticker: str
    qty: int
    instap: float
    uitstap: float
    t_in: str
    t_uit: str
    reden: str
    resultaat: float      # in valuta van de boekhouding, na slippage
    r: float              # resultaat in risico-eenheden
    ctx: dict = field(default_factory=dict)


@dataclass
class DayResult:
    dag: str
    trades: list[DayTrade] = field(default_factory=list)
    begin: float = 0.0
    eind: float = 0.0
    notities: list[str] = field(default_factory=list)


def check_times(day: date, p: Params) -> list[datetime]:
    """Kijkmomenten van de bot op één dag (New Yorkse tijd), vanaf het einde van de openingsrange."""
    start = datetime.combine(day, OPEN) + timedelta(minutes=p.or_min)
    end = datetime.combine(day, CLOSE)
    out, t = [], start
    while t < end:
        out.append(t)
        t += timedelta(minutes=p.check_every)
    return out


def _vwap(bars: list[Bar5]) -> float | None:
    vol = sum(b.v for b in bars)
    if vol <= 0:
        return None
    return sum((b.h + b.l + b.c) / 3 * b.v for b in bars) / vol


def or_stats(bars: list[Bar5], p: Params) -> tuple[float, float, float] | None:
    """(top, bodem, volume) van de openingsrange, of None als die (nog) niet compleet is."""
    if not bars:
        return None
    day = bars[0].t.date()
    end = datetime.combine(day, OPEN) + timedelta(minutes=p.or_min)
    ob = [b for b in bars if b.t.replace(tzinfo=None) < end]
    if len(ob) < p.or_min // 5:
        return None
    return max(b.h for b in ob), min(b.l for b in ob), sum(b.v for b in ob)


def entry_signal(ticker: str, done: list[Bar5], or_: tuple[float, float, float], avg_or_vol: float | None,
                 market_ok: bool, p: Params) -> tuple[bool, str, float]:
    """Mag hij nu kopen? Geeft (ja/nee, uitleg, rangscore) op basis van alleen afgesloten blokken."""
    top, bodem, ovol = or_
    last = done[-1]
    if not market_ok:
        return False, "markt staat onder de opening", 0.0
    if (top - bodem) / top > p.max_or_pct:
        return False, "openingsrange te wild", 0.0
    if not avg_or_vol:
        return False, "nog geen normaal volume bekend", 0.0
    rvol = ovol / avg_or_vol
    if rvol < p.min_rvol:
        return False, f"te weinig volume ({rvol:.1f}x normaal)", 0.0
    if last.c <= top:
        return False, "nog geen uitbraak", 0.0
    if last.c > top * (1 + p.max_chase):
        return False, "al te ver boven de range", 0.0
    if p.vwap_filter:
        vw = _vwap(done)
        if vw is None or last.c < vw:
            return False, "onder de VWAP", 0.0
    return True, f"uitbraak boven {top:.2f} met {rvol:.1f}x volume", rvol


def size(equity: float, entry: float, stop: float, p: Params) -> int:
    risk_ps = entry - stop
    if risk_ps <= 0:
        return 0
    q = min(equity * p.risk_per_trade / risk_ps, equity * p.max_weight / entry)
    return int(math.floor(q))


class DayEngine:
    """Eén beursdag van de daytrade-bot, stap voor stap (één stap = één kijkmoment).

    De test op oude koersen roept step() aan voor elk kijkmoment van de dag; het echte oefenen roept step() aan
    bij elke ronde (elk kwartier) en bewaart de stand tussendoor met to_dict()/from_dict().
    """

    def __init__(self, day: date, equity: float, p: Params = Params()):
        self.day, self.p = day, p
        self.res = DayResult(dag=day.isoformat(), begin=equity, eind=equity)
        self.open: dict[str, Pos] = {}
        self.traded: set[str] = set()
        self.realized = 0.0
        self.prev: datetime | None = None
        self.klaar = False
        self.redenen: dict[str, int] = {}   # waarom aandelen bij het laatste kijkmoment niet gekocht werden

    # ---------- bewaren tussen rondes ----------
    def to_dict(self) -> dict:
        return {"dag": self.res.dag, "begin": self.res.begin, "realized": self.realized, "klaar": self.klaar,
                "prev": self.prev.isoformat() if self.prev else None, "traded": sorted(self.traded),
                "notities": self.res.notities, "trades": [asdict(t) for t in self.res.trades],
                "open": {k: {**asdict(v), "t_in": v.t_in.isoformat()} for k, v in self.open.items()}}

    @classmethod
    def from_dict(cls, d: dict, p: Params = Params()) -> DayEngine:
        e = cls(date.fromisoformat(d["dag"]), float(d["begin"]), p)
        e.realized = float(d.get("realized", 0.0))
        e.klaar = bool(d.get("klaar"))
        e.prev = datetime.fromisoformat(d["prev"]) if d.get("prev") else None
        e.traded = set(d.get("traded", []))
        e.res.notities = list(d.get("notities", []))
        e.res.trades = [DayTrade(**t) for t in d.get("trades", [])]
        e.open = {k: Pos(**{**v, "t_in": datetime.fromisoformat(v["t_in"])}) for k, v in d.get("open", {}).items()}
        e.res.eind = e.res.begin + e.realized
        return e

    def _close(self, pos: Pos, price: float, when: datetime, why: str) -> None:
        fill = price * (1 - self.p.slippage)
        pnl = (fill - pos.entry) * pos.qty
        self.realized += pnl
        self.res.trades.append(DayTrade(self.res.dag, pos.ticker, pos.qty, round(pos.entry, 4), round(fill, 4),
                                        pos.t_in.strftime("%H:%M"), when.strftime("%H:%M"), why, round(pnl, 2),
                                        round(pnl / pos.risk, 3) if pos.risk else 0.0, dict(pos.ctx)))
        del self.open[pos.ticker]
        self.res.eind = self.res.begin + self.realized

    def step(self, t: datetime, day_bars: dict[str, list[Bar5]], avg_or_vol: dict[str, float],
             fill_at=None, allow_entries: bool = True, context: dict | None = None) -> list[str]:
        """Kijkmoment t (New Yorkse tijd, zonder tijdzone). Gebruikt alleen blokken die vóór t begonnen.
        fill_at(ticker, t) -> prijs waartegen nu gekocht/verkocht wordt (test: opening van het blok op t).
        Geeft een lijst met wat er gebeurde, in gewone woorden."""
        p, day, log = self.p, self.day, []
        if self.klaar:
            return log
        idx = {tk: {b.t.replace(tzinfo=None): b for b in bs} for tk, bs in day_bars.items()}
        if fill_at is None:
            def fill_at(tk, when):
                b = idx.get(tk, {}).get(when)
                return b.o if b else _last_close(day_bars.get(tk, []), when)
        # 1. Blokken sinds het vorige kijkmoment: stop of winstdoel geraakt?
        span_start = self.prev or datetime.combine(day, OPEN)
        for tk in list(self.open):
            pos = self.open[tk]
            m = span_start
            while m < t:
                b = idx.get(tk, {}).get(m)
                m += timedelta(minutes=5)
                if not b or b.t.replace(tzinfo=None) < pos.t_in:
                    continue
                if b.l <= pos.stop:
                    self._close(pos, min(b.o, pos.stop), b.t, "stop-loss")
                    log.append(f"{tk}: stop-loss geraakt")
                    break
                if pos.target and b.h >= pos.target:
                    self._close(pos, max(b.o, pos.target), b.t, "winstdoel")
                    log.append(f"{tk}: winstdoel gehaald")
                    break
        self.prev = t
        # 2. Eind van de dag: alles verkopen.
        if t.time() >= p.exit_at:
            for tk in list(self.open):
                prijs = fill_at(tk, t)
                if prijs is None:
                    prijs = self.open[tk].entry
                self._close(self.open[tk], prijs, t, "einde van de dag")
                log.append(f"{tk}: verkocht aan het einde van de dag")
            self.klaar = True
            return log
        # 3. Kopen?
        if not allow_entries or t.time() > p.entry_until or len(self.res.trades) + len(self.open) >= p.max_trades:
            return log
        unreal = sum(((_last_close(day_bars.get(x.ticker, []), t) or x.entry) - x.entry) * x.qty for x in self.open.values())
        if (self.realized + unreal) / self.res.begin <= p.day_stop:
            if "daglimiet" not in self.res.notities:
                self.res.notities.append("daglimiet")
                log.append("daglimiet bereikt: vandaag niets meer kopen")
            return log
        context = context or {}
        self.redenen = {}
        mkt = day_bars.get(p.market) or []
        m_done = [b for b in mkt if b.t.replace(tzinfo=None) < t]
        market_ok = (not p.market_filter) or (bool(m_done) and m_done[-1].c > mkt[0].o)
        if p.markt_trend_filter and (context.get(p.market) or {}).get("dagtrend") == "dalend":
            market_ok = False
        kandidaten = []
        for tk, bs in day_bars.items():
            if tk in self.open or tk in self.traded:
                continue
            if p.dagtrend_filter and (context.get(tk) or {}).get("dagtrend") != "stijgend":
                continue
            o = or_stats(bs, p)
            done = [b for b in bs if b.t.replace(tzinfo=None) < t]
            if not o or not done:
                continue
            ok, why, score = entry_signal(tk, done, o, avg_or_vol.get(tk), market_ok, p)
            if ok:
                kandidaten.append((score, tk, o, why))
            else:
                self.redenen[why] = self.redenen.get(why, 0) + 1
        for _score, tk, o, why in sorted(kandidaten, key=lambda x: -x[0]):
            if len(self.open) >= p.max_open or len(self.res.trades) + len(self.open) >= p.max_trades:
                break
            prijs = fill_at(tk, t)
            if not prijs:
                continue
            entry = prijs * (1 + p.slippage)
            stop = max(o[1], entry * (1 - p.max_risk_pct))
            if stop >= entry:
                continue
            q = size(self.res.begin + self.realized, entry, stop, p)
            if q < 1:
                continue
            target = entry + p.target_r * (entry - stop) if p.use_target else None
            ctx = entry_context(tk, day_bars, t, o, avg_or_vol.get(tk), context, p)
            self.open[tk] = Pos(tk, q, entry, stop, target, t, (entry - stop) * q, ctx)
            self.traded.add(tk)
            log.append(f"{tk}: gekocht ({q} stuks, {why})")
        return log


def entry_context(tk: str, day_bars: dict[str, list[Bar5]], t: datetime, o: tuple[float, float, float],
                  avg_vol: float | None, context: dict | None, p: Params) -> dict:
    """Hoe de situatie eruitzag op het moment van kopen: de dag zelf en de daggrafiek (om later van te leren)."""
    done = [b for b in day_bars.get(tk, []) if b.t.replace(tzinfo=None) < t]
    mkt = [b for b in day_bars.get(p.market, []) if b.t.replace(tzinfo=None) < t]
    dc = (context or {}).get(tk) or {}
    mc = (context or {}).get(p.market) or {}
    top, bodem, ovol = o
    open_ = done[0].o if done else None
    ctx = {"tijd": t.strftime("%H:%M"),
           "rvol": round(ovol / avg_vol, 2) if avg_vol else None,
           "or_breedte": round((top - bodem) / top, 4) if top else None,
           "boven_range": round(done[-1].c / top - 1, 4) if done and top else None,
           "markt_vandaag": round(mkt[-1].c / mkt[0].o - 1, 4) if mkt else None,
           "dag_tot_nu": round(done[-1].c / open_ - 1, 4) if done and open_ else None,
           "gap": round(open_ / dc["vorig_slot"] - 1, 4) if open_ and dc.get("vorig_slot") else None}
    for k in ("dagtrend", "plek", "terugval", "boven_sma50"):
        if k in dc:
            ctx[k] = dc[k]
    if mc.get("dagtrend"):
        ctx["markt_dagtrend"] = mc["dagtrend"]
    return ctx


def simulate_day(day_bars: dict[str, list[Bar5]], avg_or_vol: dict[str, float], equity: float,
                 p: Params = Params(), context: dict | None = None) -> DayResult:
    """Speelt één beursdag na zoals de bot hem live zou doen: alleen op kijkmomenten beslissen, met
    alleen de blokken die op dat moment al afgesloten zijn; vullen tegen de opening van het volgende blok."""
    any_bars = next((b for b in day_bars.values() if b), None)
    if not any_bars:
        return DayResult(dag="", begin=equity, eind=equity)
    day = any_bars[0].t.date()
    e = DayEngine(day, equity, p)
    for t in check_times(day, p):
        e.step(t, day_bars, avg_or_vol, context=context)
        if e.klaar:
            break
    for tk in list(e.open):  # vangnet: de data hield eerder op
        last = _last_close(day_bars.get(tk, []), datetime.combine(day, CLOSE))
        e._close(e.open[tk], last if last is not None else e.open[tk].entry, datetime.combine(day, CLOSE), "einde van de dag")
    return e.res


def _last_close(bars: list[Bar5], before: datetime) -> float | None:
    done = [b for b in bars if b.t.replace(tzinfo=None) < before]
    return done[-1].c if done else None


def split_days(bars: list[Bar5]) -> dict[date, list[Bar5]]:
    out: dict[date, list[Bar5]] = {}
    for b in bars:
        if OPEN <= b.t.time() < CLOSE:
            out.setdefault(b.t.date(), []).append(b)
    return out


def avg_or_volumes(history: dict[str, dict[date, list[Bar5]]], day: date, p: Params) -> dict[str, float]:
    """Gemiddeld volume in de openingsrange over de vorige rvol_days dagen (alleen dagen vóór 'day')."""
    out = {}
    for tk, days in history.items():
        vols = []
        for d in sorted(x for x in days if x < day)[-p.rvol_days:]:
            s = or_stats(days[d], p)
            if s:
                vols.append(s[2])
        if len(vols) >= max(3, p.rvol_days // 2):
            out[tk] = sum(vols) / len(vols)
    return out


def backtest(data: dict[str, list[Bar5]], p: Params = Params(), start_equity: float = 10_000.0,
             daily: dict | None = None) -> dict:
    """Alle dagen in de data naspelen. De eerste rvol_days dagen dienen alleen om 'normaal volume' te leren.
    daily: dagkoersen per aandeel (voor de daggrafiek-analyse); alleen dagen vóór de handelsdag worden gebruikt."""
    from .daytrade_leren import dag_context
    per = {tk: split_days(bs) for tk, bs in data.items()}
    days = sorted({d for x in per.values() for d in x})
    eq = start_equity
    curve, trades, dagen = [], [], []
    for d in days[p.rvol_days:]:
        day_bars = {tk: x[d] for tk, x in per.items() if d in x and len(x[d]) >= 70}
        if p.market not in day_bars:
            continue
        r = simulate_day(day_bars, avg_or_volumes(per, d, p), eq, p, dag_context(daily, d) if daily else None)
        eq = r.eind
        trades += r.trades
        dagen.append({"dag": r.dag, "resultaat": round(r.eind - r.begin, 2), "trades": len(r.trades),
                      "daglimiet": "daglimiet" in r.notities})
        curve.append((r.dag, round(eq, 2)))
    return {"params": _params_dict(p), "start": start_equity, "eind": round(eq, 2), "curve": curve,
            "trades": [asdict(t) for t in trades], "dagen": dagen, "stats": stats(trades, curve, start_equity)}


def stats(trades: list[DayTrade], curve: list[tuple[str, float]], start: float) -> dict:
    n = len(trades)
    wins = [t for t in trades if t.resultaat > 0]
    peak, mdd = start, 0.0
    for _, v in curve:
        peak = max(peak, v)
        mdd = min(mdd, v / peak - 1)
    days = len(curve)
    eind = curve[-1][1] if curve else start
    gross_win = sum(t.resultaat for t in wins)
    gross_loss = -sum(t.resultaat for t in trades if t.resultaat <= 0)
    return {"trades": n, "dagen": days, "dagen_met_trade": len({t.dag for t in trades}),
            "winst_pct": round(len(wins) / n, 3) if n else None,
            "gem_r": round(sum(t.r for t in trades) / n, 3) if n else None,
            "rendement": round(eind / start - 1, 4), "max_daling": round(mdd, 4),
            "profit_factor": round(gross_win / gross_loss, 2) if gross_loss else None,
            "redenen": {r: sum(1 for t in trades if t.reden == r) for r in ("stop-loss", "winstdoel", "einde van de dag")}}


def _params_dict(p: Params) -> dict:
    d = asdict(p)
    return {k: (v.strftime("%H:%M") if isinstance(v, time) else v) for k, v in d.items()}


def variant(p: Params, **kw) -> Params:
    return replace(p, **kw)
