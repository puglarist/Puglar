# Puglar

## Debug Patch Release (2026-02)

This repository currently ships doctrine assets (PDF/ZIP) rather than executable code, so this debugging patch focuses on **asset integrity checks** and **support diagnostics** for downstream users.

### Patch highlights
- Added a recommended integrity-validation workflow before sharing or printing assets.
- Added quick commands to detect accidental file corruption during transfer.
- Added a minimal triage checklist for users reporting broken or unreadable files.

### Integrity validation
From the repository root:

```bash
# List file sizes and modified times for quick visual checks
find . -maxdepth 1 -type f \( -name '*.pdf' -o -name '*.zip' \) -print0 | xargs -0 ls -lh

# Generate checksums for release verification
sha256sum *.pdf *.zip > RELEASE_CHECKSUMS.sha256

# Verify checksums after transfer
sha256sum -c RELEASE_CHECKSUMS.sha256
```

### Debug triage checklist
When someone reports a bad asset:
1. Confirm the file extension is unchanged (`.pdf` / `.zip`).
2. Recompute checksum and compare with `RELEASE_CHECKSUMS.sha256`.
3. Re-download or re-copy the file if checksum fails.
4. If checksum passes but the file still won't open, test with an alternate reader and report the exact file name.

### Release operator notes
- Regenerate `RELEASE_CHECKSUMS.sha256` whenever any PDF/ZIP changes.
- Commit checksum updates in the same commit as asset updates to keep releases reproducible.
