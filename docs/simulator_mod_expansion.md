# Simulator Realism Expansion Pack (Design + Build Plan)

This document adds a practical implementation plan for a high-fidelity GTA-style simulator mod expansion focused on realism, garage systems, and modern supercar content.

## 1) Mod Menu Feature Set (Expanded)

### Driving + Physics
- **Realistic traction model toggle** (street / sport / race / wet)
- **Tire heat simulation** (cold grip penalty, overheating fade)
- **Brake fade + thermal windows**
- **Fuel mass simulation** (car gets lighter as fuel burns)
- **ABS / TC / ESC presets** (OEM, Track, Off)
- **Suspension tuning UI**: spring rate, damping, ride height, anti-roll bias

### Player Simulation Systems
- **Inertia camera and body roll reaction**
- **Driver fatigue mode** (reduced reaction under long sessions)
- **Damage persistence** (does not reset on spawn unless repaired)
- **Insurance + repair economy switch**

### World Realism
- **Traffic density by district + time**
- **Weather traction multiplier map**
- **Road surface classes** (asphalt, painted lines, cobble, gravel)
- **Night visibility and adaptive headlight intensity**

### Utility + Accessibility
- **Per-feature hotkey mapping**
- **Preset manager** (Arcade / Sim / Hardcore)
- **Live telemetry HUD** (tire temp, brake temp, aero load, fuel burn)

## 2) GTA 6-style Gameplay Logic (portable to a GTA 5 mod framework)

- **Contextual events system**: dynamic roadside incidents and police/EMS logic based on district risk scores
- **Adaptive pursuit behavior**: AI response scales by crime severity, witness count, and player heat
- **Economy loop**: legal racing contracts, garage upgrades, and salvage market
- **Faction trust meter**: unlocks races, tuning vendors, and rare part access
- **Character state variables**: stress, focus, and notoriety affecting mission outcomes

## 3) Garage Logic + Graphics

### Garage Core Systems
- Slot-based storage with visual occupancy
- Upgrade tree per vehicle:
  - Engine internals
  - Forced induction
  - Aero package
  - Chassis reinforcement
  - Brake kit
  - Drivetrain tuning
- **Persistent setup sheets**:
  - Track setup
  - Street setup
  - Rain setup
- **Wear model**:
  - Oil life
  - Tire compound wear
  - Brake pad wear
  - Engine health

### Garage Visual Targets
- PBR material workflow for:
  - Car paint (clear coat + flake)
  - Carbon fiber anisotropy
  - Brushed metal and forged wheel finishes
- Reflection probes and baked AO in indoor garage volumes
- Toolbench and lift interaction points for upgrade previews

## 4) Supercar Asset Build Plan (today's models)

> Legal note: only use assets with licenses that permit redistribution/modification. Avoid ripping proprietary assets from commercial titles.

### Target vehicles (initial pack)
1. Ferrari SF90 Stradale (inspired naming for legal-safe in-game variant)
2. Lamborghini Revuelto
3. McLaren 750S
4. Porsche 911 GT3 RS (992)
5. Mercedes-AMG ONE
6. Aston Martin Valkyrie
7. Rimac Nevera
8. Koenigsegg Jesko

### LOD + texture budget recommendation
- **LOD0**: 120k–180k tris
- **LOD1**: 60k–90k tris
- **LOD2**: 20k–35k tris
- **LOD3**: 5k–10k tris
- **Texture sets**: 2k/4k PBR (basecolor, normal, ORM, clearcoat/flake mask)

### Required deliverables per car
- Drivable body mesh
- Separated wheel meshes
- Calipers/discs for animated braking
- Interior dashboard + steering wheel
- Damage-ready detachable parts (doors, hood, bumper)
- Collision proxies + shadow mesh

## 5) Free Modded GTA 5 Asset Integration Strategy

- Build an **asset manifest** with license + origin URL + attribution
- Normalize naming conventions and skeleton references
- Convert materials into unified PBR shader slots
- Enforce scale validation (meter-based), wheelbase checks, and suspension points
- Add automated validation for missing textures and broken normals

See: `mods/supercar_asset_manifest.json` for starter metadata schema.

## 6) Implementation Milestones

### Milestone A — Foundation
- Add feature flags and runtime config loader
- Add telemetry overlay
- Add garage data model and persistence

### Milestone B — Realism Systems
- Integrate tire + brake thermal simulation
- Add weather/surface grip modifiers
- Add persistent damage and economy loop

### Milestone C — Content
- Import first 3 supercars with full LOD chain
- Build garage scenes and reflection setup
- Validate performance and memory budgets

### Milestone D — Polish
- Preset UX and balancing pass
- AI pursuit tuning
- Bugfix + optimization + license audit
