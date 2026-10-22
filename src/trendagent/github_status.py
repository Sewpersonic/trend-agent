"""Overzicht van de laatste GitHub-runs voor het dashboard (tabblad GitHub).

Haalt met de GitHub-CLI (gh) de laatste runs van alle workflows op en schrijft dashboard/github.json:
per run wanneer, wat, of het goed ging, en bij een fout welke stap misging, in gewone taal.
Verandert niets aan de bots.
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

WAT = {
    "practice": "Dagelijkse ronde van de bots",
    "onderzoek": "Wekelijks onderzoek",
    "backtest": "Backtest over 5 jaar",
    "tests": "Controle van de code",
    "diagnose": "Test van de koersbron",
    "broker": "Oefenaccount Trading 212",
    "daytrade": "Daytrade-bot",
}
PER_WORKFLOW = {"daytrade": 4}   # draait 28 keer per dag: alleen de laatste paar tonen

STAP = {
    "Trend-agent": "De trend-agent liep vast.",
    "Investeerder": "De investeerder liep vast.",
    "Dagoverzicht": "Het dagoverzicht kon niet worden gemaakt.",
    "Cijfers voor het dashboard": "De cijfers voor het dashboard konden niet worden gemaakt.",
    "Resultaat opslaan in de repository": "Opslaan op GitHub lukte niet (vaak tijdelijk; de volgende ronde probeert het opnieuw).",
    "Gezondheidscontrole": "De koersdata was niet betrouwbaar (bijvoorbeeld koersen niet bijgewerkt) of een bot liep vast. De bot heeft daarom niets gekocht.",
    "Onderzoek": "Het onderzoek zelf liep vast (bijvoorbeeld koersen downloaden mislukte).",
    "Oefenaccount Trading 212": "De koppeling met het oefenaccount van Trading 212 lukte niet (zie het verslag).",
    "Controle oefenaccount": "Het oefenaccount van Trading 212 gaf een fout of een order lukte niet. De bots zelf draaiden gewoon door. Zie het tabblad Oefenaccount.",
    "Volglijst": "De volglijst (extra beleggingen bekijken) lukte niet. De bots draaiden gewoon door.",
    "Volglijst (alleen kijken)": "De volglijst (extra beleggingen bekijken) lukte niet. Het oefenaccount werkte gewoon.",
    "Ronde": "De daytrade-bot liep vast in deze ronde. Hij heeft daarom niets gekocht; de volgende ronde probeert het opnieuw.",
    "Test op 5-minutenkoersen": "De test van de daytrade-bot lukte niet (meestal koersen downloaden).",
    "pip install -e .": "Installeren van de software lukte niet (meestal tijdelijk bij GitHub).",
}


def _gh(args: list[str]) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True, timeout=60).stdout


def collect(limit: int = 200, per_workflow: int = 12) -> list[dict]:
    runs = json.loads(_gh(["run", "list", "-L", str(limit), "--json",
                           "databaseId,workflowName,status,conclusion,createdAt,updatedAt,event,displayTitle,url"]))
    out: list[dict] = []
    seen: dict[str, int] = {}
    for r in runs:
        naam = r.get("workflowName", "")
        if naam == "status":
            continue  # het ophalen zelf niet tonen
        seen[naam] = seen.get(naam, 0) + 1
        if seen[naam] > PER_WORKFLOW.get(naam, per_workflow):
            continue  # niet laten overspoelen door veel code-controles
        uitkomst = {"success": "goed", "failure": "fout", "cancelled": "geannuleerd", "skipped": "overgeslagen",
                    "timed_out": "fout"}.get(r.get("conclusion") or "", "bezig" if r.get("status") != "completed" else "onbekend")
        fout_stap, uitleg = "", ""
        if uitkomst == "fout":
            try:
                jobs = json.loads(_gh(["run", "view", str(r["databaseId"]), "--json", "jobs"]))["jobs"]
                for j in jobs:
                    for st in j.get("steps", []):
                        if st.get("conclusion") == "failure":
                            fout_stap = st.get("name", "")
                            break
                    if fout_stap:
                        break
            except Exception:  # noqa: BLE001
                pass
            uitleg = STAP.get(fout_stap, f"De stap '{fout_stap}' ging mis." if fout_stap else "Onbekend waar het misging.")
        elif uitkomst == "geannuleerd":
            uitleg = "Gestopt voordat hij klaar was (bijvoorbeeld omdat er een nieuwere run begon). Geen probleem."
        start = datetime.fromisoformat(r["createdAt"].replace("Z", "+00:00"))
        eind = datetime.fromisoformat(r["updatedAt"].replace("Z", "+00:00")) if r.get("updatedAt") else start
        out.append({
            "id": str(r["databaseId"]), "workflow": r.get("workflowName", ""),
            "wat": WAT.get(r.get("workflowName", ""), r.get("workflowName", "")),
            "start": start.isoformat(), "duur_min": round((eind - start).total_seconds() / 60, 1),
            "aanleiding": {"schedule": "automatisch volgens schema", "push": "na een wijziging in de code",
                           "workflow_dispatch": "met de hand gestart"}.get(r.get("event", ""), r.get("event", "")),
            "uitkomst": uitkomst, "fout_stap": fout_stap, "uitleg": uitleg, "link": r.get("url", ""),
        })
    # Een fout is 'opgelost' als een latere run van dezelfde workflow wel goed ging (lijst is nieuwste eerst).
    for i, row in enumerate(out):
        if row["uitkomst"] == "fout":
            row["opgelost"] = any(o["workflow"] == row["workflow"] and o["uitkomst"] == "goed" for o in out[:i])
    return out


def voorstellen() -> list[dict]:
    """Open voorstellen van het wekelijkse onderzoek (pull requests op een voorstel/-tak): wachten op jouw ja of nee."""
    try:
        prs = json.loads(_gh(["pr", "list", "--state", "open", "--json", "number,title,url,createdAt,headRefName"]))
    except Exception:  # noqa: BLE001
        return []
    return [{"id": f"voorstel-{p['number']}", "soort": "voorstel", "workflow": "voorstel", "wat": "Voorstel van het onderzoek",
             "titel": p.get("title", ""), "start": p.get("createdAt", ""), "uitkomst": "wacht", "link": p.get("url", ""),
             "uitleg": "Het onderzoek vond een regel die bewezen beter werkte. Jij beslist: Merge = overnemen, Close = niet."}
            for p in prs if str(p.get("headRefName", "")).startswith("voorstel/")]


def write(path: Path) -> Path:
    rows = voorstellen() + collect()
    if not rows:
        rows = [{"id": "leeg", "leeg": True, "reden": "Nog geen runs gevonden."}]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    return path


if __name__ == "__main__":
    print(write(Path("dashboard/github.json")), datetime.now(timezone.utc).isoformat())
