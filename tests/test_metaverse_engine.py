from datetime import datetime, timedelta, timezone

from src.metaverse_engine import (
    AvatarState,
    MetaverseEngine,
    PortalLink,
    TimeboxedEvent,
    WorldShard,
)


def build_engine() -> MetaverseEngine:
    engine = MetaverseEngine()
    engine.register_shard(WorldShard("hub", "Hub", 100, "city"))
    engine.register_shard(WorldShard("forest", "Verdant Rim", 40, "forest"))
    engine.register_shard(WorldShard("arena", "Sky Arena", 20, "floating"))
    engine.link_portal(PortalLink("hub", "forest", unlock_level=1))
    engine.link_portal(PortalLink("forest", "arena", unlock_level=5))
    engine.link_portal(PortalLink("hub", "arena", unlock_level=5))
    engine.spawn_avatar(AvatarState("ava-1", "hub"))
    engine.spawn_avatar(AvatarState("ava-2", "hub"))
    return engine


def test_avatar_travel_with_unlock_requirements() -> None:
    engine = build_engine()
    assert engine.travel("ava-1", "forest", avatar_level=1) == "forest"

    try:
        engine.travel("ava-1", "arena", avatar_level=3)
        raise AssertionError("Expected permission error for low-level avatar")
    except PermissionError:
        pass

    assert engine.travel("ava-1", "arena", avatar_level=5) == "arena"


def test_asset_minting_and_transfers_update_inventory() -> None:
    engine = build_engine()
    engine.mint_asset("asset-dragon-bike", "ava-1")

    assert "asset-dragon-bike" in engine.avatars["ava-1"].inventory
    assert engine.asset_owners["asset-dragon-bike"] == "ava-1"

    engine.transfer_asset("asset-dragon-bike", "ava-2")

    assert "asset-dragon-bike" not in engine.avatars["ava-1"].inventory
    assert "asset-dragon-bike" in engine.avatars["ava-2"].inventory
    assert engine.asset_owners["asset-dragon-bike"] == "ava-2"


def test_event_scheduling_and_live_event_query() -> None:
    engine = build_engine()
    now = datetime.now(timezone.utc)

    engine.schedule_event(
        TimeboxedEvent(
            event_id="meteor-shower",
            title="Meteor Shower XP Surge",
            starts_at=now - timedelta(minutes=10),
            ends_at=now + timedelta(minutes=10),
            active_shards={"hub", "forest"},
        )
    )
    engine.schedule_event(
        TimeboxedEvent(
            event_id="arena-finals",
            title="Arena Finals",
            starts_at=now + timedelta(hours=1),
            ends_at=now + timedelta(hours=2),
            active_shards={"arena"},
        )
    )

    live_ids = {event.event_id for event in engine.live_events(now=now)}
    assert live_ids == {"meteor-shower"}


def test_population_tracking_by_shard() -> None:
    engine = build_engine()
    assert engine.shard_population() == {"hub": 2, "forest": 0, "arena": 0}

    with pytest.raises(ValueError):
        engine.assign_quest("ava-1", "quest-meteor-sample")



def test_event_multiplier_applies_to_activity_xp() -> None:
    engine = build_engine()
    now = datetime.now(timezone.utc)

    engine.schedule_event(
        TimeboxedEvent(
            event_id="double-xp-forest",
            title="Forest XP Rush",
            starts_at=now - timedelta(minutes=5),
            ends_at=now + timedelta(minutes=5),
            active_shards={"hub"},
            experience_multiplier=2.0,
        )
    )

    engine.grant_activity_experience("ava-1", base_experience=50, now=now)
    assert engine.avatar_progress["ava-1"].experience == 100


def test_party_travel_requires_friendship_and_level() -> None:
    engine = build_engine()

    engine.create_party("party-1", "ava-1")
    with pytest.raises(PermissionError):
        engine.add_party_member("party-1", "ava-2")

    engine.add_friendship("ava-1", "ava-2")
    engine.add_party_member("party-1", "ava-2")

    with pytest.raises(PermissionError):
        engine.party_travel("party-1", "arena")

    engine.gain_experience("ava-1", 400)
    engine.gain_experience("ava-2", 400)
    moved = engine.party_travel("party-1", "arena")

    assert moved == ["ava-1", "ava-2"]
    assert engine.shard_population() == {"hub": 0, "forest": 0, "arena": 2}


def test_top_avatars_by_experience_returns_ranked_subset() -> None:
    engine = build_engine()
    engine.gain_experience("ava-1", 120)
    engine.gain_experience("ava-2", 260)

    assert engine.top_avatars_by_experience(limit=1) == [("ava-2", 260)]
    engine.travel("ava-2", "forest", avatar_level=1)
    assert engine.shard_population() == {"hub": 1, "forest": 1, "arena": 0}
