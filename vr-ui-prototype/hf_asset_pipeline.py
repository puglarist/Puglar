"""Minimal helper for generating a Quest-ready 3D asset pipeline plan with Hugging Face models.

This script does not bundle or mirror third-party datasets/models. It creates structured
prompts and request payloads you can use with your own HF token and downstream UE5 tools.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class AssetRequest:
    name: str
    style: str
    target_polycount: int
    pbr_textures: bool = True
    scale_meters: float = 1.0


def build_requests() -> list[AssetRequest]:
    return [
        AssetRequest("street-rifle", "near-future tactical", 12000),
        AssetRequest("wrist-computer", "sleek industrial", 7000),
        AssetRequest("medical-kit", "modular field gear", 5000),
        AssetRequest("urban-backpack", "high-detail nylon", 9000),
    ]


def write_payloads(out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "dataset": "olympusmonsgames/unreal-engine-5-code-split",
        "model_hint": "facebook/sam-3d-objects",
        "export_profile": {
            "platform": "Meta Quest",
            "format": "glb",
            "texture_size": 1024,
            "lods": [1.0, 0.5, 0.25],
        },
        "assets": [asdict(req) for req in build_requests()],
    }

    file_path = out_dir / "hf_asset_payloads.json"
    file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return file_path


if __name__ == "__main__":
    output = write_payloads(Path("artifacts"))
    print(f"Wrote payload templates to: {output}")
