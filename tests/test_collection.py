"""The release promise is three selected workflows for each device."""

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build
import ring

ROOT = Path(__file__).resolve().parents[1]


class CollectionTests(unittest.TestCase):
    def test_six_selected_catalogs_are_present_and_valid(self):
        expected = {
            "profiles": {
                "code-workflow": 83,
                "ai-workflow": 51,
                "browser-workflow": 46,
            },
            "rings": {"code-ring": 81, "work-ring": 81, "flow-ring": 72},
        }
        for folder, counts in expected.items():
            paths = list((ROOT / folder).glob("*.json"))
            self.assertEqual({p.stem for p in paths}, set(counts))
            for path in paths:
                catalog = json.loads(path.read_text(encoding="utf-8"))
                with self.subTest(catalog=path.stem):
                    self.assertEqual(catalog["id"], path.stem)
                    if folder == "profiles":
                        build.validate_catalog(catalog)
                        self.assertEqual(len(catalog["prompts"]), counts[path.stem])
                        self.assertEqual(len(catalog["pages"][0]["buttons"]), 15)
                    else:
                        ring.validate_ring(catalog)
                        self.assertEqual(
                            sum(len(p["actions"]) for p in catalog["folders"]),
                            counts[path.stem],
                        )
                        self.assertTrue(
                            all(len(p["actions"]) == 9 for p in catalog["folders"])
                        )


if __name__ == "__main__":
    unittest.main()
