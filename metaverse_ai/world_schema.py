"""Shared data structures for generated metaverse worlds."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class BiomeSeed:
    name: str
    climate: str
    elevation_hint: str
    poi_density: float = 0.5


@dataclass
class WorldSpec:
    project_name: str
    engine: str
    map_size_km: float
    style_prompt: str
    target_platforms: List[str]
    biomes: List[BiomeSeed] = field(default_factory=list)


@dataclass
class GeneratedAssets:
    heightmap_path: str
    minimap_path: str
    texture_atlas_path: str
    metadata: Dict[str, str] = field(default_factory=dict)
