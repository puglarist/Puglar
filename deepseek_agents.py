#!/usr/bin/env python3
"""Run parallel DeepSeek agents and synthesize one final answer.

Examples:
  export DEEPSEEK_API_KEY=...

  # Use one built-in preset
  python deepseek_agents.py --task "Build go-to-market plan" --preset execution

  # Use multiple presets + custom agents
  python deepseek_agents.py \
    --task "Launch v1" \
    --preset execution --preset product \
    --agent "Finance:Estimate weekly burn and ROI"

  # Discover presets
  python deepseek_agents.py --list-presets
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

PRESET_AGENTS: dict[str, list[str]] = {
    "execution": [
        "Planner:Create a phased execution plan with priorities and dependencies.",
        "Researcher:Gather assumptions, unknowns, and validation questions.",
        "Implementer:Convert strategy into concrete daily/weekly actions.",
        "Critic:Stress-test the plan and identify weak points.",
        "Risk Officer:Map risks, early warning indicators, and mitigations.",
        "Metrics Lead:Define KPIs, baselines, and review cadence.",
        "Comms Lead:Create status update format and escalation routes.",
        "Ops Lead:Define execution cadence and accountability checkpoints.",
    ],
    "product": [
        "PM:Define product goals, scope, and milestone sequencing.",
        "UX:Outline user journeys, friction points, and UX requirements.",
        "Engineer:Propose architecture and implementation milestones.",
        "QA:Create test strategy and release quality gates.",
        "Security:Highlight security/privacy risks and controls.",
        "Growth:Define adoption loop, activation, and retention levers.",
        "Data:Define instrumentation and analytics events.",
        "Support:Prepare launch runbooks and support workflows.",
    ],
    "strategy": [
        "Strategist:Define strategic options and trade-offs.",
        "Market Analyst:Estimate TAM/SAM/SOM and demand signals.",
        "Competitor Analyst:Map alternatives and differentiation.",
        "Finance:Model budget scenarios, constraints, and ROI.",
        "Legal/Compliance:Identify policy and regulatory considerations.",
        "Operator:Convert strategy into an operating plan.",
    ],
}


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
    temperature: float,
    timeout_s: int,
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
        with request.urlopen(req, timeout=timeout_s) as resp:
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
    temperature: float,
    timeout_s: int,
    max_workers: int,
) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    specs = list(agents)
    results: list[tuple[int, str, str]] = []
    failures: list[tuple[str, str]] = []

    def one(index: int, spec: AgentSpec) -> tuple[int, str, str]:
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
            temperature=temperature,
            timeout_s=timeout_s,
        )
        return index, spec.name, out

    workers = max(1, min(max_workers, len(specs)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        future_map = {
            pool.submit(one, idx, spec): (idx, spec)
            for idx, spec in enumerate(specs)
        }
        for future in as_completed(future_map):
            idx, spec = future_map[future]
            try:
                results.append(future.result())
            except Exception as exc:  # noqa: BLE001
                failures.append((spec.name, str(exc)))

    # stable order by initial position; safe even with duplicate names
    results.sort(key=lambda item: item[0])
    ordered_results = [(name, text) for _, name, text in results]
    return ordered_results, failures


def synthesize(
    *,
    api_key: str,
    base_url: str,
    model: str,
    task: str,
    agent_outputs: list[tuple[str, str]],
    temperature: float,
    timeout_s: int,
) -> str:
    compiled = "\n\n".join(f"## {name}\n{text}" for name, text in agent_outputs)
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
        temperature=temperature,
        timeout_s=timeout_s,
    )


def build_agents(agent_args: list[str], preset_args: list[str]) -> list[AgentSpec]:
    raw_agents: list[str] = []
    for preset in preset_args:
        raw_agents.extend(PRESET_AGENTS[preset])
    raw_agents.extend(agent_args)
    return [parse_agent(raw) for raw in raw_agents]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run parallel DeepSeek agents and synthesize one final result."
    )
    parser.add_argument("--task", help="Overall objective for the agent swarm.")
    parser.add_argument(
        "--agent",
        action="append",
        default=[],
        help="Agent spec in 'Name:Role instructions' format. Can be repeated.",
    )
    parser.add_argument(
        "--preset",
        action="append",
        default=[],
        choices=sorted(PRESET_AGENTS.keys()),
        help="Predefined multi-agent pack to add. Can be repeated.",
    )
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="List built-in presets and exit.",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=8,
        help="Concurrency limit for agent execution (default: 8).",
    )
    parser.add_argument(
        "--agent-temperature",
        type=float,
        default=0.3,
        help="Temperature for specialist agents (default: 0.3).",
    )
    parser.add_argument(
        "--synthesis-temperature",
        type=float,
        default=0.2,
        help="Temperature for synthesis pass (default: 0.2).",
    )
    parser.add_argument(
        "--timeout-s",
        type=int,
        default=120,
        help="HTTP timeout in seconds per DeepSeek call (default: 120).",
    )
    args = parser.parse_args()

    if args.list_presets:
        print("Available presets:")
        for name, preset_agents in PRESET_AGENTS.items():
            print(f"- {name} ({len(preset_agents)} agents)")
        return 0

    if not args.task:
        print("Missing --task. Provide an objective, or use --list-presets.", file=sys.stderr)
        return 2

    if args.max_workers < 1:
        print("--max-workers must be >= 1.", file=sys.stderr)
        return 2

    try:
        agents = build_agents(args.agent, args.preset)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if len(agents) < 2:
        print(
            "Please provide at least 2 total agents (via --preset and/or --agent).",
            file=sys.stderr,
        )
        return 2

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("Missing DEEPSEEK_API_KEY environment variable.", file=sys.stderr)
        return 2

    model = os.getenv("DEEPSEEK_MODEL", DEFAULT_MODEL)
    base_url = os.getenv("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL)

    outputs, failures = run_parallel_agents(
        api_key=api_key,
        base_url=base_url,
        model=model,
        task=args.task,
        agents=agents,
        temperature=args.agent_temperature,
        timeout_s=args.timeout_s,
        max_workers=args.max_workers,
    )

    if not outputs:
        print("All agent calls failed. Nothing to synthesize.", file=sys.stderr)
        for name, err in failures:
            print(f"- {name}: {err}", file=sys.stderr)
        return 1

    print("\n=== AGENT OUTPUTS ===\n")
    for name, text in outputs:
        print(f"--- {name} ---")
        print(text)
        print()

    if failures:
        print("=== AGENT FAILURES (partial) ===", file=sys.stderr)
        for name, err in failures:
            print(f"- {name}: {err}", file=sys.stderr)

    try:
        final = synthesize(
            api_key=api_key,
            base_url=base_url,
            model=model,
            task=args.task,
            agent_outputs=outputs,
            temperature=args.synthesis_temperature,
            timeout_s=args.timeout_s,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"Failed during synthesis: {exc}", file=sys.stderr)
        return 1

    print("\n=== SYNTHESIZED PLAN ===\n")
    print(final)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
