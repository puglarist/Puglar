# Puglar

This repository now includes a lightweight **Combat Studio toolkit** under `src/combat_studio` for orchestrating:

- Netflix studio pipeline stages
- RunPod connectivity helpers
- Hugging Face LLM catalog expansion
- Enhanced torrent profile/manifest building
- Gameplay logic packs for GTA, MW2 ProMod, COD4 ProMod, and Minecraft (with toggleable logic + mob menu controls)

## Quick start

```bash
python3 -m unittest discover -s tests
```

## Module overview

- `providers.py`: RunPod connector + Hugging Face model catalog.
- `netflix_studio.py`: stage-based project pipeline.
- `torrent_builder.py`: reusable torrent profiles and manifest generation.
- `game_logic.py`: logic presets and toggles for requested game systems.
