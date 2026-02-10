# Puglar Assets

This folder contains reusable source assets for graphics, maps, and 3D content.

## Graphics

- `graphics/puglar-logo-mark.svg` — icon/crest style mark.
- `graphics/puglar-logo-lockup.svg` — full logo with wordmark.
- `graphics/puglar-badge.svg` — circular badge for covers/stickers.
- `graphics/puglar-field-pattern.svg` — subtle background pattern.

## 3D

- `3d/puglar-training-ground.obj` + `.mtl` — low-poly training ground blockout.
- `3d/puglar-scout-drone.gltf` — lightweight glTF scout drone mesh.

## Maps

- `maps/puglar-region-map.svg` — stylized region map illustration.
- `maps/puglar-zones.geojson` — zone polygons and metadata.

## Usage guidance

- Prefer SVG for print and scalable UI surfaces.
- Use GeoJSON as the source of truth for gameplay/mission zones.
- Keep 3D assets in open interchange formats (OBJ, glTF) for tool compatibility.
