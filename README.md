# Puglar

This repository is an artifact platform containing doctrine PDFs and ZIP archives.

## Testing and Compliance

To support repeated, iterative validation, this repo now includes an automated platform verifier:

- Script: `./validate_platform.sh`
- Default mode: runs 3 full validation passes
- Example intensive run: `./validate_platform.sh 4`

### What the validator checks each iteration

1. Discovers all `.pdf` and `.zip` artifacts in the repo root.
2. Confirms artifact naming convention (`Puglar_*`).
3. Confirms every artifact is non-empty.
4. Validates PDFs by checking:
   - `%PDF-` file signature
   - `%%EOF` marker near the end of file
5. Validates ZIP integrity with `unzip -tqq`.
6. Calculates SHA-256 checksums for all artifacts.
7. Compares checksums between iterations to detect drift.

### Compliance checks

The validation flow performs compliance checks for:

- Required repository metadata (`README.md` present)
- File naming policy (`Puglar_*`)
- File integrity (PDF/ZIP structural checks)
- Content stability across repeated test runs (checksum consistency)

If two files have identical content, the script reports this as a warning (not a hard failure), which is useful for spotting duplicates intentionally or unintentionally included in the platform.

## Usage

```bash
./validate_platform.sh
./validate_platform.sh 5
```

A successful run ends with:

`All platform validation and compliance checks passed for <N> iterations.`
