#!/usr/bin/env python3
"""Create audio with Hugging Face and scrape audio files from webpages."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

AUDIO_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".flac",
    ".ogg",
    ".m4a",
    ".aac",
    ".opus",
    ".webm",
}


class AudioLinkParser(HTMLParser):
    """Extract likely audio file links from HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.links: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        attrs_dict = dict(attrs)
        if tag in {"audio", "source"}:
            src = attrs_dict.get("src")
            if src:
                self.links.add(src)
        if tag == "a":
            href = attrs_dict.get("href")
            if href:
                self.links.add(href)


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]", "_", name)
    return cleaned.strip("._") or "audio_file"


def is_probably_audio(url_or_path: str, content_type: Optional[str] = None) -> bool:
    parsed = urlparse(url_or_path)
    ext = Path(parsed.path).suffix.lower()
    if ext in AUDIO_EXTENSIONS:
        return True
    guessed, _ = mimetypes.guess_type(parsed.path)
    if guessed and guessed.startswith("audio/"):
        return True
    if content_type and content_type.startswith("audio/"):
        return True
    return False


def http_get(url: str, headers: Optional[dict[str, str]] = None, data: bytes | None = None) -> tuple[bytes, str, int]:
    req = Request(url, data=data, headers=headers or {}, method="POST" if data is not None else "GET")
    with urlopen(req, timeout=180) as response:
        content = response.read()
        content_type = response.headers.get("Content-Type", "")
        status = getattr(response, "status", 200)
    return content, content_type, status


def collect_audio_urls(page_url: str) -> list[str]:
    html_bytes, _, _ = http_get(page_url)
    parser = AudioLinkParser()
    parser.feed(html_bytes.decode("utf-8", errors="ignore"))

    resolved_links = [urljoin(page_url, raw_link) for raw_link in parser.links]
    return sorted(set(link for link in resolved_links if is_probably_audio(link)))


def download_file(url: str, output_dir: Path) -> Path:
    content, content_type, _ = http_get(url)
    content_type = content_type.split(";")[0].strip()
    if not is_probably_audio(url, content_type=content_type):
        raise ValueError(f"URL does not look like audio content: {url}")

    parsed = urlparse(url)
    original_name = Path(parsed.path).name or "audio"
    safe_name = sanitize_filename(original_name)
    target = output_dir / safe_name

    i = 1
    while target.exists():
        target = output_dir / f"{target.stem}_{i}{target.suffix}"
        i += 1

    target.write_bytes(content)
    return target


def scrape_audio_files(page_url: str, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    urls = collect_audio_urls(page_url)
    downloaded = []
    for url in urls:
        try:
            downloaded.append(download_file(url, output_dir))
        except Exception as exc:  # noqa: BLE001
            print(f"[WARN] failed to download {url}: {exc}")
    return downloaded


def generate_audio_hf(
    text: str,
    output_file: Path,
    model: str,
    token: str,
    voice_preset: Optional[str] = None,
) -> Path:
    output_file.parent.mkdir(parents=True, exist_ok=True)

    api_url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload: dict[str, object] = {"inputs": text}
    if voice_preset:
        payload["parameters"] = {"voice_preset": voice_preset}

    response_bytes, content_type, _ = http_get(
        api_url,
        headers=headers,
        data=json.dumps(payload).encode("utf-8"),
    )

    if "application/json" in content_type:
        msg = response_bytes.decode("utf-8", errors="ignore")
        raise RuntimeError(
            "HF returned JSON (model warming, error, or unsupported request). "
            f"Response: {msg[:500]}"
        )

    output_file.write_bytes(response_bytes)
    return output_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scrape audio files and generate audio using Hugging Face API"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scrape = subparsers.add_parser("scrape", help="Find and download audio files from a URL")
    scrape.add_argument("url", help="Webpage URL to inspect for audio links")
    scrape.add_argument(
        "--output-dir",
        type=Path,
        default=Path("downloaded_audio"),
        help="Directory to store scraped audio files",
    )

    generate = subparsers.add_parser("generate", help="Generate audio from text using HF API")
    generate.add_argument("--text", required=True, help="Text prompt to convert to speech")
    generate.add_argument(
        "--output-file",
        type=Path,
        default=Path("generated_audio.wav"),
        help="Target audio file path",
    )
    generate.add_argument(
        "--model",
        default="suno/bark",
        help="Hugging Face model ID for text-to-speech",
    )
    generate.add_argument(
        "--voice-preset",
        default=None,
        help="Optional voice preset for models that support it",
    )
    generate.add_argument(
        "--token",
        default=os.getenv("HF_TOKEN"),
        help="Hugging Face API token (or set HF_TOKEN env var)",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "scrape":
        files = scrape_audio_files(args.url, args.output_dir)
        print(f"Downloaded {len(files)} audio file(s).")
        for file_path in files:
            print(f" - {file_path}")
        return 0

    if args.command == "generate":
        if not args.token:
            parser.error("--token or HF_TOKEN environment variable is required")
        output = generate_audio_hf(
            text=args.text,
            output_file=args.output_file,
            model=args.model,
            token=args.token,
            voice_preset=args.voice_preset,
        )
        print(f"Generated audio saved to: {output}")
        return 0

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
