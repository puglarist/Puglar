# Puglar

This repository stores the Puglar doctrine document set (PDF handbooks/cards and ZIP archives).

## Debugging / integrity checks

If files fail to open or extract, run the built-in validation script:

```bash
./validate_assets.sh
```

What it verifies:

- Every `*.pdf` file is checked via `pdfinfo` (preferred), `file`, or a fallback PDF signature check.
- Every `*.zip` file passes `unzip -t` archive integrity tests.

## Requirements

- `bash`
- `unzip`
- Optional: `pdfinfo` (from poppler)
- Optional: `file`
