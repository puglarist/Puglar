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
class Route:
    method: str
    path: str
    result: str


@dataclass
class Block:
    kind: str
    name: str
    fields: list[Field] = field(default_factory=list)
    routes: list[Route] = field(default_factory=list)


@dataclass
class Contract:
    module: str
    version: str
    blocks: list[Block]


def _sanitize_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if line.strip():
            lines.append(line)
    return lines


def parse_contract(text: str) -> Contract:
    lines = _sanitize_lines(text)
    if not lines:
        raise ValueError("Contract is empty")

    m = re.match(r"^module\s+([\w\.]+)\s+v([\d\.]+)$", lines[0].strip())
    if not m:
        raise ValueError("First non-empty line must be: module <Name> v<version>")
    module, version = m.group(1), m.group(2)

    blocks: list[Block] = []
    i = 1
    while i < len(lines):
        head = lines[i].strip()
        hm = re.match(r"^(type|entity|system|storage|api)\s+(\w+)\s*\{$", head)
        if not hm:
            raise ValueError(f"Invalid block header: {head}")
        kind, name = hm.group(1), hm.group(2)
        i += 1
        block = Block(kind=kind, name=name)

        while i < len(lines) and lines[i].strip() != "}":
            line = lines[i].strip()

            route_m = re.match(r"^route\s+(GET|POST|PUT|PATCH|DELETE)\s+(\S+)\s*->\s*(\w+)$", line)
            if route_m:
                block.routes.append(
                    Route(
                        method=route_m.group(1),
                        path=route_m.group(2),
                        result=route_m.group(3),
                    )
                )
                i += 1
                continue

            field_m = re.match(r"^(\w+)\s*:\s*(.+)$", line)
            if field_m:
                value = field_m.group(2).split("@", 1)[0].strip()
                block.fields.append(Field(name=field_m.group(1), type_name=value))

            i += 1

        if i >= len(lines) or lines[i].strip() != "}":
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
    for block in contract.blocks:
        if block.kind not in {"type", "entity"}:
            continue
        out.append(f"export interface {block.name} {{")
        for f in block.fields:
            out.append(f"  {f.name}: {ts_type(f.type_name)};")
        out.append("}\n")
    return "\n".join(out)


def emit_rust(contract: Contract) -> str:
    out = [f"// Generated from {contract.module} v{contract.version}"]
    for block in contract.blocks:
        if block.kind not in {"type", "entity"}:
            continue
        out.append("#[derive(Debug, Clone)]")
        out.append(f"pub struct {block.name} {{")
        for f in block.fields:
            out.append(f"    pub {f.name}: {rs_type(f.type_name)},")
        out.append("}\n")
    return "\n".join(out)


def emit_manifest(contract: Contract) -> dict:
    return {
        "module": contract.module,
        "version": contract.version,
        "blocks": [
            {
                "kind": block.kind,
                "name": block.name,
                "fields": [{"name": f.name, "type": f.type_name} for f in block.fields],
                "routes": [
                    {"method": r.method, "path": r.path, "result": r.result}
                    for r in block.routes
                ],
            }
            for block in contract.blocks
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=pathlib.Path)
    parser.add_argument("--out", type=pathlib.Path, default=pathlib.Path("build"))
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8")
    contract = parse_contract(text)

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "contract.manifest.json").write_text(
        json.dumps(emit_manifest(contract), indent=2),
        encoding="utf-8",
    )
    (args.out / "runtime.types.ts").write_text(
        emit_typescript(contract),
        encoding="utf-8",
    )
    (args.out / "runtime.types.rs").write_text(
        emit_rust(contract),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
