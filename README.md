# Puglar

## GTA 6 Vehicles Builder

This repository now includes a small builder script that can collect vehicle entries from the GTABase GTA 6 vehicles page and export them as JSON.

### Build the dataset

```bash
python scripts/build_gta6_vehicles.py --url https://www.gtabase.com/gta-6/vehicles/ --out data/gta6_vehicles.json
```

### Offline parsing mode

If you already have an HTML copy of the page:

```bash
python scripts/build_gta6_vehicles.py --from-file /path/to/vehicles.html --out data/gta6_vehicles.json
```
