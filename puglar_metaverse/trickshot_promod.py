from __future__ import annotations

from dataclasses import dataclass
from random import Random


@dataclass
class WeaponProfile:
    name: str
    damage: float
    ads_speed: float
    recoil: float
    projectile_speed: float


class ProModEngine:
    """MW2-style trickshot and movement realism balancing."""

    def __init__(self, seed: int = 42):
        self.rng = Random(seed)
        self.gravity_scale = 1.12
        self.air_control = 0.74

    def trickshot_multiplier(self, spin_degrees: float, airtime_s: float, swap_count: int) -> float:
        spin_bonus = min(spin_degrees / 1080.0, 1.0) * 1.8
        air_bonus = min(airtime_s / 1.8, 1.0) * 1.2
        swap_bonus = min(swap_count, 4) * 0.22
        return 1.0 + spin_bonus + air_bonus + swap_bonus

    def resolve_shot(
        self,
        weapon: WeaponProfile,
        distance_m: float,
        spin_degrees: float,
        airtime_s: float,
        swap_count: int,
    ) -> dict:
        promod = self.trickshot_multiplier(spin_degrees, airtime_s, swap_count)
        spread = weapon.recoil * (1 + spin_degrees / 720.0)
        accuracy_roll = self.rng.uniform(0.0, 1.0)
        hit_probability = max(0.05, min(0.98, 1.0 - spread - (distance_m / 1500.0)))
        hit = accuracy_roll <= hit_probability
        damage = weapon.damage * promod if hit else 0.0
        return {
            "weapon": weapon.name,
            "hit": hit,
            "hit_probability": round(hit_probability, 4),
            "damage": round(damage, 2),
            "trickshot_multiplier": round(promod, 3),
        }
