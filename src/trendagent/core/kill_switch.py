"""Centrale kill switch.

De status staat in een klein JSON-bestand, zodat hij een herstart overleeft.
Iedere agent controleert de kill switch vóór elke actie.

Regels:
- AANZETTEN mag door: de mens, de Monitoring Agent en de Risk Manager.
- UITZETTEN mag alleen een mens.
- Is het bestand onleesbaar of beschadigd, dan geldt de kill switch als AAN
  (bij twijfel: stoppen).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

HUMAN = "human"
ALLOWED_TO_ACTIVATE = {HUMAN, "monitoring", "risk_manager"}


class KillSwitchPermissionError(PermissionError):
    pass


class KillSwitch:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _read(self) -> dict:
        if not self.path.exists():
            return {"active": False}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(data.get("active"), bool):
                raise ValueError("ongeldig veld 'active'")
            return data
        except (OSError, ValueError):
            # Fail closed: een kapot bestand betekent: alles stoppen.
            return {"active": True, "reason": "kill-switchbestand onleesbaar", "by": "system"}

    def is_active(self) -> bool:
        return self._read()["active"]

    def status(self) -> dict:
        return self._read()

    def activate(self, reason: str, by: str) -> None:
        if by not in ALLOWED_TO_ACTIVATE:
            raise KillSwitchPermissionError(f"'{by}' mag de kill switch niet aanzetten")
        self._write({"active": True, "reason": reason, "by": by})

    def deactivate(self, by: str) -> None:
        if by != HUMAN:
            raise KillSwitchPermissionError("Alleen een mens mag de kill switch uitzetten")
        self._write({"active": False, "reason": "handmatig vrijgegeven", "by": by})

    def _write(self, data: dict) -> None:
        data["changed_at_utc"] = datetime.now(timezone.utc).isoformat()
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data), encoding="utf-8")
        tmp.replace(self.path)  # atomair: nooit een half geschreven bestand
