# Puglar XR (GitHub Pages + Meta Quest)

This repository now includes a lightweight **WebXR metaverse starter** that can be hosted on **GitHub Pages** and run as a **PWA** with **hand-tracking** on Meta Quest.

## Features

- WebXR immersive VR session (`immersive-vr`) with `hand-tracking`
- Visible per-joint spheres for left/right hands when Quest detects hands
- Simple 3D world scaffold (floor, grid, ambient structures)
- PWA support (manifest + service worker) for installable behavior
- GitHub Pages-friendly static files

## Quick start (local)

```bash
python3 -m http.server 8080
```

Open <http://localhost:8080>.

> Note: full VR + hand tracking requires Quest Browser over HTTPS on a device with WebXR support.

## Deploy to GitHub Pages

1. Push this repository to GitHub.
2. In **Settings → Pages**, select the current branch and root folder (`/`).
3. Wait for Pages deployment.
4. Open the `https://<user>.github.io/<repo>/` URL in Meta Quest Browser.

## Meta Quest usage checklist

- Use **Meta Quest Browser**
- Allow motion/sensor permissions if prompted
- Ensure hand tracking is enabled in Quest settings
- Tap **Enter VR**
- Bring both hands into camera view

## Files

- `index.html` – shell UI + module entry
- `styles.css` – overlay and theme styling
- `app.js` – Three.js scene, WebXR setup, and hand-joint rendering
- `manifest.webmanifest` – PWA metadata
- `sw.js` – service worker for caching core assets
