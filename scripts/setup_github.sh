#!/usr/bin/env bash
# Create the GitHub repo for this site, push it, and turn on GitHub Pages.
#
#   ./scripts/setup_github.sh                    # uses defaults below
#   ./scripts/setup_github.sh myuser my-repo     # override owner / repo
#
# Auth: either `gh auth login` first, or export GITHUB_TOKEN with 'repo' scope.

set -euo pipefail

OWNER="${1:-bcollier}"
REPO="${2:-ben.collier.phd}"
BRANCH="main"

cd "$(dirname "$0")/.."

echo "==> Target: https://github.com/${OWNER}/${REPO}"

have_gh_auth() { command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; }

create_with_gh() {
  echo "==> Creating repo with gh"
  gh repo create "${OWNER}/${REPO}" --public --disable-wiki --source=. --remote=github --push
}

create_with_api() {
  echo "==> Creating repo with the GitHub API"
  local auth_user payload endpoint
  auth_user="$(curl -fsS -H "Authorization: Bearer ${GITHUB_TOKEN}" https://api.github.com/user | sed -n 's/.*"login": *"\([^"]*\)".*/\1/p' | head -1)"
  payload="{\"name\":\"${REPO}\",\"private\":false,\"has_wiki\":false,\"description\":\"Faculty site for Ben Collier — ben.collier.phd\"}"

  if [ "${auth_user}" = "${OWNER}" ]; then
    endpoint="https://api.github.com/user/repos"
  else
    endpoint="https://api.github.com/orgs/${OWNER}/repos"
  fi

  curl -fsS -X POST "${endpoint}" \
    -H "Authorization: Bearer ${GITHUB_TOKEN}" \
    -H "Accept: application/vnd.github+json" \
    -d "${payload}" >/dev/null || echo "   (repo may already exist — continuing)"

  git remote remove github 2>/dev/null || true
  git remote add github "https://x-access-token:${GITHUB_TOKEN}@github.com/${OWNER}/${REPO}.git"
  git push -u github "${BRANCH}"
}

enable_pages() {
  local token="${GITHUB_TOKEN:-}"
  if [ -z "${token}" ] && have_gh_auth; then
    token="$(gh auth token)"
  fi
  [ -z "${token}" ] && { echo "==> Skipping Pages API (no token); enable it in Settings → Pages"; return; }

  echo "==> Enabling GitHub Pages from ${BRANCH} / root"
  curl -fsS -X POST "https://api.github.com/repos/${OWNER}/${REPO}/pages" \
    -H "Authorization: Bearer ${token}" \
    -H "Accept: application/vnd.github+json" \
    -d "{\"source\":{\"branch\":\"${BRANCH}\",\"path\":\"/\"}}" >/dev/null \
    || echo "   (Pages may already be enabled — continuing)"
}

if have_gh_auth; then
  create_with_gh
elif [ -n "${GITHUB_TOKEN:-}" ]; then
  create_with_api
else
  cat <<'EOF'
No GitHub credentials found.

Do one of these first, then re-run this script:

  gh auth login                       # interactive, recommended locally
  export GITHUB_TOKEN=ghp_xxx         # a token with 'repo' scope

Or create the repo by hand at https://github.com/new (name: ben.collier.phd),
then:

  git remote add github https://github.com/bcollier/ben.collier.phd.git
  git push -u github main
EOF
  exit 1
fi

enable_pages

cat <<EOF

Done.

  Repo:   https://github.com/${OWNER}/${REPO}
  Pages:  https://${OWNER}.github.io/${REPO}/     <- hand this in for class

No custom domain is attached yet, on purpose: attaching one makes GitHub
redirect the github.io URL, which would break the course link.

When DNS for collier.phd is ready:

  1. CNAME   ben    ${OWNER}.github.io
  2. Redirect collier.phd -> https://ben.collier.phd/   (301, at your DNS host)
  3. ./scripts/enable_domain.sh ${OWNER} ${REPO}
EOF
