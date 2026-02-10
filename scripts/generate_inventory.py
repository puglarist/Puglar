#!/usr/bin/env python3
"""Generate a markdown inventory of the repository's PDF/ZIP assets."""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path


ASSET_EXTENSIONS = {".pdf", ".zip"}


@dataclass(frozen=True)
class Asset:
    path: Path
    size_bytes: int
    sha256: str

    @property
    def size_mb(self) -> float:
        return self.size_bytes / (1024 * 1024)


def find_assets(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.iterdir()
        if path.is_file() and path.suffix.lower() in ASSET_EXTENSIONS
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_assets(root: Path) -> list[Asset]:
    assets: list[Asset] = []
    for path in find_assets(root):
        assets.append(
            Asset(
                path=path,
                size_bytes=path.stat().st_size,
                sha256=sha256_file(path),
            )
        )
    return assets


def render_markdown(assets: list[Asset], generated_from: Path) -> str:
    total_bytes = sum(asset.size_bytes for asset in assets)
    lines = [
        "# Asset Inventory",
        "",
        f"Generated from: `{generated_from}`",
        "",
        f"Total assets: **{len(assets)}**",
        f"Total size: **{total_bytes / (1024 * 1024):.2f} MB**",
        "",
        "## Files",
        "",
        "| File | Type | Size (MB) | SHA-256 |",
        "|---|---:|---:|---|",
    ]

    for asset in assets:
        lines.append(
            f"| `{asset.path.name}` | `{asset.path.suffix.lower()}` | {asset.size_mb:.2f} | `{asset.sha256}` |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Regenerate this file after adding/removing assets.",
            "- Hashes allow integrity checks across mirrors and releases.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Repository root to scan (default: current directory)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/ASSET_INVENTORY.md"),
        help="Output markdown path (default: docs/ASSET_INVENTORY.md)",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    assets = collect_assets(root)

    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_markdown(assets, root), encoding="utf-8")
    print(f"Wrote {output} with {len(assets)} assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
