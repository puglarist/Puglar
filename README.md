# Combat Studio (Puglar)

Combat Studio is a simulation-level combat engine that combines:
- **Synthetic fighter generation** for realistic, repeatable logic testing
- **Round-by-round tactical simulation** with telemetry
- **RunPod API integration** for scalable remote execution
- **GitHub API integration** for reporting and collaboration workflows

## What is included

- `combat_studio/synthetic_data.py`: realistic synthetic fighter profiles
- `combat_studio/simulator.py`: multi-round combat model with knockdown and decision logic
- `combat_studio/pipeline.py`: end-to-end payload creation and API workflow orchestration
- `combat_studio/runpod_client.py`: RunPod endpoint client
- `combat_studio/github_client.py`: GitHub issue/workflow client

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

## Local simulation example

```python
from combat_studio.pipeline import build_simulation_payload

payload = build_simulation_payload(seed=7)
print(payload["result"]["winner_id"], payload["result"]["method"])
```

## RunPod integration

Set environment variables:

```bash
export RUNPOD_API_KEY="..."
export RUNPOD_ENDPOINT_ID="..."
```

Then:

```python
from combat_studio.pipeline import execute_remote_simulation

response = execute_remote_simulation(seed=9)
print(response)
```

## GitHub integration

Set environment variables:

```bash
export GITHUB_TOKEN="..."
export GITHUB_OWNER="your-org-or-user"
export GITHUB_REPO="your-repo"
```

Then:

```python
from combat_studio.pipeline import build_simulation_payload, publish_result_to_github

local_result = build_simulation_payload(seed=12)
issue = publish_result_to_github(local_result)
print(issue["html_url"])
```

## Notes on realism

This simulator is deterministic when seeded and models:
- Attribute-driven exchanges (speed/power/IQ/defense/adaptation)
- Momentum shifts and stamina decay
- Knockdown probability and control-time influence
- Scoring for judges' decisions when no finish occurs

Tune `CombatStudio(rounds=..., exchange_density=...)` and fighter attributes for your target doctrine.
