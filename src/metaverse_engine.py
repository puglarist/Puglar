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
    experience_multiplier: float = 1.0
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

        self.friends: Dict[str, Set[str]] = {}
        self.parties: Dict[str, Set[str]] = {}

        if shard.max_players <= 0:
            raise ValueError("max_players must be positive")
        self.friends[avatar.avatar_id] = set()
        if portal.unlock_level < 1:
            raise ValueError("unlock_level must be at least 1")
    def _effective_level(self, avatar_id: str, avatar_level: int | None) -> int:
        if avatar_level is not None:
            return avatar_level
        return self.avatar_progress[avatar_id].level

        if to_shard not in self.shards:
            raise ValueError(f"Unknown destination shard: {to_shard}")
        available_links = self.portals.get(avatar.shard_id, [])
        matched = [p for p in available_links if p.to_shard == to_shard]
        if not matched:
        effective_level = self._effective_level(avatar_id, avatar_level)
        required_level = min(link.unlock_level for link in matched)
        if event.starts_at > event.ends_at:
            raise ValueError("Event start time must be before end time")
        if event.experience_multiplier < 1.0:
            raise ValueError("experience_multiplier must be at least 1.0")

    def experience_multiplier_for_avatar(
        self,
        avatar_id: str,
        now: datetime | None = None,
    ) -> float:
        avatar = self.avatars.get(avatar_id)
        if not avatar:
            raise ValueError(f"Avatar not found: {avatar_id}")

        multiplier = 1.0
        for event in self.live_events(now):
            if avatar.shard_id in event.active_shards:
                multiplier *= event.experience_multiplier
        return multiplier

    def grant_activity_experience(
        self,
        avatar_id: str,
        base_experience: int,
        now: datetime | None = None,
    ) -> AvatarProgress:
        if base_experience < 0:
            raise ValueError("base_experience must be non-negative")

        multiplier = self.experience_multiplier_for_avatar(avatar_id, now)
        adjusted = int(base_experience * multiplier)
        return self.gain_experience(avatar_id, adjusted)

        if template.minimum_level < 1:
            raise ValueError("minimum_level must be at least 1")
        if template.reward_experience < 0:
            raise ValueError("reward_experience must be non-negative")
        if quest_id in self.completed_quests[avatar_id]:
            raise ValueError(f"Quest already completed by avatar: {quest_id}")
    def add_friendship(self, avatar_a: str, avatar_b: str) -> None:
        if avatar_a == avatar_b:
            raise ValueError("Cannot friend the same avatar")
        if avatar_a not in self.avatars or avatar_b not in self.avatars:
            raise ValueError("Both avatars must exist")
        self.friends[avatar_a].add(avatar_b)
        self.friends[avatar_b].add(avatar_a)

    def create_party(self, party_id: str, leader_avatar_id: str) -> None:
        if party_id in self.parties:
            raise ValueError(f"Party already exists: {party_id}")
        if leader_avatar_id not in self.avatars:
            raise ValueError(f"Avatar not found: {leader_avatar_id}")
        self.parties[party_id] = {leader_avatar_id}

    def add_party_member(self, party_id: str, avatar_id: str) -> None:
        party = self.parties.get(party_id)
        if party is None:
            raise ValueError(f"Party not found: {party_id}")
        if avatar_id not in self.avatars:
            raise ValueError(f"Avatar not found: {avatar_id}")

        if party:
            is_friend = any(member in self.friends[avatar_id] for member in party)
            if not is_friend:
                raise PermissionError("Avatar must be friends with at least one party member")

        party.add(avatar_id)

    def party_travel(self, party_id: str, to_shard: str) -> List[str]:
        party = self.parties.get(party_id)
        if party is None:
            raise ValueError(f"Party not found: {party_id}")

        members = sorted(party)
        for avatar_id in members:
            avatar = self.avatars[avatar_id]
            available_links = self.portals.get(avatar.shard_id, [])
            matched = [p for p in available_links if p.to_shard == to_shard]
            if not matched:
                raise PermissionError(f"No portal from {avatar.shard_id} to {to_shard} for {avatar_id}")
            required_level = min(link.unlock_level for link in matched)
            level = self.avatar_progress[avatar_id].level
            if level < required_level:
                raise PermissionError(
                    f"Avatar {avatar_id} level {level} below required {required_level}"
                )

        destination_capacity = self.shards[to_shard].max_players
        current_population = self.shard_population()[to_shard]
        moving_from_destination = sum(1 for a in members if self.avatars[a].shard_id == to_shard)
        incoming = len(members) - moving_from_destination
        if current_population + incoming > destination_capacity:
            raise OverflowError(f"Destination shard is full: {to_shard}")

        for avatar_id in members:
            self.avatars[avatar_id].shard_id = to_shard
            self.avatars[avatar_id].position = (0.0, 0.0, 0.0)
        return members


    def top_avatars_by_experience(self, limit: int = 10) -> List[Tuple[str, int]]:
        if limit <= 0:
            raise ValueError("limit must be positive")
        rankings = [
            (avatar_id, progress.experience)
            for avatar_id, progress in self.avatar_progress.items()
        ]
        rankings.sort(key=lambda item: item[1], reverse=True)
        return rankings[:limit]
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
