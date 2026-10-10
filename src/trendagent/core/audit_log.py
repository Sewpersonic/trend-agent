"""Auditlog: een logboek waaraan alleen kan worden toegevoegd.

Elke regel is een JSON-object met de hash van de vorige regel erin
(een 'hash-keten'). Wie achteraf een regel wijzigt of verwijdert, breekt de
keten, en verify() ziet dat direct.

Gevoelige velden (sleutels, wachtwoorden, tokens) worden gemaskeerd voordat
ze worden weggeschreven, zodat ze nooit in een log terechtkomen.
"""

from __future__ import annotations

import hashlib
import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GENESIS_HASH = "0" * 64
_SENSITIVE_WORDS = ("key", "secret", "token", "password", "passphrase", "seed")
REDACTED = "***REDACTED***"


def _redact(value: Any) -> Any:
    """Maskeert recursief alle waarden waarvan de veldnaam gevoelig klinkt."""
    if isinstance(value, dict):
        return {
            k: (REDACTED if any(w in str(k).lower() for w in _SENSITIVE_WORDS) else _redact(v))
            for k, v in value.items()
        }
    if isinstance(value, list):
        return [_redact(v) for v in value]
    return value


def _hash(entry_without_hash: dict) -> str:
    canonical = json.dumps(entry_without_hash, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class AuditLog:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _last_hash(self) -> str:
        if not self.path.exists():
            return GENESIS_HASH
        last = GENESIS_HASH
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    last = json.loads(line)["hash"]
        return last

    def append(self, event: str, actor: str, details: dict | None = None) -> dict:
        """Voegt één gebeurtenis toe en geeft de opgeslagen regel terug."""
        with self._lock:
            entry = {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "event": event,
                "actor": actor,
                "details": _redact(details or {}),
                "prev_hash": self._last_hash(),
            }
            entry["hash"] = _hash(entry)
            with self.path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, default=str) + "\n")
            return entry

    def entries(self) -> list[dict]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]

    def verify(self) -> bool:
        """True als de keten intact is, False als er iets is gewijzigd of verwijderd."""
        prev = GENESIS_HASH
        for entry in self.entries():
            stored = entry.get("hash")
            body = {k: v for k, v in entry.items() if k != "hash"}
            if body.get("prev_hash") != prev or _hash(body) != stored:
                return False
            prev = stored
        return True
