#!/usr/bin/env bash
# Copies the Connections game into this site from its own repository,
# bcollier/connections_demo, which stays the single source of truth for the
# player and the puzzle packs. The site keeps a plain copy so /connections/
# is static files like every other page (no iframe, no build step).
#
#   scripts/sync_connections.sh                       # from GitHub, latest main
#   scripts/sync_connections.sh ~/Code/connections_demo  # from a local checkout
#
# Then: python3 scripts/build.py, check /connections/, and open a pull request.
# Never edit the copied files here; change them in connections_demo and sync.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO="bcollier/connections_demo"
FILES=("player/player.js:js/connections/player.js" "packs/packs.js:js/connections/packs.js" "player/player.css:css/connections.css")
mkdir -p "$ROOT/js/connections"

if [ $# -ge 1 ]; then
  SRC="$(cd "$1" && pwd)"
  SHA="$(git -C "$SRC" rev-parse HEAD)"
  if [ -n "$(git -C "$SRC" status --porcelain -- player packs)" ]; then
    echo "warning: $SRC has uncommitted changes in player/ or packs/" >&2
  fi
  for pair in "${FILES[@]}"; do cp "$SRC/${pair%%:*}" "$ROOT/${pair##*:}"; done
else
  SHA="$(git ls-remote "https://github.com/$REPO.git" refs/heads/main | cut -f1)"
  for pair in "${FILES[@]}"; do
    curl -fsSL "https://raw.githubusercontent.com/$REPO/$SHA/${pair%%:*}" -o "$ROOT/${pair##*:}"
  done
fi

printf '%s\n' "Copied from https://github.com/$REPO at commit $SHA by scripts/sync_connections.sh." \
  "Do not edit these files here: change them in $REPO and sync again." > "$ROOT/js/connections/SOURCE.txt"
echo "synced Connections from $REPO@${SHA:0:7}"
