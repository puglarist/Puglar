# Puglar

## Simulator Data Scrape (Logic + Graphics)

This repository now includes a local scraper that mines the existing doctrine PDFs/archives for snippets related to:

- **simulator logic** (commands, phases, drills, awareness/training cues)
- **graphics direction** (visual framing, cross-angle cues, card/illustration language)

Run:

```bash
python scripts/scrape_simulator_data.py
```

Output:

- `data/simulator_logic_graphics_scrape.json` – extracted snippets grouped by category, with source attribution.

Use this dataset to seed simulator behavior trees/state machines and to align visual prompts/material references for high-fidelity rendering targets (e.g., Unreal Engine quality pipelines).
