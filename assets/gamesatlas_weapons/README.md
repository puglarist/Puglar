# GamesAtlas Weapons scrape asset pack

Source URL scraped:
- https://www.gamesatlas.com/cod-warzone-2/weapons/

## Reverse-engineering notes

The `/cod-warzone-2/weapons/` page currently renders a **combined cross-title weapons listing** in server HTML cards (not an exposed JSON API feed for this page path).

Extraction strategy used:
1. Load the page in a headless browser.
2. Select `a:has(img)` nodes.
3. Keep only cards where:
   - `href` contains `/weapons/`
   - image path contains `/weapons/resized/`
4. Parse card text into:
   - title
   - category
   - optional season label
5. Derive `game` slug from card URL (`/cod-.../`).
6. De-duplicate cards by `(href, image)`.

## Built assets

- `weapons.json`: normalized weapon card records.
- `weapons.csv`: tabular export for analytics.
- `summary.json`: counts by game and category.

## Snapshot stats

- Total de-duplicated weapons: **164**
- Games present in this page snapshot:
  - `cod-black-ops-6`: 67
  - `cod-modern-warfare-3`: 60
  - `cod-black-ops-7`: 37
