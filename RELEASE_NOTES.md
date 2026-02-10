# Release Notes

## 2026-02 Major Patch Release

### Added
- Introduced `scripts/generate_catalog.py` to produce a deterministic artifact catalog for all top-level PDF/ZIP files.
- Added generated `CATALOG.md` containing:
  - artifact counts by type,
  - total distribution size,
  - per-file SHA-256 checksums and size.

### Changed
- Expanded `README.md` from a placeholder to a complete release/operations guide with:
  - repository content overview,
  - checksum verification instructions,
  - catalog regeneration command,
  - publishing checklist.

### Why this matters
These patches significantly improve release confidence and reproducibility by making artifact inventory and integrity verification first-class, documented workflows.
