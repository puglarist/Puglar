# Puglar MetaQuest Metaverse Schema

This repository includes a GitHub Pages-friendly web bundle and JSON Schema for defining metaverse game engine capability profiles that are compatible with Meta Quest browser-based WebXR experiences.

## Files

- `schema/metaverse-game-engine.schema.json` – JSON Schema (Draft 2020-12) with Quest-specific conditional requirements.
- `schema/example.metaquest-profile.json` – Example profile intended to pass the schema.
- `index.html` – Static GitHub Pages app that performs runtime and validation checks.
- `app.js` – Client-side diagnostics and schema/profile smoke checks.

## What is improved

- Quest-targeted profiles now require `runtime.webXR.immersiveVR=true` and `runtime.webXR.controllerSupport=true`.
- The demo page now checks:
  - secure context,
  - `navigator.xr` availability,
  - immersive VR session support,
  - Quest user-agent hints,
  - structural schema/profile expectations.

## GitHub Pages + Meta Quest setup

1. Push to GitHub.
2. Enable **Pages** from the repository root on this branch.
3. Open the generated URL from Meta Quest Browser.
4. Confirm the runtime checklist shows WebXR-related checks as passing.

## Local check

```bash
python3 -m http.server 4173
```

Then open `http://localhost:4173`.
