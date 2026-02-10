# WendyVerse Engine Blueprint (Three.js + VR + World/Server Builder)

This document turns the idea into a buildable plan: a modular web-first metaverse stack that combines:

- **Three.js + WebXR** for cross-platform VR rendering
- **Competitive shooter modules** (MW2 promod-inspired rulesets)
- **Sandbox crafting modules** (Minecraft/Fortnite/Warzone-style loops)
- **World Builder + Server Builder** tooling
- **Mod Menu SDK** with permission and anti-cheat boundaries

---

## 1) Core Product Direction

### Vision
Build a **creator-first metaverse engine** where a creator can:

1. Build a world visually
2. Attach gameplay modules (arena shooter, survival crafting, BR)
3. Publish server profiles with scaling + moderation rules
4. Enable curated mods through signed packages

### Primary Experience Loops

- **Builder Loop**: edit terrain, place assets, script interactions, test in VR.
- **Server Loop**: deploy rulesets, tune tickrate/netcode profile, moderate.
- **Player Loop**: join worlds, progress via session profile, craft/fight/compete.

---

## 2) Better-Than-"Prisma-only" Data Layer

Instead of relying on a single ORM schema as the center of truth, use a **polyglot, contract-first architecture**:

## Data strategy

- **Postgres + Prisma** for account, economy, inventory, social graph metadata.
- **Event store** (Kafka/Redpanda or Postgres event table) for gameplay events.
- **Redis** for fast match/session state.
- **Object storage** for world snapshots, user-generated maps, mod bundles.
- **JSON Schema / Zod contracts** versioned in repo for all game payloads.

### Why this is better

- Server-authoritative systems need event history + replay, not only row CRUD.
- Mods and clients need stable versioned contracts independent of DB internals.
- Live games need low-latency hot data (Redis) and durable analytics streams.

---

## 3) Service Topology

### Runtime services

- `gateway-api`: auth, account, profile, social endpoints
- `world-service`: world publishing/versioning/snapshots
- `match-service`: lobbies, queues, matchmaking
- `simulation-service`: authoritative combat/physics/session loop
- `mod-service`: package registry, signature verification, policy checks
- `builder-service`: collaborative editing sessions + autosave
- `analytics-service`: ingest + dashboards + anti-cheat indicators

### Shared packages

- `@wendy/contracts`: schemas + generated types
- `@wendy/netcode`: snapshots, delta compression, lag compensation helpers
- `@wendy/mod-sdk`: sandbox APIs for trusted mods
- `@wendy/world-kit`: terrain chunks, biomes, props, prefabs

---

## 4) Gameplay Architecture

### ECS-centric simulation

Use **Entity Component System** to blend multiple genres in one runtime:

- Combat components: `Weapon`, `Recoil`, `Hitbox`, `ArmorPlate`
- Building components: `BuildPiece`, `EditState`, `MaterialCost`
- Survival components: `ResourceNode`, `CraftQueue`, `ToolDurability`

### Authoritative multiplayer

- Fixed tick simulation (`30-60 Hz`) server-side
- Client prediction + server reconciliation
- Lag compensation for hitscan weapons
- Deterministic subset for competitive playlists

### Mode system

- `PromodArenaMode`: stripped loadouts, recoil skill ceiling, objective focus
- `BattleRoyaleMode`: shrinking zone, contracts, loot rarity tables
- `CreativeSurvivalMode`: harvest, craft, build, defend

Modes are data-driven and can be composed per world.

---

## 5) World Builder + Server Builder

### World Builder features

- Node-based logic graph (triggers, timers, score, AI spawners)
- Terrain sculpt + voxel patches + prefab placement
- Lighting/weather/time-of-day profiles
- VR editing mode (grab, place, scale, annotate)

### Server Builder features

- Preset templates: `Arena`, `BR`, `Creative`, `Hybrid`
- Tickrate/profile selector: low-cost vs competitive
- Region + autoscaling profile
- Moderation panel: whitelist/ban/mute/report workflow
- Rule DSL example:

```yaml
ruleset: promod_hardcore
friendly_fire: false
respawn:
  mode: wave
  interval_sec: 15
weapons:
  allowed: ["m4", "ak47", "mp5"]
  one_shot_snipers: false
build_mode:
  enabled: true
  max_structures_per_team: 250
```

---

## 6) Mod Menu / Modding Framework (Safe by design)

### Mod package model

- Mods are signed bundles (`.wmod`)
- Declared capabilities in manifest (`ui.overlay`, `gameplay.rules`, `cosmetics`)
- Runtime sandbox with API allowlist and CPU/memory quotas

### Permission model

- Server owner approves capabilities
- Client sees capability prompts before enabling optional overlays
- Anti-cheat blocks forbidden categories (aim-assist, wallhacks, memory hooks)

### Mod SDK surfaces

- UI overlays (HUD widgets, minimap skins, callouts)
- Match event listeners (killfeed transforms, announcer packs)
- Custom game rules bounded by server authority

---

## 7) Anti-Cheat + Trust

- Server-authoritative combat + movement validation
- Replay-based cheat detection (impossible aim deltas, velocity spikes)
- Signed clients for ranked playlists
- Trust score per account/server/mod package

---

## 8) Build Roadmap

### Phase 0 (2-4 weeks): Foundation

- Contracts package + schema versioning
- Basic Three.js/WebXR scene with networked avatar sync
- Postgres/Redis baseline and auth pipeline

### Phase 1 (4-8 weeks): Core Multiplayer

- Matchmaking + lobby + session allocation
- Authoritative shooter loop (movement, weapons, damage)
- Simple world publish/join flow

### Phase 2 (6-10 weeks): Creator Tooling

- World Builder MVP with prefab placement + scripting graph
- Server Builder presets + moderation tools
- Snapshotting + rollback support

### Phase 3 (6-12 weeks): Mod Ecosystem

- Mod registry + signing pipeline
- Safe mod APIs + capability prompts
- Creator economy hooks (optional revenue share)

---

## 9) MVP Definition

A valid MVP should let one creator:

1. Build a small arena world
2. Publish a server with promod-like tuning
3. Enable one approved HUD mod
4. Host 16 players with stable netcode and anti-cheat telemetry

---

## 10) Suggested Repo Layout

```text
/apps
  /client-webxr
  /world-builder
  /server-builder
  /gateway-api
  /simulation-service
  /mod-service
/packages
  /contracts
  /netcode
  /mod-sdk
  /world-kit
/docs
  METAVERSE_ENGINE_BLUEPRINT.md
  schemas/
```
