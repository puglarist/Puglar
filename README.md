# Puglar

Puglar is a doctrine distribution repository containing field manuals, training cards, and archive bundles in PDF/ZIP format.

## Major Patch Release

This release introduces repository-level quality and release-management improvements:

- A full machine-generated `CATALOG.md` with SHA-256 checksums, file counts, and total package size.
- A reproducible catalog generation script in `scripts/generate_catalog.py`.
- Structured release notes in `RELEASE_NOTES.md` to make future patch cycles more trackable.

## Repository Contents

- `*.pdf`: standalone manuals, training cards, and printable assets.
- `*.zip`: bundled doctrine archives.
- `CATALOG.md`: generated manifest with checksums and sizes.
- `scripts/generate_catalog.py`: generator for `CATALOG.md`.
- `RELEASE_NOTES.md`: human-readable patch summary.

## Integrity Verification

To verify a specific file manually:

```bash
sha256sum "Puglar_Handbook.pdf"
```

Compare the output hash against `CATALOG.md`.

## Regenerating the Catalog

```bash
python3 scripts/generate_catalog.py
```

## Publishing Checklist

1. Add or update PDFs/ZIPs.
2. Regenerate `CATALOG.md`.
3. Update `RELEASE_NOTES.md`.
4. Commit and tag the release.
