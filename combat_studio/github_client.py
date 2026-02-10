from __future__ import annotations

import json
import os
from typing import Any, Dict
from urllib import request


class GitHubClient:
    """GitHub API wrapper for storing simulation artifacts and reports."""

    def __init__(self, token: str | None = None, owner: str | None = None, repo: str | None = None) -> None:
        self.token = token or os.getenv("GITHUB_TOKEN", "")
        self.owner = owner or os.getenv("GITHUB_OWNER", "")
        self.repo = repo or os.getenv("GITHUB_REPO", "")
        self.base_url = "https://api.github.com"

    def create_issue(self, title: str, body: str, labels: list[str] | None = None) -> Dict[str, Any]:
        if not self.token or not self.owner or not self.repo:
            raise ValueError("GitHub credentials are missing. Set GITHUB_TOKEN, GITHUB_OWNER, and GITHUB_REPO.")

        req = request.Request(
            url=f"{self.base_url}/repos/{self.owner}/{self.repo}/issues",
            data=json.dumps({"title": title, "body": body, "labels": labels or ["simulation"]}).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))

    def trigger_workflow(self, workflow_id: str, ref: str, inputs: Dict[str, str] | None = None) -> None:
        if not self.token or not self.owner or not self.repo:
            raise ValueError("GitHub credentials are missing. Set GITHUB_TOKEN, GITHUB_OWNER, and GITHUB_REPO.")

        req = request.Request(
            url=f"{self.base_url}/repos/{self.owner}/{self.repo}/actions/workflows/{workflow_id}/dispatches",
            data=json.dumps({"ref": ref, "inputs": inputs or {}}).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with request.urlopen(req, timeout=30):
            return
