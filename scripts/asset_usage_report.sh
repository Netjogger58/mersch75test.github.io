#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

OUT_DIR="data"
OUT_FILE="$OUT_DIR/asset-usage-report.tsv"
mkdir -p "$OUT_DIR"

# Extract Media references from HTML/CSS/JS, normalize URL encoding for spaces.
rg -No "Media[^\"') ]+|Media/[^\"')]+" --glob '*.html' --glob '*.css' --glob '*.js' \
  | sed "s/%20/ /g" \
  | sed 's#^\./##' \
  | sort \
  | uniq -c \
  | awk '{count=$1; $1=""; sub(/^ +/, "", $0); print count"\t"$0}' \
  > "$OUT_FILE"

echo "Wrote $OUT_FILE"
