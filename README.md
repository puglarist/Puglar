# Puglar

This repository currently stores printable doctrine assets (PDFs and archives) for the Puglar training system.

## Iteration Log

Because this project is asset-first (rather than code-first), iterations are tracked by publication waves and versioned document outputs.

### Iteration 1 — Baseline Canon
- Added the first handbook and omnibus references.
- Established pocket/field card formats for print workflows.
- Output examples in repo: `Puglar_Handbook.pdf`, `Puglar_Omnibus_Final_v1.pdf`, `Puglar_Pocket_Drill_Cards.pdf`.

### Iteration 2 — Doctrine Consolidation
- Bundled material into archive packs for distribution.
- Expanded language support and handbook variants.
- Output examples in repo: `Puglar_Full_Doctrine_Archive_v2.zip`, `Puglar_Handbook_v2_Language_Guide.pdf`.

### Iteration 3 — Seasonal and Environment-Specific Drills
- Added winter/summer and weather-specific command card sets.
- Refined quick-reference micro cards for field use.
- Output examples in repo: `Puglar_Winter_Summer_Micro_Cards.pdf`, `Puglar_Command_Stances_Winter_Rain_Cards.pdf`, `Puglar_Seasonal_Drill_Cards.pdf`.

### Iteration 4 — Ranger and Awareness Expansion
- Added ranger awareness and attention protocols.
- Produced deeper training references and specialized card decks.
- Output examples in repo: `Puglar_Ranger_Awareness_Manual_v4.pdf`, `Puglar_AEN_Attention_Gorilla_Rest_v2_Cards.pdf`.

### Iteration 5 — Archive and Roadmap Maturity
- Published updated doctrine archive package.
- Added long-horizon development and progression cards.
- Output examples in repo: `Puglar_Full_Doctrine_Archive_v5.zip`, `Puglar_Iron_Cross_5_Year_Roadmap_Cards.pdf`.

## Current Priorities (Next Iteration)

1. **Normalize naming conventions**
   - Remove duplicate naming variants (for example, `Puglar_Pocket_Drill_Cards.pdf` vs `Puglar_Pocket_Drill_Cards 2.pdf`).
2. **Add source manifest**
   - Create a machine-readable index (CSV/JSON) for each asset with version, purpose, and print profile.
3. **Define release checklist**
   - Add quality gates for pagination, bleed margins, and print-safe typography.

## Contribution Notes

- When publishing a new document version, add it to the relevant iteration section.
- Prefer semantic suffixes (`vN`) and avoid ambiguous duplicate filenames.
- Keep release artifacts in the repository root unless a future `/releases` structure is introduced.
