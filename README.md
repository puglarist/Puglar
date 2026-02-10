# Puglar

## Rust-Inspired (Clean-Room) World Builder Prototype

This repository now includes a **clean-room pipeline** that:

1. Extracts publicly visible text structure from the Rust Fandom Building page.
2. Generates placeholder assets (SVG icons) that are original and non-copyrighted.
3. Builds a procedural map JSON.
4. Creates a GUI layout JSON for an admin/server and map UI.
5. Emits game-logic rules as JSON for a prototype survival loop.

> Important: The pipeline does **not** copy or redistribute game assets. It creates original placeholders and a reusable architecture you can extend.

### Run

```bash
python3 tools/rust_building_pipeline.py --out prototype_output
```

### Output

- `scraped/building_page.json`
- `assets/icons/*.svg`
- `maps/procedural_map.json`
- `gui/layout.json`
- `logic/game_rules.json`
