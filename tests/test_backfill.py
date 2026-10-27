from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from ingest import backfill
from ingest.youtube import VideoEvidence


SUMMARY = {
    "tldr": "Small outputs make judgment cheap.",
    "key_takeaways": ["First.", "Second."],
    "key_moments": [{"timestamp": "1:05", "label": "The key demo"}],
    "review_questions": [{"question": "Why?", "answer": "Because."}],
}

LEGACY = """# Old Lesson

Date: 2026-04-20
Source: personal notes
Tags: ai, agents

## Overview
Body.

## Further Reading
- [Link](https://example.com)

## Personal Notes
Forwarded email
Source: https://youtu.be/abc123?si=x
"""


# Keep these tests hermetic even when the host's .env.local holds a real TypeSafe key.
_no_jev = patch("ingest.config.TYPESAFE_API_KEY", "")


def setUpModule() -> None:
    _no_jev.start()


def tearDownModule() -> None:
    _no_jev.stop()

class BackfillTests(unittest.TestCase):
    def test_legacy_page_becomes_frontmatter(self) -> None:
        page = backfill.parse_page(Path("2026-04-20-old.md"), LEGACY)
        self.assertEqual(page.get("title"), "Old Lesson")
        self.assertEqual(page.get("date"), "2026-04-20")
        self.assertEqual(page.get("tags"), "[ai, agents]")
        self.assertTrue(page.body.startswith("## Overview"))

    @patch("ingest.backfill._summarize", return_value=dict(SUMMARY))
    @patch("ingest.youtube.fetch_video")
    def test_upgrade_recovers_source_and_adds_video_metadata(self, fetch_video, summarize) -> None:
        fetch_video.return_value = VideoEvidence(
            transcript="[1:05] demo", metadata={"duration_seconds": 600, "channel": "Chan"}
        )
        page = backfill.parse_page(Path("2026-04-20-old.md"), LEGACY)
        changes = backfill.upgrade_page(page, metadata=True, summaries=True, use_transcripts=True)

        self.assertEqual(page.get("source"), "https://www.youtube.com/watch?v=abc123")
        self.assertEqual(page.get("source_type"), "youtube")
        self.assertEqual(page.get("duration_seconds"), "600")
        self.assertEqual(page.get("channel"), "Chan")
        self.assertIn("summary+moments", changes)
        self.assertEqual(summarize.call_args.args[1], "[1:05] demo")
        body = page.body
        self.assertTrue(body.startswith("## TL;DR"))
        self.assertIn("https://www.youtube.com/watch?v=abc123&t=65s", body)
        self.assertLess(body.index("## Test Yourself"), body.index("## Further Reading"))
        self.assertLess(body.index("## Further Reading"), body.index("## Personal Notes"))

    @patch("ingest.youtube.fetch_video_metadata", return_value={"duration_seconds": 42})
    def test_metadata_only_run_is_idempotent(self, _metadata) -> None:
        with TemporaryDirectory() as directory:
            pages = Path(directory)
            page = pages / "2026-09-01-video.md"
            page.write_text(
                '---\ntitle: "Video"\nsource: "https://www.youtube.com/watch?v=abc123"\n'
                'date: "2026-09-01"\ntags: [x]\nsource_type: "youtube"\n---\n\n## Overview\nBody.\n',
                encoding="utf-8",
            )
            with patch.object(backfill, "PAGES_DIR", pages):
                kwargs = dict(metadata=True, summaries=False, use_transcripts=False,
                              limit=0, match="", dry_run=False, pause=0)
                backfill.run(**kwargs)
                first = page.read_text(encoding="utf-8")
                backfill.run(**kwargs)
            self.assertIn("duration_seconds: 42", first)
            self.assertEqual(first, page.read_text(encoding="utf-8"))
            self.assertEqual(_metadata.call_count, 1)

    def test_summary_without_transcript_drops_moments(self) -> None:
        page = backfill.parse_page(
            Path("2026-09-01-web.md"),
            '---\ntitle: "Web"\nsource: "https://example.com/a"\n---\n\n## Overview\nBody.',
        )
        with patch("ingest.codex.run_codex_structured", return_value=dict(SUMMARY)):
            backfill.upgrade_page(page, metadata=True, summaries=True, use_transcripts=True)
        self.assertEqual(page.get("source_type"), "web")
        self.assertIn("## Key Takeaways", page.body)
        self.assertNotIn("## Key Moments", page.body)


if __name__ == "__main__":
    unittest.main()
