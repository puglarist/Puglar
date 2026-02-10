# Puglar MetaQuest Metaverse Schema

This repository now includes a GitHub Pages-friendly web bundle and JSON Schema for defining metaverse game engine features that can run in the Meta Quest browser.

## Files

- `schema/metaverse-game-engine.schema.json` – JSON Schema (Draft 2020-12) for metaverse/game-engine capability descriptors.
- `schema/example.metaquest-profile.json` – Example profile validated by the schema.
- `index.html` – Static GitHub Pages app that loads and displays schema details and a Meta Quest compatibility checklist.
- `app.js` – Client-side rendering logic with UA-based Quest detection.

## GitHub Pages + Meta Quest notes

1. Push this branch to GitHub.
2. In repository settings, enable **Pages** with source set to this branch root.
3. Open the generated Pages URL directly from the Meta Quest browser.
4. Ensure HTTPS is enabled (GitHub Pages provides HTTPS by default), which is required for WebXR APIs.

## Local check

```bash
python3 -m http.server 4173
```

Then open `http://localhost:4173`.
