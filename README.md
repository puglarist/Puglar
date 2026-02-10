# Puglar

## Three.js VR/Metaverse Graphics Upgrade

This repository now includes a **Three.js package baseline** for higher-fidelity VR/metaverse and game-engine style graphics.

### Added package stack

- `three`: core renderer and WebXR support.
- `postprocessing`: modern effect pipeline (bloom, tone mapping, DOF, motion effects).
- `screen-space-reflections`: higher-quality real-time reflections.
- `three-mesh-bvh`: accelerated raycasting and spatial queries for large worlds.
- `three-stdlib`: production-ready helpers/loaders/controls.
- `camera-controls`: smoother, cinematic camera movement.
- `@dimforge/rapier3d-compat`: performant physics for immersive scenes.
- `stats.js`: real-time FPS diagnostics.

Optional React stack:

- `@react-three/fiber`, `@react-three/drei`, `@react-three/xr`.

### Why this can feel "10x better"

The biggest gains come from combining:

1. Better visual effects (`postprocessing`, SSR).
2. Better scene-query performance (`three-mesh-bvh`).
3. Better interaction quality (physics + camera control + XR tooling).
4. Continuous profiling (`stats.js`) to keep frame time VR-safe.

> Note: "10x" in graphics is workload-dependent and should be validated with frame-time benchmarks on target hardware.

### Install

```bash
npm install
```

### Quick check

```bash
npm run check
```
