#!/usr/bin/env python3
"""Generate a markdown catalog of doctrine artifacts in this repository."""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path


EXTENSIONS = {".pdf", ".zip"}


@dataclass
class Artifact:
    path: Path
    size_bytes: int
    sha256: str

    @property
    def extension(self) -> str:
        return self.path.suffix.lower().lstrip(".")

    @property
    def size_mb(self) -> float:
        return self.size_bytes / (1024 * 1024)


def compute_sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def collect_artifacts(repo_root: Path) -> list[Artifact]:
    artifacts: list[Artifact] = []
    for path in sorted(repo_root.iterdir()):
        if not path.is_file():
            continue
        if path.suffix.lower() not in EXTENSIONS:
            continue
        artifacts.append(
            Artifact(
                path=path,
                size_bytes=path.stat().st_size,
                sha256=compute_sha256(path),
            )
        )
    return artifacts


def build_markdown(artifacts: list[Artifact]) -> str:
    total_size = sum(a.size_bytes for a in artifacts)
    pdf_count = sum(1 for a in artifacts if a.extension == "pdf")
    zip_count = sum(1 for a in artifacts if a.extension == "zip")

    lines = [
        "# Puglar Artifact Catalog",
        "",
        "Machine-generated catalog of distributable artifacts.",
        "",
        "## Snapshot",
        "",
        f"- Total artifacts: **{len(artifacts)}**",
        f"- PDF files: **{pdf_count}**",
        f"- ZIP files: **{zip_count}**",
        f"- Total size: **{total_size / (1024 * 1024):.2f} MiB**",
        "",
        "## Files",
        "",
        "| File | Type | Size (MiB) | SHA-256 |",
        "|---|---:|---:|---|",
    ]

    for artifact in artifacts:
        lines.append(
            f"| `{artifact.path.name}` | {artifact.extension.upper()} | "
            f"{artifact.size_mb:.2f} | `{artifact.sha256}` |"
        )

    lines += [
        "",
        "---",
        "",
        "Regenerate with:",
        "",
        "```bash",
        "python3 scripts/generate_catalog.py",
        "```",
        "",
    ]

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Path to repository root.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output markdown file (default: <repo-root>/CATALOG.md).",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    output = args.output.resolve() if args.output else repo_root / "CATALOG.md"

    artifacts = collect_artifacts(repo_root)
    markdown = build_markdown(artifacts)
    output.write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
