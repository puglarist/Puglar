#!/usr/bin/env python3
"""Build BO6 map blueprints from scraped GamesAtlas index data."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "data" / "bo6_maps_scraped_index.json"
OUT_DIR = ROOT / "build" / "bo6_map_blueprints"
COMBINED_PATH = ROOT / "build" / "bo6_maps_blueprints.json"

SMALL_MAP_HINTS = {"pit", "stakeout", "gala", "bullet", "exchange", "mothball", "nomad", "signal", "blitz", "eclipse", "racket", "heirloom", "warhead"}


def infer_size(slug: str, playlists: list[str], map_type: str) -> str:
    if map_type == "zombies":
        return "large"
    if "2v2" in playlists or slug in SMALL_MAP_HINTS:
        return "small"
    return "medium"


def infer_lanes(size: str, map_type: str) -> int:
    if map_type == "zombies":
        return 5
    return 2 if size == "small" else 3


def infer_combat_pace(size: str, playlists: list[str], map_type: str) -> str:
    if map_type == "zombies":
        return "scaling"
    if "2v2" in playlists:
        return "high"
    return "medium"


def build_blueprint(entry: dict) -> dict:
    size = infer_size(entry["slug"], entry["playlists"], entry["type"])
    lane_count = infer_lanes(size, entry["type"])
    pace = infer_combat_pace(size, entry["playlists"], entry["type"])

    return {
        "id": entry["slug"],
        "name": entry["name"],
        "source_url": entry["url"],
        "map_type": entry["type"],
        "release_window": entry["release_window"],
        "supported_playlists": entry["playlists"],
        "reverse_engineered_layout": {
            "size_class": size,
            "lane_count": lane_count,
            "verticality": "medium" if entry["type"] == "multiplayer" else "high",
            "combat_pace": pace,
            "dominant_engagement_range": "close" if size == "small" else "mixed",
        },
        "build_checklist": [
            "Block out shell and exterior boundaries",
            "Place primary objective lanes and intersections",
            "Add elevation changes and power positions",
            "Add cover pass and spawn safety pass",
            "Tune traversal times and sightline balance",
        ],
    }


def main() -> None:
    payload = json.loads(INDEX_PATH.read_text())
    blueprints = [build_blueprint(m) for m in payload["maps"]]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for bp in blueprints:
        (OUT_DIR / f"{bp['id']}.json").write_text(json.dumps(bp, indent=2) + "\n")

    COMBINED_PATH.write_text(json.dumps({"count": len(blueprints), "maps": blueprints}, indent=2) + "\n")
    print(f"Built {len(blueprints)} map blueprints into {OUT_DIR}")


if __name__ == "__main__":
    main()
