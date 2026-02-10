# Puglar

This repository is a document bundle for the Puglar doctrine PDFs and archives.

## Faster local tasks

Use the task helper to quickly inspect, debug, and maintain the asset set:

```bash
python3 tools/puglar_tasks.py inventory
python3 tools/puglar_tasks.py inventory --json
python3 tools/puglar_tasks.py find handbook
python3 tools/puglar_tasks.py duplicates
python3 tools/puglar_tasks.py check
python3 tools/puglar_tasks.py check --strict
```

### What each command does

- `inventory`: Lists all top-level `.pdf` and `.zip` assets and reports aggregate size.
- `find <query>`: Fast case-insensitive filename lookup.
- `duplicates`: Compares file digests to detect exact binary duplicates.
- `check`: Runs lightweight integrity checks. Hard failures include missing/empty assets; filename-family collisions are warnings unless `--strict` is used.

## Notes

- The helper intentionally scans only repository-root assets to keep checks fast.
- No external dependencies are required; it uses Python standard library only.
