#!/usr/bin/env bash
# Attach ben.collier.phd to the GitHub Pages site. Run this ONLY after DNS resolves.
#
#   ./scripts/enable_domain.sh [owner] [repo]
#
# Attaching a custom domain makes GitHub redirect the <owner>.github.io URL to
# the domain. If your class still needs the github.io link, wait.

set -euo pipefail

OWNER="${1:-bcollier}"
REPO="${2:-ben.collier.phd}"
DOMAIN="ben.collier.phd"

cd "$(dirname "$0")/.."

echo "==> Checking DNS for ${DOMAIN}"
if command -v dig >/dev/null 2>&1; then
  dig +short "${DOMAIN}" || true
  if [ -z "$(dig +short "${DOMAIN}")" ]; then
    echo "!! ${DOMAIN} does not resolve yet. Add this record first:"
    echo "     CNAME   ben   ${OWNER}.github.io"
    read -r -p "Continue anyway? [y/N] " reply
    [ "${reply}" = "y" ] || exit 1
  fi
fi

echo "==> Writing CNAME"
echo "${DOMAIN}" > CNAME

echo "==> Pointing absolute URLs at https://${DOMAIN}"
# Canonical tags, Open Graph URLs, the sitemap, and the feed all carry absolute
# URLs. They must move to the custom domain in the same commit as the CNAME, or
# the live site advertises the github.io address as canonical.
python3 - <<'PY'
import json
from pathlib import Path

path = Path("data/site.json")
site = json.loads(path.read_text(encoding="utf-8"))
site["domain_live"] = True
path.write_text(json.dumps(site, indent=2) + "\n", encoding="utf-8")
print("   data/site.json: domain_live = true")
PY
python3 scripts/build.py

git add CNAME data/site.json .
git commit -m "Attach custom domain ${DOMAIN}" || echo "   (nothing to commit)"

for remote in github origin; do
  if git remote get-url "${remote}" >/dev/null 2>&1; then
    git push "${remote}" HEAD && break
  fi
done

TOKEN="${GITHUB_TOKEN:-}"
if [ -z "${TOKEN}" ] && command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  TOKEN="$(gh auth token)"
fi

if [ -n "${TOKEN}" ]; then
  echo "==> Setting the Pages custom domain via API"
  curl -fsS -X PUT "https://api.github.com/repos/${OWNER}/${REPO}/pages" \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Accept: application/vnd.github+json" \
    -d "{\"cname\":\"${DOMAIN}\",\"https_enforced\":true}" >/dev/null \
    || echo "   (set it manually in Settings → Pages)"
else
  echo "==> No token: set the domain in Settings → Pages, then tick Enforce HTTPS"
fi

echo
echo "Live at https://${DOMAIN}/ once GitHub finishes the DNS check."
echo "Remember the apex redirect: collier.phd -> https://${DOMAIN}/"
