"""Export QC and hand-in packaging contract using synthetic CVAT-shaped ZIPs."""

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from inspect_submissions import expected_for, inspect_all, inspect_task, task_registry  # noqa: E402
from package_submission import package  # noqa: E402


class ExportWorkflow(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.exports = self.base / "submissions"
        self.exports.mkdir()

    def _zip(self, name, members):
        path = self.exports / f"{name}.zip"
        with zipfile.ZipFile(path, "w") as archive:
            for key, content in members.items():
                archive.writestr(key, content)
        return path

    def _semantic(self, name="easy_semantic", mask_names=None):
        info = task_registry()[name]
        images, classes = expected_for(name, info)
        names = images if mask_names is None else mask_names
        members = {"labelmap.txt": "\n".join(f"{cls}:1,2,3::" for cls in classes)}
        members.update({f"SegmentationClass/{Path(image).stem}.png": b"\x89PNG\r\n\x1a\n" for image in names})
        return self._zip(name, members)

    def _coco(self, name="medium_instance", missing_image=False, bad_seg=False):
        info = task_registry()[name]
        images, classes = expected_for(name, info)
        names = sorted(images)
        if missing_image:
            names.pop()
        payload = {"images": [{"id": i, "file_name": filename, "height": 50, "width": 50}
                              for i, filename in enumerate(names, 1)],
                   "categories": [{"id": 1, "name": sorted(classes)[0]}],
                   "annotations": [{"id": 1, "image_id": 1, "category_id": 1,
                                    "segmentation": [] if bad_seg else [[1, 1, 10, 1, 10, 10]]}]}
        return self._zip(name, {"annotations/instances_default.json": json.dumps(payload)})

    def test_semantic_happy_path_and_missing_image(self):
        self._semantic()
        self.assertEqual(inspect_task("easy_semantic", self.exports / "easy_semantic.zip")["errors"], [])
        self._semantic(mask_names={"wrong.jpg"})
        result = inspect_task("easy_semantic", self.exports / "easy_semantic.zip")
        self.assertTrue(any("thiếu mask ảnh" in issue for issue in result["errors"]))
        self.assertTrue(any("không thuộc task" in issue for issue in result["errors"]))

    def test_coco_polygon_and_rle_contract(self):
        self._coco()
        result = inspect_task("medium_instance", self.exports / "medium_instance.zip")
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["details"]["segmentation_kinds"], {"polygon": 1})
        self._coco(bad_seg=True)
        result = inspect_task("medium_instance", self.exports / "medium_instance.zip")
        self.assertTrue(any("polygon/RLE" in issue for issue in result["errors"]))
        self._coco(missing_image=True)
        result = inspect_task("medium_instance", self.exports / "medium_instance.zip")
        self.assertTrue(any("thiếu ảnh" in issue for issue in result["errors"]))

    def test_coco_rle_and_malformed_id(self):
        path = self._coco()
        with zipfile.ZipFile(path) as archive:
            payload = json.loads(archive.read("annotations/instances_default.json"))
        payload["annotations"][0]["segmentation"] = {"size": [50, 50], "counts": [10, 20, 2470]}
        self._zip("medium_instance", {"annotations/instances_default.json": json.dumps(payload)})
        result = inspect_task("medium_instance", path)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["details"]["segmentation_kinds"], {"RLE": 1})
        payload["annotations"][0]["image_id"] = []
        self._zip("medium_instance", {"annotations/instances_default.json": json.dumps(payload)})
        result = inspect_task("medium_instance", path)
        self.assertTrue(any("id không hợp lệ" in issue for issue in result["errors"]))

    def test_rejects_unsafe_zip_member(self):
        self._zip("easy_semantic", {"../bad.txt": "hello"})
        result = inspect_task("easy_semantic", self.exports / "easy_semantic.zip")
        self.assertTrue(any("không an toàn" in issue for issue in result["errors"]))

    def test_partial_package_contains_report_exports_and_hashes(self):
        self._semantic()
        report = self.base / "REPORT.md"
        report.write_text("# Báo cáo\n")
        output = self.base / "day5-D5_012.zip"
        manifest = package(self.exports, report, output, "D5_012")
        self.assertIn("easy_semantic", manifest["tasks_present"])
        self.assertIn("hard_panoptic", manifest["tasks_missing"])
        with zipfile.ZipFile(output) as archive:
            self.assertEqual(set(archive.namelist()), {"REPORT.md", "exports/easy_semantic.zip", "manifest.json"})
            self.assertEqual(json.loads(archive.read("manifest.json"))["learner_id"], "D5_012")

    def test_all_task_contracts_are_visible(self):
        report = inspect_all(self.exports)
        self.assertEqual(len(report["tasks"]), 9)
        self.assertEqual(report["missing_count"], 9)
        self.assertEqual(report["error_count"], 0)


if __name__ == "__main__":
    unittest.main()
