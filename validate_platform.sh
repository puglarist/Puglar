#!/usr/bin/env bash
set -euo pipefail

ITERATIONS="${1:-3}"

if ! [[ "$ITERATIONS" =~ ^[0-9]+$ ]] || [ "$ITERATIONS" -lt 1 ]; then
  echo "ERROR: iterations must be a positive integer" >&2
  exit 2
fi

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

mapfile -d '' DOCS < <(find . -maxdepth 1 -type f \( -name '*.pdf' -o -name '*.zip' \) -print0 | sort -z)

if [ "${#DOCS[@]}" -eq 0 ]; then
  echo "ERROR: no .pdf or .zip artifacts found"
  exit 1
fi

if [ ! -f README.md ]; then
  echo "ERROR: README.md missing"
  exit 1
fi

echo "Discovered ${#DOCS[@]} artifacts"

expected_hashes=""
for ((i=1; i<=ITERATIONS; i++)); do
  echo "---- iteration ${i}/${ITERATIONS} ----"
  hashes_file="$(mktemp)"

  for path in "${DOCS[@]}"; do
    rel="${path#./}"

    if [[ ! "$rel" =~ ^Puglar_ ]]; then
      echo "ERROR: artifact does not follow naming convention: $rel"
      exit 1
    fi

    size="$(wc -c < "$rel")"
    if [ "$size" -le 0 ]; then
      echo "ERROR: zero-byte artifact: $rel"
      exit 1
    fi

    if [[ "$rel" == *.pdf ]]; then
      python3 - "$rel" <<'PY'
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
data = path.read_bytes()
if not data.startswith(b"%PDF-"):
    print(f"ERROR: {path} missing PDF signature")
    raise SystemExit(1)
if b"%%EOF" not in data[-4096:]:
    print(f"ERROR: {path} missing EOF marker near file end")
    raise SystemExit(1)
PY
    elif [[ "$rel" == *.zip ]]; then
      unzip -tqq "$rel"
    fi

    python3 - "$rel" >> "$hashes_file" <<'PY'
import hashlib
import pathlib
import sys
p = pathlib.Path(sys.argv[1])
print(f"{hashlib.sha256(p.read_bytes()).hexdigest()}\t{p}")
PY
  done

  sort "$hashes_file" -o "$hashes_file"

  if [ -z "$expected_hashes" ]; then
    expected_hashes="$hashes_file"
  else
    if ! diff -u "$expected_hashes" "$hashes_file" > /dev/null; then
      echo "ERROR: checksum drift detected between iterations"
      diff -u "$expected_hashes" "$hashes_file" || true
      exit 1
    fi
    rm -f "$hashes_file"
  fi

  echo "iteration ${i} passed"
done

if [ -n "$expected_hashes" ]; then
  duplicates="$(cut -f1 "$expected_hashes" | sort | uniq -d || true)"
  if [ -n "$duplicates" ]; then
    echo "WARNING: duplicate artifacts detected by checksum:" >&2
    while IFS= read -r hash; do
      [ -z "$hash" ] && continue
      awk -F'\t' -v h="$hash" '$1==h {print "  - " $2}' "$expected_hashes" >&2
    done <<< "$duplicates"
  fi
fi

echo "All platform validation and compliance checks passed for ${ITERATIONS} iterations."
