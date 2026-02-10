from __future__ import annotations

import json
import os
from typing import Any, Dict
from urllib import request


class RunPodClient:
    """Minimal RunPod API wrapper for submitting simulation workloads."""

    def __init__(self, api_key: str | None = None, endpoint_id: str | None = None) -> None:
        self.api_key = api_key or os.getenv("RUNPOD_API_KEY", "")
        self.endpoint_id = endpoint_id or os.getenv("RUNPOD_ENDPOINT_ID", "")
        self.base_url = "https://api.runpod.ai/v2"

    def submit_simulation(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.api_key or not self.endpoint_id:
            raise ValueError("RunPod credentials are missing. Set RUNPOD_API_KEY and RUNPOD_ENDPOINT_ID.")

        req = request.Request(
            url=f"{self.base_url}/{self.endpoint_id}/run",
            data=json.dumps({"input": payload}).encode("utf-8"),
            headers={"Authorization": self.api_key, "Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))

    def get_status(self, job_id: str) -> Dict[str, Any]:
        if not self.api_key or not self.endpoint_id:
            raise ValueError("RunPod credentials are missing. Set RUNPOD_API_KEY and RUNPOD_ENDPOINT_ID.")

        req = request.Request(
            url=f"{self.base_url}/{self.endpoint_id}/status/{job_id}",
            headers={"Authorization": self.api_key},
            method="GET",
        )
        with request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
