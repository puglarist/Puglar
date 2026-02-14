# Puglar

This repository now includes a lightweight build step to generate an inventory of doctrine artifacts (PDF/ZIP files).

## Build

```bash
make build
```

This generates:

- `catalog.json` (machine-readable artifact metadata)
- `CATALOG.md` (human-readable artifact table)

## Clean generated outputs

```bash
make clean
```
