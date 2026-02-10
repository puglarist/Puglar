from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable

from .actor import Actor


@dataclass(slots=True)
class TickConfig:
    """Fixed-step tick model for deterministic gameplay simulation."""

    fixed_delta_seconds: float = 1.0 / 90.0
    max_substeps: int = 8


@dataclass(slots=True)
class SimulationWorld:
    """Unreal-like world loop with fixed substeps and actor queries."""

    tick_config: TickConfig = field(default_factory=TickConfig)
    actors: Dict[str, Actor] = field(default_factory=dict)
    _accumulator: float = 0.0

    def spawn_actor(self, actor: Actor) -> None:
        self.actors[actor.name] = actor

    def get_actor(self, name: str) -> Actor | None:
        return self.actors.get(name)

    def find_actors_with_tags(self, tags: Iterable[str]) -> list[Actor]:
        required = set(tags)
        return [actor for actor in self.actors.values() if actor.has_all_tags(required)]

    def advance(self, frame_delta_seconds: float) -> int:
        """Advance the world. Returns number of fixed simulation steps consumed."""
        self._accumulator += max(frame_delta_seconds, 0.0)
        steps = 0

        while (
            self._accumulator >= self.tick_config.fixed_delta_seconds
            and steps < self.tick_config.max_substeps
        ):
            for actor in self.actors.values():
                actor.tick(self.tick_config.fixed_delta_seconds)

            self._accumulator -= self.tick_config.fixed_delta_seconds
            steps += 1

        return steps
