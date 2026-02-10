# Puglar

A doctrine asset repository containing handbooks, field cards, training cards, and archive bundles.

## Repository Structure
- Root: source doctrine PDFs and ZIP bundles.
- `PROJECT_TASKS.md`: active planning document with missing-items analysis and phased execution.
- `catalog/manifest.json`: machine-readable metadata and categorization for repository assets.
- `scripts/validate_manifest.py`: validator that checks manifest entries against files on disk.

## Current Status
This repository has started a foundational build-out to improve maintainability and discoverability:
1. Task list and gap analysis established.
2. Manifest creation introduced.
3. Validation workflow added.

## Maintenance Workflow
1. Add new asset files to the repository root (or a future dedicated assets folder).
2. Update `catalog/manifest.json` with:
   - `filename`
   - `type`
   - `category`
   - `version` (when known)
   - `notes`
3. Run validation:
   ```bash
   python3 scripts/validate_manifest.py
   ```
4. Resolve any missing/extra file warnings before commit.

## Next Priorities
See `PROJECT_TASKS.md` for the phased plan and outstanding work.
