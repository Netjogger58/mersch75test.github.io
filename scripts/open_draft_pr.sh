#!/usr/bin/env bash
set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI is required."
  exit 1
fi

BASE_BRANCH="${1:-main}"
TITLE="${2:-WIP: continue work}"

CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

if [[ "$CURRENT_BRANCH" == "$BASE_BRANCH" ]]; then
  echo "Refusing to open PR from base branch '$BASE_BRANCH'. Switch to a feature/recovery branch."
  exit 1
fi

gh pr create --draft --base "$BASE_BRANCH" --head "$CURRENT_BRANCH" --title "$TITLE" --fill
