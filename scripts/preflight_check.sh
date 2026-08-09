#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

node scripts/check_local_links.js
node scripts/check_media_policy.js

echo "Preflight checks passed."
