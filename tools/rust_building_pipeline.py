#!/usr/bin/env python3
"""Clean-room Rust-inspired content pipeline.

This script intentionally avoids copying proprietary art/assets.
It only extracts text structure from a public wiki page and generates
original placeholder data/artifacts.
"""

from __future__ import annotations

import argparse
import json
import random
import urllib.request
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List
from urllib.error import URLError

DEFAULT_URL = "https://rust.fandom.com/wiki/Building"


class _HeadingAndParagraphParser(HTMLParser):
    """Extract coarse heading and paragraph content from an HTML document."""

    def __init__(self) -> None:
        super().__init__()
        self.current_tag = None
        self.current_heading = "Overview"
        self.sections: Dict[str, List[str]] = {self.current_heading: []}
        self._buffer: List[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        self.current_tag = tag.lower()
        if self.current_tag in {"h2", "h3", "h4", "p", "li"}:
            self._buffer = []

    def handle_endtag(self, tag: str) -> None:
        t = tag.lower()
        if t not in {"h2", "h3", "h4", "p", "li"}:
            return
        text = " ".join("".join(self._buffer).split())
        if not text:
            return
        if t in {"h2", "h3", "h4"}:
            self.current_heading = text
            self.sections.setdefault(self.current_heading, [])
        else:
            self.sections.setdefault(self.current_heading, []).append(text)

    def handle_data(self, data: str) -> None:
        if self.current_tag in {"h2", "h3", "h4", "p", "li"}:
            self._buffer.append(data)


def scrape_building_page(url: str = DEFAULT_URL) -> Dict[str, object]:
    """Download and extract page text sections from a wiki page."""
    req = urllib.request.Request(url, headers={"User-Agent": "PuglarPrototypeBot/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            html = response.read().decode("utf-8", errors="ignore")

        parser = _HeadingAndParagraphParser()
        parser.feed(html)

        filtered_sections = {
            key: value[:20]
            for key, value in parser.sections.items()
            if value and len(" ".join(value)) > 40
        }
        warnings: List[str] = []
    except URLError as err:
        filtered_sections = {
            "Overview": [
                "Network-restricted fallback mode. Supply a local HTML snapshot for deterministic extraction.",
                "Use --url file:///absolute/path/to/Building.html to parse saved source content.",
            ],
            "Building Tiers": [
                "Twig -> Wood -> Stone -> Metal -> Armored progression template for prototype balancing.",
            ],
        }
        warnings = [f"Fetch failed for source URL: {err}"]

    return {
        "source_url": url,
        "notes": [
            "Only public text structure is extracted.",
            "No game textures, models, or copyrighted UI resources are copied.",
        ],
        "warnings": warnings,
        "sections": filtered_sections,
    }


@dataclass
class Tile:
    x: int
    y: int
    biome: str
    elevation: float
    poi: str | None


def build_procedural_map(width: int = 24, height: int = 24, seed: int = 42) -> Dict[str, object]:
    """Create a prototype survival map with biome/POI metadata."""
    rng = random.Random(seed)
    biomes = ["snow", "forest", "desert", "temperate", "coast"]
    pois = [None, None, None, "outpost", "harbor", "quarry", "monument"]

    tiles: List[Tile] = []
    for y in range(height):
        for x in range(width):
            noise = rng.random()
            if y < height * 0.2:
                biome = "snow"
            elif y > height * 0.8:
                biome = "desert"
            else:
                biome = biomes[int(noise * len(biomes)) % len(biomes)]

            elevation = round((rng.random() + noise) / 2, 3)
            poi = rng.choice(pois) if rng.random() > 0.92 else None
            tiles.append(Tile(x=x, y=y, biome=biome, elevation=elevation, poi=poi))

    return {
        "seed": seed,
        "size": {"width": width, "height": height},
        "legend": {
            "biomes": biomes,
            "pois": [p for p in {"outpost", "harbor", "quarry", "monument"}],
        },
        "tiles": [asdict(t) for t in tiles],
    }


def generate_placeholder_icons(out_dir: Path) -> List[str]:
    """Create original placeholder SVG icons for key build categories."""
    icon_templates = {
        "wood_wall": '<rect x="10" y="10" width="80" height="80" fill="#8b5a2b" stroke="#1f1f1f" stroke-width="4"/>',
        "stone_foundation": '<polygon points="50,8 92,32 92,78 50,92 8,78 8,32" fill="#8f9299" stroke="#23262e" stroke-width="4"/>',
        "metal_door": '<rect x="22" y="8" width="56" height="84" rx="4" fill="#9ea7b8" stroke="#20242d" stroke-width="4"/><circle cx="66" cy="50" r="4" fill="#20242d"/>',
        "tool_cupboard": '<rect x="18" y="18" width="64" height="64" fill="#6f4a2a" stroke="#1e1510" stroke-width="4"/><rect x="30" y="30" width="40" height="40" fill="#a7784e"/>',
    }

    created = []
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, shape in icon_templates.items():
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            f"{shape}"
            "</svg>"
        )
        path = out_dir / f"{name}.svg"
        path.write_text(svg, encoding="utf-8")
        created.append(path.name)
    return created


def build_gui_layout() -> Dict[str, object]:
    """Define a game-like GUI metadata structure for HUD, map, and admin panel."""
    return {
        "theme": {"background": "#15181f", "panel": "#1f2430", "accent": "#9bc53d", "text": "#f5f7fa"},
        "screens": [
            {
                "name": "world_map",
                "panels": [
                    {"id": "map_canvas", "anchor": "center", "size": [0.72, 0.82]},
                    {"id": "vendors_panel", "anchor": "left", "size": [0.22, 0.7]},
                    {"id": "resource_filter", "anchor": "right", "size": [0.06, 0.6]},
                ],
            },
            {
                "name": "server_admin",
                "panels": [
                    {"id": "players_list", "anchor": "left", "size": [0.24, 0.8]},
                    {"id": "server_info", "anchor": "center", "size": [0.24, 0.8]},
                    {"id": "cvars_editor", "anchor": "center_right", "size": [0.24, 0.8]},
                    {"id": "usercontent_gallery", "anchor": "right", "size": [0.24, 0.8]},
                ],
            },
        ],
    }


def build_game_rules() -> Dict[str, object]:
    """Prototype survival/building game rules and state transitions."""
    return {
        "resources": {
            "wood": {"stack": 1000, "gather_rate": 15},
            "stone": {"stack": 1000, "gather_rate": 12},
            "metal_fragments": {"stack": 1000, "gather_rate": 6},
            "high_quality_metal": {"stack": 100, "gather_rate": 1},
        },
        "building_tiers": [
            {"name": "twig", "hp_multiplier": 0.3, "upkeep": 1.0},
            {"name": "wood", "hp_multiplier": 0.8, "upkeep": 1.2},
            {"name": "stone", "hp_multiplier": 1.4, "upkeep": 1.5},
            {"name": "metal", "hp_multiplier": 2.0, "upkeep": 1.9},
            {"name": "armored", "hp_multiplier": 2.8, "upkeep": 2.4},
        ],
        "state_machine": {
            "states": ["spawn", "gather", "build", "raid", "defend", "respawn"],
            "transitions": [
                ["spawn", "gather"],
                ["gather", "build"],
                ["build", "defend"],
                ["defend", "raid"],
                ["raid", "respawn"],
                ["respawn", "gather"],
            ],
        },
    }


def write_json(path: Path, payload: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run(output_root: Path, source_url: str) -> Dict[str, object]:
    scraped = scrape_building_page(source_url)
    procedural_map = build_procedural_map()
    gui = build_gui_layout()
    logic = build_game_rules()
    icons = generate_placeholder_icons(output_root / "assets" / "icons")

    write_json(output_root / "scraped" / "building_page.json", scraped)
    write_json(output_root / "maps" / "procedural_map.json", procedural_map)
    write_json(output_root / "gui" / "layout.json", gui)
    write_json(output_root / "logic" / "game_rules.json", logic)

    return {
        "output_root": str(output_root),
        "icons_created": icons,
        "sections_extracted": len(scraped.get("sections", {})),
        "map_tiles": len(procedural_map.get("tiles", [])),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a clean-room Rust-inspired content prototype")
    parser.add_argument("--url", default=DEFAULT_URL, help="Source documentation URL")
    parser.add_argument("--out", default="prototype_output", help="Output directory")
    args = parser.parse_args()

    summary = run(Path(args.out), args.url)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
