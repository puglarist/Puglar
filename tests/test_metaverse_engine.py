import unittest

from engine.metaverse_engine import Item, MetaverseEngine, Player, Quest, Region


class TestMetaverseEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = MetaverseEngine()
        self.engine.add_region(Region("r1", "Sanctum", danger_level=1))
        self.engine.add_region(Region("r2", "Wilds", danger_level=3))
        self.engine.connect_regions("r1", "r2")

        self.engine.add_player(Player("p1", "Ari", "r1"))
        self.engine.add_player(Player("p2", "Bo", "r1"))

    def test_player_movement_requires_energy_and_connection(self):
        self.engine.players["p1"].energy = 20
        self.engine.move_player("p1", "r2")
        self.assertEqual("r2", self.engine.players["p1"].location_id)
        self.assertEqual(11, self.engine.players["p1"].energy)

    def test_attack_clamps_hp_to_zero_and_awards_xp(self):
        self.engine.players["p1"].inventory.append(Item("Blade", "weapon", power=15))
        damage = self.engine.attack_player("p1", "p2", 100)
        self.assertEqual(115, damage)
        self.assertEqual(0, self.engine.players["p2"].hp)
        self.assertGreaterEqual(self.engine.players["p1"].xp, 30)

    def test_healing_item_caps_hp(self):
        p1 = self.engine.players["p1"]
        p1.hp = 95
        p1.inventory.append(Item("Bandage", "healing", power=20))
        used = self.engine.use_item("p1", "Bandage")
        self.assertTrue(used)
        self.assertEqual(100, p1.hp)

    def test_quest_progress_and_completion(self):
        self.engine.register_quest(Quest("Hunter", objective="defeat", target_amount=1, reward_xp=50))
        self.engine.assign_quest("p1", "Hunter")
        self.engine.players["p1"].inventory.append(Item("Sword", "weapon", power=100))
        self.engine.attack_player("p1", "p2", 5)

        completed = self.engine.complete_quest_if_ready("p1", "Hunter")
        self.assertTrue(completed)
        self.assertNotIn("Hunter", self.engine.players["p1"].active_quests)

    def test_simulate_tick_updates_weather_and_recovery(self):
        p1 = self.engine.players["p1"]
        p1.energy = 80
        p1.hp = 90
        for _ in range(5):
            self.engine.simulate_tick()

        self.assertGreaterEqual(p1.energy, 84)
        self.assertEqual(91, p1.hp)
        snap = self.engine.region_snapshot("r1")
        self.assertIn(snap["weather"], {"clear", "rain", "storm", "fog"})


if __name__ == "__main__":
    unittest.main()
