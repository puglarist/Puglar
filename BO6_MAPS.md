# BO6 Maps: Scraped Index + Reverse-Engineered Build Blueprints

This repository now includes a structured Black Ops 6 map dataset sourced from:

- https://www.gamesatlas.com/cod-black-ops-6/maps/

## Files

- `data/bo6_maps_scraped_index.json`  
  Normalized map index (slug, name, source URL, playlist support, release window, map type).
- `tools/build_bo6_maps.py`  
  Builder that transforms the scraped index into map blueprint files.
- `build/bo6_map_blueprints/*.json`  
  One reverse-engineered map blueprint per map.
- `build/bo6_maps_blueprints.json`  
  Combined file with all generated map blueprints.

## Build

```bash
python tools/build_bo6_maps.py
```

## Reverse-engineering approach

The generated blueprint files use deterministic heuristics to infer base layout guidance:

- `size_class`: inferred from playlist support and known small-map slugs.
- `lane_count`: 2 for small MP maps, 3 for medium MP maps, 5 for zombies maps.
- `combat_pace`: high for maps supporting 2v2, medium for standard 6v6, scaling for zombies.
- `dominant_engagement_range`: close for small maps, mixed otherwise.

These blueprints are intended as implementation scaffolds for graybox/prototyping workflows, not official developer layouts.
