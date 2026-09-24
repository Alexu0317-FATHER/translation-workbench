import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from check_stage import check_stage


class StageCheckerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "source.md").write_text("# Source\n\nText.\n", encoding="utf-8")
        (self.root / "translation.md").write_text(
            "# Translation\n\n译文。\n", encoding="utf-8"
        )
        (self.root / "initial-draft.md").write_bytes(
            (self.root / "translation.md").read_bytes()
        )
        (self.root / "drafting-notes.md").write_text(
            "# Drafting notes\n\nNo open issues.\n", encoding="utf-8"
        )
        self.handoff_path = self.root / "handoff.json"
        self.write_handoff([])

    def tearDown(self):
        self.temp.cleanup()

    def write_handoff(self, terms):
        data = {
            "schema_version": 1,
            "material_complete": True,
            "translation_unit": {
                "project": "Test",
                "id": "unit-1",
                "source_language": "English",
                "target_language": "Chinese",
            },
            "source": {"original": "local", "path": "source.md", "verified": True},
            "glossary": None,
            "context_to_read": [],
            "terms": terms,
            "warnings": [],
        }
        self.handoff_path.write_text(json.dumps(data), encoding="utf-8")

    def finalization(self, **overrides):
        args = {
            "handoff": "handoff.json",
            "translation": "translation.md",
            "initial_draft": "initial-draft.md",
            "drafting_notes": "drafting-notes.md",
            "review_notes": "review-notes.md",
        }
        args.update(overrides)
        return check_stage("finalization", self.root, **args)

    def test_translation_is_ready_with_ready_context(self):
        result = check_stage("translation", self.root, handoff="handoff.json")
        self.assertEqual("ready", result["status"])

    def test_translation_is_blocked_by_pending_term(self):
        self.write_handoff(
            [{"source": "Text", "target": None, "disposition": "pending"}]
        )
        result = check_stage("translation", self.root, handoff="handoff.json")
        self.assertEqual("blocked", result["status"])
        self.assertEqual("terms_pending", result["context_status"])

    def test_finalization_starts_without_prior_review(self):
        result = self.finalization()
        self.assertEqual("ready", result["status"])

    def test_finalization_requires_retrievable_initial_draft(self):
        (self.root / "initial-draft.md").unlink()
        result = self.finalization()
        self.assertEqual("blocked", result["status"])

    def test_finalization_rejects_changed_draft_at_start(self):
        (self.root / "translation.md").write_text("Edited already", encoding="utf-8")
        result = self.finalization()
        self.assertEqual("blocked", result["status"])
        self.assertIn("initial draft unchanged", [c["name"] for c in result["checks"] if not c["ok"]])

    def test_finalization_protects_existing_review_record(self):
        (self.root / "review-notes.md").write_text("existing", encoding="utf-8")
        result = self.finalization()
        self.assertEqual("blocked", result["status"])

    def test_finalization_can_resume_after_working_translation_changes(self):
        (self.root / "review-notes.md").write_text("decisions", encoding="utf-8")
        (self.root / "translation.md").write_text("Edited from decisions", encoding="utf-8")
        result = self.finalization(resume=True)
        self.assertEqual("ready", result["status"])

    def test_finalization_resume_requires_existing_record(self):
        result = self.finalization(resume=True)
        self.assertEqual("blocked", result["status"])

    def test_snapshot_must_be_a_separate_file(self):
        result = self.finalization(initial_draft="translation.md")
        self.assertEqual("blocked", result["status"])

    def test_cli_uses_blocked_exit_code(self):
        self.write_handoff(
            [{"source": "Text", "target": None, "disposition": "pending"}]
        )
        completed = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).with_name("check_stage.py")),
                "translation",
                "--project-root",
                str(self.root),
                "--handoff",
                str(self.handoff_path),
            ],
            check=False,
            capture_output=True,
        )
        self.assertEqual(2, completed.returncode, completed.stderr.decode())
        payload = json.loads(completed.stdout.decode("utf-8"))
        self.assertEqual("blocked", payload["status"])


if __name__ == "__main__":
    unittest.main()
