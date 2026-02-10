#!/usr/bin/env python3
"""Build a simple Markdown catalog from data/gta6_weapons.json."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "gta6_weapons.json"
OUTPUT_FILE = ROOT / "data" / "gta6_weapons.md"


def main() -> None:
    payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    weapons = payload["weapons"]

    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in weapons:
        grouped[item["status"]].append(item)

    lines: list[str] = []
    lines.append("# GTA 6 Weapons Reverse-Engineered Catalog")
    lines.append("")
    lines.append(f"Source: {payload['source']}")
    lines.append(f"Capture timestamp (UTC): {payload['captured_at_utc']}")
    lines.append("")

    for status in ("confirmed", "unconfirmed"):
        section = grouped.get(status, [])
        lines.append(f"## {status.title()} ({len(section)})")
        lines.append("")
        lines.append("| Weapon | Category | Based On | Evidence | URL |")
        lines.append("|---|---|---|---|---|")
        for weapon in sorted(section, key=lambda w: w["name"].lower()):
            based_on = weapon["based_on"] or "-"
            lines.append(
                f"| {weapon['name']} | {weapon['category']} | {based_on} | {weapon['evidence']} | {weapon['url']} |"
            )
        lines.append("")

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
