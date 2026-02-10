#!/usr/bin/env python3
"""Build a simple catalog for the Puglar repository artifacts."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT_JSON = ROOT / "catalog.json"
OUTPUT_MD = ROOT / "CATALOG.md"
TRACKED_SUFFIXES = {".pdf", ".zip"}


@dataclass
class Artifact:
    filename: str
    extension: str
    size_bytes: int
    sha256_12: str


def short_sha256(path: Path, length: int = 12) -> str:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest[:length]


def collect_artifacts(root: Path) -> list[Artifact]:
    artifacts: list[Artifact] = []
    for path in sorted(root.iterdir()):
        if not path.is_file() or path.name in {OUTPUT_JSON.name, OUTPUT_MD.name}:
            continue
        if path.suffix.lower() not in TRACKED_SUFFIXES:
            continue
        artifacts.append(
            Artifact(
                filename=path.name,
                extension=path.suffix.lower(),
                size_bytes=path.stat().st_size,
                sha256_12=short_sha256(path),
            )
        )
    return artifacts


def write_catalog_json(artifacts: list[Artifact]) -> None:
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "artifact_count": len(artifacts),
        "artifacts": [asdict(a) for a in artifacts],
    }
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_catalog_markdown(artifacts: list[Artifact]) -> None:
    lines = [
        "# Puglar Artifact Catalog",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "",
        "| File | Type | Size (bytes) | SHA-256 (first 12) |",
        "|---|---|---:|---|",
    ]
    for artifact in artifacts:
        lines.append(
            f"| `{artifact.filename}` | `{artifact.extension}` | {artifact.size_bytes} | `{artifact.sha256_12}` |"
        )

    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    artifacts = collect_artifacts(ROOT)
    write_catalog_json(artifacts)
    write_catalog_markdown(artifacts)
    print(f"Built catalog for {len(artifacts)} artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
