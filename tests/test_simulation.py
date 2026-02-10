from combat_studio.pipeline import build_simulation_payload
from combat_studio.synthetic_data import export_dataset, generate_fighters


def test_synthetic_generation_shape() -> None:
    fighters = generate_fighters(4, seed=100)
    assert len(fighters) == 4
    assert fighters[0].fighter_id == "F-0000"

    records = export_dataset(fighters)
    assert records[2]["name"]
    assert 45.0 <= records[1]["power"] <= 99.0


def test_simulation_payload_is_consistent() -> None:
    payload = build_simulation_payload(seed=77)

    assert len(payload["fighters"]) == 2
    assert payload["result"]["winner_id"] in {
        payload["fighters"][0]["fighter_id"],
        payload["fighters"][1]["fighter_id"],
    }
    assert payload["result"]["method"] in {"TKO", "Decision"}
    assert payload["result"]["telemetry"]
