import unittest

from tools.threegs_build import emit_manifest, parse_contract

SAMPLE = """module Demo.Core v0.1

type Vec3 {
  x: f32
  y: f32
  z: f32
}

entity Player {
  id: uid
  inventory: list<Vec3>
}
"""

SAMPLE_WITH_SYSTEM_AND_API = """module Demo.Game v0.2

entity Input {
  axisX: f32 @clamp(-1, 1)
  axisY: f32 @clamp(-1, 1)
}

system Movement {
  reads: Input.axisX, Input.axisY
  writes: Input.axisX
}

api InputAPI {
  route GET /input/:id -> Input
}
"""


class ThreeGsBuildTests(unittest.TestCase):
    def test_parse_contract(self):
        contract = parse_contract(SAMPLE)
        self.assertEqual(contract.module, "Demo.Core")
        self.assertEqual(len(contract.blocks), 2)

    def test_manifest_has_blocks(self):
        manifest = emit_manifest(parse_contract(SAMPLE))
        self.assertEqual(manifest["blocks"][0]["name"], "Vec3")
        self.assertEqual(manifest["blocks"][1]["fields"][1]["type"], "list<Vec3>")

    def test_manifest_keeps_system_field_values(self):
        manifest = emit_manifest(parse_contract(SAMPLE_WITH_SYSTEM_AND_API))
        movement = next(b for b in manifest["blocks"] if b["name"] == "Movement")
        self.assertEqual(movement["fields"][0]["type"], "Input.axisX, Input.axisY")

    def test_manifest_captures_api_routes(self):
        manifest = emit_manifest(parse_contract(SAMPLE_WITH_SYSTEM_AND_API))
        api = next(b for b in manifest["blocks"] if b["name"] == "InputAPI")
        self.assertEqual(api["routes"][0]["method"], "GET")
        self.assertEqual(api["routes"][0]["path"], "/input/:id")
        self.assertEqual(api["routes"][0]["result"], "Input")


if __name__ == "__main__":
    unittest.main()
