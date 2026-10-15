#!/usr/bin/env bash
# Gedeeld opslaan voor alle workflows: alleen de opgegeven bestanden committen en pushen naar main.
# - Bij een botsing met een andere workflow wint deze (nieuwste) versie van de gegenereerde bestanden (-X theirs).
# - Een mislukte rebase wordt altijd afgebroken, zodat de volgende poging schoon begint.
# - Faalt het opslaan definitief, dan stopt de stap met een fout (de run wordt rood).
# Gebruik: bash scripts/opslaan.sh "commitbericht" pad1 pad2 ...
set -u
msg="$1"; shift
git config user.name "trend-agent[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
for f in "$@"; do
  if [ -e "$f" ]; then git add -- "$f"; fi
done
if git diff --cached --quiet; then echo "Niets gewijzigd."; exit 0; fi
git commit -q -m "$msg"
git stash push -u -q -m "niet opslaan" >/dev/null 2>&1 || true   # andere wijzigingen van deze run horen hier niet bij
for i in 1 2 3 4 5; do
  if git pull --rebase -X theirs -q origin main; then
    if git push -q origin HEAD:main; then break; fi
  else
    git rebase --abort >/dev/null 2>&1 || true
  fi
  echo "Opslaan mislukt (poging $i), opnieuw over 15 seconden..."; sleep 15
done
git fetch -q origin main
if [ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]; then echo "Opslaan definitief mislukt"; exit 1; fi
echo "Opgeslagen."
