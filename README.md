# Puglar

## Metaverse World Builder (Hugging Face + Agents)

This repository now includes a starter implementation for generating realistic world maps
and running a Codex-style AI chat agent for metaverse world design and modding workflows.

### What is included

- `metaverse_ai/hf_pipelines.py`:
  - Loads Hugging Face models for planning and image generation.
  - Generates minimap + heightmap starter assets from prompts.
- `metaverse_ai/agent_runtime.py`:
  - Defines a `smolagents`-based in-engine assistant (`Metaverse Codex`).
  - Exposes a `build_world` tool for prompt-to-world generation.
- `metaverse_ai/world_schema.py`:
  - Shared dataclasses for world specs and generated asset metadata.
- `metaverse_ai/modding_guidelines.md`:
  - Guardrails for legal/approved GTA and MW2-style server modding workflows.

### Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r metaverse_ai/requirements.txt
```

Create and run the agent:

```python
from metaverse_ai.agent_runtime import create_codex_world_agent

agent = create_codex_world_agent()
result = agent.run(
    "Build a realistic coastal city world with mountain outskirts for Unreal Engine"
)
print(result)
```

Generate a world preview directly:

```python
from metaverse_ai.hf_pipelines import HFPipelineRegistry, generate_world_preview
from metaverse_ai.world_schema import BiomeSeed, WorldSpec

registry = HFPipelineRegistry()
spec = WorldSpec(
    project_name="neon_harbor",
    engine="Unreal",
    map_size_km=24,
    style_prompt="photorealistic overcast megacity, dense districts, believable roads",
    target_platforms=["PC", "Console"],
    biomes=[
        BiomeSeed(name="coast", climate="humid", elevation_hint="flat"),
        BiomeSeed(name="industrial", climate="temperate", elevation_hint="flat"),
        BiomeSeed(name="highlands", climate="cool", elevation_hint="steep"),
    ],
)

assets = generate_world_preview(spec, out_dir="./generated", registry=registry)
print(assets)
```

### Notes for GTA / MW2-style worlds and servers

- Use AI generation for **content creation and server logic prototyping**.
- Avoid anti-cheat bypass, exploit automation, or unauthorized reverse engineering.
- Keep deployment server-authoritative and private where required.
