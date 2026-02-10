from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class NetflixStudioPipeline:
    """Simple orchestration for long-form content generation workflows."""

    project_name: str
    stages: List[str] = field(
        default_factory=lambda: [
            "concept",
            "episode-outline",
            "script-draft",
            "review-pass",
            "release-package",
        ]
    )

    def add_stage(self, stage: str) -> None:
        if stage not in self.stages:
            self.stages.append(stage)

    def remove_stage(self, stage: str) -> None:
        if stage in self.stages:
            self.stages.remove(stage)

    def describe(self) -> str:
        return f"{self.project_name}: " + " -> ".join(self.stages)
