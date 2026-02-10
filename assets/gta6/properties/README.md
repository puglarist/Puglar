# GTA 6 Properties (GTABase) - Scraped Assets

This folder contains scraped data assets from:
- https://www.gtabase.com/gta-6/properties/

## Files
- `gta6_properties.json`: normalized JSON dataset.
- `gta6_properties.csv`: flat CSV for spreadsheet/database import.

## Notes
- At scrape time, GTABase listed **1 clearly confirmed property** on this page:
  - Leonida Keys Safehouse
- Additional properties are described as coming soon after release.
- Direct CLI HTTP requests from this environment were blocked by a proxy (HTTP 403 tunnel), so extraction was done through the browser automation runtime.
