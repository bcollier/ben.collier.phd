#!/usr/bin/env bash
# Create the GitHub repo for this site, push it, and turn on GitHub Pages.
#
#   ./scripts/setup_github.sh                    # uses defaults below
#   ./scripts/setup_github.sh myuser my-repo     # override owner / repo
#
# Auth, in order of preference:
#   export GITHUB_TOKEN=...   a token that can create repos (see below)
#   gh auth login             interactive
#
# If the repo already exists, this script skips creation and just pushes.

set -euo pipefail

OWNER="${1:-bcollier}"
REPO="${2:-ben.collier.phd}"
BRANCH="main"
API="https://api.github.com"

cd "$(dirname "$0")/.."

echo "==> Target: https://github.com/${OWNER}/${REPO}"

token=""
if [ -n "${GITHUB_TOKEN:-}" ]; then
  token="${GITHUB_TOKEN}"
elif command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  token="$(gh auth token 2>/dev/null || true)"
fi

if [ -z "${token}" ]; then
  cat <<'EOF'
No GitHub credentials found. Do one of these, then re-run:

  gh auth login                  # interactive, easiest locally
  export GITHUB_TOKEN=ghp_xxx    # classic token with 'repo' scope

Or create the repo by hand at https://github.com/new (name: ben.collier.phd)
and re-run this script — it will detect the repo and just push.
EOF
  exit 1
fi

api() {
  # api <method> <path> [body]  -> prints "HTTP_STATUS<newline>BODY"
  local method="$1" path="$2" body="${3:-}"
  local args=(-sS -w '\n%{http_code}' -X "${method}" "${API}${path}"
              -H "Authorization: Bearer ${token}"
              -H "Accept: application/vnd.github+json"
              -H "X-GitHub-Api-Version: 2022-11-28")
  [ -n "${body}" ] && args+=(-d "${body}")
  local out status
  out="$(curl "${args[@]}")"
  status="${out##*$'\n'}"
  printf '%s\n%s' "${status}" "${out%$'\n'*}"
}

status_of() { printf '%s' "$1" | head -n 1; }

repo_exists() {
  local resp
  resp="$(api GET "/repos/${OWNER}/${REPO}")"
  [ "$(status_of "${resp}")" = "200" ]
}

explain_creation_failure() {
  cat <<EOF

!! The token cannot create repositories.

GitHub requires the "Administration: Read and write" permission for
POST /user/repos. Contents and Pages are not enough. Fine-grained tokens
also cannot create repos inside an organization at all.

Pick whichever is less annoying:

  A. Create it in the browser (30 seconds, no new token)
       https://github.com/new
       Name: ${REPO}   Visibility: Public   Do NOT add a README
     Then re-run this script. It will detect the repo and push.

  B. Edit the token to add Administration
       https://github.com/settings/personal-access-tokens
       -> your token -> Repository permissions
       -> Administration: Read and write -> Save
     Then re-run this script.

  C. Use a classic token with the whole 'repo' scope
       https://github.com/settings/tokens

EOF
}

if repo_exists; then
  echo "==> Repo already exists, skipping creation"
else
  echo "==> Creating repo"
  payload="{\"name\":\"${REPO}\",\"private\":false,\"has_wiki\":false,\"has_projects\":false,\"description\":\"Faculty site for Ben Collier — ben.collier.phd\"}"
  resp="$(api POST "/user/repos" "${payload}")"
  code="$(status_of "${resp}")"
  case "${code}" in
    201) echo "    created" ;;
    403)
      explain_creation_failure
      exit 1
      ;;
    422) echo "    already exists (422), continuing" ;;
    *)
      echo "!! Unexpected response ${code} creating the repo:"
      printf '%s\n' "${resp}" | tail -n +2 | head -c 600
      echo
      exit 1
      ;;
  esac
fi

echo "==> Pushing ${BRANCH}"
git remote remove github 2>/dev/null || true
git remote add github "https://github.com/${OWNER}/${REPO}.git"
# Send the token via a header so it never lands in .git/config or the remote URL.
git -c "http.https://github.com/.extraheader=Authorization: Bearer ${token}" \
    push -u github "${BRANCH}"

echo "==> Enabling GitHub Pages from ${BRANCH} / root"
resp="$(api POST "/repos/${OWNER}/${REPO}/pages" "{\"source\":{\"branch\":\"${BRANCH}\",\"path\":\"/\"}}")"
case "$(status_of "${resp}")" in
  201|409) echo "    Pages is on" ;;
  403) echo "    !! token lacks Pages: write — turn it on in Settings → Pages" ;;
  *)    echo "    !! could not enable Pages automatically; do it in Settings → Pages" ;;
esac

cat <<EOF

Done.

  Repo:   https://github.com/${OWNER}/${REPO}
  Pages:  https://${OWNER}.github.io/${REPO}/     <- hand this in for class

Pages can take a minute or two to build the first time.

No custom domain is attached yet, on purpose: attaching one makes GitHub
redirect the github.io URL, which would break the course link.

When DNS for collier.phd is ready:

  1. CNAME   ben    ${OWNER}.github.io
  2. Redirect collier.phd -> https://ben.collier.phd/   (301, at your DNS host)
  3. ./scripts/enable_domain.sh ${OWNER} ${REPO}
EOF
