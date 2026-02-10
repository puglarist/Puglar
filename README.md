# Puglar

## GitHub release automation

A workflow was added at `.github/workflows/github-release.yml`.

- Trigger: push a tag like `v1.0.0` or run the workflow manually.
- Result: creates a GitHub Release and uploads all `*.pdf` and `*.zip` files as release assets.

## PWA metaverse deployment

A deploy workflow was added at `.github/workflows/deploy-pwa-metaverse.yml`.

- Trigger: changes to `metaverse-pwa/**` on `main` or `work`, or manual dispatch.
- Result: publishes `metaverse-pwa/` to GitHub Pages.

The PWA entrypoint is `metaverse-pwa/index.html`, with a manifest and service worker for offline caching.
