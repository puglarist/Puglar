# Puglar

## BO6 weapon asset scraper

This repository now includes a build script that scrapes the GamesAtlas Black Ops 6 weapons page and creates a local asset bundle.

### Run

```bash
python scripts/build_gamesatlas_bo6_assets.py
```

### Output

- `build/bo6_weapons/page.html` (captured source page)
- `build/bo6_weapons/weapons.json` (structured metadata)
- `build/bo6_weapons/images/*` (downloaded weapon images when reachable)

If the environment blocks outbound access to `gamesatlas.com`, run the script in a network that allows that endpoint.
