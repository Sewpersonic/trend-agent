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
import http.client
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DEMO_BASE = "https://demo.trading212.com/api/v0"
MAX_ORDERS = 6
MAX_ORDER_EUR = 3000.0  # trend-agent zet hooguit ~25% van €10.000 in één aandeel
# Grove omrekening naar euro voor de ordergrens (alleen voor de veiligheidsgrens, niet voor de boekhouding).
FX_NAAR_EUR = {"EUR": 1.0, "USD": 0.95, "GBP": 1.2, "GBX": 0.012, "CHF": 1.05}

# Yahoo-beurssuffix -> mogelijke Trading 212-tickerletter (bv. ASML.AS -> ASMLa_EQ). Wordt gecontroleerd met de
# instrumentenlijst van Trading 212; alleen een ticker die daar echt bestaat wordt gebruikt.
SUFFIX = {"AS": ["a"], "DE": ["d"], "PA": ["p"], "MI": ["m"], "MC": ["e"], "L": ["l"], "SW": ["z"], "BR": ["b"]}


class BrokerError(RuntimeError):
    def __init__(self, msg: str, onzeker: bool = False):
        super().__init__(msg)
        self.onzeker = onzeker  # True: een order kan wel of niet zijn aangekomen


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
                if e.code in (408, 500, 502, 503, 504) and method != "GET":
                    raise BrokerError(f"HTTP {e.code} bij {method} {path}: onbekend of de order is aangekomen.", onzeker=True) from None
                if e.code == 429 and poging < 2:
                    self._sleep(6 if "instruments" not in path else 55)
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
                raise BrokerError(f"Trading 212 niet bereikbaar: {e.reason}", onzeker=method != "GET") from None
            except (OSError, ValueError, http.client.HTTPException) as e:  # time-out, afgebroken antwoord, kapotte JSON
                raise BrokerError(f"Geen goed antwoord van Trading 212 ({type(e).__name__}).", onzeker=method != "GET") from None
        raise BrokerError("Te veel verzoeken achter elkaar (rate limit).")

    def summary(self) -> dict:
        r = self._req("GET", "/equity/account/summary") or {}
        if not isinstance(r, dict):
            raise BrokerError("Onverwacht antwoord op de accountgegevens.")
        return r

    def positions(self) -> list[dict]:
        return _items(self._req("GET", "/equity/positions"), "posities")

    def open_orders(self) -> list[dict]:
        return _items(self._req("GET", "/equity/orders"), "openstaande orders")

    def instruments(self) -> list[dict]:
        return _items(self._req("GET", "/equity/metadata/instruments"), "instrumenten")

    def market_order(self, ticker: str, quantity: float) -> dict:
        return self._req("POST", "/equity/orders/market", {"ticker": ticker, "quantity": quantity}) or {}

    def cancel_order(self, order_id) -> None:
        self._req("DELETE", f"/equity/orders/{order_id}")


def _items(r, wat: str) -> list[dict]:
    """Accepteer een lijst of {"items": [...]}; al het andere is een fout (dan geen orders)."""
    if r is None:
        return []
    if isinstance(r, dict) and isinstance(r.get("items"), list):
        r = r["items"]
    if not isinstance(r, list) or not all(isinstance(x, dict) for x in r):
        raise BrokerError(f"Onverwachte vorm van de {wat} van Trading 212; voor de zekerheid niets gedaan.")
    return r


def _tq(x: dict, wat: str) -> tuple[str, float]:
    """Ticker en aantal uit een positie of order, in beide vormen (plat of onder 'instrument')."""
    t = x.get("ticker") or (x.get("instrument") or {}).get("ticker")
    q = x.get("quantity", x.get("qty"))
    if not t or q is None:
        raise BrokerError(f"Een {wat} van Trading 212 mist ticker of aantal; voor de zekerheid niets gedaan.")
    return t, float(q)


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


def plan_orders(target: dict[str, dict], filled: dict[str, float], pending: dict[str, list[dict]] | None = None) -> list[dict]:
    """Welke orders zijn nodig om het oefenaccount gelijk te zetten met de trend-agent.

    - Nooit short: verkopen alleen tot wat echt in het account staat (uitgevoerd, niet onderweg).
    - Staat er voor een aandeel nog een order open, dan geen nieuwe order: eerst afwachten. Wil de bot het aandeel
      niet meer, dan wordt een openstaande koop ingetrokken.
    - Verkopen eerst, dan kopen.
    """
    pending = pending or {}
    orders = []
    for t212, info in target.items():
        have = filled.get(t212, 0.0)
        open_ = pending.get(t212, [])
        if open_:
            open_buys = [o for o in open_ if float(o.get("quantity") or 0) > 0]
            if info["qty"] <= have and open_buys:
                for o in open_buys:
                    orders.append({"ticker": t212, "yahoo": info["yahoo"], "actie": "intrekken", "order_id": o.get("id"),
                                   "quantity": 0.0, "waarde_eur": 0.0})
            continue
        diff = round(info["qty"] - have, 6)
        if abs(diff) < 1e-9:
            continue
        if diff < 0:
            diff = -min(-diff, have)
            if abs(diff) < 1e-9:
                continue
        orders.append({"ticker": t212, "yahoo": info["yahoo"], "actie": "koop" if diff > 0 else "verkoop", "quantity": diff,
                       "waarde_eur": round(abs(diff) * info["prijs"] * info.get("fx", FX_NAAR_EUR.get(info["valuta"], 1.0)), 2)})
    return sorted(orders, key=lambda o: {"intrekken": 0, "verkoop": 1, "koop": 2}[o["actie"]])


def _instruments(client: "T212Demo", state_dir: Path) -> list[dict]:
    """Instrumentenlijst, één keer per dag opgehaald (Trading 212 staat maar 1 verzoek per 50 seconden toe)."""
    cache = state_dir / "t212_instrumenten.json"
    try:
        c = json.loads(cache.read_text(encoding="utf-8"))
        if c.get("dag") == datetime.now(timezone.utc).date().isoformat() and c.get("items"):
            return c["items"]
    except (OSError, ValueError):
        pass
    items = client.instruments()
    keep = [{k: i.get(k) for k in ("ticker", "currencyCode", "shortName", "type", "name")} for i in items]
    try:
        cache.write_text(json.dumps({"dag": datetime.now(timezone.utc).date().isoformat(), "items": keep}), encoding="utf-8")
    except OSError:
        pass
    return keep


def sync(state_dir: Path, client: T212Demo, orders_aan: bool, kill_active: bool, managed: set[str] | None = None,
         verslag: dict | None = None) -> dict:
    """Vergelijk en zet gelijk. Schrijft in 'verslag' (ook als het halverwege misgaat blijft bewaard wat er al gebeurde)."""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    port = json.loads((state_dir / "portfolio.json").read_text(encoding="utf-8"))
    bot_pos = port.get("positions", {})
    if verslag is None:
        verslag = {}
    verslag.update({"tijd": now, "status": "ok", "reden": "", "orders": [], "niet_gekoppeld": []})
    managed = set(managed or set())
    verslag["managed"] = sorted(managed)

    # Eerst openstaande orders, dan posities: een order die er tussendoor wordt uitgevoerd telt dan dubbel
    # (dus eerder te weinig dan te veel kopen), nooit nul keer.
    pend_raw = client.open_orders()
    positions = client.positions()
    summ = client.summary()
    instruments = _instruments(client, state_dir)
    verslag["account"] = summ
    verslag["posities"] = positions
    filled: dict[str, float] = {}
    for p in positions:
        t, q = _tq(p, "positie")
        filled[t] = filled.get(t, 0.0) + q
    pending: dict[str, list[dict]] = {}
    verslag["open_orders"] = []
    for o in pend_raw:
        t, q = _tq(o, "order")
        done = float(o.get("filledQuantity") or 0)
        rest = q - done if q > 0 else q + abs(done)
        pending.setdefault(t, []).append({"id": o.get("id"), "quantity": rest})
        verslag["open_orders"].append({"ticker": t, "quantity": rest, "status": o.get("status")})

    target: dict[str, dict] = {}
    for y, p in bot_pos.items():
        t = map_ticker(y, p.get("currency", ""), instruments)
        if not t:
            verslag["niet_gekoppeld"].append(y)
            continue
        verslag.setdefault("koppeling", {})[y] = t
        target[t] = {"yahoo": y, "qty": float(p["qty"]), "prijs": float(p.get("highest_close") or p.get("entry_price") or 0),
                     "valuta": p.get("currency", "EUR"), "fx": float(p.get("entry_fx") or FX_NAAR_EUR.get(p.get("currency", "EUR"), 1.0))}
    for t in managed:
        if t not in target and (filled.get(t, 0) > 0 or pending.get(t)):
            target[t] = {"yahoo": t, "qty": 0.0, "prijs": 0.0, "valuta": "EUR", "fx": 1.0}

    plan = plan_orders(target, filled, pending)
    verslag["plan"] = plan
    wacht = [t for t in target if pending.get(t)]
    if wacht:
        verslag["wacht_op"] = wacht
    if kill_active:
        verslag.update(status="alleen kijken", reden="De kill switch staat aan: er worden geen orders geplaatst.")
        return verslag
    if not orders_aan:
        verslag.update(status="alleen kijken", reden="Orders staan uit in config/broker.json.")
        return verslag
    gedaan = 0
    for o in plan:
        if gedaan >= MAX_ORDERS:
            verslag["reden"] = f"Meer dan {MAX_ORDERS} orders nodig; de rest volgt in de volgende ronde."
            break
        if o["actie"] == "koop" and o["waarde_eur"] > MAX_ORDER_EUR:
            verslag["orders"].append({**o, "uitkomst": "overgeslagen", "reden": f"boven de grens van €{MAX_ORDER_EUR:.0f}"})
            continue
        if o["actie"] == "koop":
            managed.add(o["ticker"])  # vóór de order vastleggen: ook bij een time-out weet hij later dat dit van ons is
            verslag["managed"] = sorted(managed)
        try:
            if o["actie"] == "intrekken":
                client.cancel_order(o["order_id"])
                verslag["orders"].append({**o, "uitkomst": "ingetrokken"})
            else:
                r = client.market_order(o["ticker"], o["quantity"])
                verslag["orders"].append({**o, "uitkomst": "geplaatst", "antwoord": r})
            gedaan += 1
        except BrokerError as e:
            verslag["orders"].append({**o, "uitkomst": "mislukt" if not e.onzeker else "onzeker", "reden": str(e)})
            verslag["status"] = "deels mislukt"
            if e.onzeker:
                verslag["reden"] = "Onzeker of een order is aangekomen; voor de zekerheid deze ronde gestopt. De volgende ronde kijkt eerst wat er echt staat."
                break
    return verslag


def run(state_dir: Path, config_path: Path, check_only: bool = False, client: T212Demo | None = None,
        save_state: bool = True) -> dict:
    from .core.kill_switch import KillSwitch
    out_path = state_dir / "broker.json"
    try:
        prev = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
    except ValueError:
        prev = {}
    verslag: dict = {}
    try:
        cfg = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
        client = client or T212Demo()
        kill = KillSwitch(state_dir / "kill_switch.json").is_active()
        sync(state_dir, client, orders_aan=bool(cfg.get("orders_aan")) and not check_only,
             kill_active=kill, managed=set(prev.get("managed", [])), verslag=verslag)
        if check_only and verslag["status"] == "alleen kijken" and cfg.get("orders_aan"):
            verslag["reden"] = "Alleen gecontroleerd: geen orders geplaatst."
    except Exception as e:  # noqa: BLE001 - elk probleem: verslag schrijven, niets meer doen
        # Wat er al gebeurde (orders, managed) blijft in 'verslag' staan.
        verslag.update({"tijd": verslag.get("tijd") or datetime.now(timezone.utc).isoformat(timespec="seconds"),
                        "status": "fout",
                        "reden": str(e) if isinstance(e, BrokerError) else f"Onverwachte fout: {type(e).__name__}: {e}"})
        verslag.setdefault("orders", [])
        verslag["managed"] = sorted(set(verslag.get("managed", [])) | set(prev.get("managed", [])))
        for k in ("account", "posities", "open_orders", "koppeling"):
            if k not in verslag and k in prev:
                verslag[k] = prev[k]
    verslag.setdefault("managed", prev.get("managed", []))
    hist = prev.get("geschiedenis", [])
    if verslag.get("orders") or verslag["status"] in ("fout", "deels mislukt") or not hist:
        hist.append({"tijd": verslag["tijd"], "status": verslag["status"], "reden": verslag.get("reden", ""),
                     "orders": [{k: o.get(k) for k in ("ticker", "quantity", "actie", "waarde_eur", "uitkomst", "reden")}
                                for o in verslag.get("orders", [])]})
    verslag["geschiedenis"] = hist[-60:]
    if save_state:
        out_path.write_text(json.dumps(verslag, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return verslag
