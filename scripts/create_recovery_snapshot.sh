#!/usr/bin/env bash
set -euo pipefail

STAMP="${1:-$(date +%Y-%m-%d-%H%M)}"
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
CURRENT_SHA="$(git rev-parse HEAD)"
REMOTE="${2:-origin}"

LOCAL_NAME="backup/${STAMP}-${CURRENT_BRANCH}"
REMOTE_NAME="backup/${STAMP}-${CURRENT_BRANCH}"

echo "Creating local backup branch: $LOCAL_NAME -> $CURRENT_SHA"
git branch "$LOCAL_NAME" "$CURRENT_SHA"

echo "Pushing backup branch to $REMOTE/$REMOTE_NAME"
git push "$REMOTE" "$LOCAL_NAME:$REMOTE_NAME"

echo "Backup created: $REMOTE_NAME"
