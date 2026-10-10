"""Opdrachtregel.

  python -m trendagent run               één ronde met echte (gratis) koersen van Yahoo
  python -m trendagent run --simulated   één ronde met verzonnen koersen (geen internet nodig)
  python -m trendagent status            toon het laatste rapport
  python -m trendagent kill "reden"      zet de kill switch aan
  python -m trendagent resume            zet de kill switch uit (alleen jij, de mens)
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

    if args.cmd == "resume":
        ks.deactivate(by=HUMAN)
        path = s.state_dir / "portfolio.json"
        pf = Portfolio.load(path, s.starting_cash_eur)
        pf.consecutive_losses = 0
        pf.save(path)
        print("Kill switch staat uit en de verliesteller is gereset.")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
