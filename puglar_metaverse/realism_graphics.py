from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GraphicsProfile:
    texture_quality: float = 1.0
    shadow_distance: float = 1.0
    volumetric_fog: float = 1.0
    skin_shading: float = 1.0
    weapon_roughness: float = 1.0


class GraphicsEngine:
    """Heuristic realism score for graphics presets."""

    def realism_score(self, profile: GraphicsProfile) -> float:
        weighted = (
            profile.texture_quality * 0.24
            + profile.shadow_distance * 0.21
            + profile.volumetric_fog * 0.19
            + profile.skin_shading * 0.18
            + profile.weapon_roughness * 0.18
        )
        return round(max(0.0, min(1.0, weighted)), 3)
