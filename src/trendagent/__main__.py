"""Opdrachtregel.

  python -m trendagent run               één ronde met echte (gratis) koersen van Yahoo
  python -m trendagent run --simulated   één ronde met verzonnen koersen (geen internet nodig)
  python -m trendagent status            toon het laatste rapport
  python -m trendagent kill "reden"      zet de kill switch aan
  python -m trendagent resume            zet de kill switch uit (alleen jij, de mens)
  python -m trendagent backtest          test de regels op de afgelopen jaren (echte koersen)
  python -m trendagent backtest --simulated   idem op verzonnen koersen (zonder internet)
  python -m trendagent invest            één ronde van de investeerder
  python -m trendagent onderzoek         varianten testen + leerrapport (schrijft alleen naar onderzoek/)
  python -m trendagent health --check    controle na de dagelijkse ronde; foutcode als er iets mis is
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
    run.add_argument("--een-bron", action="store_true", help="alleen Yahoo, zonder controle door Stooq/ECB")
    sub.add_parser("status", help="toon het laatste rapport")
    kill = sub.add_parser("kill", help="zet de kill switch aan")
    kill.add_argument("reason", nargs="?", default="handmatig gestopt")
    sub.add_parser("resume", help="zet de kill switch uit en reset de verliesteller")
    bt = sub.add_parser("backtest", help="test de regels op de afgelopen jaren")
    bt.add_argument("--years", type=int, default=5, help="aantal jaren (standaard 5)")
    bt.add_argument("--simulated", action="store_true", help="verzonnen koersen, voor een proef")
    bt.add_argument("--out", default=None, help="map voor de resultaten")
    bt.add_argument("--strategie", choices=["trend", "investeerder", "beide", "controles"], default="beide",
                    help="controles = investeerder met alleen ETF's en zonder crypto")
    inv = sub.add_parser("invest", help="één ronde van de investeerder (maandelijks herverdelen)")
    inv.add_argument("--simulated", action="store_true", help="gebruik verzonnen koersen")
    inv.add_argument("--een-bron", action="store_true", help="alleen Yahoo, zonder controle door Stooq/ECB")
    rs = sub.add_parser("onderzoek", help="varianten testen en leren van resultaten (past niets aan)")
    rs.add_argument("--years", type=int, default=5)
    rs.add_argument("--simulated", action="store_true")
    rs.add_argument("--out", default="onderzoek")
    vs = sub.add_parser("voorstel", help="aanbeveling van het onderzoek in config/productie.json zetten (voor een pull request)")
    vs.add_argument("--aanbeveling", default="onderzoek/aanbeveling.json")
    vs.add_argument("--body", default="voorstel.md", help="bestand voor de tekst van het voorstel")
    ov = sub.add_parser("overzicht", help="dagoverzicht van beide bots schrijven (rapporten/OVERZICHT.md)")
    ov.add_argument("--simulated", action="store_true")
    hc = sub.add_parser("health", help="gezondheid van de laatste rondes tonen")
    hc.add_argument("--check", action="store_true", help="foutcode 1 als er iets mis is")
    args = parser.parse_args(argv)

    s = load_settings()
    ks = KillSwitch(s.state_dir / "kill_switch.json")

    if args.cmd == "run":
        today = _market_day(args)
        try:
            provider = _live_provider(args, today)
        except DataError as exc:
            print(f"Fout: {exc}", file=sys.stderr)
            return 2
        try:
            agent = TrendAgent(s, provider)
            rep = agent.run(today)
        except Exception as exc:  # noqa: BLE001  (onverwachte fout: vastleggen en melden)
            _write_health(s, "trend", {"day": today.isoformat(), "status": "FOUT",
                                       "fout": f"{type(exc).__name__}: {exc}"})
            raise
        _write_health(s, "trend", {"day": rep.day, "status": rep.status, "versie": rep.version,
                                   "waarschuwingen": rep.warnings[:20], **rep.health})
        _trend_charts(s, agent, rep.day)
        print((s.state_dir / "report.md").read_text(encoding="utf-8"))
        return 0

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

    if args.cmd == "invest":
        return _invest(s, args)

    if args.cmd == "onderzoek":
        return _research(s, args)

    if args.cmd == "health":
        return _health(s, args.check)

    if args.cmd == "voorstel":
        return _proposal(args.aanbeveling, args.body)

    if args.cmd == "overzicht":
        import json
        from . import summary
        health = s.state_dir / "health.json"
        days = []
        if health.exists():
            try:
                days = [h.get("day") for h in json.loads(health.read_text(encoding="utf-8")).values() if h.get("day")]
            except ValueError:
                days = []
        day = max(days) if days else _market_day(args).isoformat()
        path = summary.write(s.state_dir, s.reports_dir, day)
        try:
            from . import dagrapport
            dagrapport.write(s.state_dir, s.reports_dir, day)
        except Exception as exc:  # noqa: BLE001  (Excel mag het overzicht nooit laten mislukken)
            print(f"dagrapport.xlsx mislukt: {type(exc).__name__}: {exc}")
        print(path.read_text(encoding="utf-8"))
        return 0

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

    from .backtest import HistoricalProvider, download_history, run_backtest, run_investor_backtest
    from .backtest_report import write_all
    from .universe import CRYPTO, UNIVERSE

    today = datetime.now(timezone.utc).date()
    if args.simulated:
        sim = SimulatedProvider(end=today)
        n = (args.years + 1) * 260
        bars = {i.ticker: sim.history(i, n) for i in UNIVERSE + CRYPTO}
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
    from functools import partial

    from dataclasses import replace as _replace

    from .strategies import production_mix
    prod = production_mix()

    runs = {"trend": ("Trend-agent", run_backtest, "backtest/resultaten"),
            "investeerder": ("Investeerder", run_investor_backtest, "backtest/investeerder"),
            "alleen-etf": ("Investeerder (alleen ETF's)",
                           partial(run_investor_backtest, mix=_replace(prod, satellite_kinds=("ETF",), satellite_count=3)),
                           "backtest/controle-alleen-etf"),
            "zonder-crypto": ("Investeerder (zonder crypto)",
                              partial(run_investor_backtest, mix=_replace(prod, crypto_weight=0.0,
                                                                         core_weight=prod.core_weight + prod.crypto_weight)),
                              "backtest/controle-zonder-crypto")}
    groups = {"beide": ["trend", "investeerder"], "controles": ["alleen-etf", "zonder-crypto"]}
    chosen = groups.get(args.strategie, [args.strategie])
    for key in chosen:
        label, fn, default_out = runs[key]
        print(f"Backtest {label} van {start} t/m {today}...")
        result = fn(s, provider, start, today)
        out = Path(args.out or default_out) if len(chosen) == 1 else Path(default_out)
        write_all(result, out, args.years, label)
        print((out / "RAPPORT.md").read_text(encoding="utf-8"))
    return 0


def _invest(s, args) -> int:
    from .investor import Book, Investor, render
    from .reports import write_investor_excel

    today = _market_day(args)
    try:
        provider = _live_provider(args, today)
    except DataError as exc:
        print(f"Fout: {exc}", file=sys.stderr)
        return 2
    from .strategies import production_mix
    inv = Investor(s, provider, production_mix())
    try:
        out = inv.run(today)
    except Exception as exc:  # noqa: BLE001
        _write_health(s, "investeerder", {"day": today.isoformat(), "status": "FOUT",
                                          "fout": f"{type(exc).__name__}: {exc}"})
        raise
    _write_health(s, "investeerder", {"day": out["day"], "status": out["status"], "versie": out["version"],
                                      "waarschuwingen": out["warnings"][:20], **out.get("health", {})})
    book = Book.load(inv.path, s.starting_cash_eur)
    md = render(out, book)
    (s.state_dir / "investeerder.md").write_text(md, encoding="utf-8")
    s.reports_dir.mkdir(parents=True, exist_ok=True)
    (s.reports_dir / f"{today.isoformat()}-investeerder.md").write_text(md, encoding="utf-8")
    write_investor_excel(book, out, s.reports_dir / "investeerder.xlsx")
    _investor_charts(s, inv, book, out["day"])
    print(md)
    return 0


def _market_day(args):
    """Simulatie: vandaag. Echt: de handelsdag waarvan de slotkoersen nu binnen horen te zijn."""
    now = datetime.now(timezone.utc)
    if getattr(args, "simulated", False):
        return now.date()
    from .features import expected_market_day
    return expected_market_day(now)


def _charts_for(s, day: str, bot: str, items: list, xlsx_name: str, note_name: str) -> None:
    """items: (ticker, bars, titel, instap, stop, valuta). Fouten in grafieken stoppen nooit de bot."""
    try:
        from . import charts
        folder = charts.chart_dir(s.reports_dir, day)
        import json
        from . import excel_charts
        paths, datas = [], []
        for ticker, bars, title, entry, stop, cur, *extra in items:
            if bars and len(bars) >= 20:
                opened, sold = (extra + [None, None])[:2]
                paths.append(charts.candle_chart(bars, title, folder / f"{bot}-{ticker}.png", entry, stop, cur,
                                                 opened=opened, sold=sold))
                data = charts.chart_data(bars, title, entry, stop, cur, opened=opened, sold=sold)
                (folder / f"{bot}-{ticker}.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
                datas.append(dict(data, bot=bot))
        note = s.reports_dir / note_name
        if paths and note.exists():
            with note.open("a", encoding="utf-8") as f:
                f.write(charts.markdown_section(paths, s.reports_dir))
        # In Excel: echte Excel-grafieken (scherp, met waarden bij de muis); de plaatjes blijven in de notities.
        excel_charts.add(s.reports_dir / xlsx_name, datas)
        charts.prune(s.reports_dir)
    except Exception as exc:  # noqa: BLE001
        print(f"Grafieken overgeslagen: {type(exc).__name__}: {exc}", file=sys.stderr)


def _trend_charts(s, agent, day: str) -> None:
    if not s.write_reports:
        return
    from .universe import BY_TICKER
    bars = getattr(agent, "last_bars", {}) or {}
    pf = Portfolio.load(agent.portfolio_path, s.starting_cash_eur)
    items = []
    for t, pos in pf.positions.items():
        inst = BY_TICKER.get(t)
        items.append((t, bars.get(t), f"{inst.name if inst else t} ({t})", pos.entry_price, pos.stop, pos.currency,
                      pos.opened, None))
    for tr in pf.trades:
        if tr.day == day and tr.side == "SELL" and tr.ticker not in pf.positions:
            inst = BY_TICKER.get(tr.ticker)
            items.append((tr.ticker, bars.get(tr.ticker), f"{inst.name if inst else tr.ticker} ({tr.ticker}) - verkocht",
                          None, None, inst.currency if inst else "", None, (tr.day, tr.price)))
    _charts_for(s, day, "trend", items, "trend-agent.xlsx", f"{day}.md")


def _investor_charts(s, inv, book, day: str) -> None:
    from .universe import BY_TICKER
    bars = getattr(inv, "last_bars", {}) or {}
    items = []
    for t in sorted(book.qty, key=lambda t: -book.cost_eur.get(t, 0)):
        inst = BY_TICKER.get(t)
        items.append((t, bars.get(t), f"{inst.name if inst else t} ({t})", None, None, inst.currency if inst else ""))
    _charts_for(s, day, "investeerder", items, "investeerder.xlsx", f"{day}-investeerder.md")


def _live_provider(args, today):
    """Standaard: Yahoo als hoofdbron, gecontroleerd door Stooq en de ECB."""
    if args.simulated:
        return SimulatedProvider(end=today)
    if args.een_bron:
        return YahooProvider()
    from .sources import MultiSourceProvider
    return MultiSourceProvider()


# ------------------------------------------------------------------ health

MAX_FAILED_SHARE = 0.30
MAX_STALE_SHARE = 0.40


def _write_health(s, bot: str, info: dict) -> None:
    import json
    path = s.state_dir / "health.json"
    data = {}
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            data = {}
    info["vastgelegd_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    data[bot] = info
    s.state_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")


def health_problems(data: dict) -> list[str]:
    problems = []
    for bot in ("trend", "investeerder"):
        h = data.get(bot)
        if not h:
            problems.append(f"{bot}: geen gezondheidsgegevens (ronde niet gedraaid?)")
            continue
        if h.get("status") in ("FOUT", "GEEN HANDEL"):
            problems.append(f"{bot}: status {h['status']} {h.get('fout', '')}".strip())
        asked, failed = h.get("gevraagd", 0), h.get("mislukt", 0)
        if asked and failed / asked > MAX_FAILED_SHARE:
            problems.append(f"{bot}: {failed} van {asked} koersreeksen mislukt")
        stale = h.get("verouderd", 0)
        if asked and stale / asked >= MAX_STALE_SHARE:
            problems.append(f"{bot}: {stale} van {asked} koersen niet bijgewerkt (storing bij de bron of beursvakantie)")
    return problems


def _health(s, check: bool) -> int:
    import json
    path = s.state_dir / "health.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    for bot, h in data.items():
        print(f"{bot}: {h.get('status')} op {h.get('day')}, {h.get('ok', '?')}/{h.get('gevraagd', '?')} reeksen ok, "
              f"regime {h.get('regime', '?')}, versie {h.get('versie', '?')}")
        src = h.get("bronnen")
        if src:
            print(f"  koersbronnen: {src['koersen']}, wisselkoers {src['wisselkoers']}"
                  + (f", afwijkend: {', '.join(src['afwijkend'])}" if src.get("afwijkend") else ""))
            if src.get("fout_tweede_bron"):
                print(f"  tweede bron: {src.get('tweede_bron')} ({src['fout_tweede_bron']})")
        for w in h.get("waarschuwingen", [])[:5]:
            print(f"  - {w}")
    problems = health_problems(data)
    for p in problems:
        print(f"PROBLEEM: {p}")
    return 1 if (check and problems) else 0


# --------------------------------------------------------------- onderzoek

def _research(s, args) -> int:
    import csv
    import json
    from datetime import timedelta
    from pathlib import Path

    from . import evaluation, learning
    from .backtest import HistoricalProvider, download_history
    from .investor import Book
    from .portfolio import Portfolio
    from .strategies import investor_version, production_mix, trend_version
    from .universe import CRYPTO, UNIVERSE

    today = datetime.now(timezone.utc).date()
    if args.simulated:
        sim = SimulatedProvider(end=today)
        n = (args.years + 1) * 260
        bars = {i.ticker: sim.history(i, n) for i in UNIVERSE + CRYPTO}
        fx = {b.day: 0.92 for b in bars["SPY"]}
    else:
        try:
            bars, fx = download_history(args.years)
        except Exception as exc:  # noqa: BLE001
            print(f"Downloaden mislukt: {exc}", file=sys.stderr)
            return 2
    provider = HistoricalProvider(bars, fx)
    start = today - timedelta(days=round(args.years * 365.25))
    base = replace_settings(s)

    sections, rows, recommendations = [], [], []
    for kind in ("trend", "investeerder"):
        print(f"Onderzoek {kind}...")
        results = evaluation.run_variants(kind, base, provider, start, today)
        text, verdicts = evaluation.render(kind, results, provider)
        sections.append(text)
        days = [d for d, _ in results[0].equity]
        prod_version = trend_version(base) if kind == "trend" else investor_version(production_mix())
        accepted = {v.variant: v.accepted for v in verdicts}
        winners = [r for r in results if accepted.get(r.name)]
        if winners:
            best = max(winners, key=lambda r: evaluation.metrics_row(r, days)["sharpe_holdout"])
            m = evaluation.metrics_row(best, days)
            prod_m = evaluation.metrics_row(results[0], days)
            recommendations.append({"strategie": kind, "variant": best.name, "wijziging": best.params,
                                    "productieversie": prod_version,
                                    "sharpe_holdout": round(m["sharpe_holdout"], 3),
                                    "sharpe_holdout_productie": round(prod_m["sharpe_holdout"], 3),
                                    "max_daling": round(m["max_daling"], 4),
                                    "max_daling_productie": round(prod_m["max_daling"], 4)})
        for r in results:
            m = evaluation.metrics_row(r, days)
            rows.append([today.isoformat(), kind, r.name, prod_version if r.name == "productie" else "",
                         f"{m['totaal']:.4f}", f"{m['sharpe']:.3f}", f"{m['sharpe_holdout']:.3f}",
                         f"{m['max_daling']:.4f}", m["trades"],
                         "productie" if r.name == "productie" else ("AANBEVOLEN" if accepted.get(r.name) else "niet")])
        if kind == "trend":
            prod = next(r for r in results if r.name == "productie")
            sections.append(learning.render("Trend-agent: lessen uit 5 jaar backtest (productie)", prod.trades))
            live_path = s.state_dir / "portfolio.json"
            if live_path.exists():
                pf = Portfolio.load(live_path, s.starting_cash_eur)
                sections.append(learning.render("Trend-agent: lessen uit het oefenen (nepgeld, live)",
                                                pf.trades, reference=prod.trades, equity_history=pf.equity_history))
    inv_path = s.state_dir / "investeerder.json"
    if inv_path.exists():
        book = Book.load(inv_path, s.starting_cash_eur)
        vb = learning.vs_benchmark(book.equity_history)
        if vb:
            sections.append(f"## Investeerder live (nepgeld)\n\nVan {vb['van']} t/m {vb['tot']}: investeerder "
                            f"{vb['bot']:+.2%}, wereld-ETF {vb['etf']:+.2%}, verschil {vb['verschil']:+.2%}.\n")

    header = [f"# Onderzoeksrapport {today}", "",
              "Dit rapport test varianten van beide strategieën op echte koersen en kijkt wat de bots leren van hun "
              "eigen trades. **Er wordt niets automatisch aangepast.** Een aanbevolen variant gaat pas in productie "
              "als jij (of iemand die je vertrouwt) de instelling in de code aanpast; daarna draait de backtest opnieuw "
              "en loopt de nieuwe versie eerst weken mee op papier.", "",
              "> Resultaten uit het verleden zijn geen garantie. De aandelenlijst is in 2026 gekozen (survivorship bias).", ""]
    report = "\n".join(header) + "\n" + "\n".join(sections)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "LAATSTE.md").write_text(report, encoding="utf-8")
    (out / f"{today.isoformat()}.md").write_text(report, encoding="utf-8")
    (out / "aanbeveling.json").write_text(json.dumps(recommendations, indent=2, ensure_ascii=False) + "\n",
                                          encoding="utf-8")
    hist = out / "historie.csv"
    new = not hist.exists()
    with hist.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["datum", "strategie", "variant", "productieversie", "totaal", "sharpe", "sharpe_holdout",
                        "max_daling", "trades", "oordeel"])
        w.writerows(rows)
    print(report)
    return 0


def _proposal(rec_path: str, body_path: str) -> int:
    """Zet aanbevolen wijzigingen in config/productie.json. Geeft 0 als er iets veranderde, 3 als er niets te doen is.

    Wordt alleen gebruikt op een aparte voorstel-branch; samenvoegen in main doet een mens.
    """
    import json
    from pathlib import Path

    from .core.production import load_production, save_production

    path = Path(rec_path)
    recs = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    if not recs:
        print("Geen aanbeveling: niets te doen.")
        return 3
    prod = load_production()
    lines = ["Het wekelijkse onderzoek vond een variant die **alle** toetsen haalde (ongeziene periode, "
             "alle deelperiodes, dubbele kosten, grootste daling). Dit voorstel past alleen "
             "`config/productie.json` aan.", "",
             "**Samenvoegen (Merge)** = de bot gebruikt dit vanaf de volgende ronde. **Sluiten (Close)** = niets verandert.", ""]
    changed = False
    for r in recs:
        section = prod[r["strategie"]]
        before = dict(section)
        section.update(r["wijziging"])
        changed |= section != before
        lines += [f"### {r['strategie']}: {r['variant']}", "",
                  f"- Wijziging: `{json.dumps(r['wijziging'])}`",
                  f"- Sharpe op ongeziene periode: {r['sharpe_holdout']} (nu {r['sharpe_holdout_productie']})",
                  f"- Grootste daling: {r['max_daling']:.1%} (nu {r['max_daling_productie']:.1%})",
                  f"- Huidige versie: {r['productieversie']}", ""]
    if not changed:
        print("Aanbeveling staat al in productie: niets te doen.")
        return 3
    save_production(prod)
    lines += ["> Resultaten uit het verleden zijn geen garantie. Tip: laat de nieuwe versie een paar weken op papier "
              "meedraaien voordat je conclusies trekt. Volledig rapport: `onderzoek/LAATSTE.md`."]
    Path(body_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


def replace_settings(s):
    """Onderzoek schrijft nooit in state/: alles draait in tijdelijke mappen."""
    from dataclasses import replace
    return replace(s, write_reports=False)


if __name__ == "__main__":
    sys.exit(main())
