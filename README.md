# Puglar

## 3GS Proposal

This repository includes a draft 3GS contract format and now ships with a working low-overhead builder that parses `.3gs` contracts and generates runtime stubs.

- Blueprint: `docs/3gs_engine_blueprint.md`
- Sample contract file: `docs/world_core.3gs`
- Builder: `tools/threegs_build.py`

## Build commands

```bash
make build-all
make test
```

`make build-all` compiles `docs/world_core.3gs` into:
- `build/world_core/contract.manifest.json`
- `build/world_core/runtime.types.ts`
- `build/world_core/runtime.types.rs`
