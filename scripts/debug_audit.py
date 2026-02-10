#!/usr/bin/env python3
"""Quick debug audit for repository artifacts.

Checks:
1. Duplicate files by content hash
2. Human-facing naming collisions such as "name 2.pdf"
3. Zip archive readability
"""

from __future__ import annotations

import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent.parent


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def artifact_files() -> list[Path]:
    return sorted(
        p for p in ROOT.iterdir() if p.is_file() and p.suffix.lower() in {".pdf", ".zip"}
    )


def normalized_name(path: Path) -> str:
    """Normalize duplicate suffixes like "file 2.pdf"."""
    return re.sub(r"\s+\d+(?=\.[A-Za-z0-9]+$)", "", path.name)


def check_duplicates(files: list[Path]) -> list[str]:
    by_hash: dict[str, list[Path]] = defaultdict(list)
    for f in files:
        by_hash[sha256(f)].append(f)

    findings: list[str] = []
    for same_files in by_hash.values():
        if len(same_files) > 1:
            findings.append(
                "duplicate-by-hash: " + ", ".join(str(p.name) for p in same_files)
            )
    return findings


def check_name_collisions(files: list[Path]) -> list[str]:
    by_norm: dict[str, list[Path]] = defaultdict(list)
    for f in files:
        by_norm[normalized_name(f)].append(f)

    findings: list[str] = []
    for same_files in by_norm.values():
        if len(same_files) > 1:
            findings.append(
                "naming-collision: " + ", ".join(str(p.name) for p in same_files)
            )
    return findings


def check_zip_integrity(files: list[Path]) -> list[str]:
    findings: list[str] = []
    for f in files:
        if f.suffix.lower() != ".zip":
            continue
        try:
            with zipfile.ZipFile(f) as zf:
                bad_member = zf.testzip()
                if bad_member:
                    findings.append(f"zip-corruption: {f.name} -> first bad member: {bad_member}")
        except zipfile.BadZipFile:
            findings.append(f"zip-corruption: {f.name} -> unreadable zip container")
    return findings


def main() -> int:
    files = artifact_files()
    if not files:
        print("No .pdf/.zip artifacts found.")
        return 0

    findings = []
    findings.extend(check_duplicates(files))
    findings.extend(check_name_collisions(files))
    findings.extend(check_zip_integrity(files))

    print(f"Scanned {len(files)} artifacts.")
    if not findings:
        print("No issues detected.")
        return 0

    print("Issues detected:")
    for item in findings:
        print(f"- {item}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
