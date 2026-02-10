"""Combat sport simulator with support for multiple fighting styles.

The simulator models stylistic strengths/weaknesses, strategy choices,
and fighter condition during a round-based bout.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Dict, List, Sequence


STYLE_PROFILES: Dict[str, Dict[str, int]] = {
    "boxing": {
        "hands": 95,
        "kicks": 15,
        "grappling": 20,
        "takedown": 25,
        "defense": 80,
        "cardio": 75,
    },
    "mma": {
        "hands": 75,
        "kicks": 70,
        "grappling": 80,
        "takedown": 80,
        "defense": 75,
        "cardio": 75,
    },
    "muay_thai": {
        "hands": 80,
        "kicks": 90,
        "grappling": 35,
        "takedown": 30,
        "defense": 70,
        "cardio": 80,
    },
    "wrestling": {
        "hands": 45,
        "kicks": 20,
        "grappling": 90,
        "takedown": 95,
        "defense": 70,
        "cardio": 85,
    },
    "bjj": {
        "hands": 35,
        "kicks": 30,
        "grappling": 95,
        "takedown": 70,
        "defense": 65,
        "cardio": 78,
    },
    "kickboxing": {
        "hands": 82,
        "kicks": 86,
        "grappling": 25,
        "takedown": 20,
        "defense": 72,
        "cardio": 78,
    },
}


@dataclass
class Fighter:
    name: str
    style: str
    aggression: int = 60
    fight_iq: int = 65

    def __post_init__(self) -> None:
        if self.style not in STYLE_PROFILES:
            raise ValueError(
                f"Unknown style '{self.style}'. Choose from: {', '.join(available_styles())}"
            )
        if not 0 <= self.aggression <= 100:
            raise ValueError("aggression must be between 0 and 100")
        if not 0 <= self.fight_iq <= 100:
            raise ValueError("fight_iq must be between 0 and 100")


@dataclass
class BoutResult:
    winner: Fighter
    loser: Fighter
    rounds_fought: int
    winner_health: int
    loser_health: int
    scorecard: Dict[str, int]
    events: List[str]


def available_styles() -> Sequence[str]:
    return tuple(STYLE_PROFILES.keys())


def _strategy_weights(style: str) -> Dict[str, int]:
    profile = STYLE_PROFILES[style]
    return {
        "strike": profile["hands"] + profile["kicks"],
        "pressure": profile["hands"] + profile["cardio"],
        "grapple": profile["grappling"] + profile["takedown"],
        "counter": profile["defense"] + profile["hands"],
    }


def _pick_strategy(rng: Random, fighter: Fighter, health: int) -> str:
    weights = _strategy_weights(fighter.style)
    if fighter.aggression > 70:
        weights["pressure"] += 20
        weights["strike"] += 10
    if fighter.fight_iq > 75:
        weights["counter"] += 15
        weights["grapple"] += 10
    if health < 35:
        weights["counter"] += 30
        weights["pressure"] = max(10, weights["pressure"] - 20)

    strategies = list(weights.keys())
    bucket = []
    for strategy in strategies:
        bucket.extend([strategy] * max(1, weights[strategy] // 10))
    return rng.choice(bucket)


def _round_effectiveness(rng: Random, fighter: Fighter, strategy: str, opponent_style: str) -> int:
    p = STYLE_PROFILES[fighter.style]
    o = STYLE_PROFILES[opponent_style]

    if strategy == "strike":
        base = int(0.6 * p["hands"] + 0.5 * p["kicks"])
        resistance = int(0.45 * o["defense"])
    elif strategy == "pressure":
        base = int(0.55 * p["hands"] + 0.35 * p["cardio"] + 0.25 * p["kicks"])
        resistance = int(0.35 * o["defense"] + 0.2 * o["cardio"])
    elif strategy == "grapple":
        base = int(0.55 * p["grappling"] + 0.55 * p["takedown"])
        resistance = int(0.45 * o["grappling"] + 0.25 * o["defense"])
    else:  # counter
        base = int(0.55 * p["defense"] + 0.45 * p["hands"])
        resistance = int(0.3 * 50 + 0.25 * o["defense"])

    variance = rng.randint(-8, 12)
    iq_edge = int((fighter.fight_iq - 50) * 0.15)
    result = base - resistance + variance + iq_edge
    return max(1, result)


def simulate_bout(
    fighter_a: Fighter,
    fighter_b: Fighter,
    rounds: int = 3,
    seed: int | None = None,
) -> BoutResult:
    if rounds < 1:
        raise ValueError("rounds must be at least 1")

    rng = Random(seed)
    health = {fighter_a.name: 100, fighter_b.name: 100}
    scorecard = {fighter_a.name: 0, fighter_b.name: 0}
    events: List[str] = []

    for round_number in range(1, rounds + 1):
        strategy_a = _pick_strategy(rng, fighter_a, health[fighter_a.name])
        strategy_b = _pick_strategy(rng, fighter_b, health[fighter_b.name])

        a_output = _round_effectiveness(rng, fighter_a, strategy_a, fighter_b.style)
        b_output = _round_effectiveness(rng, fighter_b, strategy_b, fighter_a.style)

        a_damage = max(1, a_output // 5)
        b_damage = max(1, b_output // 5)

        health[fighter_b.name] = max(0, health[fighter_b.name] - a_damage)
        health[fighter_a.name] = max(0, health[fighter_a.name] - b_damage)

        if a_output > b_output:
            scorecard[fighter_a.name] += 10
            scorecard[fighter_b.name] += 9
            events.append(
                f"Round {round_number}: {fighter_a.name} wins round ({strategy_a} over {strategy_b})."
            )
        elif b_output > a_output:
            scorecard[fighter_b.name] += 10
            scorecard[fighter_a.name] += 9
            events.append(
                f"Round {round_number}: {fighter_b.name} wins round ({strategy_b} over {strategy_a})."
            )
        else:
            scorecard[fighter_a.name] += 10
            scorecard[fighter_b.name] += 10
            events.append(f"Round {round_number}: even round.")

        if health[fighter_a.name] == 0 or health[fighter_b.name] == 0:
            events.append(f"Fight stopped in round {round_number} due to damage.")
            break

    rounds_fought = len([e for e in events if e.startswith("Round")])

    if health[fighter_a.name] != health[fighter_b.name]:
        winner = fighter_a if health[fighter_a.name] > health[fighter_b.name] else fighter_b
    else:
        winner = fighter_a if scorecard[fighter_a.name] >= scorecard[fighter_b.name] else fighter_b
    loser = fighter_b if winner is fighter_a else fighter_a

    return BoutResult(
        winner=winner,
        loser=loser,
        rounds_fought=rounds_fought,
        winner_health=health[winner.name],
        loser_health=health[loser.name],
        scorecard=scorecard,
        events=events,
    )


if __name__ == "__main__":
    a = Fighter("Atlas", "boxing", aggression=72, fight_iq=68)
    b = Fighter("Rogue", "mma", aggression=65, fight_iq=75)
    result = simulate_bout(a, b, rounds=5, seed=7)

    print(f"Winner: {result.winner.name} ({result.winner.style})")
    print(f"Health: {result.winner_health} - {result.loser_health}")
    print(f"Scorecard: {result.scorecard}")
    for event in result.events:
        print(f"- {event}")
