#!/usr/bin/env python3
"""Regenerate ASSET_MANIFEST.md with file sizes and SHA-256 checksums."""

from __future__ import annotations

import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = REPO_ROOT / "ASSET_MANIFEST.md"
EXTENSIONS = {".pdf", ".zip"}


def sha256sum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    assets = sorted(
        [
            path
            for path in REPO_ROOT.iterdir()
            if path.is_file() and path.suffix.lower() in EXTENSIONS
        ],
        key=lambda p: p.name.lower(),
    )

    lines = [
        "# Asset Manifest",
        "",
        "Machine-generated inventory of distributable assets with sizes and SHA-256 checksums.",
        "",
        "| File | Type | Size (MB) | SHA-256 |",
        "|---|---:|---:|---|",
    ]

    for path in assets:
        size_mb = path.stat().st_size / (1024 * 1024)
        lines.append(
            f"| `{path.name}` | {path.suffix.lower().lstrip('.')} | {size_mb:.2f} | `{sha256sum(path)}` |"
        )

    lines.extend(["", f"Total assets: **{len(assets)}**", ""])
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated {OUTPUT.relative_to(REPO_ROOT)} with {len(assets)} assets")


if __name__ == "__main__":
    main()
