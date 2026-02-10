# Puglar Web App

This repository now contains a simple static web app (`index.html`, `styles.css`, `script.js`) that can be hosted with **GitHub Pages**.

## How to open the web app from GitHub Pages

1. Push this repository to GitHub.
2. In your GitHub repo, go to **Settings → Pages**.
3. Under **Build and deployment**, choose:
   - **Source**: *Deploy from a branch*
   - **Branch**: `main` (or your default branch), folder `/ (root)`
4. Click **Save**.
5. Wait for deployment to finish, then open:

```text
https://<your-github-username>.github.io/<repo-name>/
```

Example:

```text
https://octocat.github.io/Puglar/
```

## Open locally (without GitHub Pages)

Run:

```bash
python3 -m http.server 8080
```

Then open:

```text
http://localhost:8080
```
