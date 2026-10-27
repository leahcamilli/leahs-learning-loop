from __future__ import annotations

import unittest

from pathlib import Path
from tempfile import TemporaryDirectory

from build_site import _parse_page, add_related_articles


class RelatedArticlesTests(unittest.TestCase):
    def test_related_articles_prefer_shared_specific_tags(self) -> None:
        articles = [
            {
                "id": "retrieval-one",
                "title": "Building Retrieval Systems",
                "date": "2026-07-16",
                "tags": ["ai", "retrieval", "knowledge-management"],
            },
            {
                "id": "retrieval-two",
                "title": "Practical Knowledge Retrieval",
                "date": "2026-07-15",
                "tags": ["retrieval", "knowledge-management"],
            },
            {
                "id": "unrelated",
                "title": "Power Apps Date Controls",
                "date": "2026-07-14",
                "tags": ["power-apps", "forms"],
            },
        ]
        add_related_articles(articles)
        self.assertEqual(articles[0]["related"][0]["id"], "retrieval-two")

    def test_shared_canonical_topics_link_notes_with_different_tags(self) -> None:
        articles = [
            {"id": "a", "title": "Agent loops", "date": "2026-09-01", "tags": ["agents"], "topics": ["ai-agents"]},
            {"id": "b", "title": "Multi-step tools", "date": "2026-09-02", "tags": ["agentic-ai"], "topics": ["ai-agents"]},
        ]
        add_related_articles(articles)
        self.assertEqual(articles[0]["related"][0]["id"], "b")
        self.assertEqual(articles[0]["related"][0]["shared_tags"], ["ai-agents"])
        self.assertNotIn("unrelated", [item["id"] for item in articles[0]["related"]])


class PageMetadataTests(unittest.TestCase):
    def _parse(self, text: str) -> dict:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "2026-09-22-page.md"
            path.write_text(text, encoding="utf-8")
            return _parse_page(path)

    def test_video_time_and_tldr_are_exposed(self) -> None:
        page = self._parse(
            '---\ntitle: "Video"\nsource: "https://youtu.be/abc"\ndate: "2026-09-22"\n'
            'tags: [x]\nchannel: "Chan"\nduration_seconds: 1843\n---\n\n'
            "## TL;DR\n\n> Short answer\n> continues.\n\n## Overview\nBody."
        )
        self.assertEqual(page["source_type"], "youtube")
        self.assertEqual(page["channel"], "Chan")
        self.assertEqual(page["minutes"], 30.7)
        self.assertFalse(page["minutes_estimated"])
        self.assertEqual(page["tldr"], "Short answer continues.")

    def test_article_reading_time_is_estimated_from_captured_text(self) -> None:
        page = self._parse(
            '---\ntitle: "Post"\nsource: "https://example.com/p"\ndate: "2026-09-22"\n'
            "tags: []\nsource_type: \"web\"\nsource_characters: 13000\n---\n\n## Overview\nBody."
        )
        self.assertEqual(page["minutes"], 10.0)
        self.assertTrue(page["minutes_estimated"])
        self.assertEqual(page["tldr"], "")

    def test_jev_profile_fields_are_exposed(self) -> None:
        page = self._parse(
            '---\ntitle: "P"\nsource: "https://example.com/p"\ntags: [llms]\n'
            'topics: [ai-agents, mcp]\nkind: "tutorial"\ndepth: 2\nactionability: 3\n---\n\nBody.'
        )
        self.assertEqual(page["topics"], ["ai-agents", "mcp"])
        self.assertEqual((page["kind"], page["depth"], page["actionability"]), ("tutorial", 2, 3))

    def test_video_without_length_has_unknown_time(self) -> None:
        page = self._parse(
            '---\ntitle: "Video"\nsource: "https://www.youtube.com/watch?v=abc"\n---\n\nBody.'
        )
        self.assertIsNone(page["minutes"])


if __name__ == "__main__":
    unittest.main()

