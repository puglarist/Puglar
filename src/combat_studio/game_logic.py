from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class GTACombatLogic:
    aim_assist_level: float = 0.45
    pursuit_aggressiveness: float = 0.7
    vehicle_cover_priority: float = 0.8

    def tune_for_ranked(self) -> None:
        self.aim_assist_level = 0.3
        self.pursuit_aggressiveness = 0.85
        self.vehicle_cover_priority = 0.9


@dataclass
class MW2ProModLogic:
    movement_multiplier: float = 1.08
    recoil_scalar: float = 0.92
    ttk_modifier: float = 0.98


@dataclass
class COD4ProModLogic:
    strafe_speed: float = 1.06
    sprint_cooldown_seconds: float = 0.4
    grenade_warning_seconds: float = 1.2


@dataclass
class MobMenu:
    enabled_mobs: List[str] = field(
        default_factory=lambda: ["zombie", "skeleton", "creeper", "enderman"]
    )
    boss_mobs: List[str] = field(default_factory=lambda: ["wither", "ender_dragon"])

    def add_mob(self, mob_name: str, boss: bool = False) -> None:
        target = self.boss_mobs if boss else self.enabled_mobs
        if mob_name not in target:
            target.append(mob_name)


@dataclass
class MinecraftLogic:
    world_name: str = "main-world"
    logic_toggles: Dict[str, bool] = field(
        default_factory=lambda: {
            "survival_ai": True,
            "mob_scaling": True,
            "dynamic_weather": True,
            "raid_events": False,
        }
    )
    mob_menu: MobMenu = field(default_factory=MobMenu)

    def toggle(self, feature: str, enabled: bool) -> None:
        self.logic_toggles[feature] = enabled

    def go_to_world(self, world_name: str) -> None:
        self.world_name = world_name
