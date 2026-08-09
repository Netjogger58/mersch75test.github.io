#!/usr/bin/env bash
set -euo pipefail

BASE_BRANCH="${1:-main}"
STAMP="${2:-$(date +%Y-%m-%d)}"
NEW_BRANCH="recovery/${STAMP}-integration"

git fetch origin --prune
git checkout -B "$NEW_BRANCH" "origin/$BASE_BRANCH"
git push -u origin "$NEW_BRANCH"

echo "Created integration branch: $NEW_BRANCH"
