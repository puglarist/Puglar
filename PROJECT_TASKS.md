# Puglar Build Task List

## Current Repository State
- Repository currently contains doctrine/training PDFs and ZIP archives, with only a minimal `README.md`.
- No structured catalog, metadata index, or validation tooling exists yet.
- No onboarding or maintenance workflow is documented.

## What’s Missing
1. **Asset index and metadata**
   - No machine-readable manifest for all PDFs/ZIPs.
   - No categories, descriptions, or version tracking.
2. **Basic validation tooling**
   - No quick way to verify referenced files actually exist.
   - No repeatable integrity check for future additions/removals.
3. **Contributor workflow docs**
   - No guidance for adding new doctrine assets.
   - No task tracking for phased build-out.
4. **Release/readiness structure**
   - No checklist for publishing a coherent release bundle.
   - No status reporting on what has started vs. pending.

## What Needs Done (Prioritized)

### Phase 1 — Foundation (start now)
- [x] Create this task document with scope + priorities.
- [ ] Expand README with purpose, structure, and maintenance flow.
- [ ] Create a machine-readable asset manifest (`catalog/manifest.json`).
- [ ] Add a validation script to verify manifest/file consistency.

### Phase 2 — Curation
- [ ] Add short descriptions/tags for each doctrine asset.
- [ ] Add version/edition fields where known (v1/v2/v4/v5, etc.).
- [ ] Define naming conventions for future file drops.

### Phase 3 — Operational Readiness
- [ ] Add release checklist for publishing complete packs.
- [ ] Add changelog policy for major doctrine updates.
- [ ] Add optional checksum support for archive integrity.

## Build-Out Started in This Pass
- Started **Phase 1** by creating project task tracking.
- Next immediate build steps in this pass:
  1. Expand README.
  2. Introduce `catalog/manifest.json`.
  3. Add and run a manifest validator.
