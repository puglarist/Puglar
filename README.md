# Puglar Metaverse (Meta Quest + GitHub Pages)

This repository now includes a deployable WebXR metaverse built with **A-Frame** and optimized for **Meta Quest Browser**.

## What you get

- VR-ready 3D world with a training dome and doctrine library
- Desktop fallback controls (WASD + mouse)
- In-world interactive pads for teleporting between areas
- In-world document wall linking core Puglar PDFs
- Static hosting compatibility for GitHub Pages (no build step needed)

## Run locally

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000`.

## Deploy on GitHub Pages

1. Push this repo to GitHub.
2. In GitHub, open **Settings → Pages**.
3. Under **Build and deployment**, choose:
   - **Source**: `Deploy from a branch`
   - **Branch**: `main` (or your default branch), folder `/ (root)`
4. Save and wait for deployment.
5. Open the Pages URL from Meta Quest Browser.

## Meta Quest compatibility checklist

- Use latest **Meta Quest Browser**
- Keep repo public or ensure your Quest browser can access it
- Ensure HTTPS (GitHub Pages provides this automatically)
- Click **Enter VR (Meta Quest)** in the top-left panel

## Project files

- `index.html` — A-Frame scene and interactive world layout
- `app.js` — WebXR detection, teleport handlers, document links
- `styles.css` — Overlay UI and accessible control styling

