import hashlib
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

    def test_translation_is_ready_with_ready_context(self):
        result = check_stage(
            "translation", self.root, handoff="handoff.json"
        )
        self.assertEqual("ready", result["status"])

    def test_translation_is_blocked_by_pending_term(self):
        self.write_handoff(
            [{"source": "Text", "target": None, "disposition": "pending"}]
        )
        result = check_stage(
            "translation", self.root, handoff="handoff.json"
        )
        self.assertEqual("blocked", result["status"])
        self.assertEqual("terms_pending", result["context_status"])

    def test_independent_review_returns_draft_hash(self):
        result = check_stage(
            "independent-review",
            self.root,
            handoff="handoff.json",
            translation="translation.md",
            review_notes="review-notes.md",
        )
        self.assertEqual("ready", result["status"])
        expected = hashlib.sha256((self.root / "translation.md").read_bytes()).hexdigest()
        self.assertEqual(expected, result["draft_sha256"])

    def test_independent_review_refuses_existing_output(self):
        (self.root / "review-notes.md").write_text("existing", encoding="utf-8")
        result = check_stage(
            "independent-review",
            self.root,
            handoff="handoff.json",
            translation="translation.md",
            review_notes="review-notes.md",
        )
        self.assertEqual("blocked", result["status"])

    def test_review_complete_accepts_unchanged_draft(self):
        (self.root / "review-notes.md").write_text("reviewed", encoding="utf-8")
        expected = hashlib.sha256((self.root / "translation.md").read_bytes()).hexdigest()
        result = check_stage(
            "review-complete",
            self.root,
            translation="translation.md",
            review_notes="review-notes.md",
            expected_draft_sha256=expected,
        )
        self.assertEqual("ready", result["status"])

    def test_review_complete_blocks_changed_draft(self):
        (self.root / "review-notes.md").write_text("reviewed", encoding="utf-8")
        result = check_stage(
            "review-complete",
            self.root,
            translation="translation.md",
            review_notes="review-notes.md",
            expected_draft_sha256="0" * 64,
        )
        self.assertEqual("blocked", result["status"])

    def test_finalization_requires_both_note_files(self):
        result = check_stage(
            "finalization",
            self.root,
            handoff="handoff.json",
            translation="translation.md",
            drafting_notes="drafting-notes.md",
            review_notes="review-notes.md",
        )
        self.assertEqual("blocked", result["status"])

    def test_finalization_is_ready_with_required_files(self):
        digest = hashlib.sha256((self.root / "translation.md").read_bytes()).hexdigest()
        (self.root / "review-notes.md").write_text(
            "# Review\n\n"
            f"<!-- translation-workbench:draft-sha256-before={digest} -->\n"
            f"<!-- translation-workbench:draft-sha256-after={digest} -->\n",
            encoding="utf-8",
        )
        result = check_stage(
            "finalization",
            self.root,
            handoff="handoff.json",
            translation="translation.md",
            drafting_notes="drafting-notes.md",
            review_notes="review-notes.md",
        )
        self.assertEqual("ready", result["status"])

    def test_finalization_blocks_missing_review_hash_markers(self):
        (self.root / "review-notes.md").write_text("reviewed", encoding="utf-8")
        result = check_stage(
            "finalization",
            self.root,
            handoff="handoff.json",
            translation="translation.md",
            drafting_notes="drafting-notes.md",
            review_notes="review-notes.md",
        )
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
