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


def simulate_day(day_bars: dict[str, list[Bar5]], avg_or_vol: dict[str, float], equity: float,
                 p: Params = Params()) -> DayResult:
    """Speelt één beursdag na zoals de bot hem live zou doen: alleen op kijkmomenten beslissen, met
    alleen de blokken die op dat moment al afgesloten zijn; vullen tegen de opening van het volgende blok."""
    any_bars = next((b for b in day_bars.values() if b), None)
    res = DayResult(dag="", begin=equity, eind=equity)
    if not any_bars:
        return res
    day = any_bars[0].t.date()
    res.dag = day.isoformat()
    open_: dict[str, Pos] = {}
    traded: set[str] = set()
    realized = 0.0
    idx = {t: {b.t.replace(tzinfo=None): b for b in bs} for t, bs in day_bars.items()}
    ors = {t: or_stats(bs, p) for t, bs in day_bars.items()}
    mkt = day_bars.get(p.market) or []
    mkt_open = mkt[0].o if mkt else None
    times = check_times(day, p)

    def close_pos(pos: Pos, price: float, when: datetime, why: str) -> None:
        nonlocal realized
        fill = price * (1 - p.slippage)
        pnl = (fill - pos.entry) * pos.qty
        realized += pnl
        res.trades.append(DayTrade(res.dag, pos.ticker, pos.qty, round(pos.entry, 4), round(fill, 4),
                                   pos.t_in.strftime("%H:%M"), when.strftime("%H:%M"), why, round(pnl, 2),
                                   round(pnl / pos.risk, 3) if pos.risk else 0.0))

    prev = None
    for k, t in enumerate(times):
        # 1. Blokken sinds het vorige kijkmoment: stop of winstdoel geraakt?
        span_start = prev or (datetime.combine(day, OPEN))
        for tk in list(open_):
            pos = open_[tk]
            m = span_start
            while m < t:
                b = idx.get(tk, {}).get(m)
                m += timedelta(minutes=5)
                if not b or b.t.replace(tzinfo=None) < pos.t_in:
                    continue
                if b.l <= pos.stop:
                    close_pos(pos, min(b.o, pos.stop), b.t, "stop-loss")
                    del open_[tk]
                    break
                if pos.target and b.h >= pos.target:
                    close_pos(pos, max(b.o, pos.target), b.t, "winstdoel")
                    del open_[tk]
                    break
        prev = t
        # 2. Eind van de dag: alles verkopen tegen de opening van het volgende blok.
        if t.time() >= p.exit_at:
            for tk in list(open_):
                b = idx.get(tk, {}).get(t)
                last = b.o if b else _last_close(day_bars[tk], t)
                if last is not None:
                    close_pos(open_[tk], last, t, "einde van de dag")
                del open_[tk]
            break
        # 3. Kopen?
        if t.time() > p.entry_until or len(res.trades) + len(open_) >= p.max_trades:
            continue
        unreal = sum(((_last_close(day_bars[x.ticker], t) or x.entry) - x.entry) * x.qty for x in open_.values())
        if (realized + unreal) / equity <= p.day_stop:
            if "daglimiet" not in res.notities:
                res.notities.append("daglimiet")
            continue
        m_done = [b for b in mkt if b.t.replace(tzinfo=None) < t]
        market_ok = (not p.market_filter) or (bool(m_done) and mkt_open is not None and m_done[-1].c > mkt_open)
        kandidaten = []
        for tk, bs in day_bars.items():
            if tk in open_ or tk in traded or not ors.get(tk):
                continue
            done = [b for b in bs if b.t.replace(tzinfo=None) < t]
            if not done:
                continue
            ok, _, score = entry_signal(tk, done, ors[tk], avg_or_vol.get(tk), market_ok, p)
            if ok:
                kandidaten.append((score, tk))
        for score, tk in sorted(kandidaten, reverse=True):
            if len(open_) >= p.max_open or len(res.trades) + len(open_) >= p.max_trades:
                break
            nb = idx.get(tk, {}).get(t)
            if not nb:
                continue
            entry = nb.o * (1 + p.slippage)
            top, bodem, _ = ors[tk]
            stop = max(bodem, entry * (1 - p.max_risk_pct))
            if stop >= entry:
                continue
            q = size(equity + realized, entry, stop, p)
            if q < 1:
                continue
            target = entry + p.target_r * (entry - stop) if p.use_target else None
            open_[tk] = Pos(tk, q, entry, stop, target, t, (entry - stop) * q)
            traded.add(tk)
    for tk in list(open_):  # vangnet: data hield eerder op
        last = _last_close(day_bars[tk], datetime.combine(day, CLOSE))
        if last is not None:
            close_pos(open_[tk], last, datetime.combine(day, CLOSE), "einde van de dag")
    res.eind = equity + realized
    return res


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


def backtest(data: dict[str, list[Bar5]], p: Params = Params(), start_equity: float = 10_000.0) -> dict:
    """Alle dagen in de data naspelen. De eerste rvol_days dagen dienen alleen om 'normaal volume' te leren."""
    per = {tk: split_days(bs) for tk, bs in data.items()}
    days = sorted({d for x in per.values() for d in x})
    eq = start_equity
    curve, trades, dagen = [], [], []
    for d in days[p.rvol_days:]:
        day_bars = {tk: x[d] for tk, x in per.items() if d in x and len(x[d]) >= 70}
        if p.market not in day_bars:
            continue
        r = simulate_day(day_bars, avg_or_volumes(per, d, p), eq, p)
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
