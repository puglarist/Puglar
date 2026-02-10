#!/usr/bin/env python3
"""Run parallel DeepSeek agents and synthesize one final answer.

Usage:
  export DEEPSEEK_API_KEY=...
  python deepseek_agents.py \
    --task "Build go-to-market plan" \
    --agent "Strategist:Plan channels and positioning" \
    --agent "Analyst:Estimate costs and ROI" \
    --agent "Executor:Define weekly actions"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Iterable
from urllib import error, request


DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"


@dataclass(frozen=True)
class AgentSpec:
    name: str
    role_prompt: str


def parse_agent(raw: str) -> AgentSpec:
    if ":" not in raw:
        raise ValueError(
            f"Invalid --agent '{raw}'. Expected format: 'Name:Role instructions'"
        )
    name, role = raw.split(":", 1)
    name = name.strip()
    role = role.strip()
    if not name or not role:
        raise ValueError(
            f"Invalid --agent '{raw}'. Name and role instructions must be non-empty."
        )
    return AgentSpec(name=name, role_prompt=role)


def deepseek_chat_completion(
    *,
    api_key: str,
    base_url: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.3,
) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
    }

    req = request.Request(
        url=f"{base_url.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"DeepSeek API HTTP {exc.code}: {body}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"DeepSeek API connection error: {exc}") from exc

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected DeepSeek API response shape: {data}") from exc


def run_parallel_agents(
    *,
    api_key: str,
    base_url: str,
    model: str,
    task: str,
    agents: Iterable[AgentSpec],
) -> list[tuple[str, str]]:
    specs = list(agents)
    results: list[tuple[str, str]] = []

    def one(spec: AgentSpec) -> tuple[str, str]:
        system_prompt = (
            "You are a high-performance specialist AI agent. "
            "Provide practical, concise, execution-ready output."
        )
        user_prompt = (
            f"Global objective:\n{task}\n\n"
            f"Your role ({spec.name}):\n{spec.role_prompt}\n\n"
            "Return your best contribution for this role. "
            "Use headings, assumptions, and concrete steps."
        )
        out = deepseek_chat_completion(
            api_key=api_key,
            base_url=base_url,
            model=model,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )
        return spec.name, out

    with ThreadPoolExecutor(max_workers=len(specs)) as pool:
        future_map = {pool.submit(one, spec): spec for spec in specs}
        for future in as_completed(future_map):
            results.append(future.result())

    # keep stable order by original spec order
    order = {spec.name: i for i, spec in enumerate(specs)}
    results.sort(key=lambda item: order[item[0]])
    return results


def synthesize(
    *,
    api_key: str,
    base_url: str,
    model: str,
    task: str,
    agent_outputs: list[tuple[str, str]],
) -> str:
    compiled = "\n\n".join(
        f"## {name}\n{text}" for name, text in agent_outputs
    )
    system_prompt = (
        "You are a synthesis lead. Merge multiple specialist outputs into one coherent "
        "plan with clear priorities, sequencing, and trade-offs."
    )
    user_prompt = (
        f"Objective:\n{task}\n\n"
        "Specialist outputs:\n"
        f"{compiled}\n\n"
        "Produce:\n"
        "1) Unified strategy\n"
        "2) 7-day execution plan\n"
        "3) Key risks + mitigations\n"
        "4) Metrics to track\n"
    )

    return deepseek_chat_completion(
        api_key=api_key,
        base_url=base_url,
        model=model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run parallel DeepSeek agents and synthesize one final result."
    )
    parser.add_argument("--task", required=True, help="Overall objective for the agent swarm.")
    parser.add_argument(
        "--agent",
        action="append",
        default=[],
        help="Agent spec in 'Name:Role instructions' format. Can be repeated.",
    )
    args = parser.parse_args()

    if len(args.agent) < 2:
        print(
            "Please provide at least 2 --agent values for parallelization.",
            file=sys.stderr,
        )
        return 2

    try:
        agents = [parse_agent(a) for a in args.agent]
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("Missing DEEPSEEK_API_KEY environment variable.", file=sys.stderr)
        return 2

    model = os.getenv("DEEPSEEK_MODEL", DEFAULT_MODEL)
    base_url = os.getenv("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL)

    try:
        outputs = run_parallel_agents(
            api_key=api_key,
            base_url=base_url,
            model=model,
            task=args.task,
            agents=agents,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"Failed during parallel agent execution: {exc}", file=sys.stderr)
        return 1

    print("\n=== AGENT OUTPUTS ===\n")
    for name, text in outputs:
        print(f"--- {name} ---")
        print(text)
        print()

    try:
        final = synthesize(
            api_key=api_key,
            base_url=base_url,
            model=model,
            task=args.task,
            agent_outputs=outputs,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"Failed during synthesis: {exc}", file=sys.stderr)
        return 1

    print("\n=== SYNTHESIZED PLAN ===\n")
    print(final)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
