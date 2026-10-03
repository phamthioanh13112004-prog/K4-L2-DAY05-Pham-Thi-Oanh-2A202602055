"""A learner checkout must never emit a grade without protected references."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
HAS_SCORING_DEPS = all(importlib.util.find_spec(name) for name in ("numpy", "PIL", "pycocotools"))


@unittest.skipUnless(HAS_SCORING_DEPS, "Install optional scoring dependencies from requirements.txt")
class ScoringReferenceGate(unittest.TestCase):
    def test_one_task_refuses_to_score_without_reference(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scoring" / "score.py"), "easy_semantic", "missing.zip"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Protected reference missing", result.stderr)
        self.assertNotIn("points:", result.stdout)

    def test_scorecard_does_not_write_zero_grade_without_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            submissions = base / "submissions"
            submissions.mkdir()
            (submissions / "easy_semantic.zip").touch()
            output = base / "reports"
            result = subprocess.run(
                [sys.executable, str(ROOT / "scoring" / "scorecard.py"),
                 "--dir", str(submissions), "--out", str(output)],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Protected reference missing", result.stderr)
            self.assertFalse(output.exists())

    def test_tiers_scorecard_ignores_checkpoint_exports_and_caps_at_82(self):
        from scoring import scorecard

        registry = {
            "easy_semantic": {"_group": "tiers", "type": "semantic", "weight": 20},
            "medium_instance": {"_group": "tiers", "type": "instance", "weight": 32},
            "hard_panoptic": {"_group": "tiers", "type": "panoptic", "weight": 30},
            "cp1_holes": {"_group": "checkpoints", "type": "instance", "weight": 3},
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            submissions = root / "submissions"
            submissions.mkdir()
            (submissions / "easy_semantic.zip").touch()
            (submissions / "cp1_holes.zip").touch()
            with (mock.patch.object(scorecard, "ROOT", root),
                  mock.patch.object(scorecard, "load_registry", return_value=registry),
                  mock.patch.object(scorecard, "resolve_task", return_value=(
                      {"type": "semantic"}, root / "data" / "tiers" / "easy_semantic", {})),
                  mock.patch.object(scorecard, "require_reference"),
                  mock.patch.object(scorecard, "_guard_match"),
                  mock.patch.object(scorecard, "score_one", return_value={
                      "type": "semantic", "group": "tiers", "weight": 20,
                      "points": 12.0, "value": 0.7, "flags": []}) as scorer,
                  mock.patch.object(sys, "argv", ["scorecard.py", "--group", "tiers",
                                                  "--out", "reports/tiers"])):
                scorecard.main()
            import json
            result = json.loads((root / "reports" / "tiers" / "scorecard.json").read_text())
            self.assertEqual(result["max"], 82)
            self.assertEqual(result["group"], "tiers")
            self.assertEqual(result["total"], 12.0)
            self.assertEqual(len(result["tasks"]), 3)
            scorer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
