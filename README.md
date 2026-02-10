# Puglar VR Metaverse

This repository now ships a lightweight **WebXR metaverse world** designed to run from **GitHub Pages** and work in the **Meta Quest Browser**.

## What is included

- A-Frame powered 3D world with room-specific landmarks.
- VR-ready controls (`Enter VR`, Quest controllers, WASD/thumbstick movement).
- Shareable room links using `?room=<name>` so people can open the same themed world quickly.

## Run locally

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Deploy to GitHub Pages

1. Push this branch to GitHub.
2. In the repository settings, open **Pages**.
3. Set **Source** to **Deploy from a branch**.
4. Choose `main` (or your default branch) and `/ (root)`.
5. Save and wait for the Pages URL to become available.

## Use on Meta Quest

1. Open your GitHub Pages URL in Quest Browser.
2. Tap **Enter VR**.
3. Move with thumbsticks and look around naturally.
4. Use the **Copy Room Link** button if you want others to load the same room seed.

> Note: GitHub Pages is static hosting. This build provides a shared room seed experience, but not real-time multiplayer state syncing.
