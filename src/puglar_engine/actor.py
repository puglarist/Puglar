from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Set


@dataclass(slots=True)
class Transform:
    """Simple transform model similar to Unreal's transform triplet."""

    location: tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation_deg: tuple[float, float, float] = (0.0, 0.0, 0.0)
    scale: tuple[float, float, float] = (1.0, 1.0, 1.0)


class Component:
    """Composable component with overridable tick lifecycle."""

    def __init__(self, name: str):
        self.name = name
        self.owner: Actor | None = None

    def on_attach(self, owner: "Actor") -> None:
        self.owner = owner

    def tick(self, delta_seconds: float) -> None:
        """Override in derived classes for simulation behavior."""


@dataclass(slots=True)
class Actor:
    """Actor object with components and gameplay tags."""

    name: str
    transform: Transform = field(default_factory=Transform)
    gameplay_tags: Set[str] = field(default_factory=set)
    components: List[Component] = field(default_factory=list)

    def add_component(self, component: Component) -> None:
        component.on_attach(self)
        self.components.append(component)

    def add_tags(self, *tags: str) -> None:
        self.gameplay_tags.update(tags)

    def has_all_tags(self, tags: Iterable[str]) -> bool:
        return set(tags).issubset(self.gameplay_tags)

    def tick(self, delta_seconds: float) -> None:
        for component in self.components:
            component.tick(delta_seconds)
