from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Set, Tuple


@dataclass(frozen=True)
class WorldShard:
    """Represents a zone hosted in the metaverse."""

    shard_id: str
    title: str
    max_players: int
    biome: str


@dataclass
class AvatarState:
    """Tracks per-player live state in the simulation."""

    avatar_id: str
    shard_id: str
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    inventory: Set[str] = field(default_factory=set)


@dataclass
class PortalLink:
    """Bidirectional travel route between two shards."""

    from_shard: str
    to_shard: str
    unlock_level: int = 1


@dataclass
class TimeboxedEvent:
    """Global live event that can activate across shards."""

    event_id: str
    title: str
    starts_at: datetime
    ends_at: datetime
    active_shards: Set[str]

    def is_live(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return self.starts_at <= now <= self.ends_at


class MetaverseEngine:
    """Lightweight simulation core for metaverse features."""

    def __init__(self) -> None:
        self.shards: Dict[str, WorldShard] = {}
        self.avatars: Dict[str, AvatarState] = {}
        self.portals: Dict[str, List[PortalLink]] = {}
        self.events: Dict[str, TimeboxedEvent] = {}
        self.asset_owners: Dict[str, str] = {}

    def register_shard(self, shard: WorldShard) -> None:
        if shard.shard_id in self.shards:
            raise ValueError(f"Shard already exists: {shard.shard_id}")
        self.shards[shard.shard_id] = shard
        self.portals.setdefault(shard.shard_id, [])

    def spawn_avatar(self, avatar: AvatarState) -> None:
        if avatar.shard_id not in self.shards:
            raise ValueError(f"Unknown shard: {avatar.shard_id}")
        if avatar.avatar_id in self.avatars:
            raise ValueError(f"Avatar already exists: {avatar.avatar_id}")
        self.avatars[avatar.avatar_id] = avatar

    def link_portal(self, portal: PortalLink) -> None:
        if portal.from_shard not in self.shards or portal.to_shard not in self.shards:
            raise ValueError("Both shards must be registered before linking")
        self.portals[portal.from_shard].append(portal)

    def travel(self, avatar_id: str, to_shard: str, avatar_level: int = 1) -> str:
        avatar = self.avatars.get(avatar_id)
        if not avatar:
            raise ValueError(f"Avatar not found: {avatar_id}")

        available_links = self.portals.get(avatar.shard_id, [])
        matched = [p for p in available_links if p.to_shard == to_shard]
        if not matched:
            raise PermissionError(
                f"No portal from {avatar.shard_id} to {to_shard}"
            )

        required_level = min(link.unlock_level for link in matched)
        if avatar_level < required_level:
            raise PermissionError(
                f"Avatar level {avatar_level} below required {required_level}"
            )

        avatar.shard_id = to_shard
        avatar.position = (0.0, 0.0, 0.0)
        return to_shard

    def mint_asset(self, asset_id: str, owner_avatar_id: str) -> None:
        if owner_avatar_id not in self.avatars:
            raise ValueError(f"Unknown owner avatar: {owner_avatar_id}")
        if asset_id in self.asset_owners:
            raise ValueError(f"Asset already minted: {asset_id}")
        self.asset_owners[asset_id] = owner_avatar_id
        self.avatars[owner_avatar_id].inventory.add(asset_id)

    def transfer_asset(self, asset_id: str, to_avatar_id: str) -> None:
        if to_avatar_id not in self.avatars:
            raise ValueError(f"Unknown recipient avatar: {to_avatar_id}")
        from_avatar_id = self.asset_owners.get(asset_id)
        if not from_avatar_id:
            raise ValueError(f"Asset does not exist: {asset_id}")

        if from_avatar_id == to_avatar_id:
            return

        self.avatars[from_avatar_id].inventory.discard(asset_id)
        self.avatars[to_avatar_id].inventory.add(asset_id)
        self.asset_owners[asset_id] = to_avatar_id

    def schedule_event(self, event: TimeboxedEvent) -> None:
        unknown_shards = event.active_shards - self.shards.keys()
        if unknown_shards:
            unknown_str = ", ".join(sorted(unknown_shards))
            raise ValueError(f"Unknown shards in event: {unknown_str}")
        self.events[event.event_id] = event

    def live_events(self, now: datetime | None = None) -> List[TimeboxedEvent]:
        now = now or datetime.now(timezone.utc)
        return [event for event in self.events.values() if event.is_live(now)]

    def shard_population(self) -> Dict[str, int]:
        counts = {shard_id: 0 for shard_id in self.shards.keys()}
        for avatar in self.avatars.values():
            counts[avatar.shard_id] += 1
        return counts
