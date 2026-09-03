import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from check_translation_context import check_context


class TranslationContextTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "source.md").write_text(
            "# A Crossing\n\nAlice reached Moonfall before dawn.\n",
            encoding="utf-8",
        )
        (self.root / "glossary.md").write_text(
            "# Glossary\n\n| Source term | Target term | Scope | Notes |\n"
            "|---|---|---|---|\n"
            "| Moonfall | 月落城 | project | approved |\n",
            encoding="utf-8",
        )
        (self.root / "characters.md").write_text(
            "# Characters\n\n## Alice\n\n### Voice\n\nMeasured and direct.\n"
            "\n## Bob\n\nQuiet.\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def handoff(self, **updates):
        data = {
            "schema_version": 1,
            "material_complete": True,
            "translation_unit": {
                "project": "Test",
                "work": "Sample",
                "id": "crossing",
                "source_language": "English",
                "target_language": "Chinese",
            },
            "source": {
                "original": "local source",
                "path": "source.md",
                "verified": True,
            },
            "glossary": "glossary.md",
            "context_to_read": [
                {"role": "character", "path": "characters.md", "section": "Alice"}
            ],
            "terms": [],
            "warnings": [],
        }
        data.update(updates)
        path = self.root / "handoff.json"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return path

    def test_ready_and_extracts_exact_section(self):
        result = check_context(self.root, self.handoff())
        self.assertEqual("ready", result["status"])
        self.assertEqual(1, len(result["context"]))
        self.assertIn("## Alice", result["context"][0]["content"])
        self.assertNotIn("## Bob", result["context"][0]["content"])

    def test_pending_term_blocks_translation_readiness(self):
        path = self.handoff(
            terms=[{"source": "Moonfall", "target": None, "disposition": "pending"}]
        )
        result = check_context(self.root, path)
        self.assertEqual("terms_pending", result["status"])
        self.assertEqual(3, result["terms"][0]["occurrences"][0]["line"])

    def test_approved_glossary_term_is_verified(self):
        path = self.handoff(
            terms=[
                {"source": "Moonfall", "target": "月落城", "disposition": "glossary"}
            ]
        )
        result = check_context(self.root, path)
        self.assertEqual("ready", result["status"])
        self.assertEqual("present", result["terms"][0]["glossary_status"])

    def test_glossary_target_mismatch_is_error(self):
        path = self.handoff(
            terms=[
                {"source": "Moonfall", "target": "月坠城", "disposition": "glossary"}
            ]
        )
        result = check_context(self.root, path)
        self.assertEqual("error", result["status"])
        self.assertTrue(any("mismatch" in item for item in result["errors"]))

    def test_material_incomplete_is_normal_status(self):
        result = check_context(self.root, self.handoff(material_complete=False))
        self.assertEqual("material_incomplete", result["status"])
        self.assertEqual([], result["errors"])

    def test_missing_context_section_is_error(self):
        path = self.handoff(
            context_to_read=[
                {"role": "character", "path": "characters.md", "section": "Nobody"}
            ]
        )
        result = check_context(self.root, path)
        self.assertEqual("error", result["status"])
        self.assertTrue(any("Section not found" in item for item in result["errors"]))

    def test_term_absent_from_source_is_warning(self):
        path = self.handoff(
            terms=[{"source": "Elsewhere", "target": "别处", "disposition": "unit_only"}]
        )
        result = check_context(self.root, path)
        self.assertEqual("ready", result["status"])
        self.assertTrue(any("Term not found" in item for item in result["warnings"]))

    def test_invalid_json_is_error(self):
        path = self.root / "bad.json"
        path.write_text("{", encoding="utf-8")
        result = check_context(self.root, path)
        self.assertEqual("error", result["status"])
        self.assertTrue(result["errors"])

    def test_cli_emits_ready_json(self):
        path = self.handoff()
        completed = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).with_name("check_translation_context.py")),
                "--project-root",
                str(self.root),
                "--handoff",
                str(path),
            ],
            check=False,
            capture_output=True,
        )
        self.assertEqual(0, completed.returncode, completed.stderr.decode())
        payload = json.loads(completed.stdout.decode("utf-8"))
        self.assertEqual("ready", payload["status"])


if __name__ == "__main__":
    unittest.main()
