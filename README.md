# Puglar

## Fortnite + Warzone world server GUI

This repository now includes a simple Python GUI that scrapes public service-status sources and shows world server health for:

- **Fortnite** (from Epic Games Status API)
- **Call of Duty: Warzone** (from Activision Online Services page)

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server_status_gui.py
```

## Notes

- The app uses scraping/public endpoints, so layout/API changes on provider sites can affect parsing.
- Refresh can be done with the **Refresh** button.
