"""Structural checks for the learner-facing Day 5 repository."""

import html.parser
import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_COUNTS = {
    "easy_semantic": 3,
    "medium_instance": 3,
    "hard_panoptic": 2,
    "cp1_holes": 1,
    "cp2_slice": 1,
    "cp5_occlusion": 1,
    "cp3_thin": 1,
    "cp4_curb": 1,
    "cp6_coverage": 1,
}


class LocalReferences(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"href", "src"} and value:
                if not value.startswith(("#", "http:", "https:")):
                    self.references.append(value.split("#", 1)[0])


class ReleaseContract(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / "data" / "manifest.json").read_text())

    def test_starter_tasks_and_weights_are_preserved(self):
        tasks = self.manifest["tasks"]
        self.assertEqual(set(tasks), set(EXPECTED_COUNTS))
        self.assertEqual(sum(info["weight"] for info in tasks.values()), 100)
        self.assertEqual(tasks["easy_semantic"]["weight"], 20)
        self.assertEqual(tasks["medium_instance"]["weight"], 32)
        self.assertEqual(tasks["hard_panoptic"]["weight"], 30)

    def test_images_and_classes_are_present(self):
        for name, count in EXPECTED_COUNTS.items():
            base = ROOT / "data" / self.manifest["tasks"][name]["path"]
            self.assertEqual(len(list((base / "images").glob("*.jpg"))), count, name)
            self.assertTrue((base / "classes.json").is_file(), name)

    def test_cvat_raw_labels_match_starter_classes(self):
        for name in EXPECTED_COUNTS:
            base = ROOT / "data" / self.manifest["tasks"][name]["path"]
            metadata = json.loads((base / "classes.json").read_text(encoding="utf-8"))
            labels = json.loads((base / "cvat-labels.json").read_text(encoding="utf-8"))
            self.assertEqual([label["name"] for label in labels], metadata["classes"], name)
            for label in labels:
                self.assertEqual(set(label), {"name", "color", "type", "attributes"}, name)
                self.assertEqual(label["type"], "any", name)
                self.assertEqual(label["attributes"], [], name)
                self.assertRegex(label["color"], r"^#[0-9a-f]{6}$", name)
                if label["name"] in metadata.get("colors", {}):
                    rgb = metadata["colors"][label["name"]]
                    self.assertEqual(label["color"], "#{:02x}{:02x}{:02x}".format(*rgb), name)

    def test_no_reference_answers_are_shipped(self):
        self.assertFalse(list(ROOT.rglob("groundtruth")))
        self.assertFalse(list(ROOT.rglob("instances-golden.json")))

    def test_html_local_assets_exist(self):
        parser = LocalReferences()
        parser.feed((ROOT / "lab-guide.html").read_text())
        self.assertTrue(parser.references)
        for reference in parser.references:
            self.assertTrue((ROOT / reference).is_file(), reference)

    def test_cvat_screenshot_extensions_match_image_data(self):
        screenshots = list((ROOT / "docs" / "images").iterdir())
        self.assertTrue(screenshots)
        for path in screenshots:
            signature = path.read_bytes()[:8]
            if path.suffix == ".png":
                self.assertEqual(signature, b"\x89PNG\r\n\x1a\n", path.name)
            elif path.suffix == ".jpg":
                self.assertTrue(signature.startswith(b"\xff\xd8\xff"), path.name)
            else:
                self.fail(f"Unexpected screenshot type: {path.name}")

    def test_report_uses_same_score_weights(self):
        for path in (ROOT / "REPORT.md", ROOT / "reports" / "REPORT_TEMPLATE.md"):
            report = path.read_text()
            for row in ("| easy_semantic |", "| medium_instance |", "| hard_panoptic |"):
                self.assertIn(row, report, path.name)
            self.assertIn("**100**", report, path.name)

    def test_report_keeps_four_evidence_sections_and_explains_them(self):
        report = (ROOT / "reports" / "REPORT_TEMPLATE.md").read_text()
        headings = (
            "## 1. Bài đã nộp",
            "## 2. Một quyết định trước khi dùng gợi ý",
            "## 3. Một lỗi tôi tìm thấy và sửa",
            "## 4. Ba ca chưa chắc hoặc đã cân nhắc",
        )
        for heading in headings:
            self.assertIn(heading, report)
            self.assertIn(heading, (ROOT / "REPORT.md").read_text())
        self.assertIn("Bạn cần điền gì?", report)
        self.assertIn("Ví dụ cách giải thích", report)

    def test_visual_guide_covers_starter_and_not_pilot_task_names(self):
        guide = (ROOT / "lab-guide.html").read_text()
        for name in EXPECTED_COUNTS:
            self.assertIn(name, guide)
        self.assertNotIn("D05-MANUAL", guide)
        self.assertIn("data-lightbox", guide)
        self.assertIn("data-progress-label", guide)

    def test_fork_submission_route_is_consistent(self):
        for name in ("README.md", "GUIDE.md", "RUBRIC.md", "docs/SUBMISSION.md", "lab-guide.html"):
            content = (ROOT / name).read_text()
            self.assertIn("24 giờ", content, name)
            self.assertIn("VLearn", content, name)
        self.assertTrue((ROOT / "submissions" / ".gitkeep").is_file())
        ignore = (ROOT / ".gitignore").read_text()
        self.assertNotIn("submissions/", ignore)
        self.assertNotIn("REPORT.md", ignore)
        self.assertNotIn("*.zip", ignore.replace("/*.zip", ""))

    def test_single_notebook_is_valid_and_compiles(self):
        notebooks = sorted((ROOT / "notebooks").glob("*.ipynb"))
        self.assertEqual([path.name for path in notebooks], ["day5-segmentation-tu-kiem.ipynb"])
        for path in notebooks:
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(payload["nbformat"], 4, path.name)
            self.assertTrue(payload["cells"], path.name)
            joined = "\n".join("".join(cell["source"]) for cell in payload["cells"])
            self.assertIn('FORK_URL = ""', joined)
            self.assertIn("UPLOAD_ZIPS = False", joined)
            self.assertIn("BƯỚC 0 · Thư viện cần dùng", joined)
            self.assertIn('"-m", "pip", "install", "IPython"', joined)
            self.assertIn("Không cài `requirements.txt`", joined)
            self.assertIn("Nếu gặp lỗi, làm gì?", joined)
            self.assertEqual(joined.count("from inspect_submissions import task_registry"), 1)
            for cell in payload["cells"]:
                if cell["cell_type"] == "code":
                    compile("".join(cell["source"]), path.name, "exec")

    def test_notebook_install_step_skips_existing_ipython_and_handles_missing(self):
        path = ROOT / "notebooks" / "day5-segmentation-tu-kiem.ipynb"
        payload = json.loads(path.read_text(encoding="utf-8"))
        code_cells = ["".join(cell["source"]) for cell in payload["cells"] if cell["cell_type"] == "code"]
        install_cell = next(source for source in code_cells if "BƯỚC 0 — kiểm tra môi trường" in source)
        with patch("importlib.util.find_spec", return_value=object()), patch("subprocess.run") as run:
            with redirect_stdout(io.StringIO()) as output:
                exec(install_cell, {})
            self.assertIn("SẴN SÀNG", output.getvalue())
            run.assert_not_called()
        with patch("importlib.util.find_spec", return_value=None), patch("subprocess.run") as run:
            with redirect_stdout(io.StringIO()):
                exec(install_cell, {})
            self.assertEqual(run.call_args.args[0][-2:], ["install", "IPython"])


if __name__ == "__main__":
    unittest.main()
