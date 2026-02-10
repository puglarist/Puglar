# Puglar

Meta Quest-ready static launcher for doctrine PDFs and archives.

## Deploy

This repo deploys through GitHub Pages using `.github/workflows/static.yml`.

1. Push to `main`.
2. In repository settings, set Pages source to **GitHub Actions**.
3. Open the published URL in Meta Quest Browser.

## Local smoke test

```bash
python3 -m http.server 4173
```

Then open `http://localhost:4173`.
