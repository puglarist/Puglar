from puglar_metaverse.hand_tracking import HandPose, HandTrackingEngine
from puglar_metaverse.trickshot_promod import ProModEngine, WeaponProfile
from puglar_metaverse.realism_graphics import GraphicsEngine, GraphicsProfile
from puglar_metaverse.mod_menu import ModMenu


def test_hand_tracking_gesture():
    engine = HandTrackingEngine()
    pose = HandPose([(0.1, 0.1, 0.1)] * 21)
    smoothed = engine.smooth_pose("h", pose)
    assert engine.classify_gesture(smoothed) in {"open_hand", "weapon_ready", "fist"}


def test_promod_multiplier_increases_with_style():
    promod = ProModEngine(seed=1)
    weapon = WeaponProfile("Intervention", 95, 0.32, 0.18, 940)
    basic = promod.resolve_shot(weapon, 120, 0, 0.1, 0)
    stylish = promod.resolve_shot(weapon, 120, 1080, 1.8, 4)
    assert stylish["trickshot_multiplier"] > basic["trickshot_multiplier"]


def test_graphics_realism_score_bounds():
    gfx = GraphicsEngine()
    score = gfx.realism_score(GraphicsProfile(2, 2, 2, 2, 2))
    assert 0 <= score <= 1


def test_mod_menu_allowlist():
    menu = ModMenu()
    menu.set("fov", 105)
    assert menu.get("fov") == 105
