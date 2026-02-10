# Puglar WebXR Metaverse Starter

This repo now contains a lightweight WebXR metaverse starter that is ready for **GitHub Pages** and **Meta Quest Browser** hand tracking.

## What it does

- Serves a Three.js immersive VR scene.
- Requests `hand-tracking` as a WebXR optional feature.
- Shows hand models and fingertip markers when tracked.
- Detects index/thumb pinch and pulls an orb to your pinch point.

## Run locally

Because this is an ES module app, use a local web server:

```bash
python3 -m http.server 4173
```

Then open http://localhost:4173.

## Deploy to GitHub Pages

1. Push to the `work` branch.
2. In GitHub repository settings:
   - Pages → Source: **GitHub Actions**.
3. The workflow `.github/workflows/deploy-pages.yml` deploys the root directory.

## Use on Meta Quest

1. Open your `https://<user>.github.io/<repo>/` URL in **Meta Quest Browser**.
2. Click **Enter VR**.
3. Allow XR permissions when prompted.
4. Bring both hands into view; pinch thumb + index to move the orb.

If hand models fail to appear, re-enable hand tracking from Quest quick settings and reload.
