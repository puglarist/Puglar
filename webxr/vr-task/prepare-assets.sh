#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
INDEX_FILE="$ROOT_DIR/webxr/vr-task/asset-index.json"
OUT_DIR="$ROOT_DIR/webxr/vr-task/staging"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required to parse asset-index.json" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

python3 - "$INDEX_FILE" <<'PY' | while IFS='|' read -r src slug; do
import json
import re
import sys
from pathlib import Path

index_file = Path(sys.argv[1])
data = json.loads(index_file.read_text())
for source in data.get("sources", []):
    slug = re.sub(r"[^a-z0-9]+", "-", source.lower()).strip("-")
    print(f"{source}|{slug}")
PY
  src_path="$ROOT_DIR/$src"
  dst_path="$OUT_DIR/$slug"

  if [[ ! -f "$src_path" ]]; then
    echo "warning: missing source asset '$src'" >&2
    continue
  fi

  cp -f "$src_path" "$dst_path"
  echo "staged: $src -> webxr/vr-task/staging/$slug"
done

echo "Done. Assets staged in: $OUT_DIR"
