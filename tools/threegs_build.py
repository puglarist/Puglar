#!/usr/bin/env python3
"""Tiny 3GS builder: parses a .3gs contract and emits runtime stubs quickly."""
from __future__ import annotations
import argparse
import json
import pathlib
import re
from dataclasses import dataclass, field

PRIMITIVES = {
    "uid": {"ts": "string", "rs": "String"},
    "string": {"ts": "string", "rs": "String"},
    "f32": {"ts": "number", "rs": "f32"},
    "u16": {"ts": "number", "rs": "u16"},
}


@dataclass
class Field:
    name: str
    type_name: str


@dataclass
class Block:
    kind: str
    name: str
    fields: list[Field] = field(default_factory=list)


@dataclass
class Contract:
    module: str
    version: str
    blocks: list[Block]


def parse_contract(text: str) -> Contract:
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
    m = re.match(r"^module\s+([\w\.]+)\s+v([\d\.]+)$", lines[0])
    if not m:
        raise ValueError("First non-empty line must be: module <Name> v<version>")
    module, version = m.group(1), m.group(2)

    blocks: list[Block] = []
    i = 1
    while i < len(lines):
        head = lines[i]
        hm = re.match(r"^(type|entity|system|storage|api)\s+(\w+)\s*\{$", head)
        if not hm:
            raise ValueError(f"Invalid block header: {head}")
        kind, name = hm.group(1), hm.group(2)
        i += 1
        block = Block(kind=kind, name=name)
        while i < len(lines) and lines[i] != "}":
            line = lines[i].strip()
            # parse only field-style declarations (<name>: <type>)
            fm = re.match(r"^(\w+)\s*:\s*([^\s@]+)", line)
            if fm:
                block.fields.append(Field(name=fm.group(1), type_name=fm.group(2)))
            i += 1
        if i >= len(lines) or lines[i] != "}":
            raise ValueError(f"Unclosed block: {kind} {name}")
        blocks.append(block)
        i += 1

    return Contract(module=module, version=version, blocks=blocks)


def ts_type(type_name: str) -> str:
    list_m = re.match(r"^list<(\w+)>$", type_name)
    if list_m:
        return f"{list_m.group(1)}[]"
    return PRIMITIVES.get(type_name, {}).get("ts", type_name)


def rs_type(type_name: str) -> str:
    list_m = re.match(r"^list<(\w+)>$", type_name)
    if list_m:
        inner = PRIMITIVES.get(list_m.group(1), {}).get("rs", list_m.group(1))
        return f"Vec<{inner}>"
    return PRIMITIVES.get(type_name, {}).get("rs", type_name)


def emit_typescript(contract: Contract) -> str:
    out = [f"// Generated from {contract.module} v{contract.version}"]
    for b in contract.blocks:
        if b.kind not in {"type", "entity"}:
            continue
        out.append(f"export interface {b.name} {{")
        for f in b.fields:
            out.append(f"  {f.name}: {ts_type(f.type_name)};")
        out.append("}\n")
    return "\n".join(out)


def emit_rust(contract: Contract) -> str:
    out = [f"// Generated from {contract.module} v{contract.version}"]
    for b in contract.blocks:
        if b.kind not in {"type", "entity"}:
            continue
        out.append("#[derive(Debug, Clone)]")
        out.append(f"pub struct {b.name} {{")
        for f in b.fields:
            out.append(f"    pub {f.name}: {rs_type(f.type_name)},")
        out.append("}\n")
    return "\n".join(out)


def emit_manifest(contract: Contract) -> dict:
    return {
        "module": contract.module,
        "version": contract.version,
        "blocks": [
            {
                "kind": b.kind,
                "name": b.name,
                "fields": [{"name": f.name, "type": f.type_name} for f in b.fields],
            }
            for b in contract.blocks
        ],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=pathlib.Path)
    ap.add_argument("--out", type=pathlib.Path, default=pathlib.Path("build"))
    args = ap.parse_args()

    text = args.input.read_text(encoding="utf-8")
    contract = parse_contract(text)

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "contract.manifest.json").write_text(
        json.dumps(emit_manifest(contract), indent=2), encoding="utf-8"
    )
    (args.out / "runtime.types.ts").write_text(emit_typescript(contract), encoding="utf-8")
    (args.out / "runtime.types.rs").write_text(emit_rust(contract), encoding="utf-8")


if __name__ == "__main__":
    main()
