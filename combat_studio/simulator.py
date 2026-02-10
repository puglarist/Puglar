from __future__ import annotations

import random
from dataclasses import replace
from typing import Dict, List

from .models import Fighter, FightResult, RoundTelemetry


class CombatStudio:
    """Simulation engine for high-fidelity combat scenarios."""

    def __init__(self, rounds: int = 5, exchange_density: int = 14) -> None:
        self.rounds = rounds
        self.exchange_density = exchange_density

    def run(self, fighter_a: Fighter, fighter_b: Fighter, seed: int | None = None) -> FightResult:
        if seed is not None:
            random.seed(seed)

        a = replace(fighter_a)
        b = replace(fighter_b)

        scorecard: Dict[str, int] = {a.fighter_id: 0, b.fighter_id: 0}
        telemetry: List[RoundTelemetry] = []

        for round_number in range(1, self.rounds + 1):
            round_a = self._simulate_round(a, b, round_number)
            round_b = self._simulate_round(b, a, round_number)

            telemetry.extend([round_a, round_b])

            points_a = round_a.clean_hits + round_a.knockdowns * 3 + round_a.control_seconds / 20
            points_b = round_b.clean_hits + round_b.knockdowns * 3 + round_b.control_seconds / 20

            if points_a >= points_b:
                scorecard[a.fighter_id] += 10
                scorecard[b.fighter_id] += 9
                a.momentum += 1.4
                b.momentum -= 0.8
            else:
                scorecard[b.fighter_id] += 10
                scorecard[a.fighter_id] += 9
                b.momentum += 1.4
                a.momentum -= 0.8

            if round_a.knockdowns >= 2:
                return FightResult(a, b, a.fighter_id, "TKO", round_number, scorecard, telemetry)
            if round_b.knockdowns >= 2:
                return FightResult(a, b, b.fighter_id, "TKO", round_number, scorecard, telemetry)

        winner = max(scorecard, key=scorecard.get)
        method = "Decision"
        return FightResult(a, b, winner, method, self.rounds, scorecard, telemetry)

    def _simulate_round(self, striker: Fighter, defender: Fighter, round_number: int) -> RoundTelemetry:
        tempo = self.exchange_density + int((striker.aggression - defender.fight_iq) / 18)
        exchanges = max(6, tempo + random.randint(-2, 3))

        striking_efficiency = (
            striker.speed * 0.22
            + striker.power * 0.24
            + striker.fight_iq * 0.2
            + striker.momentum * 0.12
            - defender.defense * 0.18
            + striker.adaptation * 0.15
        ) / 100

        clean_hits = max(0, int(exchanges * striking_efficiency + random.uniform(0, 2.9)))
        blocked_hits = max(0, exchanges - clean_hits)

        knockdown_prob = max(0.01, (striker.power - defender.chin + striker.momentum) / 180)
        knockdowns = sum(1 for _ in range(clean_hits) if random.random() < knockdown_prob)

        control_seconds = max(0, int((striker.fight_iq + striker.stamina - defender.adaptation) * 0.8))
        stamina_spent = round(exchanges * (1.2 - striker.stamina / 180), 2)
        damage_inflicted = round(clean_hits * (striker.power / 20) + knockdowns * 8.5, 2)

        striker.stamina = max(20, striker.stamina - stamina_spent)
        defender.chin = max(15, defender.chin - damage_inflicted / 12)
        striker.momentum = max(-5, min(8, striker.momentum + knockdowns * 0.5 - blocked_hits * 0.03))

        notes = []
        if knockdowns > 0:
            notes.append(f"{striker.name} scored {knockdowns} knockdown(s).")
        if control_seconds > 120:
            notes.append(f"{striker.name} dominated clinch control.")
        if clean_hits > blocked_hits:
            notes.append(f"{striker.name} found range with clean combinations.")

        return RoundTelemetry(
            round_number=round_number,
            striker=striker.fighter_id,
            defender=defender.fighter_id,
            exchanges=exchanges,
            clean_hits=clean_hits,
            blocked_hits=blocked_hits,
            knockdowns=knockdowns,
            control_seconds=control_seconds,
            stamina_spent=stamina_spent,
            damage_inflicted=damage_inflicted,
            notes=notes,
        )
