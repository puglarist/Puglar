import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_gta6_vehicles import build_dataset, extract_vehicle_records


class BuildVehiclesTests(unittest.TestCase):
    def test_extract_vehicle_records_dedupes_and_filters(self):
        html = """
        <html><body>
          <a href="/gta-6/vehicles/">Vehicles</a>
          <a href="/gta-6/vehicles/bravado-banshee">Bravado Banshee</a>
          <a href="/gta-6/vehicles/bravado-banshee">Bravado Banshee</a>
          <a href="/gta-6/vehicles/vapid-police-cruiser"><span>Vapid Police Cruiser</span></a>
          <a href="/gta-6/vehicles/all">All Vehicles</a>
        </body></html>
        """

        records = extract_vehicle_records(html, base_url="https://www.gtabase.com/gta-6/vehicles/")

        self.assertEqual([record.name for record in records], ["Bravado Banshee", "Vapid Police Cruiser"])

    def test_build_dataset_serializes(self):
        html = '<a href="/gta-6/vehicles/bravado-banshee">Bravado Banshee</a>'
        records = extract_vehicle_records(html)
        payload = build_dataset(records, source_url="https://example.com")

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "vehicles.json"
            out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            self.assertIn("vehicle_count", out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
