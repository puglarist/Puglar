# Puglar

## Build

This repository now includes a simple packaging build.

### What it does
- Collects all top-level `.pdf` and `.zip` doctrine files.
- Copies them into `dist/puglar-package/`.
- Generates `SHA256SUMS.txt` for integrity verification.
- Produces a timestamped archive: `dist/puglar-build-<UTC_TIMESTAMP>.tar.gz`.

### Run

```bash
make build
```

### Clean

```bash
make clean
```
