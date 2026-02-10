from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from puglar_engine import Actor, Component, SimulationWorld, TickConfig, VRComfortConfig, VRRig


class CounterComponent(Component):
    def __init__(self):
        super().__init__("counter")
        self.calls = 0

    def tick(self, delta_seconds: float) -> None:
        self.calls += 1


def test_fixed_step_simulation_ticks_components():
    world = SimulationWorld(TickConfig(fixed_delta_seconds=0.01, max_substeps=10))
    actor = Actor("TestActor")
    component = CounterComponent()
    actor.add_component(component)
    world.spawn_actor(actor)

    steps = world.advance(0.025)

    assert steps == 2
    assert component.calls == 2


def test_actor_tag_query():
    world = SimulationWorld()
    player = Actor("Player")
    player.add_tags("player", "vr")
    ai = Actor("Enemy")
    ai.add_tags("ai")
    world.spawn_actor(player)
    world.spawn_actor(ai)

    matches = world.find_actors_with_tags(["player", "vr"])

    assert [a.name for a in matches] == ["Player"]


def test_vr_comfort_clamps_locomotion_and_turning():
    rig = VRRig(comfort=VRComfortConfig(max_linear_velocity_m_s=3.5, snap_turn_degrees=30))

    assert rig.apply_smooth_locomotion(9.0) == 3.5
    assert rig.apply_smooth_locomotion(-2.0) == 0.0
    assert rig.apply_turn_input(44.0, snap=True) == 30
    assert rig.apply_turn_input(180.0, snap=False) <= (
        rig.comfort.max_angular_velocity_deg_s / rig.comfort.preferred_refresh_hz
    )
