# Puglar Metaverse Prototype

This repository now includes a **playable simulation core scaffold** for:

- Realism-oriented hand-tracking inputs.
- MW2-inspired trickshot pro-mod shot resolution.
- Graphics realism profile tuning (skins, weapons, fog, shadows).
- Mod menu runtime settings with a safe allowlist.
- Hugging Face 3D asset API integration hook for generation pipelines.

> This is an engine-agnostic Python prototype intended to accelerate integration into Unreal, Unity, or custom C++/Rust game runtimes.

## Project layout

- `puglar_metaverse/hand_tracking.py` – hand landmarks, smoothing, gesture classification.
- `puglar_metaverse/trickshot_promod.py` – trickshot multiplier and shot outcome model.
- `puglar_metaverse/realism_graphics.py` – realism scoring for visual profiles.
- `puglar_metaverse/mod_menu.py` – moddable runtime configuration with allowlist.
- `puglar_metaverse/hf_asset_api.py` – Hugging Face endpoint client for 3D asset generation.
- `puglar_metaverse/simulation.py` – frame-level integration pipeline.

## Quick example

```python
from puglar_metaverse.hand_tracking import HandPose
from puglar_metaverse.trickshot_promod import WeaponProfile
from puglar_metaverse.realism_graphics import GraphicsProfile
from puglar_metaverse.simulation import RealismSimulation, SimulationFrameInput

sim = RealismSimulation()

frame = SimulationFrameInput(
    hand_id="player-1-right",
    hand_pose=HandPose([(0.1, 0.1, 0.1)] * 21),
    weapon=WeaponProfile(
        name="Intervention",
        damage=95,
        ads_speed=0.32,
        recoil=0.18,
        projectile_speed=940,
    ),
    distance_m=120,
    spin_degrees=720,
    airtime_s=1.3,
    swap_count=2,
)

gfx = GraphicsProfile(
    texture_quality=0.95,
    shadow_distance=0.9,
    volumetric_fog=0.85,
    skin_shading=0.92,
    weapon_roughness=0.94,
)

result = sim.tick(frame, gfx)
print(result)
```

## Hugging Face 3D asset generation

The API client accepts a generation prompt (e.g. "MW2 scrapyard sniper lane with realistic concrete + rust").

```python
from puglar_metaverse.hf_asset_api import HuggingFaceAssetClient, AssetRequest

client = HuggingFaceAssetClient(
    model_endpoint="https://api-inference.huggingface.co/models/<your-3d-model>",
)

payload = AssetRequest(
    prompt="MW2 style intervention sniper rifle, worn metal, tactical rail",
    style="modern warfare realism",
    poly_budget=30000,
    texture_resolution=2048,
)

# response = client.request_asset(payload)
```

## Next integration steps

1. Wire `HandTrackingEngine` to OpenXR/MediaPipe hand landmarks.
2. Replace shot heuristic with your authoritative server-side ballistics.
3. Convert realism score into dynamic preset selection for your renderer.
4. Feed generated 3D assets into import pipeline with moderation/safety checks.
5. Expand mod menu to include role-based permissions and signatures.
