"""Splitst dashboard/index.html in kleinere bestanden voor het online dashboard.

Het dashboard accepteert per bestand hooguit 256 KB. Daarom gaat de pagina in delen naar het dashboard:
  index.html  de opbouw (html), met verwijzingen naar de andere bestanden
  stijl.css   alle opmaak, in dezelfde volgorde
  app-NN.js   elk script als eigen bestand, in dezelfde volgorde (elk script houdt zijn eigen scope)
Inspringing en lege regels gaan eruit. Bewerk altijd dashboard/index.html; dit script maakt de delen opnieuw.

Gebruik: python scripts/pagina_splitsen.py [uitvoermap]   (standaard dashboard/pagina)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MAX = 250_000


def klein(tekst: str) -> str:
    return "\n".join(r.strip() for r in tekst.split("\n") if r.strip())


def splits(bron: str) -> dict[str, str]:
    css: list[str] = []

    def stijl(m: re.Match) -> str:
        css.append(m.group(1))
        return ""

    html = re.sub(r"<style\b[^>]*>(.*?)</style>", stijl, bron, flags=re.S | re.I)
    scripts: dict[str, str] = {}

    def script(m: re.Match) -> str:
        naam = f"app-{len(scripts) + 1:02d}.js"
        scripts[naam] = klein(m.group(1))
        return f'<script src="{naam}"></script>'

    html = re.sub(r"<script\b[^>]*>(.*?)</script>", script, html, flags=re.S | re.I)
    out = {"index.html": '<link rel="stylesheet" href="stijl.css">\n' + klein(html), "stijl.css": klein("\n".join(css))}
    out.update(scripts)
    for naam, tekst in out.items():
        if len(tekst.encode()) > MAX:
            raise SystemExit(f"{naam} is te groot ({len(tekst.encode())} bytes); splits het verder op.")
    return out


def main() -> None:
    doel = Path(sys.argv[1] if len(sys.argv) > 1 else "dashboard/pagina")
    doel.mkdir(parents=True, exist_ok=True)
    for oud in doel.glob("*"):
        oud.unlink()
    delen = splits(Path("dashboard/index.html").read_text(encoding="utf-8"))
    for naam, tekst in delen.items():
        (doel / naam).write_text(tekst, encoding="utf-8")
        print(f"{naam:12} {len(tekst.encode()):>7} bytes")


if __name__ == "__main__":
    main()
