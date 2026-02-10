from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha1
from pathlib import Path
from typing import Dict, List


@dataclass
class TorrentProfile:
    name: str
    piece_length: int
    private: bool = False
    trackers: List[str] = field(default_factory=list)


@dataclass
class TorrentBuilder:
    """Enhanced torrent payload builder with reusable presets and metadata checks."""

    output_dir: Path
    profiles: Dict[str, TorrentProfile] = field(default_factory=dict)

    @classmethod
    def with_defaults(cls, output_dir: Path) -> "TorrentBuilder":
        builder = cls(output_dir=output_dir)
        builder.register_profile(
            TorrentProfile(
                name="balanced",
                piece_length=2**20,
                trackers=[
                    "udp://tracker.opentrackr.org:1337/announce",
                    "udp://open.stealth.si:80/announce",
                ],
            )
        )
        builder.register_profile(
            TorrentProfile(
                name="streaming",
                piece_length=2**19,
                trackers=["udp://tracker.torrent.eu.org:451/announce"],
            )
        )
        return builder

    def register_profile(self, profile: TorrentProfile) -> None:
        if profile.piece_length <= 0 or (profile.piece_length & (profile.piece_length - 1)) != 0:
            raise ValueError("piece_length must be a positive power of two")
        self.profiles[profile.name] = profile

    def manifest_for(self, file_path: Path, profile_name: str) -> Dict[str, object]:
        if profile_name not in self.profiles:
            raise KeyError(f"Unknown profile '{profile_name}'")
        profile = self.profiles[profile_name]
        data = file_path.read_bytes()
        return {
            "name": file_path.name,
            "size": len(data),
            "piece_length": profile.piece_length,
            "private": int(profile.private),
            "trackers": profile.trackers,
            "sha1": sha1(data).hexdigest(),
        }
