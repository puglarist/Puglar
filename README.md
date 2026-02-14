# Puglar Metaverse Engine Prototype

This repository now includes a **WebXR-ready PWA prototype** designed to move the project toward an Unreal-style metaverse feel while staying deployable to **Meta Quest Browser**.

## What was added

- Real-time 3D scene built with Three.js module imports.
- Physically inspired lighting, fog, shadows, and dense "city block" geometry for engine stress testing.
- Runtime performance HUD (FPS, frame-time, draw calls, VR status).
- Dynamic resolution scaling to keep Quest frame-time stable.
- WebXR VR session button with Quest-relevant optional features.
- PWA manifest + service worker for installability and offline shell support.

## Run locally

Because this is a PWA with modules and a service worker, run from a web server:

```bash
python -m http.server 4173
```

Then visit:

- `http://localhost:4173/index.html`

## Meta Quest notes

1. Open the URL in Quest Browser.
2. Use the browser install prompt to add the PWA to your apps.
3. Tap **Enter VR** to begin immersive mode.
4. Monitor frame-time in the HUD; the renderer auto-adjusts resolution when needed.

## Next steps toward Unreal-like parity

- Add asset streaming + glTF scene loading pipeline.
- Introduce spatial audio zones and animation state machines.
- Integrate authoritative multiplayer + persistence layers.
- Add post-processing profile system tuned per Quest hardware tier.
