# Puglar

## TCG Pokémon-Inspired Crypto Tournament Emulator

This repository now includes a browser-based prototype that combines:

- **TCG battle emulation** (deck power and round-by-round eliminations)
- **Mock crypto prize pool logic** (entry fee, rake, payout splits)
- **Live graphics** drawn on `<canvas>`
- **Custom card building** that feeds into future deck generation

### Run locally

Because this is a static app, any file server works:

```bash
python3 -m http.server 4173
```

Then open `http://localhost:4173`.

### Files

- `index.html` — UI layout and controls
- `styles.css` — visual styling
- `tcg.js` — tournament logic, battle simulation, and canvas rendering

### Notes

- This is an educational mockup. It does **not** execute blockchain transactions.
- The game is Pokémon-inspired but uses custom entities and mechanics.
