"""Agent runtime for world-building and mod-scaffolding workflows.

The assistant can be embedded in a game server panel or an in-engine editor window
so designers can prompt for map generation, mission logic, and environment scripting.
"""

from smolagents import CodeAgent, Tool

from .hf_pipelines import HFPipelineRegistry, generate_world_preview
from .world_schema import BiomeSeed, WorldSpec


class BuildWorldTool(Tool):
    name = "build_world"
    description = "Generate world assets from a high-level design brief."
    inputs = {
        "project_name": {"type": "string", "description": "World project identifier."},
        "engine": {"type": "string", "description": "Engine target, e.g., Unreal, Unity, FiveM."},
        "style_prompt": {"type": "string", "description": "Visual style and atmosphere."},
    }
    output_type = "string"

    def __init__(self, registry: HFPipelineRegistry, output_dir: str = "./generated") -> None:
        super().__init__()
        self.registry = registry
        self.output_dir = output_dir

    def forward(self, project_name: str, engine: str, style_prompt: str) -> str:
        spec = WorldSpec(
            project_name=project_name,
            engine=engine,
            map_size_km=16,
            style_prompt=style_prompt,
            target_platforms=["PC"],
            biomes=[
                BiomeSeed(name="urban-core", climate="temperate", elevation_hint="flat"),
                BiomeSeed(name="coastal-industrial", climate="humid", elevation_hint="low hills"),
                BiomeSeed(name="highland-forest", climate="cool", elevation_hint="mountainous"),
            ],
        )
        assets = generate_world_preview(spec, self.output_dir, self.registry)
        return f"Generated minimap: {assets.minimap_path}; heightmap: {assets.heightmap_path}"


def create_codex_world_agent(model_id: str = "Qwen/Qwen2.5-Coder-7B-Instruct") -> CodeAgent:
    """Create a Codex-style chat agent that can build worlds and mod templates.

    Note: For GTA/MW2 workflows, keep usage within legal modding policies, private servers,
    and anti-cheat-safe scripting interfaces.
    """

    registry = HFPipelineRegistry()
    build_world = BuildWorldTool(registry)

    return CodeAgent(
        tools=[build_world],
        model=model_id,
        add_base_tools=True,
        instructions=(
            "You are Metaverse Codex, a world builder assistant. "
            "Produce structured plans for map layout, mission logic, and server-safe mod scripts."
        ),
    )
