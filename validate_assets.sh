#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$root_dir"

echo "Checking PDF files..."
pdf_count=0
while IFS= read -r -d '' pdf; do
  pdf_count=$((pdf_count + 1))
  if command -v pdfinfo >/dev/null 2>&1; then
    pdfinfo "$pdf" >/dev/null
  elif command -v file >/dev/null 2>&1; then
    file "$pdf" | grep -q 'PDF document'
  else
    # Minimal signature check fallback if neither tool exists
    head -c 5 "$pdf" | grep -q '%PDF-'
  fi
  echo "  OK: $pdf"
done < <(find . -maxdepth 1 -type f -name '*.pdf' -print0 | sort -z)

echo "Checking ZIP files..."
zip_count=0
while IFS= read -r -d '' zipf; do
  zip_count=$((zip_count + 1))
  unzip -t "$zipf" >/dev/null
  echo "  OK: $zipf"
done < <(find . -maxdepth 1 -type f -name '*.zip' -print0 | sort -z)

echo ""
echo "Summary"
echo "  PDFs checked: $pdf_count"
echo "  ZIPs checked: $zip_count"
echo "  All checks passed."
