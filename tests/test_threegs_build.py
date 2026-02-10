import unittest
from tools.threegs_build import parse_contract, emit_manifest

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


class ThreeGsBuildTests(unittest.TestCase):
    def test_parse_contract(self):
        contract = parse_contract(SAMPLE)
        self.assertEqual(contract.module, "Demo.Core")
        self.assertEqual(len(contract.blocks), 2)

    def test_manifest_has_blocks(self):
        manifest = emit_manifest(parse_contract(SAMPLE))
        self.assertEqual(manifest["blocks"][0]["name"], "Vec3")
        self.assertEqual(manifest["blocks"][1]["fields"][1]["type"], "list<Vec3>")


if __name__ == "__main__":
    unittest.main()
