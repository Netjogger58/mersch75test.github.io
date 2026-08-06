#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

if [[ "$CURRENT_BRANCH" == "main" ]]; then
  echo "Refusing to auto-push directly to main. Switch to feature/recovery branch."
  exit 1
fi

scripts/preflight_check.sh
git add -A

if git diff --cached --quiet; then
  echo "No staged changes to commit."
  exit 0
fi

COMMIT_MSG="${1:-Update $(date '+%Y-%m-%d %H:%M:%S')}"
git commit -m "$COMMIT_MSG"
git push -u origin "$CURRENT_BRANCH"
