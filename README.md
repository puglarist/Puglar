# Puglar Metaverse (GitHub Pages + Firebase)

This repo now ships a **static metaverse client** that runs directly on GitHub Pages and uses Firebase Firestore for realtime player presence.

## What is included

- `index.html`: UI + canvas shell
- `styles.css`: world and HUD styling
- `js/main.js`: Three.js scene + realtime Firestore sync
- `js/firebase-config.js`: your Firebase web config (replace placeholders)
- `.github/workflows/deploy-pages.yml`: automatic GitHub Pages deployment from `main`

## Quick setup

1. Create a Firebase project and add a **Web App**.
2. Copy the config values into `js/firebase-config.js`.
3. Enable **Cloud Firestore** in production mode.
4. Add temporary Firestore rules while testing:

```txt
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /worlds/{roomId}/players/{playerId} {
      allow read, write: if true;
    }
  }
}
```

> Tighten these rules before production use.

5. Push to `main`.
6. In GitHub repo settings, set **Pages source** to **GitHub Actions**.

After deployment, open your GitHub Pages URL and click **Join World**.

## Notes for GitHub Pages compatibility

- No backend server is required; everything is static files.
- Firebase client SDK and Three.js are loaded from CDNs.
- `.nojekyll` is included to avoid Jekyll processing issues.
