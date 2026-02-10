# 3GS Engine Blueprint

## Goal
Build a **faster-than-prisma** project description layer and a **faster-than-Unity/Unreal** execution model by using a compact 3GS architecture:

- **G1: Graph** (systems + entities + data contracts)
- **G2: Generate** (codegen to runtime targets)
- **G3: Ship** (hot-reload, deployment, and telemetry loop)

The key bet: a strict, low-capacity DSL that is easier to optimize than general-purpose schema tools and heavy editors.

---

## 1) A lightweight alternative to `schema.prisma`

### 1.1 Why Prisma-style schemas become bottlenecks
Traditional schema-first systems are excellent for DB modeling but often weak for full game/runtime workflows:

- They focus on persistence first, not runtime simulation contracts.
- They generate data-access code, but not full subsystem scaffolding.
- They are too database-centric for ECS + networking + AI loops.

### 1.2 3GS Contract DSL (`*.3gs`)
Instead of a DB-centric schema, define **runtime-first contracts** that can still map to DB, APIs, and engine data.

```3gs
module World.Core v0.1

type Vec3 {
  x: f32
  y: f32
  z: f32
}

entity Player {
  id: uid @primary
  name: string @index
  level: u16 @default(1)
  position: Vec3 @replicate(freq=20)
  stamina: f32 @clamp(0, 100)
  inventory: list<ItemRef> @max(64)
}

system Movement {
  reads: Player.position, Input.axis
  writes: Player.position, Player.stamina
  tick: fixed(60)
}

storage PlayerStore {
  backend: postgres
  partition: region
  cache: redis(ttl=30s)
}

api PlayerAPI {
  route GET /players/:id -> Player
  route POST /players -> Player
}
```

### 1.3 What this generates automatically
From one `*.3gs` file, generate:

1. Runtime component structs/classes (C++/Rust/C#).
2. Deterministic serializer (binary + JSON).
3. DB schema + migrations.
4. Query/repository code.
5. API handlers + OpenAPI spec.
6. Network replication packets.
7. Editor metadata panel descriptors.
8. Test harness stubs.

### 1.4 “Low capacity bearing” design rules (for speed)
To keep compile/codegen very fast, constrain the DSL intentionally:

- No arbitrary user logic inside schema files.
- Declarative annotations only.
- No recursive dynamic types by default.
- Deterministic ordering for all generated outputs.
- Incremental build graph keyed by per-block hashes.

This is how you “push out more code quicker”: reduce language flexibility to maximize predictable generation.

---

## 2) 3GS compiler pipeline

## 2.1 Pipeline stages
1. **Parse**: `*.3gs` -> AST.
2. **Normalize**: resolve references/types, freeze defaults.
3. **Validate**: safety constraints, netcode constraints, storage constraints.
4. **Lower** to IR: runtime IR + persistence IR + API IR.
5. **Generate** target templates.
6. **Cache** artifacts and only rebuild changed sections.

## 2.2 Performance targets
- Cold compile (100 entities): < 1.5s.
- Hot compile (single entity edit): < 150ms.
- Codegen throughput: > 10k LOC/sec on modern laptop.
- Deterministic output hash for reproducible builds.

## 2.3 Runtime targets
- Native C++ module for high-performance builds.
- Rust server target for authoritative multiplayer.
- C# tooling target for editor and gameplay scripting wrappers.

---

## 3) Beating Unity/Unreal: realistic strategy

You do not beat Unity/Unreal by feature count first; you beat them by **narrowing scope and crushing workflow latency**.

## 3.1 Wedge strategy (first market)
Target one painful niche first:

- Multiplayer sandbox / survival games with high server-authoritative logic.
- Teams that hate long editor iteration loops.
- Teams needing deterministic replay + anti-cheat foundations.

## 3.2 Value proposition
- 10x faster compile/reload loop for data + systems changes.
- Built-in authoritative netcode contracts from day one.
- One source (`*.3gs`) generates server/client/tooling contracts.

## 3.3 Product pillars
1. **Instant iteration**: sub-second hot reload for systems/data.
2. **Deterministic simulation**: rollback/replay baked in.
3. **Cloud-native multiplayer**: autoscaled server runtime.
4. **AI-native tooling**: local + Hugging Face-assisted generation.

## 3.4 24-month roadmap

### Phase 0 (0-3 months) — Core Compiler
- Ship parser + validator + IR.
- Generate Rust server models + Postgres migrations.
- Build CLI: `3gs build`, `3gs doctor`, `3gs watch`.

### Phase 1 (3-6 months) — Vertical Slice
- Minimal scene runtime with ECS.
- Network replication generator.
- Basic editor inspector from metadata.

### Phase 2 (6-12 months) — Team Adoption
- Deterministic replay system.
- Crash-safe autosave + snapshotting.
- Integrate profiling timeline.

### Phase 3 (12-24 months) — Platform Play
- Plugin SDK.
- Visual graph editor powered by DSL underneath.
- Managed cloud hosting + telemetry product.

---

## 4) Hugging Face integration plan

Use Hugging Face where it accelerates authoring, testing, and content ops—not frame-by-frame gameplay.

## 4.1 High-leverage uses
1. **Schema/contract drafting assistant**
   - Prompt: describe feature -> model suggests `*.3gs` blocks.
2. **Code review assistant for generated diffs**
   - Summarize risk in migrations/netcode changes.
3. **Quest/dialog/content generation**
   - Generate structured content JSON validated by 3GS constraints.
4. **Automated test case expansion**
   - Generate edge-case scenarios for systems contracts.

## 4.2 Suggested model classes
- Small instruct model for local fast completions.
- Strong larger model for CI review gates.
- Embedding model for docs/spec semantic search.

## 4.3 Safety and quality rails
- Force model outputs through DSL parser.
- Reject non-compiling proposals.
- Add policy checks for security/network exploit vectors.
- Keep humans in review for migrations that drop/reshape data.

---

## 5) Technical architecture (3GS stack)

- **3gs-cli**: parse/build/watch/doctor.
- **3gs-compiler**: AST -> IR -> generators.
- **3gs-runtime**: ECS + scheduler + replication layer.
- **3gs-storage**: migration and repository adapters.
- **3gs-editor**: metadata-driven panels/graph.
- **3gs-cloud**: orchestration, observability, replay archive.

---

## 6) Practical first deliverables

Week 1 deliverables:
- `world.3gs` sample contracts.
- Rust code generator for structs + serde.
- SQL migration generator.
- Golden tests for deterministic output.

Week 2-4 deliverables:
- Netcode packet generator.
- API generator (OpenAPI + handlers).
- Minimal watch mode with incremental rebuild.

Month 2 deliverables:
- Live reload demo with 1000 entities.
- Deterministic replay file format.
- Hugging Face-powered schema assistant command.

---

## 7) Success metrics

- Time from data change -> running runtime update.
- Number of files generated per single contract edit.
- Multiplayer desync rate under load.
- Time to onboard a new engineer.
- % of generated code requiring manual edits (target: near zero).

If 3GS wins, teams feel like they are editing intent, not wiring.
