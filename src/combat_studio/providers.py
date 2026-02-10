from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class RunPodConnector:
    """Stores RunPod endpoint details and builds auth headers for runtime calls."""

    api_key: str
    endpoint_id: str
    base_url: str = "https://api.runpod.ai/v2"
    timeout_seconds: int = 60

    def endpoint_url(self) -> str:
        return f"{self.base_url.rstrip('/')}/{self.endpoint_id}/run"

    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }


@dataclass
class HuggingFaceModelCatalog:
    """Registry of curated LLMs grouped by use-case for Combat/Netflix studio."""

    models: Dict[str, List[str]] = field(default_factory=dict)

    @classmethod
    def default_catalog(cls) -> "HuggingFaceModelCatalog":
        return cls(
            models={
                "general": [
                    "meta-llama/Llama-3.1-70B-Instruct",
                    "Qwen/Qwen2.5-72B-Instruct",
                    "mistralai/Mixtral-8x22B-Instruct-v0.1",
                    "google/gemma-2-27b-it",
                ],
                "code": [
                    "deepseek-ai/DeepSeek-Coder-V2-Instruct",
                    "bigcode/starcoder2-15b",
                    "Salesforce/codegen25-7b-instruct",
                ],
                "reasoning": [
                    "microsoft/Phi-3-medium-128k-instruct",
                    "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
                ],
                "lightweight": [
                    "meta-llama/Llama-3.2-3B-Instruct",
                    "Qwen/Qwen2.5-3B-Instruct",
                    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                ],
            }
        )

    def add_model(self, category: str, model_id: str) -> None:
        self.models.setdefault(category, [])
        if model_id not in self.models[category]:
            self.models[category].append(model_id)

    def all_models(self) -> List[str]:
        ordered: List[str] = []
        for entries in self.models.values():
            ordered.extend(entries)
        return ordered
