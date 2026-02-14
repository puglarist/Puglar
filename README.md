# Puglar

## Debug patch (artifact audit)

This repository is artifact-heavy (PDF + ZIP deliverables), so quick debugging focuses on package integrity and accidental duplicates.

Run:

```bash
python3 scripts/debug_audit.py
```

What it checks:

- Duplicate files by SHA-256 content hash
- Naming collisions (for example `file.pdf` and `file 2.pdf`)
- ZIP readability/corruption (`zipfile.testzip()`)

Exit code behavior:

- `0`: no issues detected
- `1`: at least one issue detected
