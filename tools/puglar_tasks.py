#!/usr/bin/env python3
"""Task utility for the Puglar document repository.

Helps with:
- Fast asset inventory (including sizes and modified time)
- Duplicate detection by SHA-256 digest
- Lightweight integrity checks for expected document families
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
ASSET_EXTENSIONS = {".pdf", ".zip"}


@dataclasses.dataclass(frozen=True)
class Asset:
    path: Path
    size: int
    suffix: str

    @property
    def stem(self) -> str:
        return self.path.stem


def discover_assets(root: Path = ROOT) -> list[Asset]:
    assets: list[Asset] = []
    for path in root.iterdir():
        if not path.is_file() or path.suffix.lower() not in ASSET_EXTENSIONS:
            continue
        stat = path.stat()
        assets.append(Asset(path=path, size=stat.st_size, suffix=path.suffix.lower()))
    return sorted(assets, key=lambda item: item.path.name.lower())


def sha256_of(path: Path, block_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(block_size):
            digest.update(chunk)
    return digest.hexdigest()


def command_inventory(args: argparse.Namespace) -> int:
    assets = discover_assets()

    payload = [
        {
            "name": asset.path.name,
            "type": asset.suffix.removeprefix("."),
            "size_bytes": asset.size,
            "size_mb": round(asset.size / (1024 * 1024), 3),
        }
        for asset in assets
    ]

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        total_bytes = sum(item["size_bytes"] for item in payload)
        print(f"Assets: {len(payload)}")
        print(f"Total size: {round(total_bytes / (1024 * 1024), 2)} MB")
        for item in payload:
            print(f"- {item['name']} ({item['size_mb']} MB)")
    return 0


def group_by_digest(paths: Iterable[Path]) -> dict[str, list[Path]]:
    groups: dict[str, list[Path]] = {}
    for path in paths:
        digest = sha256_of(path)
        groups.setdefault(digest, []).append(path)
    return groups


def command_duplicates(_: argparse.Namespace) -> int:
    assets = discover_assets()
    groups = group_by_digest([asset.path for asset in assets])
    duplicates = {k: v for k, v in groups.items() if len(v) > 1}

    if not duplicates:
        print("No duplicate binary files detected.")
        return 0

    print("Duplicate binary files detected:")
    for digest, paths in duplicates.items():
        print(f"- sha256={digest}")
        for path in paths:
            print(f"  - {path.name}")
    return 1


def canonical_family_name(filename: str) -> str:
    normalized = filename.lower()
    normalized = re.sub(r"\s+\d+(?=\.pdf$)", "", normalized)
    normalized = normalized.replace("_v1", "")
    normalized = normalized.replace("_v2", "")
    normalized = normalized.replace("_v3", "")
    normalized = normalized.replace("_v4", "")
    normalized = normalized.replace("_v5", "")
    normalized = normalized.replace(" 2", "")
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def command_check(args: argparse.Namespace) -> int:
    assets = discover_assets()

    errors: list[str] = []
    warnings: list[str] = []
    if not assets:
        errors.append("No .pdf or .zip assets found at repository root.")

    by_family: dict[str, list[Asset]] = {}
    for asset in assets:
        key = canonical_family_name(asset.path.name)
        by_family.setdefault(key, []).append(asset)

    for family, members in sorted(by_family.items()):
        if len(members) > 1:
            names = ", ".join(item.path.name for item in members)
            warnings.append(f"Multiple files in the same filename family '{family}': {names}")

    for asset in assets:
        if asset.size == 0:
            errors.append(f"Zero-byte file detected: {asset.path.name}")

    if errors:
        print("Integrity check found errors:")
        for issue in errors:
            print(f"- {issue}")
        return 1

    if warnings:
        print("Integrity check warnings:")
        for issue in warnings:
            print(f"- {issue}")
        return 1 if args.strict else 0

    print("Integrity check passed.")
    return 0


def command_find(args: argparse.Namespace) -> int:
    assets = discover_assets()
    query = args.query.lower().strip()
    matches = [asset for asset in assets if query in asset.path.name.lower()]

    if not matches:
        print(f"No assets matched query: {args.query!r}")
        return 1

    for asset in matches:
        print(asset.path.name)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fast local task runner for Puglar docs.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    inventory = subparsers.add_parser("inventory", help="List assets and sizes.")
    inventory.add_argument("--json", action="store_true", help="Emit JSON output.")
    inventory.set_defaults(func=command_inventory)

    duplicates = subparsers.add_parser("duplicates", help="Find duplicate binaries by digest.")
    duplicates.set_defaults(func=command_duplicates)

    check = subparsers.add_parser("check", help="Run lightweight integrity checks.")
    check.add_argument("--strict", action="store_true", help="Treat warnings as failures.")
    check.set_defaults(func=command_check)

    find = subparsers.add_parser("find", help="Find assets by substring.")
    find.add_argument("query", help="Case-insensitive filename substring.")
    find.set_defaults(func=command_find)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
