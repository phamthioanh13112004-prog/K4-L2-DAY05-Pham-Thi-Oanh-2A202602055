"""The released reference package cannot add or overwrite arbitrary repo files."""

import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.install_reference import expected_files, install


class InstallReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for tier, stems in (("easy_semantic", ("easy1", "easy2", "easy3")),
                            ("hard_panoptic", ("hard1", "hard2"))):
            images = self.root / "data" / "tiers" / tier / "images"
            images.mkdir(parents=True)
            for stem in stems:
                (images / f"{stem}.jpg").touch()
        self.members = {
            name: (b"\x89PNG\r\n\x1a\n" if name.endswith(".png") else json.dumps({}).encode())
            for name in expected_files(self.root)
        }

    def _zip(self, members):
        path = self.root / "reference.zip"
        with zipfile.ZipFile(path, "w") as archive:
            for name, data in members.items():
                archive.writestr(name, data)
        return path

    def test_installs_only_complete_expected_package(self):
        installed = install(self._zip(self.members), self.root)
        self.assertEqual(len(installed), 7)
        self.assertTrue(all(path.is_file() for path in installed))

    def test_rejects_missing_or_extra_file_before_writing(self):
        missing = dict(self.members)
        missing.pop(next(iter(missing)))
        with self.assertRaisesRegex(ValueError, "exactly the seven"):
            install(self._zip(missing), self.root)
        self.assertFalse(list(self.root.rglob("groundtruth")))
        extra = dict(self.members)
        extra["data/tiers/easy_semantic/groundtruth/other.png"] = b"\x89PNG\r\n\x1a\n"
        with self.assertRaisesRegex(ValueError, "exactly the seven"):
            install(self._zip(extra), self.root)

    def test_refuses_to_overwrite_existing_reference(self):
        name = next(iter(self.members))
        target = self.root / name
        target.parent.mkdir(parents=True)
        target.write_bytes(b"keep")
        with self.assertRaisesRegex(ValueError, "Refusing to overwrite"):
            install(self._zip(self.members), self.root)
        self.assertEqual(target.read_bytes(), b"keep")


if __name__ == "__main__":
    unittest.main()
