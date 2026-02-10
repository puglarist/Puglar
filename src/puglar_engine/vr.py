from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Pose:
    position_m: tuple[float, float, float]
    rotation_deg: tuple[float, float, float]


@dataclass(slots=True)
class VRComfortConfig:
    """VR constraints inspired by production comfort standards."""

    max_angular_velocity_deg_s: float = 120.0
    max_linear_velocity_m_s: float = 4.0
    preferred_refresh_hz: int = 90
    snap_turn_degrees: int = 30
    vignette_strength: float = 0.35


@dataclass(slots=True)
class VRRig:
    """Runtime VR rig state used by simulation and gameplay logic."""

    comfort: VRComfortConfig
    head: Pose = field(default_factory=lambda: Pose((0.0, 1.7, 0.0), (0.0, 0.0, 0.0)))
    left_hand: Pose = field(
        default_factory=lambda: Pose((-0.3, 1.4, 0.25), (0.0, 0.0, 0.0))
    )
    right_hand: Pose = field(
        default_factory=lambda: Pose((0.3, 1.4, 0.25), (0.0, 0.0, 0.0))
    )

    def apply_smooth_locomotion(self, desired_velocity_m_s: float) -> float:
        """Clamp velocity for motion-sickness-safe locomotion."""
        return min(max(desired_velocity_m_s, 0.0), self.comfort.max_linear_velocity_m_s)

    def apply_turn_input(self, yaw_delta_deg: float, snap: bool = True) -> float:
        """Apply turn amount with optional snap-turn quantization."""
        if snap:
            step = self.comfort.snap_turn_degrees
            if step <= 0:
                return 0.0
            snapped_steps = int(yaw_delta_deg / step)
            return snapped_steps * step

        max_delta = self.comfort.max_angular_velocity_deg_s / self.comfort.preferred_refresh_hz
        return max(min(yaw_delta_deg, max_delta), -max_delta)
