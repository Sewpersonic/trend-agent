"""Opdrachtregel.

  python -m trendagent run               één ronde met echte (gratis) koersen van Yahoo
  python -m trendagent run --simulated   één ronde met verzonnen koersen (geen internet nodig)
  python -m trendagent status            toon het laatste rapport
  python -m trendagent kill "reden"      zet de kill switch aan
  python -m trendagent resume            zet de kill switch uit (alleen jij, de mens)
  python -m trendagent backtest          test de regels op de afgelopen jaren (echte koersen)
  python -m trendagent backtest --simulated   idem op verzonnen koersen (zonder internet)
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime, timezone

from .agent import TrendAgent
from .core.config import load_settings
from .core.kill_switch import HUMAN, KillSwitch
from .data import DataError, SimulatedProvider, YahooProvider
from .portfolio import Portfolio


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="trendagent", description="Trend-agent (alleen nepgeld)")
    sub = parser.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="één handelsronde")
    run.add_argument("--simulated", action="store_true", help="gebruik verzonnen koersen")
    sub.add_parser("status", help="toon het laatste rapport")
    kill = sub.add_parser("kill", help="zet de kill switch aan")
    kill.add_argument("reason", nargs="?", default="handmatig gestopt")
    sub.add_parser("resume", help="zet de kill switch uit en reset de verliesteller")
    bt = sub.add_parser("backtest", help="test de regels op de afgelopen jaren")
    bt.add_argument("--years", type=int, default=5, help="aantal jaren (standaard 5)")
    bt.add_argument("--simulated", action="store_true", help="verzonnen koersen, voor een proef")
    bt.add_argument("--out", default="backtest/resultaten", help="map voor de resultaten")
    args = parser.parse_args(argv)

    s = load_settings()
    ks = KillSwitch(s.state_dir / "kill_switch.json")

    if args.cmd == "run":
        today = datetime.now(timezone.utc).date()
        try:
            provider = SimulatedProvider(end=today) if args.simulated else YahooProvider()
        except DataError as exc:
            print(f"Fout: {exc}", file=sys.stderr)
            return 2
        rep = TrendAgent(s, provider).run(today)
        print((s.state_dir / "report.md").read_text(encoding="utf-8"))
        return 0 if rep.status != "GESTOPT" else 1

    if args.cmd == "status":
        path = s.state_dir / "report.md"
        print(path.read_text(encoding="utf-8") if path.exists() else "Nog geen rapport. Draai eerst 'run'.")
        print(f"Kill switch: {'AAN' if ks.is_active() else 'uit'}")
        return 0

    if args.cmd == "kill":
        ks.activate(args.reason, by=HUMAN)
        print("Kill switch staat AAN. De agent handelt niet meer tot je 'resume' doet.")
        return 0

    if args.cmd == "backtest":
        return _backtest(s, args)

    if args.cmd == "resume":
        ks.deactivate(by=HUMAN)
        path = s.state_dir / "portfolio.json"
        pf = Portfolio.load(path, s.starting_cash_eur)
        pf.reset_risk_baseline()
        pf.save(path)
        print("Kill switch staat uit. Verliesteller gereset en de huidige waarde geldt als nieuwe top.")
        return 0
    return 1


def _backtest(s, args) -> int:
    from datetime import timedelta
    from pathlib import Path

    from .backtest import HistoricalProvider, download_history, run_backtest
    from .backtest_report import write_all
    from .universe import UNIVERSE

    today = datetime.now(timezone.utc).date()
    if args.simulated:
        sim = SimulatedProvider(end=today)
        n = (args.years + 1) * 260
        bars = {i.ticker: sim.history(i, n) for i in UNIVERSE}
        fx = {b.day: 0.92 for b in next(iter(bars.values()))}
    else:
        print(f"Koersen downloaden ({args.years + 1} jaar, {len(UNIVERSE)} instrumenten)...")
        try:
            bars, fx = download_history(args.years)
        except Exception as exc:  # noqa: BLE001
            print(f"Downloaden mislukt: {exc}", file=sys.stderr)
            return 2
    provider = HistoricalProvider(bars, fx)
    start = today - timedelta(days=round(args.years * 365.25))
    print(f"Backtest van {start} t/m {today}...")
    result = run_backtest(s, provider, start, today)
    out = Path(args.out)
    write_all(result, out, args.years)
    print((out / "RAPPORT.md").read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
