from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


@dataclass
class Item:
    """Portable object used by players."""

    name: str
    kind: str
    power: int = 0
    value: int = 0


@dataclass
class Quest:
    """Simple quest model with progress tracking."""

    title: str
    objective: str
    target_amount: int = 1
    reward_xp: int = 10


@dataclass
class Player:
    """Connected metaverse actor."""

    player_id: str
    name: str
    location_id: str
    hp: int = 100
    max_hp: int = 100
    level: int = 1
    xp: int = 0
    energy: int = 100
    inventory: List[Item] = field(default_factory=list)
    active_quests: Dict[str, int] = field(default_factory=dict)

    def gain_xp(self, amount: int) -> None:
        if amount <= 0:
            return
        self.xp += amount
        while self.xp >= self.level * 100:
            self.xp -= self.level * 100
            self.level += 1
            self.max_hp += 10
            self.hp = min(self.max_hp, self.hp + 10)


@dataclass
class Region:
    """World area that can contain players and events."""

    region_id: str
    name: str
    climate: str = "temperate"
    danger_level: int = 1
    connected_regions: Set[str] = field(default_factory=set)
    weather: str = "clear"


class MetaverseEngine:
    """Core game simulation engine.

    Features:
    - Player registration and movement with path validation.
    - Combat and item usage.
    - Quest assignment and completion tracking.
    - World tick simulation for weather + passive energy recovery.
    """

    def __init__(self) -> None:
        self.players: Dict[str, Player] = {}
        self.regions: Dict[str, Region] = {}
        self.quests: Dict[str, Quest] = {}
        self.tick_count: int = 0

    # ---------- region/world management ----------
    def add_region(self, region: Region) -> None:
        if region.region_id in self.regions:
            raise ValueError(f"Duplicate region id: {region.region_id}")
        self.regions[region.region_id] = region

    def connect_regions(self, a: str, b: str) -> None:
        self._require_region(a)
        self._require_region(b)
        self.regions[a].connected_regions.add(b)
        self.regions[b].connected_regions.add(a)

    # ---------- player management ----------
    def add_player(self, player: Player) -> None:
        self._require_region(player.location_id)
        if player.player_id in self.players:
            raise ValueError(f"Duplicate player id: {player.player_id}")
        self.players[player.player_id] = player

    def move_player(self, player_id: str, destination_region_id: str) -> None:
        player = self._require_player(player_id)
        self._require_region(destination_region_id)

        if destination_region_id == player.location_id:
            return

        current_region = self.regions[player.location_id]
        if destination_region_id not in current_region.connected_regions:
            raise ValueError(
                f"Invalid movement: {player.location_id} -> {destination_region_id} is not connected"
            )

        movement_cost = max(5, self.regions[destination_region_id].danger_level * 3)
        if player.energy < movement_cost:
            raise ValueError("Player does not have enough energy to move")

        player.energy -= movement_cost
        player.location_id = destination_region_id

    # ---------- gameplay systems ----------
    def attack_player(self, attacker_id: str, target_id: str, base_damage: int) -> int:
        attacker = self._require_player(attacker_id)
        target = self._require_player(target_id)

        if attacker.location_id != target.location_id:
            raise ValueError("Players must be in the same region for combat")
        if base_damage <= 0:
            raise ValueError("Damage must be positive")
        if attacker.energy < 10:
            raise ValueError("Attacker does not have enough energy")

        weapon_bonus = max(
            (item.power for item in attacker.inventory if item.kind == "weapon"),
            default=0,
        )
        damage = base_damage + weapon_bonus

        # bugfix: ensure hp never drops below zero.
        target.hp = max(0, target.hp - damage)
        attacker.energy = max(0, attacker.energy - 10)

        if target.hp == 0:
            attacker.gain_xp(30)
            self._increment_quest_progress(attacker, objective="defeat")

        return damage

    def use_item(self, player_id: str, item_name: str) -> bool:
        player = self._require_player(player_id)
        for idx, item in enumerate(player.inventory):
            if item.name != item_name:
                continue

            if item.kind == "healing":
                player.hp = min(player.max_hp, player.hp + max(1, item.power))
                player.inventory.pop(idx)
                return True

            if item.kind == "energy":
                player.energy = min(100, player.energy + max(1, item.power))
                player.inventory.pop(idx)
                return True

            if item.kind == "artifact":
                # Artifacts are persistent and increase experience instantly.
                player.gain_xp(max(5, item.value))
                return True

            return False

        return False

    # ---------- quest systems ----------
    def register_quest(self, quest: Quest) -> None:
        if quest.title in self.quests:
            raise ValueError(f"Duplicate quest title: {quest.title}")
        self.quests[quest.title] = quest

    def assign_quest(self, player_id: str, quest_title: str) -> None:
        player = self._require_player(player_id)
        if quest_title not in self.quests:
            raise ValueError(f"Unknown quest: {quest_title}")
        player.active_quests.setdefault(quest_title, 0)

    def complete_quest_if_ready(self, player_id: str, quest_title: str) -> bool:
        player = self._require_player(player_id)
        quest = self.quests.get(quest_title)
        if quest is None:
            raise ValueError(f"Unknown quest: {quest_title}")

        progress = player.active_quests.get(quest_title, 0)
        if progress < quest.target_amount:
            return False

        player.gain_xp(quest.reward_xp)
        del player.active_quests[quest_title]
        return True

    def simulate_tick(self) -> None:
        """Advance world state by one server tick."""
        self.tick_count += 1

        weather_cycle = ["clear", "rain", "storm", "fog"]
        for region in self.regions.values():
            region.weather = weather_cycle[(self.tick_count + region.danger_level) % len(weather_cycle)]

        for player in self.players.values():
            # Passive recovery capped at bounds (debug safety).
            player.energy = max(0, min(100, player.energy + 4))
            if player.hp > 0 and player.hp < player.max_hp and self.tick_count % 5 == 0:
                player.hp = min(player.max_hp, player.hp + 1)

    def region_snapshot(self, region_id: str) -> Dict[str, object]:
        self._require_region(region_id)
        players_in_region = [p.name for p in self.players.values() if p.location_id == region_id]
        region = self.regions[region_id]

        return {
            "region": region.name,
            "weather": region.weather,
            "danger_level": region.danger_level,
            "players": sorted(players_in_region),
        }

    # ---------- helpers ----------
    def _increment_quest_progress(self, player: Player, objective: str) -> None:
        for title in list(player.active_quests.keys()):
            quest = self.quests.get(title)
            if quest and quest.objective == objective:
                player.active_quests[title] = min(
                    quest.target_amount,
                    player.active_quests[title] + 1,
                )

    def _require_player(self, player_id: str) -> Player:
        if player_id not in self.players:
            raise ValueError(f"Unknown player id: {player_id}")
        return self.players[player_id]

    def _require_region(self, region_id: str) -> Region:
        if region_id not in self.regions:
            raise ValueError(f"Unknown region id: {region_id}")
        return self.regions[region_id]
