import tempfile
import unittest
from pathlib import Path

from src.combat_studio.game_logic import MinecraftLogic
from src.combat_studio.netflix_studio import NetflixStudioPipeline
from src.combat_studio.providers import HuggingFaceModelCatalog, RunPodConnector
from src.combat_studio.torrent_builder import TorrentBuilder


class CombatStudioTests(unittest.TestCase):
    def test_runpod_connector_url_and_headers(self):
        connector = RunPodConnector(api_key="abc", endpoint_id="xyz")
        self.assertEqual(connector.endpoint_url(), "https://api.runpod.ai/v2/xyz/run")
        self.assertEqual(connector.headers()["Authorization"], "Bearer abc")

    def test_huggingface_catalog_includes_expanded_models(self):
        catalog = HuggingFaceModelCatalog.default_catalog()
        self.assertIn("meta-llama/Llama-3.1-70B-Instruct", catalog.all_models())
        catalog.add_model("general", "org/new-model")
        self.assertIn("org/new-model", catalog.models["general"])

    def test_netflix_pipeline_stage_management(self):
        pipeline = NetflixStudioPipeline(project_name="combat-docuseries")
        pipeline.add_stage("localization")
        self.assertIn("localization", pipeline.stages)
        pipeline.remove_stage("localization")
        self.assertNotIn("localization", pipeline.stages)

    def test_torrent_builder_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            builder = TorrentBuilder.with_defaults(Path(tmp))
            sample = Path(tmp) / "sample.bin"
            sample.write_bytes(b"abc")
            manifest = builder.manifest_for(sample, "balanced")
            self.assertEqual(manifest["name"], "sample.bin")
            self.assertEqual(manifest["size"], 3)

    def test_minecraft_toggle_and_world_navigation(self):
        logic = MinecraftLogic()
        logic.toggle("raid_events", True)
        logic.go_to_world("hardcore-realm")
        logic.mob_menu.add_mob("warden", boss=True)
        self.assertTrue(logic.logic_toggles["raid_events"])
        self.assertEqual(logic.world_name, "hardcore-realm")
        self.assertIn("warden", logic.mob_menu.boss_mobs)


if __name__ == "__main__":
    unittest.main()
