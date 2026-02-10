# Puglar

Puglar is a doctrine/content archive containing field manuals, training cards, and bundled releases.

## Current status

The repository currently stores source PDFs/ZIPs at the root while foundational buildout work is being established.

### Buildout starter work completed

- Added a roadmap for planned delivery phases (`docs/ROADMAP.md`).
- Added a scripted asset inventory generator (`scripts/generate_inventory.py`).
- Added generated asset metadata with file hashes (`docs/ASSET_INVENTORY.md`).

## Quickstart

Regenerate the asset inventory:

```bash
python3 scripts/generate_inventory.py --root . --output docs/ASSET_INVENTORY.md
```

Then review:

- `docs/ASSET_INVENTORY.md` for current files, sizes, and SHA-256 digests.
- `docs/ROADMAP.md` for implementation phases and next steps.

## Near-term plan

1. Reorganize assets into typed folders.
2. Add per-file descriptions and intended audiences.
3. Add automated validation so metadata stays fresh.
