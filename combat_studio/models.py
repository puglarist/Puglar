from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(slots=True)
class Fighter:
    """Core combatant model used by the simulator."""

    fighter_id: str
    name: str
    weight_class: str
    style: str
    power: float
    speed: float
    stamina: float
    defense: float
    fight_iq: float
    chin: float
    aggression: float
    adaptation: float
    momentum: float = 0.0


@dataclass(slots=True)
class RoundTelemetry:
    round_number: int
    striker: str
    defender: str
    exchanges: int
    clean_hits: int
    blocked_hits: int
    knockdowns: int
    control_seconds: int
    stamina_spent: float
    damage_inflicted: float
    notes: List[str] = field(default_factory=list)


@dataclass(slots=True)
class FightResult:
    fighter_a: Fighter
    fighter_b: Fighter
    winner_id: str
    method: str
    rounds_completed: int
    scorecard: Dict[str, int]
    telemetry: List[RoundTelemetry]
