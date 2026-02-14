# Puglar

## DeepSeek AI Agents (Parallel Workflows)

This repo includes a script to run **parallel DeepSeek agents** so you can split one task into many specialist workstreams and merge outputs.

## What this enables
- Larger built-in agent teams via presets.
- Multiple presets at once (`--preset` can be repeated).
- Extra custom agents layered on top of presets.
- Controlled concurrency and per-call timeout.
- Partial-failure resilience (successful agents still synthesize).

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

### 2) List presets

```bash
python3 deepseek_agents.py --list-presets
```

### 3) Run with a preset

```bash
python3 deepseek_agents.py \
  --task "Design a 4-week training plan and risk controls" \
  --preset execution
```

### 4) Run with multiple presets and custom agents

```bash
python3 deepseek_agents.py \
  --task "Design a 4-week training plan and risk controls" \
  --preset execution \
  --preset product \
  --agent "Budget Lead:Estimate weekly resource requirements and costs" \
  --agent "Comms Lead:Prepare stakeholder updates and escalation paths"
```

### 5) Control scale and behavior

```bash
python3 deepseek_agents.py \
  --task "Plan v1 launch" \
  --preset strategy \
  --max-workers 6 \
  --agent-temperature 0.3 \
  --synthesis-temperature 0.2 \
  --timeout-s 120
```

## Built-in presets
- `execution` (8 agents)
- `product` (8 agents)
- `strategy` (6 agents)

## Files
- `deepseek_agents.py` — DeepSeek multi-agent runner with presets, concurrency controls, and synthesis.
