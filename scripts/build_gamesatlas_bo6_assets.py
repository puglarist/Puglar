#!/usr/bin/env python3
"""Scrape BO6 weapon assets from GamesAtlas and build a local asset bundle.

Usage:
  python scripts/build_gamesatlas_bo6_assets.py

Outputs:
  - build/bo6_weapons/page.html
  - build/bo6_weapons/weapons.json
  - build/bo6_weapons/images/*
"""

from __future__ import annotations

import json
import re
import ssl
import sys
from dataclasses import dataclass, asdict
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

SOURCE_URL = "https://www.gamesatlas.com/cod-black-ops-6/weapons/"
OUTPUT_ROOT = Path("build/bo6_weapons")
OUTPUT_HTML = OUTPUT_ROOT / "page.html"
OUTPUT_JSON = OUTPUT_ROOT / "weapons.json"
IMAGE_DIR = OUTPUT_ROOT / "images"

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


@dataclass
class WeaponAsset:
    name: str
    href: str
    image_url: str | None = None
    image_path: str | None = None


class AnchorImageParser(HTMLParser):
    """Collect anchors and images, then correlate by proximity in HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.anchors: list[tuple[str, str]] = []
        self.images: list[str] = []
        self._in_anchor = False
        self._anchor_href: str | None = None
        self._anchor_text_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {k: v for k, v in attrs}
        if tag == "a":
            href = attr_map.get("href")
            if href:
                self._in_anchor = True
                self._anchor_href = href
                self._anchor_text_chunks = []
        elif tag == "img":
            src = attr_map.get("src") or attr_map.get("data-src")
            if src:
                self.images.append(src)

    def handle_data(self, data: str) -> None:
        if self._in_anchor and data.strip():
            self._anchor_text_chunks.append(data.strip())

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._in_anchor:
            text = " ".join(self._anchor_text_chunks).strip()
            if self._anchor_href and text:
                self.anchors.append((self._anchor_href, text))
            self._in_anchor = False
            self._anchor_href = None
            self._anchor_text_chunks = []


def fetch_html(url: str) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    ctx = ssl.create_default_context()
    with urlopen(req, timeout=45, context=ctx) as resp:
        content_type = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(content_type, errors="replace")


def extract_candidate_weapons(html: str) -> list[WeaponAsset]:
    parser = AnchorImageParser()
    parser.feed(html)

    anchors = []
    for href, text in parser.anchors:
        absolute_href = urljoin(SOURCE_URL, href)
        if "/weapon/" in absolute_href or "/weapons/" in absolute_href:
            anchors.append((absolute_href, text))

    deduped: list[tuple[str, str]] = []
    seen = set()
    for href, text in anchors:
        key = (href, text.lower())
        if key in seen:
            continue
        seen.add(key)
        deduped.append((href, text))

    image_iter: Iterable[str | None] = iter(parser.images)
    weapons: list[WeaponAsset] = []
    for href, name in deduped:
        img = next(image_iter, None)
        if img:
            img = urljoin(SOURCE_URL, img)
        weapons.append(WeaponAsset(name=name, href=href, image_url=img))

    return weapons


def filename_from_url(url: str, fallback_index: int) -> str:
    path = urlparse(url).path
    name = Path(path).name
    if not name:
        name = f"image-{fallback_index}.jpg"
    if not Path(name).suffix:
        name = f"{name}.jpg"
    return name


def download_images(weapons: list[WeaponAsset]) -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    for idx, weapon in enumerate(weapons, start=1):
        if not weapon.image_url:
            continue

        file_name = filename_from_url(weapon.image_url, idx)
        out_path = IMAGE_DIR / file_name

        if out_path.exists() and out_path.stat().st_size > 0:
            weapon.image_path = str(out_path.relative_to(OUTPUT_ROOT))
            continue

        req = Request(weapon.image_url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=45) as resp:
                content = resp.read()
            out_path.write_bytes(content)
            weapon.image_path = str(out_path.relative_to(OUTPUT_ROOT))
        except (HTTPError, URLError, TimeoutError) as exc:
            print(f"warning: failed to download {weapon.image_url}: {exc}", file=sys.stderr)


def save_outputs(html: str, weapons: list[WeaponAsset]) -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    payload = {
        "source": SOURCE_URL,
        "weapon_count": len(weapons),
        "weapons": [asdict(w) for w in weapons],
    }
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    try:
        html = fetch_html(SOURCE_URL)
    except Exception as exc:
        print(f"error: unable to fetch source page: {exc}", file=sys.stderr)
        return 1

    weapons = extract_candidate_weapons(html)
    if not weapons:
        # Attempt one fallback extraction from JSON-like title fields.
        names = sorted(set(re.findall(r'"title"\s*:\s*"([^"]+)"', html)))
        weapons = [WeaponAsset(name=n, href=SOURCE_URL) for n in names if len(n) <= 80]

    download_images(weapons)
    save_outputs(html, weapons)

    print(f"Built assets for {len(weapons)} weapons in {OUTPUT_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
