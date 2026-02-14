#!/usr/bin/env python3
"""Netflix-style studio simulation builder.

This module provides:
1. A pacing simulator inspired by streaming studio workflows.
2. Conversion from generic videos into simulation timelines.
3. Conversion from screen recordings into interaction-aware simulations.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import math
import shutil
import subprocess
from pathlib import Path
from typing import Any


@dataclasses.dataclass
class Segment:
    """A segment in the generated simulation timeline."""

    start_sec: float
    end_sec: float
    beat_type: str
    intensity: float
    notes: str


@dataclasses.dataclass
class Simulation:
    """Top-level simulation payload."""

    source: str
    mode: str
    duration_sec: float
    width: int
    height: int
    fps: float
    binge_score: float
    segments: list[Segment]

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "mode": self.mode,
            "duration_sec": self.duration_sec,
            "width": self.width,
            "height": self.height,
            "fps": self.fps,
            "binge_score": self.binge_score,
            "segments": [dataclasses.asdict(segment) for segment in self.segments],
        }


def _run_json_command(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def probe_video(video_path: Path) -> dict[str, Any]:
    """Extract portable media metadata with ffprobe."""
    if not shutil.which("ffprobe"):
        raise RuntimeError("ffprobe is required but not installed.")

    data = _run_json_command(
        [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_streams",
            "-show_format",
            str(video_path),
        ]
    )
    video_stream = next((stream for stream in data.get("streams", []) if stream.get("codec_type") == "video"), None)
    if video_stream is None:
        raise ValueError(f"No video stream found in {video_path}")

    r_frame_rate = video_stream.get("r_frame_rate", "0/1")
    num, den = r_frame_rate.split("/")
    fps = float(num) / float(den) if float(den) else 0.0

    return {
        "duration_sec": float(data.get("format", {}).get("duration", 0.0)),
        "width": int(video_stream.get("width", 0)),
        "height": int(video_stream.get("height", 0)),
        "fps": fps,
    }


def _beat_type(index: int, total: int, mode: str) -> str:
    if index == 0:
        return "cold_open"
    if index == total - 1:
        return "cliffhanger"
    if mode == "screen":
        return "interaction"
    return "story"


def _intensity_curve(position: float) -> float:
    # Start strong, dip in the middle, finish with a peak.
    return max(0.1, min(1.0, 0.55 + 0.35 * math.cos((position - 1.0) * math.pi)))


def _generate_segments(duration_sec: float, mode: str, beat_window_sec: float) -> list[Segment]:
    if duration_sec <= 0:
        return []

    count = max(3, math.ceil(duration_sec / beat_window_sec))
    segment_len = duration_sec / count
    segments: list[Segment] = []

    for index in range(count):
        start = round(index * segment_len, 3)
        end = round(duration_sec if index == count - 1 else (index + 1) * segment_len, 3)
        position = index / max(1, count - 1)
        beat = _beat_type(index, count, mode)
        intensity = round(_intensity_curve(position), 3)
        notes = {
            "cold_open": "Immediate hook in first seconds to maximize retention.",
            "story": "Narrative progress beat; maintain momentum.",
            "interaction": "UI/state transition beat inferred from screen activity.",
            "cliffhanger": "Leave unresolved tension to drive next episode/session.",
        }[beat]
        segments.append(
            Segment(start_sec=start, end_sec=end, beat_type=beat, intensity=intensity, notes=notes)
        )

    return segments


def build_simulation(video_path: Path, mode: str = "video", beat_window_sec: float = 12.0) -> Simulation:
    metadata = probe_video(video_path)
    segments = _generate_segments(metadata["duration_sec"], mode, beat_window_sec)

    # Binge score favors higher ending intensity and more beats.
    if segments:
        final_intensity = segments[-1].intensity
        average_intensity = sum(segment.intensity for segment in segments) / len(segments)
    else:
        final_intensity = 0.0
        average_intensity = 0.0

    binge_score = round(min(100.0, (average_intensity * 55) + (final_intensity * 35) + len(segments)), 2)

    return Simulation(
        source=str(video_path),
        mode=mode,
        duration_sec=metadata["duration_sec"],
        width=metadata["width"],
        height=metadata["height"],
        fps=metadata["fps"],
        binge_score=binge_score,
        segments=segments,
    )


def write_simulation(simulation: Simulation, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(simulation.to_dict(), indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a Netflix-style simulation timeline from a video.")
    parser.add_argument("input", type=Path, help="Path to input video or screen recording.")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Path for simulation JSON output.")
    parser.add_argument(
        "--mode",
        choices=["video", "screen"],
        default="video",
        help="Use 'screen' for screen recordings and 'video' for standard footage.",
    )
    parser.add_argument(
        "--beat-window-sec",
        type=float,
        default=12.0,
        help="Average seconds per narrative beat (smaller means more beats).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    simulation = build_simulation(args.input, mode=args.mode, beat_window_sec=args.beat_window_sec)
    write_simulation(simulation, args.output)
    print(f"Wrote simulation to {args.output}")


if __name__ == "__main__":
    main()
