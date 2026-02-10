# Puglar

## VR Inventory UI Prototype (Meta Quest Friendly)

This repo now includes an **original, game-style inventory HUD prototype** inspired by the visual direction you shared, but not copying proprietary GTA assets.

Path: `vr-ui-prototype/`

### What is included
- `index.html` — responsive panel layout for inventory, profile, avatar, and actions.
- `styles.css` — dark neon visual system designed for readability in headset-style display capture.
- `app.js` — mock data renderer for quick slots, inventory cells, and transaction history.
- `hf_asset_pipeline.py` — helper script that generates a structured payload template for:
  - `olympusmonsgames/unreal-engine-5-code-split`
  - `facebook/sam-3d-objects`

### Run locally
```bash
cd vr-ui-prototype
python3 -m http.server 4173
```
Then open `http://localhost:4173`.

### Generate 3D asset request payload template
```bash
cd vr-ui-prototype
python3 hf_asset_pipeline.py
cat artifacts/hf_asset_payloads.json
```

### Notes
- This is a **clean-room prototype** for UI/UX exploration.
- Hooking to real game memory, private scripts, or copyrighted pipelines is intentionally out of scope.
