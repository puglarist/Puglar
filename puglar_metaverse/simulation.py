from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from .hand_tracking import HandTrackingEngine, HandPose
from .trickshot_promod import ProModEngine, WeaponProfile
from .realism_graphics import GraphicsEngine, GraphicsProfile
from .mod_menu import ModMenu


@dataclass
class SimulationFrameInput:
    hand_id: str
    hand_pose: HandPose
    weapon: WeaponProfile
    distance_m: float
    spin_degrees: float
    airtime_s: float
    swap_count: int


class RealismSimulation:
    def __init__(self):
        self.hands = HandTrackingEngine()
        self.promod = ProModEngine()
        self.graphics = GraphicsEngine()
        self.mods = ModMenu()

    def tick(self, frame: SimulationFrameInput, gfx: GraphicsProfile) -> Dict[str, Any]:
        smoothed = self.hands.smooth_pose(frame.hand_id, frame.hand_pose)
        gesture = self.hands.classify_gesture(smoothed)
        shot = self.promod.resolve_shot(
            frame.weapon,
            frame.distance_m,
            frame.spin_degrees,
            frame.airtime_s,
            frame.swap_count,
        )
        realism = self.graphics.realism_score(gfx)
        return {
            "gesture": gesture,
            "shot": shot,
            "graphics_realism": realism,
            "mods": self.mods.export(),
        }
