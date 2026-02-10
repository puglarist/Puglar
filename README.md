# Puglar Metaverse Streaming Prototype

This repository now includes a front-end prototype that combines:

- **ROLL SDK integration scaffold** for wallet/network initialization and media upload flow.
- **MTV movie channel logic** for now-playing/trending/genre rails.
- **Uploader workflow** for movie/video ingestion into an in-memory library.
- **AdSense placeholders** so monetization can be wired in once approved IDs are available.

## Run locally

```bash
cd /workspace/Puglar
python3 -m http.server 4173
```

Open `http://localhost:4173/app/`.

## Production checklist

1. Replace mock `RollSDKAdapter` implementation in `app/app.js` with the real ROLL SDK package calls.
2. Move library persistence from in-memory storage to your backend/database.
3. Replace AdSense placeholders (`ca-pub-REPLACE_WITH_YOUR_ID`, sample slot IDs) with verified publisher + slot IDs.
4. Add content moderation, rights management, and legal compliance for uploaded media.
5. Add authentication and role-based access for creators, moderators, and admins.
