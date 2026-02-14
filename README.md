# Puglar

A document repository for Puglar doctrine, drills, field cards, and print-ready training assets.

## What this repository is

This repo is an **asset library** (PDF + ZIP artifacts), not an application codebase.

- Use individual PDFs for focused printing and field use.
- Use ZIP archives for full offline distribution snapshots.
- Use `ASSET_MANIFEST.md` for deterministic file verification (size + SHA-256).

## Asset index

### Doctrine and handbooks
- `Puglar_Handbook.pdf`
- `Puglar_Handbook_v2_Language_Guide.pdf`
- `Puglar_Omnibus_Final_v1.pdf`
- `Puglar_Sacred_Core_Scroll.pdf`
- `Puglar_Ranger_Awareness_Manual_v4.pdf`
- `Puglar_TreeWebs_Handbook_v2_Climb_and_Shade.pdf`

### Cards, drills, and workouts
- `Puglar_Pocket_Drill_Cards.pdf`
- `Puglar_Pocket_Drill_Cards 2.pdf`
- `Puglar_Seasonal_Drill_Cards.pdf`
- `Puglar_Micro_Command_Cards_Wallet.pdf`
- `Puglar_Command_Stances_Winter_Rain_Cards.pdf`
- `Puglar_AEN_Attention_Gorilla_Rest_v2_Cards.pdf`
- `Puglar_Winter_Summer_Micro_Cards.pdf`
- `Puglar_Youth_Training_Cards.pdf`
- `Puglar_Waterproof_Field_Cards.pdf`
- `Puglar_Physical_Doctrine_Workouts.pdf`

### Planning and production aids
- `Puglar_Iron_Cross_5_Year_Roadmap_Cards.pdf`
- `Puglar_Iron_Cross_Illustrated_Angle_Plates.pdf`
- `Puglar_Lamination_Cut_Guides.pdf`

### Full archives
- `Puglar_Full_Doctrine_Archive_v2.zip`
- `Puglar_Full_Doctrine_Archive_v5.zip`

## Quick start

```bash
git clone <repo-url>
cd Puglar
```

Open any PDF with your local viewer, or extract a full archive:

```bash
unzip Puglar_Full_Doctrine_Archive_v5.zip -d ./puglar_archive_v5
```

## Integrity verification

Checksums and file sizes are tracked in [`ASSET_MANIFEST.md`](./ASSET_MANIFEST.md).

To manually verify one file hash:

```bash
sha256sum "Puglar_Handbook.pdf"
# Compare output to the matching row in ASSET_MANIFEST.md
```

## Contribution and maintenance

When adding or replacing assets:

1. Use descriptive, versioned filenames (example: `Title_v3.pdf`).
2. Regenerate `ASSET_MANIFEST.md` so hashes/sizes stay accurate.
3. Update this README index if categories or asset names change.

## License

No license file is currently present. Add `LICENSE` if distribution terms should be explicit.
