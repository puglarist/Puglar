from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict

from .github_client import GitHubClient
from .runpod_client import RunPodClient
from .simulator import CombatStudio
from .synthetic_data import generate_fighters


def build_simulation_payload(seed: int = 42) -> Dict[str, Any]:
    fighters = generate_fighters(2, seed=seed)
    studio = CombatStudio(rounds=5, exchange_density=16)
    result = studio.run(fighters[0], fighters[1], seed=seed)

    return {
        "fighters": [asdict(f) for f in fighters],
        "result": {
            "winner_id": result.winner_id,
            "method": result.method,
            "rounds_completed": result.rounds_completed,
            "scorecard": result.scorecard,
            "telemetry": [asdict(t) for t in result.telemetry],
        },
    }


def execute_remote_simulation(seed: int = 42) -> Dict[str, Any]:
    """Generate synthetic bout logic locally, then submit to RunPod for heavy analysis."""
    payload = build_simulation_payload(seed=seed)
    runpod = RunPodClient()
    return runpod.submit_simulation(payload)


def publish_result_to_github(result: Dict[str, Any], title: str = "Combat Studio Simulation Report") -> Dict[str, Any]:
    """Store simulation outcomes in GitHub for collaboration and traceability."""
    body = f"## Auto-generated simulation report\n\n```json\n{result}\n```"
    client = GitHubClient()
    return client.create_issue(title=title, body=body, labels=["combat-studio", "simulation"])
