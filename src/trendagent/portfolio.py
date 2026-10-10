"""De nep-portefeuille (paper trading).

Er gaat nooit echt geld om. Kopen en verkopen gebeurt alleen in dit bestand,
met realistische tegenvallers: slippage (iets slechtere prijs) en kosten.
Alles staat in euro's; Amerikaanse posities worden met de wisselkoers omgerekend.

De toestand wordt opgeslagen in state/portfolio.json, zodat de agent elke
dag verder kan waar hij gebleven was.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class Position:
    ticker: str
    currency: str
    qty: float
    entry_price: float      # in lokale valuta, inclusief slippage
    stop: float             # in lokale valuta
    highest_close: float
    opened: str             # datum ISO
    entry_fx: float         # lokale valuta -> EUR bij aankoop
    risk_eur: float         # verlies in EUR als de beginstop wordt geraakt
    last_checked: str = ""  # laatste handelsdag die tegen de stop is gecontroleerd


@dataclass
class Trade:
    day: str
    ticker: str
    side: str               # "BUY" of "SELL"
    qty: float
    price: float            # lokale valuta
    fx: float
    value_eur: float
    costs_eur: float
    reason: str
    pnl_eur: float | None = None


@dataclass
class Portfolio:
    cash_eur: float
    positions: dict[str, Position] = field(default_factory=dict)
    trades: list[Trade] = field(default_factory=list)
    equity_history: list[dict] = field(default_factory=list)   # [{"day":..., "equity":...}]
    consecutive_losses: int = 0

    # ---------------------------------------------------------------- opslag

    @classmethod
    def load(cls, path: Path, starting_cash: float) -> "Portfolio":
        if not path.exists():
            return cls(cash_eur=starting_cash)
        raw = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            cash_eur=raw["cash_eur"],
            positions={k: Position(**v) for k, v in raw["positions"].items()},
            trades=[Trade(**t) for t in raw["trades"]],
            equity_history=raw["equity_history"],
            consecutive_losses=raw.get("consecutive_losses", 0),
        )

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "cash_eur": round(self.cash_eur, 2),
            "positions": {k: asdict(v) for k, v in self.positions.items()},
            "trades": [asdict(t) for t in self.trades],
            "equity_history": self.equity_history,
            "consecutive_losses": self.consecutive_losses,
        }
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        tmp.replace(path)

    # ------------------------------------------------------------ waardering

    def equity(self, prices: dict[str, float], fx: dict[str, float]) -> float:
        """Totale waarde in EUR. Zonder actuele prijs telt de instapprijs (voorzichtig: geen winst bijtellen)."""
        total = self.cash_eur
        for p in self.positions.values():
            price = prices.get(p.ticker, p.entry_price)
            total += p.qty * price * fx[p.currency]
        return total

    def open_risk_eur(self, fx: dict[str, float]) -> float:
        """Hoeveel er verloren gaat als ALLE stops nu worden geraakt (alleen verliezen tellen)."""
        risk = 0.0
        for p in self.positions.values():
            risk += max(0.0, (p.entry_price - p.stop) * p.qty * fx[p.currency])
        return risk

    def peak_equity(self) -> float | None:
        return max((e["equity"] for e in self.equity_history), default=None)

    def record_equity(self, day: str, equity: float) -> None:
        if self.equity_history and self.equity_history[-1]["day"] == day:
            self.equity_history[-1]["equity"] = round(equity, 2)
        else:
            self.equity_history.append({"day": day, "equity": round(equity, 2)})

    # ------------------------------------------------------------- handelen

    def buy(self, day: str, ticker: str, currency: str, qty: float, price: float,
            stop: float, fx: float, costs_eur: float, reason: str) -> Trade:
        value = qty * price * fx
        if value + costs_eur > self.cash_eur + 1e-6:
            raise ValueError("onvoldoende (nep)geld")
        if ticker in self.positions:
            raise ValueError("bijkopen in een bestaande positie is niet toegestaan")
        self.cash_eur -= value + costs_eur
        self.positions[ticker] = Position(
            ticker, currency, qty, price, stop, price, day, fx,
            risk_eur=round((price - stop) * qty * fx + costs_eur, 2), last_checked=day)
        t = Trade(day, ticker, "BUY", qty, round(price, 4), fx, round(value, 2), round(costs_eur, 2), reason)
        self.trades.append(t)
        return t

    def sell(self, day: str, ticker: str, price: float, fx: float, costs_eur: float, reason: str) -> Trade:
        p = self.positions.pop(ticker)
        value = p.qty * price * fx
        cost_basis = p.qty * p.entry_price * p.entry_fx
        buy_costs = next((t.costs_eur for t in reversed(self.trades)
                          if t.ticker == ticker and t.side == "BUY"), 0.0)
        pnl = value - cost_basis - costs_eur - buy_costs
        self.cash_eur += value - costs_eur
        self.consecutive_losses = self.consecutive_losses + 1 if pnl < 0 else 0
        t = Trade(day, ticker, "SELL", p.qty, round(price, 4), fx, round(value, 2),
                  round(costs_eur, 2), reason, pnl_eur=round(pnl, 2))
        self.trades.append(t)
        return t
