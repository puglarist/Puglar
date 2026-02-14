# Puglar Doctrine Archive

This repository stores printable Puglar doctrine material (PDFs) and bundled archives.

## Quick Inventory

### Core handbooks and manuals
- `Puglar_Handbook.pdf`
- `Puglar_Handbook_v2_Language_Guide.pdf`
- `Puglar_Omnibus_Final_v1.pdf`
- `Puglar_Ranger_Awareness_Manual_v4.pdf`
- `Puglar_TreeWebs_Handbook_v2_Climb_and_Shade.pdf`
- `Puglar_Sacred_Core_Scroll.pdf`

### Cards and field references
- `Puglar_AEN_Attention_Gorilla_Rest_v2_Cards.pdf`
- `Puglar_Command_Stances_Winter_Rain_Cards.pdf`
- `Puglar_Iron_Cross_5_Year_Roadmap_Cards.pdf`
- `Puglar_Micro_Command_Cards_Wallet.pdf`
- `Puglar_Physical_Doctrine_Workouts.pdf`
- `Puglar_Pocket_Drill_Cards.pdf`
- `Puglar_Seasonal_Drill_Cards.pdf`
- `Puglar_Waterproof_Field_Cards.pdf`
- `Puglar_Winter_Summer_Micro_Cards.pdf`
- `Puglar_Youth_Training_Cards.pdf`

### Technical / print support
- `Puglar_Iron_Cross_Illustrated_Angle_Plates.pdf`
- `Puglar_Lamination_Cut_Guides.pdf`

### Bundled archives
- `Puglar_Full_Doctrine_Archive_v2.zip`
- `Puglar_Full_Doctrine_Archive_v5.zip`

## Repository housekeeping

- Duplicate file copies should not be kept when they are byte-identical.
- If a replacement file is needed, prefer versioned naming (for example `_v2`, `_v3`) instead of copy-style suffixes.

### Duplicate check example

```bash
md5sum "Puglar_Pocket_Drill_Cards.pdf" "Puglar_Pocket_Drill_Cards 2.pdf"
```

If checksums match, keep one canonical file and remove the duplicate copy.
