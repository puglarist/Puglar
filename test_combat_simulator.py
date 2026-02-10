import unittest

from combat_simulator import Fighter, available_styles, simulate_bout


class CombatSimulatorTests(unittest.TestCase):
    def test_styles_include_boxing_and_mma(self):
        styles = set(available_styles())
        self.assertIn("boxing", styles)
        self.assertIn("mma", styles)
        self.assertIn("muay_thai", styles)

    def test_deterministic_bout_with_seed(self):
        a = Fighter("Atlas", "boxing", aggression=72, fight_iq=68)
        b = Fighter("Rogue", "mma", aggression=65, fight_iq=75)

        result = simulate_bout(a, b, rounds=5, seed=7)

        self.assertEqual(result.winner.name, "Rogue")
        self.assertEqual(result.rounds_fought, 5)
        self.assertEqual(result.scorecard["Atlas"], 47)
        self.assertEqual(result.scorecard["Rogue"], 49)

    def test_unknown_style_raises(self):
        with self.assertRaises(ValueError):
            Fighter("Ghost", "karate")


if __name__ == "__main__":
    unittest.main()
