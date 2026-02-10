from __future__ import annotations

import random
from dataclasses import asdict
from typing import Dict, Iterable, List

from .models import Fighter

FIRST_NAMES = [
    "Malik", "Arjun", "Victor", "Nadia", "Elena", "Tariq", "Mina", "Kai", "Ryo", "Anya"
]
LAST_NAMES = ["Stone", "Vale", "Ortega", "Azim", "Dray", "Mori", "Santos", "Rowe", "Lin", "Ibarra"]
WEIGHT_CLASSES = ["Flyweight", "Bantamweight", "Featherweight", "Lightweight", "Welterweight", "Middleweight"]
STYLES = ["Pressure Boxing", "Counter Striking", "Wrestle-Boxing", "Kickboxing", "Sambo", "Muay Thai"]


def _roll(min_value: float = 45.0, max_value: float = 99.0) -> float:
    return round(random.uniform(min_value, max_value), 2)


def generate_fighters(size: int, seed: int = 42) -> List[Fighter]:
    """Create realistic synthetic fighters for simulation and training logic."""
    random.seed(seed)
    fighters: List[Fighter] = []
    for idx in range(size):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        fighters.append(
            Fighter(
                fighter_id=f"F-{idx:04d}",
                name=f"{first} {last}",
                weight_class=random.choice(WEIGHT_CLASSES),
                style=random.choice(STYLES),
                power=_roll(),
                speed=_roll(),
                stamina=_roll(),
                defense=_roll(),
                fight_iq=_roll(),
                chin=_roll(),
                aggression=_roll(),
                adaptation=_roll(),
            )
        )
    return fighters


def export_dataset(fighters: Iterable[Fighter]) -> List[Dict[str, object]]:
    """Transform fighter objects into records that can be persisted to JSON or a DB."""
    return [asdict(fighter) for fighter in fighters]
