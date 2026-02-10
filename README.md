# Puglar

This repo now contains a reverse-engineered GTA 6 weapons dataset sourced from:

- https://www.gtabase.com/gta-6/weapons/

## What was built out

- `data/gta6_weapons.json`
  - Structured list of currently indexed GTA 6 weapons.
  - Includes categories, real-world inspiration (`based_on`), status (`confirmed` vs `unconfirmed`), and source evidence.
- `scripts/build_weapons_catalog.py`
  - Converts the JSON into a human-readable markdown catalog.
- `data/gta6_weapons.md`
  - Generated markdown report.

## Generate the markdown catalog

```bash
python3 scripts/build_weapons_catalog.py
```

## Notes

- "Confirmed" entries are the ones with working dedicated weapon pages under `/gta-6/weapons/<slug>`.
- "Unconfirmed" entries are pulled from temporary image assets on the source page (`/images/gta-6/weapons/temp/*`) that do not currently have live detail pages.
