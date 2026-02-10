# Puglar

Puglar now includes an Unreal-inspired gameplay/simulation core with VR-first guardrails.

## What was added

- **Actor + Component architecture** (`Actor`, `Component`, `Transform`)
- **Gameplay tags** for data-driven actor querying
- **Deterministic fixed-step simulation loop** with configurable substepping
- **VR rig model** with comfort-centric locomotion and turning clamps

## Quick usage

```python
from puglar_engine import Actor, SimulationWorld, TickConfig, VRComfortConfig, VRRig

world = SimulationWorld(TickConfig(fixed_delta_seconds=1/90, max_substeps=8))
player = Actor("VRPlayer")
player.add_tags("player", "vr", "pawn")
world.spawn_actor(player)

steps = world.advance(1/60)

rig = VRRig(comfort=VRComfortConfig())
speed = rig.apply_smooth_locomotion(6.0)  # clamped for comfort
turn = rig.apply_turn_input(47.0, snap=True)  # snap turn in 30-degree increments
```

## Structure

- `src/puglar_engine/actor.py` – actor/component/gameplay-tag logic
- `src/puglar_engine/simulation.py` – fixed-step simulation world loop
- `src/puglar_engine/vr.py` – VR rig + comfort constraints
- `tests/` – simulation and VR behavior checks
