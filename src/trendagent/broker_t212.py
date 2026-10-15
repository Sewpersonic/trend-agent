"""Koppeling met het OEFENACCOUNT (demo) van Trading 212. Alleen nepgeld.

Veiligheid (niet uit te zetten in de code):
- Alleen het demo-adres https://demo.trading212.com wordt ooit gebruikt; het echte adres (live) wordt geweigerd.
- Alleen als PAPER_TRADING=true.
- De sleutel komt uit de GitHub-geheimen T212_DEMO_KEY en T212_DEMO_SECRET (nooit in de code of de chat).
- Geen hefboom, geen short: er wordt nooit meer verkocht dan het oefenaccount bezit.
- Hooguit MAX_ORDERS orders per ronde en hooguit MAX_ORDER_EUR per order.
- Kill switch aan of orders uit in config/broker.json: dan alleen kijken, niets plaatsen.

Wat het doet: het oefenaccount volgt de trend-agent. Het verschil tussen wat de trend-agent volgens zijn eigen
boekhouding bezit en wat er in het oefenaccount staat, wordt met marktorders rechtgezet.
Lukt iets niet (geen sleutel, storing), dan gebeurt er niets en staat de reden in state/broker.json.
"""

from __future__ import annotations

import base64
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DEMO_BASE = "https://demo.trading212.com/api/v0"
MAX_ORDERS = 6
MAX_ORDER_EUR = 2500.0
# Grove omrekening naar euro voor de ordergrens (alleen voor de veiligheidsgrens, niet voor de boekhouding).
FX_NAAR_EUR = {"EUR": 1.0, "USD": 0.95, "GBP": 1.2, "GBX": 0.012, "CHF": 1.05}

# Yahoo-beurssuffix -> mogelijke Trading 212-tickerletter (bv. ASML.AS -> ASMLa_EQ). Wordt gecontroleerd met de
# instrumentenlijst van Trading 212; alleen een ticker die daar echt bestaat wordt gebruikt.
SUFFIX = {"AS": ["a"], "DE": ["d"], "PA": ["p"], "MI": ["m"], "MC": ["e"], "L": ["l"], "SW": ["z"], "BR": ["b"]}


class BrokerError(RuntimeError):
    pass


class T212Demo:
    def __init__(self, key: str | None = None, secret: str | None = None, base: str = DEMO_BASE,
                 opener=None, sleep=time.sleep):
        if not base.startswith("https://demo.trading212.com/"):
            raise BrokerError("Alleen het oefenaccount (demo.trading212.com) is toegestaan.")
        if os.environ.get("PAPER_TRADING", "").lower() != "true":
            raise BrokerError("PAPER_TRADING staat niet op true; de koppeling doet niets.")
        key = key if key is not None else os.environ.get("T212_DEMO_KEY", "")
        secret = secret if secret is not None else os.environ.get("T212_DEMO_SECRET", "")
        if not key:
            raise BrokerError("Geen sleutel gevonden (GitHub-geheim T212_DEMO_KEY ontbreekt).")
        # Nieuwe sleutels: sleutel + geheime code als Basic-auth. Oude sleutels: alleen de sleutel.
        self._auth = ("Basic " + base64.b64encode(f"{key}:{secret}".encode()).decode()) if secret else key
        self.base = base
        self._open = opener or urllib.request.urlopen
        self._sleep = sleep

    def _req(self, method: str, path: str, body: dict | None = None):
        data = json.dumps(body).encode() if body is not None else None
        for poging in range(3):
            req = urllib.request.Request(self.base + path, data=data, method=method,
                                         headers={"Authorization": self._auth, "Content-Type": "application/json",
                                                  "Accept": "application/json"})
            try:
                with self._open(req, timeout=30) as r:
                    raw = r.read()
                    return json.loads(raw) if raw else None
            except urllib.error.HTTPError as e:
                if e.code == 429 and poging < 2:
                    self._sleep(6)
                    continue
                detail = ""
                try:
                    detail = e.read().decode()[:300]
                except Exception:  # noqa: BLE001
                    pass
                uitleg = {401: "sleutel of geheime code klopt niet", 403: "de sleutel mist een recht",
                          404: "niet gevonden"}.get(e.code, "fout bij Trading 212")
                raise BrokerError(f"HTTP {e.code} ({uitleg}) bij {method} {path}. {detail}".strip()) from None
            except urllib.error.URLError as e:
                raise BrokerError(f"Trading 212 niet bereikbaar: {e.reason}") from None
        raise BrokerError("Te veel verzoeken achter elkaar (rate limit).")

    def summary(self) -> dict:
        return self._req("GET", "/equity/account/summary") or {}

    def positions(self) -> list[dict]:
        return self._req("GET", "/equity/positions") or []

    def instruments(self) -> list[dict]:
        return self._req("GET", "/equity/metadata/instruments") or []

    def orders_history(self, limit: int = 20) -> list[dict]:
        r = self._req("GET", f"/equity/history/orders?limit={limit}") or {}
        return r.get("items", r if isinstance(r, list) else [])

    def market_order(self, ticker: str, quantity: float) -> dict:
        return self._req("POST", "/equity/orders/market", {"ticker": ticker, "quantity": quantity}) or {}


def map_ticker(yahoo: str, currency: str, instruments: list[dict]) -> str | None:
    """Yahoo-ticker (MSFT, SAP.DE, SHELL.AS) -> Trading 212-ticker, alleen als die in de instrumentenlijst staat."""
    known = {i.get("ticker"): i for i in instruments}
    base, _, suf = yahoo.partition(".")
    base = base.replace("-", "_")
    cands = [f"{base}_US_EQ"] if not suf else [f"{base}{s}_EQ" for s in SUFFIX.get(suf, [])]
    for c in cands:
        i = known.get(c)
        if i and (not currency or i.get("currencyCode") in (currency, None)):
            return c
    # Terugval: zelfde korte naam en valuta, alleen als er precies één is.
    same = [i for i in instruments if i.get("shortName") == base and i.get("currencyCode") == currency
            and i.get("type") in ("STOCK", "ETF", None)]
    return same[0]["ticker"] if len(same) == 1 else None


def _pos_qty(positions: list[dict]) -> dict[str, float]:
    out = {}
    for p in positions:
        t = p.get("ticker") or (p.get("instrument") or {}).get("ticker")
        q = p.get("quantity")
        if t is not None and q is not None:
            out[t] = float(q)
    return out


def plan_orders(target: dict[str, dict], have: dict[str, float]) -> list[dict]:
    """Welke orders zijn nodig om het oefenaccount gelijk te zetten met de trend-agent. Nooit short."""
    orders = []
    for t212, info in target.items():
        diff = round(info["qty"] - have.get(t212, 0.0), 6)
        if abs(diff) < 1e-9:
            continue
        if diff < 0:
            diff = -min(-diff, have.get(t212, 0.0))  # nooit meer verkopen dan er is
        orders.append({"ticker": t212, "yahoo": info["yahoo"], "quantity": diff,
                       "waarde_eur": round(abs(diff) * info["prijs"] * FX_NAAR_EUR.get(info["valuta"], 1.0), 2)})
    # Posities in het oefenaccount die de trend-agent niet (meer) heeft: verkopen, maar alleen tickers die wij
    # eerder zelf hebben gekocht (managed), zodat we nooit iets anders aanraken.
    return orders


def sync(state_dir: Path, client: T212Demo, orders_aan: bool, kill_active: bool, managed: set[str] | None = None) -> dict:
    """Vergelijk en zet gelijk. Geeft een verslag terug (ook bij fouten)."""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    port = json.loads((state_dir / "portfolio.json").read_text(encoding="utf-8"))
    bot_pos = port.get("positions", {})
    verslag: dict = {"tijd": now, "status": "ok", "reden": "", "orders": [], "niet_gekoppeld": []}

    summ = client.summary()
    verslag["account"] = summ
    positions = client.positions()
    verslag["posities"] = positions
    instruments = client.instruments()
    have = _pos_qty(positions)

    target: dict[str, dict] = {}
    for y, p in bot_pos.items():
        t = map_ticker(y, p.get("currency", ""), instruments)
        if not t:
            verslag["niet_gekoppeld"].append(y)
            continue
        target[t] = {"yahoo": y, "qty": float(p["qty"]), "prijs": float(p.get("highest_close") or p.get("entry_price") or 0),
                     "valuta": p.get("currency", "EUR")}
    managed = set(managed or set())
    for t in managed:
        if t not in target and have.get(t, 0) > 0:
            target[t] = {"yahoo": t, "qty": 0.0, "prijs": 0.0, "valuta": "EUR"}

    plan = plan_orders(target, have)
    verslag["plan"] = plan
    if kill_active:
        verslag.update(status="alleen kijken", reden="De kill switch staat aan: er worden geen orders geplaatst.")
        return verslag
    if not orders_aan:
        verslag.update(status="alleen kijken", reden="Orders staan uit in config/broker.json.")
        return verslag
    for o in plan[:MAX_ORDERS]:
        if o["waarde_eur"] > MAX_ORDER_EUR:
            verslag["orders"].append({**o, "uitkomst": "overgeslagen", "reden": f"boven de grens van €{MAX_ORDER_EUR:.0f}"})
            continue
        try:
            r = client.market_order(o["ticker"], o["quantity"])
            verslag["orders"].append({**o, "uitkomst": "geplaatst", "antwoord": r})
            if o["quantity"] > 0:
                managed.add(o["ticker"])
        except BrokerError as e:
            verslag["orders"].append({**o, "uitkomst": "mislukt", "reden": str(e)})
            verslag["status"] = "deels mislukt"
    if len(plan) > MAX_ORDERS:
        verslag["reden"] = f"Meer dan {MAX_ORDERS} orders nodig; de rest volgt in de volgende ronde."
    verslag["managed"] = sorted(managed)
    return verslag


def run(state_dir: Path, config_path: Path, check_only: bool = False, client: T212Demo | None = None) -> dict:
    from .core.kill_switch import KillSwitch
    cfg = {}
    if config_path.exists():
        cfg = json.loads(config_path.read_text(encoding="utf-8"))
    out_path = state_dir / "broker.json"
    prev = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
    try:
        client = client or T212Demo()
        kill = KillSwitch(state_dir / "kill_switch.json").is_active()
        verslag = sync(state_dir, client, orders_aan=bool(cfg.get("orders_aan")) and not check_only,
                       kill_active=kill, managed=set(prev.get("managed", [])))
        if check_only and verslag["status"] == "alleen kijken" and cfg.get("orders_aan"):
            verslag["reden"] = "Alleen gecontroleerd (proef): geen orders geplaatst."
    except BrokerError as e:
        verslag = {"tijd": datetime.now(timezone.utc).isoformat(timespec="seconds"), "status": "fout", "reden": str(e),
                   "orders": [], "managed": prev.get("managed", [])}
    verslag.setdefault("managed", prev.get("managed", []))
    hist = prev.get("geschiedenis", [])
    hist.append({"tijd": verslag["tijd"], "status": verslag["status"], "reden": verslag.get("reden", ""),
                 "orders": [{k: o.get(k) for k in ("ticker", "quantity", "waarde_eur", "uitkomst", "reden")} for o in verslag.get("orders", [])]})
    verslag["geschiedenis"] = hist[-60:]
    out_path.write_text(json.dumps(verslag, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return verslag
