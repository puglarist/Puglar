#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import re
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from zipfile import ZipFile

SIM_LOGIC_KEYWORDS = {"logic", "drill", "sequence", "timing", "command", "state", "awareness", "simulation", "training", "cycle", "routine", "phase", "decision"}
GRAPHICS_KEYWORDS = {"graphics", "visual", "render", "lighting", "angle", "illustrated", "diagram", "map", "cards", "ink", "color", "frame", "cross", "formation"}


@dataclass
class Snippet:
    source: str
    category: str
    text: str


def _decode_pdf_literal(text: str) -> str:
    text = text.replace(r"\(", "(").replace(r"\)", ")").replace(r"\\", "\\")

    def repl(match: re.Match[str]) -> str:
        return chr(int(match.group(1), 8))

    return re.sub(r"\\([0-7]{1,3})", repl, text)


def _extract_text_from_stream(stream: bytes) -> list[str]:
    out: list[str] = []
    for raw in re.findall(rb"\((?:[^\\)]|\\.)*\)\s*Tj", stream):
        literal = raw.rsplit(b")", 1)[0][1:]
        out.append(_decode_pdf_literal(literal.decode("latin-1", "ignore")))

    for array_blob in re.findall(rb"\[(.*?)\]\s*TJ", stream, flags=re.S):
        parts = re.findall(rb"\((?:[^\\)]|\\.)*\)", array_blob)
        if parts:
            out.append("".join(_decode_pdf_literal(p[1:-1].decode("latin-1", "ignore")) for p in parts))

    return [line.strip() for line in out if line.strip()]


def _decode_pdf_stream(data: bytes, filters: list[str]) -> bytes:
    buf = data
    for flt in filters:
        if flt == "FlateDecode":
            buf = zlib.decompress(buf)
        elif flt == "ASCII85Decode":
            cleaned = buf.strip()
            if not cleaned.endswith(b"~>"):
                cleaned += b"~>"
            buf = base64.a85decode(cleaned, adobe=True)
        else:
            return data
    return buf


def extract_pdf_text(pdf_bytes: bytes) -> list[str]:
    lines: list[str] = []
    cursor = 0

    while True:
        stream_pos = pdf_bytes.find(b"stream", cursor)
        if stream_pos == -1:
            break

        dict_end = pdf_bytes.rfind(b">>", 0, stream_pos)
        dict_start = pdf_bytes.rfind(b"<<", 0, dict_end)
        if dict_start == -1 or dict_end == -1:
            cursor = stream_pos + 6
            continue

        dict_blob = pdf_bytes[dict_start + 2 : dict_end]
        data_start = stream_pos + len(b"stream")
        if pdf_bytes[data_start : data_start + 2] == b"\r\n":
            data_start += 2
        elif pdf_bytes[data_start : data_start + 1] in (b"\n", b"\r"):
            data_start += 1

        end_pos = pdf_bytes.find(b"endstream", data_start)
        if end_pos == -1:
            break

        stream_blob = pdf_bytes[data_start:end_pos].rstrip(b"\r\n")

        filters: list[str] = []
        m_arr = re.search(rb"/Filter\s*\[(.*?)\]", dict_blob, re.S)
        if m_arr:
            filters = [x.decode("ascii", "ignore") for x in re.findall(rb"/([A-Za-z0-9]+)", m_arr.group(1))]
        else:
            m_one = re.search(rb"/Filter\s*/([A-Za-z0-9]+)", dict_blob)
            if m_one:
                filters = [m_one.group(1).decode("ascii", "ignore")]

        decoded = _decode_pdf_stream(stream_blob, filters)
        lines.extend(_extract_text_from_stream(decoded))
        cursor = end_pos + len(b"endstream")

    return lines


def categorize_line(line: str) -> list[str]:
    lower = line.lower()
    tags = []
    if any(k in lower for k in SIM_LOGIC_KEYWORDS):
        tags.append("simulator_logic")
    if any(k in lower for k in GRAPHICS_KEYWORDS):
        tags.append("graphics")
    return tags


def iter_pdf_sources(root: Path) -> Iterable[tuple[str, bytes]]:
    for pdf in sorted(root.glob("*.pdf")):
        yield pdf.name, pdf.read_bytes()
    for zf in sorted(root.glob("*.zip")):
        with ZipFile(zf) as archive:
            for name in archive.namelist():
                if name.lower().endswith(".pdf"):
                    yield f"{zf.name}:{name}", archive.read(name)


def scrape(root: Path) -> dict:
    snippets: list[Snippet] = []
    source_stats: dict[str, int] = {}
    for source, pdf_bytes in iter_pdf_sources(root):
        lines = extract_pdf_text(pdf_bytes)
        source_stats[source] = len(lines)
        for line in lines:
            for tag in categorize_line(line):
                snippets.append(Snippet(source=source, category=tag, text=line))

    by_category: dict[str, list[dict[str, str]]] = {"simulator_logic": [], "graphics": []}
    seen: set[tuple[str, str, str]] = set()
    for snip in snippets:
        key = (snip.source, snip.category, snip.text)
        if key in seen:
            continue
        seen.add(key)
        by_category[snip.category].append({"source": snip.source, "text": snip.text})

    return {
        "summary": {
            "sources_scanned": len(source_stats),
            "total_extracted_lines": sum(source_stats.values()),
            "simulator_logic_matches": len(by_category["simulator_logic"]),
            "graphics_matches": len(by_category["graphics"]),
        },
        "source_line_counts": source_stats,
        "results": by_category,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--out", type=Path, default=Path("data/simulator_logic_graphics_scrape.json"))
    args = parser.parse_args()

    payload = scrape(args.root)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2))
    print(f"Wrote scrape output -> {args.out}")


if __name__ == "__main__":
    main()
