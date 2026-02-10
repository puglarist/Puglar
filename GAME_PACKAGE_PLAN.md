# Rust Game Expansion Plan: 20 New Packages

This plan introduces 20 modular Rust crates inspired by proven gameplay loops from major PC games and mod communities. Each package is structured for integration into a larger ECS/game-engine pipeline and includes a graphics enhancement target.

## Package Roadmap

| # | Package | Logic Inspiration (PC games/mods) | Rust Feature Scope | Graphics Enhancement Scope |
|---|---|---|---|---|
| 1 | `ai-director-core` | Left 4 Dead AI Director, Vermintide pacing mods | Event-driven threat scheduler, spawn budget model, tension curves | Dynamic fog density, color grading per threat phase |
| 2 | `ballistics-overhaul` | Arma ballistic mods, STALKER weapon packs | Projectile penetration tables, drag simulation, ricochet model | Tracer rendering, impact decal layering, heat shimmer |
| 3 | `colony-needs-sim` | RimWorld need systems, Dwarf Fortress sims | Need decay components, utility-AI behavior scoring | Mood-state post-processing tint and UI pulse cues |
| 4 | `dynamic-quest-graph` | Witcher 3 quest branching, Skyrim quest mods | Graph-based quest states, conditional transitions, rollback checkpoints | Cinematic transition overlays and branching node map UI |
| 5 | `encounter-procgen` | Diablo rift generation, PoE map mods | Seeded encounter templates, weighted mutation engine | Region-specific atmospheric particles and lighting LUTs |
| 6 | `faction-reputation` | Mount & Blade diplomacy, Fallout faction mods | Reputation matrices, consequence propagation, decay/recovery | Banner/icon material swaps and settlement ambience color shifts |
| 7 | `forging-crafting-plus` | Minecraft tech mods, Monster Hunter forge trees | Recipe DAG validation, quality tiers, deterministic stat synthesis | Crafting VFX pipeline with sparks, bloom, and glow trails |
| 8 | `graphics-postfx-stack` | ENB/ReShade pipelines, cinematic reshade presets | Renderer-agnostic postfx graph, pass ordering and profiling | SSAO, film grain, chromatic aberration, adaptive exposure |
| 9 | `havok-style-ragdoll-bridge` | GTA/Euphoria-inspired ragdoll mods | Skeletal impulse blending, animation-to-ragdoll transitions | Motion blur weighting by limb velocity |
| 10 | `inventory-tetris-system` | Resident Evil inventory grids, Tarkov stash mods | 2D bin packing, rotation rules, quick-merge ops | Item rarity outlines, hover shaders, contextual lighting |
| 11 | `loot-affix-roller` | Diablo affix systems, Grim Dawn loot mods | Deterministic RNG seed chains, tier constraints, affix tags | Rarity beams, emissive pulse, stat tooltip micro-animations |
| 12 | `mod-hotload-runtime` | Skyrim Script Extender ecosystem, Factorio mods | Dynamic library reload boundary, ABI-safe plugin interfaces | Live shader/hud hot reload preview channel |
| 13 | `network-prediction-rs` | Source engine lag compensation, fighting game rollback | Snapshot buffers, client prediction, reconciliation hooks | Interpolation debug overlays and ghosted correction trails |
| 14 | `open-world-streamer` | GTA streaming, Unreal World Partition concepts | Cell streaming scheduler, async asset priority queues | Distance-based mesh LOD blend and terrain morph smoothing |
| 15 | `parkour-movement-kit` | Mirror's Edge traversal, Dying Light movement mods | State machine for vault/wall-run/slide, stamina integration | Camera inertia curves, speed-line VFX, landing impact shake |
| 16 | `physics-destruction-lite` | Red Faction GeoMod concepts, teardown-style mods | Breakable chunk graph, impulse thresholds, debris lifecycle | Debris dust, contact sparks, dynamic shadow updates |
| 17 | `quest-cinematics-rs` | Mass Effect dialogue scenes, cinematic camera mods | Timeline sequencer, camera tracks, animation cue dispatch | Depth-of-field ramps, letterbox transitions, focal pull effects |
| 18 | `rust-combat-primitives` | Soulslike combat mods, Mordhau melee systems | Hitbox/hurtbox framework, stamina windows, interrupt priorities | Weapon trail ribbons and directional hit flash |
| 19 | `shader-material-pipeline` | Unreal material editor workflows, modded PBR packs | Material graph compiler, shader permutation cache | PBR upgrades, SSR tuning, anisotropic highlights |
| 20 | `survival-weather-sim` | The Long Dark weather model, dayz survival mods | Temperature/wetness simulation, storm events, shelter checks | Volumetric rain/snow, wet surface reflections, cloud shadowing |

## Build Status

A Rust workspace scaffold has been created with all 20 packages under `packages/`, each exposing a minimal `package_id()` function. This gives a buildable baseline to incrementally implement gameplay logic and graphics systems.

## Suggested Milestones

1. **Foundation sprint (Week 1–2):** Complete APIs for simulation-oriented crates (`ai-director-core`, `survival-weather-sim`, `faction-reputation`, `colony-needs-sim`).
2. **Combat + progression sprint (Week 3–4):** Implement `rust-combat-primitives`, `ballistics-overhaul`, `loot-affix-roller`, `inventory-tetris-system`.
3. **Graphics sprint (Week 5–6):** Integrate `graphics-postfx-stack`, `shader-material-pipeline`, and VFX hooks for combat/crafting packages.
4. **Runtime/modding sprint (Week 7):** Deliver `mod-hotload-runtime` and compatibility tests.
5. **World integration sprint (Week 8):** Connect streaming, quests, and cinematics packages for vertical-slice gameplay.
