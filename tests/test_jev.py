from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from ingest import backfill, jev
from ingest.lesson import render_markdown
from ingest.sources import FetchedSource, SourceQualityError, judge_source
from ingest.topics import TOPICS


TRANSCRIPT = "\n".join(
    [
        "[0:00] Welcome, today we look at classifiers.",
        "[0:30] A classifier picks from a few fixed outcomes.",
        "[2:10] Here is the routing demo for support tickets.",
        "[5:00] Pricing is about a tenth of an LLM call.",
    ]
)


def _lesson() -> dict:
    return {
        "title": "Classifiers",
        "tldr": "Use classifiers for bounded choices.",
        "overview": "Overview.",
        "key_concepts": [{"name": "Routing", "explanation": "..."}],
        "key_takeaways": ["Classifiers pick fixed outcomes.", "They cure cancer.", "  "],
        "key_moments": [
            {"timestamp": "2:10", "label": "Routing demo"},
            {"timestamp": "0:30", "label": "Unrelated label"},
            {"timestamp": "59:00", "label": "Beyond the transcript"},
        ],
    }


def _answers(**overrides) -> dict:
    answers = {jev._key("topic", slug): {"type": "noul", "noul": 0.1} for slug in TOPICS}
    answers[jev._key("topic", "classifiers-and-structured-output")] = {"type": "noul", "noul": 0.93}
    answers[jev._key("topic", "ai-agents")] = {"type": "noul", "noul": 0.55}
    answers["kind"] = {"type": "choice", "choice": "tutorial", "confidence": 0.8, "probabilities": {}}
    answers["depth"] = {"type": "score", "score": 1.6, "confidence": 0.7, "legend": {}, "probabilities": {}}
    answers["actionability"] = {"type": "score", "score": 2.4, "confidence": 0.7, "legend": {}, "probabilities": {}}
    answers["takeaway_0"] = {"type": "noul", "noul": 0.97}
    answers["takeaway_1"] = {"type": "noul", "noul": 0.02}
    answers["moment_0"] = {"type": "noul", "noul": 0.9}
    answers["moment_1"] = {"type": "noul", "noul": 0.1}
    answers.update(overrides)
    return answers


def _response(status: int, payload: dict | None = None, headers: dict | None = None) -> MagicMock:
    response = MagicMock(status_code=status, headers=headers or {}, text="error body")
    response.json.return_value = payload or {}
    return response


@patch("ingest.jev.config.TYPESAFE_API_KEY", "test-key")
class JevTransportTests(unittest.TestCase):
    @patch("ingest.jev.time.sleep")
    @patch("ingest.jev.requests.post")
    def test_ask_retries_rate_limits_and_sends_contract(self, post, sleep) -> None:
        post.side_effect = [
            _response(429, headers={"retry-after": "1"}),
            _response(200, {"model": "jev", "answers": {"q": {"type": "noul", "noul": 0.9}}, "usage": {}}),
        ]
        answers = jev.ask({"text": "hi"}, {"q": jev.noul("Is it?")})
        self.assertEqual(answers["q"]["noul"], 0.9)
        sleep.assert_called_once_with(1.0)
        url, kwargs = post.call_args.args[0], post.call_args.kwargs
        self.assertTrue(url.endswith("/v1/systemone"))
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer test-key")
        self.assertEqual(kwargs["json"]["model"], "jev-latest")
        self.assertEqual(kwargs["json"]["questions"]["q"], {"type": "noul", "instructions": "Is it?"})

    @patch("ingest.jev.requests.post", return_value=_response(422))
    def test_ask_raises_on_client_error_without_retry(self, post) -> None:
        with self.assertRaises(jev.JevError):
            jev.ask("state", {"q": jev.noul("Is it?")})
        self.assertEqual(post.call_count, 1)


@patch("ingest.jev.config.TYPESAFE_API_KEY", "test-key")
class JevReviewTests(unittest.TestCase):
    def test_request_grounds_takeaways_and_moments_with_transcript_windows(self) -> None:
        state, questions = jev.build_review_request(_lesson(), source_text=TRANSCRIPT, transcript=TRANSCRIPT)
        self.assertEqual(state["takeaways"], ["Classifiers pick fixed outcomes.", "They cure cancer."])
        self.assertEqual(len(state["moments"]), 2)  # 59:00 has no transcript window
        self.assertIn("[2:10] Here is the routing demo", state["moments"][0]["transcript_excerpt"])
        self.assertNotIn("[5:00]", state["moments"][1]["transcript_excerpt"])
        self.assertEqual(len([q for q in questions if q.startswith("topic_")]), len(TOPICS))
        self.assertEqual(questions["depth"]["type"], "score")
        self.assertEqual(len(questions["depth"]["criteria"]), 4)
        self.assertEqual(set(questions["kind"]["criteria"]), set(jev.KINDS))
        self.assertIn("takeaway_1", questions)
        self.assertTrue(all(q.replace("_", "").isalnum() for q in questions))

    def test_oversized_source_is_not_used_for_grounding(self) -> None:
        with patch("ingest.jev.config.JEV_MAX_SOURCE_CHARS", 10):
            state, questions = jev.build_review_request(_lesson(), source_text=TRANSCRIPT)
        self.assertNotIn("takeaways", state)
        self.assertFalse(any(q.startswith("takeaway_") for q in questions))

    @patch("ingest.jev.ask")
    def test_review_applies_policy(self, ask) -> None:
        ask.return_value = _answers()
        lesson = jev.review_lesson(_lesson(), source_text=TRANSCRIPT, transcript=TRANSCRIPT)
        self.assertEqual(lesson["key_takeaways"], ["Classifiers pick fixed outcomes."])
        self.assertEqual(
            [m["timestamp"] for m in lesson["key_moments"]], ["2:10", "59:00"]
        )  # unjudged moment kept; the render step drops it if past the video's end
        self.assertEqual(lesson["topics"], ["classifiers-and-structured-output", "ai-agents"])
        self.assertEqual((lesson["kind"], lesson["depth"], lesson["actionability"]), ("tutorial", 2, 2))

    @patch("ingest.jev.ask", side_effect=jev.JevError("down"))
    def test_review_failure_leaves_lesson_untouched(self, _ask) -> None:
        lesson = _lesson()
        self.assertEqual(jev.review_lesson(dict(lesson), source_text=TRANSCRIPT), lesson)

    def test_without_key_nothing_is_called(self) -> None:
        with patch("ingest.jev.config.TYPESAFE_API_KEY", ""), patch("ingest.jev.ask") as ask:
            jev.review_lesson(_lesson(), source_text=TRANSCRIPT)
            self.assertIsNone(jev.substantive_probability("u", "web", "text"))
        ask.assert_not_called()


@patch("ingest.jev.config.TYPESAFE_API_KEY", "test-key")
class JevSourceGateTests(unittest.TestCase):
    def _source(self) -> FetchedSource:
        return FetchedSource(url="https://example.com/a", kind="web", content="Accept cookies " * 100)

    @patch("ingest.jev.ask", return_value={"substantive": {"type": "noul", "noul": 0.04}})
    def test_non_substantive_source_is_rejected_before_codex(self, _ask) -> None:
        with self.assertRaises(SourceQualityError):
            judge_source(self._source())

    @patch("ingest.jev.ask", side_effect=jev.JevError("down"))
    def test_gate_fails_open(self, _ask) -> None:
        self.assertEqual(judge_source(self._source()).url, "https://example.com/a")


class ProfileRenderingTests(unittest.TestCase):
    def test_profile_frontmatter_is_rendered(self) -> None:
        lesson = {**_lesson(), "tags": ["x"], "how_it_works": "h", "training_exercise": "t",
                  "topics": ["ai-agents"], "kind": "tutorial", "depth": 2, "actionability": 3}
        source = FetchedSource(url="https://example.com/a", kind="web", content="x" * 900)
        markdown = render_markdown(lesson, source=source, date="2026-09-23", fingerprint="f")
        self.assertIn('topics: [ai-agents]\nkind: "tutorial"\ndepth: 2\nactionability: 3\n---', markdown)


@patch("ingest.jev.config.TYPESAFE_API_KEY", "test-key")
class BackfillProfileTests(unittest.TestCase):
    @patch("ingest.jev.ask")
    def test_jev_only_profiles_page_without_codex(self, ask) -> None:
        ask.return_value = _answers()
        page = backfill.parse_page(
            Path("2026-09-01-a.md"),
            '---\ntitle: "A"\nsource: "https://example.com/a"\nsource_type: "web"\n---\n\n'
            "## TL;DR\n\n> Existing summary.\n\n## Overview\nBody.",
        )
        with patch("ingest.backfill._summarize") as summarize:
            changes = backfill.upgrade_page(
                page, metadata=False, summaries=False, use_transcripts=False, profile=True
            )
        summarize.assert_not_called()
        self.assertIn("profile", changes)
        self.assertEqual(page.get("kind"), "tutorial")
        self.assertEqual(page.get("topics"), "[classifiers-and-structured-output, ai-agents]")
        state = ask.call_args.args[0]
        self.assertEqual(state["lesson"]["tldr"], "Existing summary.")
        # Already-profiled pages are skipped.
        ask.reset_mock()
        backfill.upgrade_page(page, metadata=False, summaries=False, use_transcripts=False)
        ask.assert_not_called()



@patch("ingest.jev.config.TYPESAFE_API_KEY", "test-key")
class TopicPrecisionTests(unittest.TestCase):
    def test_broad_topic_needs_stronger_evidence(self) -> None:
        answers = _answers(**{
            jev._key("topic", "software-engineering"): {"type": "noul", "noul": 0.7},
            jev._key("topic", "developer-tools"): {"type": "noul", "noul": 0.7},
        })
        review = jev.parse_review(answers, takeaway_count=0, moment_count=0)
        topics = [slug for slug, _ in review.topics]
        self.assertIn("developer-tools", topics)
        self.assertNotIn("software-engineering", topics)

    @patch("ingest.jev.ask")
    def test_retopic_rejudges_only_pages_with_that_topic(self, ask) -> None:
        from tempfile import TemporaryDirectory
        ask.return_value = _answers(**{jev._key("topic", slug): {"type": "noul", "noul": 0.1} for slug in TOPICS})
        with TemporaryDirectory() as directory:
            pages = Path(directory)
            head = '---\ntitle: "{t}"\nsource: "https://example.com/{t}"\nsource_type: "web"\n'
            tagged = pages / "2026-09-02-tagged.md"
            tagged.write_text(head.format(t="a") + 'topics: [software-engineering, mcp]\nkind: "news"\n---\n\nBody.\n')
            other = pages / "2026-09-01-other.md"
            other.write_text(head.format(t="b") + 'topics: [mcp]\nkind: "news"\n---\n\nBody.\n')
            before = other.read_text()
            with patch.object(backfill, "PAGES_DIR", pages):
                backfill.run(metadata=False, summaries=False, use_transcripts=False, profile=True,
                             limit=0, match="", dry_run=False, pause=0, retopic="software-engineering")
            self.assertEqual(ask.call_count, 1)
            self.assertIn("topics: []", tagged.read_text())
            self.assertIn('kind: "tutorial"', tagged.read_text())
            self.assertEqual(other.read_text(), before)


if __name__ == "__main__":
    unittest.main()
