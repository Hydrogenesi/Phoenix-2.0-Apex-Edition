import re
import unittest
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
CODEX = ROOT / "docs" / "codex"
BOOK_DIRS = sorted(CODEX.glob("Book*"))
WORD_RE = re.compile(r"\b\w+[\w'’\-]*\b")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class CodexStructureTests(unittest.TestCase):
    def test_master_index_and_book_count(self):
        self.assertTrue((CODEX / "INDEX.md").exists())
        self.assertEqual(len(BOOK_DIRS), 13)

    def test_chapter_totals_match_declared_counts(self):
        total = 0
        for book_dir in BOOK_DIRS:
            schema = json.loads((book_dir / "schema.json").read_text(encoding="utf-8"))
            chapters = sorted((book_dir / "chapters").glob("ch*.md"))
            self.assertEqual(schema["chapters"], len(chapters), book_dir.name)
            self.assertEqual(schema["content_status"], "complete")
            total += len(chapters)
        self.assertEqual(total, 306)

    def test_chapters_have_required_sections_and_word_counts(self):
        required_sections = [
            "# ",
            "## Overview",
            "## Key Concepts",
            "## Framework Integration",
            "## Core Content",
            "### Tri-Column Harmony",
            "### Mathematical Formulation",
            "### Practical Application",
            "### Invocation Sequence",
            "## Cross-References",
            "## Summary",
        ]
        for chapter in CODEX.glob("Book*/chapters/ch*.md"):
            text = chapter.read_text(encoding="utf-8")
            word_count = len(WORD_RE.findall(text))
            self.assertGreaterEqual(word_count, 800, chapter.as_posix())
            self.assertLessEqual(word_count, 1200, chapter.as_posix())
            for section in required_sections:
                self.assertIn(section, text, f"{section} missing from {chapter}")

    def test_relative_links_resolve(self):
        for markdown_file in list(CODEX.glob("INDEX.md")) + list(CODEX.glob("Book*/INDEX.md")) + list(CODEX.glob("Book*/chapters/ch*.md")):
            text = markdown_file.read_text(encoding="utf-8")
            for target in LINK_RE.findall(text):
                if target.startswith("http"):
                    continue
                resolved = (markdown_file.parent / target).resolve()
                self.assertTrue(resolved.exists(), f"Broken link in {markdown_file}: {target}")

    def test_docs_entrypoints_exist(self):
        self.assertTrue((ROOT / "docs" / "index.md").exists())
        self.assertTrue((ROOT / "mkdocs.yml").exists())


if __name__ == "__main__":
    unittest.main()
