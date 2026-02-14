# Puglar

Puglar is now scaffolded as a **Progressive Web App (PWA)** starter with a robust **Prisma data schema** intended for immersive training, simulation, progression tracking, and content delivery.

## What's included

- `prisma/schema.prisma`: expanded schema for users, teams, training plans, sessions, progression, simulations, assets, and telemetry.
- `web/`: vanilla PWA starter (installable + offline fallback) with:
  - `index.html`
  - `styles.css`
  - `app.js`
  - `manifest.webmanifest`
  - `sw.js`
- `scripts/build.mjs`: lightweight build script that copies `web/` assets into `dist/`.

## Quick start

```bash
npm install
npm run build
npm run check
```

Then serve `dist/` with any static file server.
