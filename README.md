# Puglar

## DeepSeek AI Agents (Parallel Workflows)

This repo now includes a starter script to run **parallel DeepSeek agents** so you can split a task into multiple workstreams and combine results.

### What this enables
- Run multiple AI agents at the same time against the same objective.
- Assign each agent a different role (planner, critic, implementer, etc.).
- Merge outputs into one actionable final result.

## Quick start

### 1) Set your API key

```bash
export DEEPSEEK_API_KEY="<your_deepseek_api_key>"
```

Optional overrides:

```bash
export DEEPSEEK_MODEL="deepseek-chat"
export DEEPSEEK_BASE_URL="https://api.deepseek.com"
```

### 2) Run parallel agents

```bash
python3 deepseek_agents.py \
  --task "Design a 4-week training plan and risk controls" \
  --agent "Planner:Create the timeline and milestones" \
  --agent "Risk Officer:Identify failure modes and mitigations" \
  --agent "Operator:Turn the plan into daily execution steps"
```

The script calls DeepSeek concurrently and then asks a synthesizer pass to combine all agent outputs into one final response.

## Files
- `deepseek_agents.py` — production-ready starter for DeepSeek multi-agent parallel execution.
