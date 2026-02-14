from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any
import json
import os
import urllib.request


@dataclass
class AssetRequest:
    prompt: str
    style: str = "mw2 realism"
    poly_budget: int = 25000
    texture_resolution: int = 2048


class HuggingFaceAssetClient:
    """Thin client for 3D generation-capable Hugging Face endpoints."""

    def __init__(self, model_endpoint: str, token: Optional[str] = None):
        self.model_endpoint = model_endpoint
        self.token = token or os.environ.get("HF_TOKEN")

    def build_payload(self, req: AssetRequest) -> Dict[str, Any]:
        return {
            "inputs": {
                "prompt": req.prompt,
                "style": req.style,
                "poly_budget": req.poly_budget,
                "texture_resolution": req.texture_resolution,
                "format": "glb",
            }
        }

    def request_asset(self, req: AssetRequest, timeout_s: int = 120) -> Dict[str, Any]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        body = json.dumps(self.build_payload(req)).encode("utf-8")
        request = urllib.request.Request(self.model_endpoint, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(request, timeout=timeout_s) as response:
            return json.loads(response.read().decode("utf-8"))
