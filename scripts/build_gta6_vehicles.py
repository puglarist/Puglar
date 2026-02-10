#!/usr/bin/env python3
"""Build a GTA 6 vehicles dataset from a GTABase page.

Usage:
  python scripts/build_gta6_vehicles.py \
    --url https://www.gtabase.com/gta-6/vehicles/ \
    --out data/gta6_vehicles.json

For offline/debug parsing:
  python scripts/build_gta6_vehicles.py --from-file page.html --out data/gta6_vehicles.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.error import URLError, HTTPError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


DEFAULT_URL = "https://www.gtabase.com/gta-6/vehicles/"


@dataclass(frozen=True)
class VehicleRecord:
    name: str
    url: str


def fetch_html(url: str, timeout: int = 25) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/125.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        encoding = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(encoding, errors="replace")


def _norm_ws(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def extract_vehicle_records(html: str, base_url: str = DEFAULT_URL) -> list[VehicleRecord]:
    pattern = re.compile(
        r'<a[^>]+href="(?P<href>[^"]*/gta-6/vehicles/[^"]+)"[^>]*>(?P<text>.*?)</a>',
        flags=re.IGNORECASE | re.DOTALL,
    )

    disallowed = {
        "gta 6 vehicles",
        "vehicles",
        "all vehicles",
        "more vehicles",
        "view all",
    }

    records: dict[str, VehicleRecord] = {}
    for match in pattern.finditer(html):
        href = match.group("href")
        text = _norm_ws(re.sub(r"<[^>]*>", "", match.group("text")))

        if not text:
            continue

        lowered = text.casefold()
        if lowered in disallowed:
            continue

        if len(text) < 2 or len(text) > 80:
            continue

        absolute_url = urljoin(base_url, href)
        path = urlparse(absolute_url).path
        slug = path.rstrip("/").split("/")[-1]

        # Skip category/list pages; keep likely model pages.
        if slug in {"vehicles", "gta-6"}:
            continue

        # Deduplicate by normalized model name.
        key = lowered
        records[key] = VehicleRecord(name=text, url=absolute_url)

    return sorted(records.values(), key=lambda r: r.name.casefold())


def build_dataset(records: Iterable[VehicleRecord], source_url: str) -> dict:
    record_list = list(records)
    return {
        "source_url": source_url,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "vehicle_count": len(record_list),
        "vehicles": [
            {
                "name": record.name,
                "url": record.url,
            }
            for record in record_list
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL, help="Source URL to fetch.")
    parser.add_argument("--from-file", help="Read HTML from a local file instead of URL.")
    parser.add_argument("--out", default="data/gta6_vehicles.json", help="Output JSON path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        if args.from_file:
            html = Path(args.from_file).read_text(encoding="utf-8")
            source = f"file://{Path(args.from_file).resolve()}"
        else:
            html = fetch_html(args.url)
            source = args.url

        records = extract_vehicle_records(html, base_url=args.url)
        dataset = build_dataset(records, source_url=source)

        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(dataset, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        print(f"Wrote {dataset['vehicle_count']} vehicles to {out_path}")
        return 0
    except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
        print(f"Failed to build vehicle dataset: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
