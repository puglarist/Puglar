"""GTA-6 style iteration simulator.

Runs 500 improvement passes over simplified game systems:
- world logic
- graphics fidelity
- dance/booty-shake animation effects
- performance stability
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random


@dataclass
class GameBuild:
    logic_score: float = 10.0
    graphics_score: float = 10.0
    booty_shake_effect_score: float = 10.0
    performance_score: float = 10.0

    def clamp(self) -> None:
        self.logic_score = min(100.0, self.logic_score)
        self.graphics_score = min(100.0, self.graphics_score)
        self.booty_shake_effect_score = min(100.0, self.booty_shake_effect_score)
        self.performance_score = min(100.0, self.performance_score)


class GTASimulator:
    def __init__(self, iterations: int = 500, seed: int = 6) -> None:
        self.iterations = iterations
        self.rng = Random(seed)
        self.build = GameBuild()

    def iterate_once(self, step: int) -> GameBuild:
        # Earlier iterations improve rapidly; later ones tune details.
        early_multiplier = max(0.2, 1.0 - (step / self.iterations) * 0.8)

        logic_gain = (0.05 + self.rng.random() * 0.25) * early_multiplier
        graphics_gain = (0.06 + self.rng.random() * 0.28) * early_multiplier
        animation_gain = (0.04 + self.rng.random() * 0.22) * early_multiplier

        # Performance usually lags behind visual upgrades, then catches up.
        perf_gain = (0.03 + self.rng.random() * 0.20) * (0.8 + step / self.iterations)

        # Graphics + animation can temporarily reduce performance.
        perf_tax = (graphics_gain + animation_gain) * 0.15

        self.build.logic_score += logic_gain
        self.build.graphics_score += graphics_gain
        self.build.booty_shake_effect_score += animation_gain
        self.build.performance_score += max(0.0, perf_gain - perf_tax)
        self.build.clamp()

        return GameBuild(
            logic_score=self.build.logic_score,
            graphics_score=self.build.graphics_score,
            booty_shake_effect_score=self.build.booty_shake_effect_score,
            performance_score=self.build.performance_score,
        )

    def run_with_full_trace(self) -> list[tuple[int, GameBuild]]:
        history: list[tuple[int, GameBuild]] = []
        for step in range(1, self.iterations + 1):
            snapshot = self.iterate_once(step)
            history.append((step, snapshot))
        return history


def main() -> None:
    sim = GTASimulator(iterations=500, seed=6)
    history = sim.run_with_full_trace()

    print("=== GTA 6 Logic/Graphics Booty-Shake Iteration Report ===")
    print(f"Iterations executed: {sim.iterations}")
    print("\n--- Full Iteration Trace (all 500 iterations) ---")

    for step, state in history:
        print(
            f"Iter {step:03d} | "
            f"Logic {state.logic_score:6.2f} | "
            f"Graphics {state.graphics_score:6.2f} | "
            f"BootyFX {state.booty_shake_effect_score:6.2f} | "
            f"Perf {state.performance_score:6.2f}"
        )

    _, final_build = history[-1]
    print("\n--- Final Scores ---")
    print(f"Logic score: {final_build.logic_score:.2f}/100")
    print(f"Graphics score: {final_build.graphics_score:.2f}/100")
    print(f"Booty-shake effects score: {final_build.booty_shake_effect_score:.2f}/100")
    print(f"Performance stability score: {final_build.performance_score:.2f}/100")


if __name__ == "__main__":
    main()
