"""Puglar Engine core package.

A lightweight simulation framework inspired by Unreal Engine concepts:
- Actor/Component composition
- Gameplay tags
- Fixed-step world simulation
- VR rig modeling with comfort safeguards
"""

from .actor import Actor, Component, Transform
from .simulation import SimulationWorld, TickConfig
from .vr import VRComfortConfig, VRRig, Pose

__all__ = [
    "Actor",
    "Component",
    "Transform",
    "SimulationWorld",
    "TickConfig",
    "VRComfortConfig",
    "VRRig",
    "Pose",
]
