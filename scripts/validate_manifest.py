#!/usr/bin/env python3
"""Validate catalog/manifest.json against repository files."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "catalog" / "manifest.json"


IGNORED_FILES = {
    "README.md",
    "PROJECT_TASKS.md",
}
IGNORED_SUFFIXES = {".py", ".md", ".json"}


def load_manifest(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def gather_repo_assets(root: Path) -> set[str]:
    assets: set[str] = set()
    for item in root.iterdir():
        if not item.is_file():
            continue
        if item.name in IGNORED_FILES:
            continue
        if item.suffix.lower() in IGNORED_SUFFIXES:
            continue
        assets.add(item.name)
    return assets


def main() -> int:
    manifest = load_manifest(MANIFEST_PATH)
    entries = manifest.get("assets", [])

    listed = {entry["filename"] for entry in entries}
    actual = gather_repo_assets(ROOT)

    missing_from_disk = sorted(listed - actual)
    missing_from_manifest = sorted(actual - listed)

    has_errors = False

    if missing_from_disk:
        has_errors = True
        print("ERROR: Listed in manifest but not found on disk:")
        for name in missing_from_disk:
            print(f"  - {name}")

    if missing_from_manifest:
        has_errors = True
        print("ERROR: Found on disk but not listed in manifest:")
        for name in missing_from_manifest:
            print(f"  - {name}")

    if has_errors:
        return 1

    print("Manifest validation passed: manifest and repository assets are in sync.")
    print(f"Asset count: {len(actual)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
