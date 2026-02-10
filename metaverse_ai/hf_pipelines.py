"""Hugging Face model wiring for world-generation workflows.

This module keeps model loading and inference separate from game-engine logic so that
Unreal, Unity, Godot, or custom engines can call the same API.
"""

from pathlib import Path

from diffusers import StableDiffusionXLPipeline
from transformers import AutoModelForCausalLM, AutoTokenizer

from .world_schema import GeneratedAssets, WorldSpec


class HFPipelineRegistry:
    """Loads and caches text/image models used by the metaverse builder."""

    def __init__(self, cache_dir: str = "./.model-cache") -> None:
        self.cache_dir = cache_dir
        self._sdxl = None
        self._planner_model = None
        self._planner_tokenizer = None

    def planner(self, model_id: str = "mistralai/Mistral-7B-Instruct-v0.3"):
        if self._planner_model is None:
            self._planner_tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir=self.cache_dir)
            self._planner_model = AutoModelForCausalLM.from_pretrained(model_id, cache_dir=self.cache_dir)
        return self._planner_model, self._planner_tokenizer

    def sdxl(self, model_id: str = "stabilityai/stable-diffusion-xl-base-1.0"):
        if self._sdxl is None:
            self._sdxl = StableDiffusionXLPipeline.from_pretrained(model_id, cache_dir=self.cache_dir)
        return self._sdxl


def generate_world_preview(spec: WorldSpec, out_dir: str, registry: HFPipelineRegistry) -> GeneratedAssets:
    """Generate a concept minimap/heightmap pair from a world specification."""

    output = Path(out_dir)
    output.mkdir(parents=True, exist_ok=True)

    pipe = registry.sdxl()
    style = (
        f"top down realistic terrain concept art, procedural world map, {spec.style_prompt}, "
        f"biomes: {', '.join(b.name for b in spec.biomes)}"
    )
    image = pipe(prompt=style, num_inference_steps=30, guidance_scale=8.0).images[0]

    minimap_path = output / f"{spec.project_name}_minimap.png"
    heightmap_path = output / f"{spec.project_name}_heightmap.png"
    texture_atlas_path = output / f"{spec.project_name}_atlas.png"

    image.save(minimap_path)
    image.convert("L").save(heightmap_path)
    image.save(texture_atlas_path)

    return GeneratedAssets(
        heightmap_path=str(heightmap_path),
        minimap_path=str(minimap_path),
        texture_atlas_path=str(texture_atlas_path),
        metadata={"engine": spec.engine, "map_size_km": str(spec.map_size_km)},
    )
