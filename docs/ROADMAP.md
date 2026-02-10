# Puglar Buildout Roadmap

This roadmap translates the current repository into an executable build plan.

## Phase 0 — Repository Foundation (in progress)

- [x] Add a repeatable asset inventory generator (`scripts/generate_inventory.py`).
- [x] Create a machine-readable inventory with integrity hashes (`docs/ASSET_INVENTORY.md`).
- [x] Establish roadmap and operating docs for collaborators.

## Phase 1 — Content Structure

- [ ] Split assets into folders (`manuals/`, `cards/`, `archives/`) while preserving canonical names.
- [ ] Add short descriptions + audience labels to each item.
- [ ] Add release notes for each versioned document and archive.

## Phase 2 — Access + Discoverability

- [ ] Publish a browsable index page generated from the inventory.
- [ ] Add tags (e.g., training, doctrine, field-use, youth, seasonal).
- [ ] Provide mirrored download URLs and integrity verification snippets.

## Phase 3 — Quality + Maintenance

- [ ] Add CI check to regenerate inventory and fail on stale metadata.
- [ ] Add validation for duplicate names and unexpected file types.
- [ ] Define semantic release process for archive updates.

## Definition of done for the initial buildout

1. Contributors can run one command to refresh asset metadata.
2. The repository clearly communicates what exists and what is planned.
3. New assets can be added with minimal manual editing.
