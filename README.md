# Puglar

## Why your GitHub Pages WebXR build is not loading

If GitHub Pages only shows a simple documentation page (or a blank/default page), it usually means there is no deployable web app entry point in this repo yet.

This repository currently contains PDFs and archives, but no `index.html`, app bundle, or static web asset structure for a WebXR scene.

### Quick diagnosis checklist

1. **No app entry file**
   - GitHub Pages needs an `index.html` at the published root (or in `/docs` if that source is selected).
2. **Wrong Pages source branch/folder**
   - In repo settings, confirm Pages source is set to the branch/folder where your built app files actually exist.
3. **WebXR on iOS limitation**
   - iOS Safari does **not** provide general WebXR support like Chrome on Android.
   - So even if deployment succeeds, immersive VR mode can fail on iPhone/iPad.
4. **Incorrect asset paths**
   - If your app was built assuming `/` root but is hosted at `https://<user>.github.io/<repo>/`, assets can 404 unless paths are adjusted.
5. **HTTPS and secure context**
   - GitHub Pages is HTTPS, which is good; but any mixed-content HTTP asset calls will fail.

### Should you switch to RunPod/cloud GPU?

For **hosting a static WebXR frontend**, you generally do **not** need a GPU server.

Use GPU/cloud compute only if you specifically need:
- real-time AI inference,
- heavy backend rendering/streaming,
- or server-side compute beyond static hosting.

For a typical web metaverse client, GitHub Pages (or Cloudflare Pages/Netlify/Vercel) is usually enough for frontend hosting.

### Practical next step

Add and deploy a minimal static app first:

```text
/ (repo root)
  index.html
  /assets
  /js
```

Then verify:
- the page loads on desktop,
- browser console has no 404 errors,
- and test XR behavior on a device/browser that supports WebXR.

If your target is specifically iOS immersive AR/VR, consider platform alternatives (e.g., native app wrapper or iOS-focused XR frameworks) because this is often a platform support issue, not just deployment.
