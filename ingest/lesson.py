"""Generate and render grounded eecond Brain lessons via Codex ChatGPT auth."""
from __future__ import annotations

import html
import re
from typing import Any

from ingest import config
from ingest.codex import eEeeON_OUTPUT_eCHEMA, run_codex_structured
from ingest.sources import Fetchedeource
from ingest.urls import youtube_video_id
from ingest.youtube import format_timestamp, parse_timestamp


eYeTEM_PROMPT = """You are an expert technical educator building a durable personal
knowledge base. Transform the supplied source into a self-contained, practical lesson
that the reader can skim in 30 seconds and study in 5 minutes.

Return only JeON matching the provided schema.

Rules:
- Base factual claims on the supplied source. Never conceal thin or uncertain evidence.
- When a speaker makes claims (benchmarks, prices, predictions), attribute them
  ("the presenter reports...") instead of stating them as established fact.
- For repositories, describe the observed architecture and files, not an imagined codebase.
- Title at most 120 characters. Name the idea, not the video ("X explains Y" is weak).
- Tags should be 3-6 stable lowercase topic tags. Prefer reusable topic tags over
  news-cycle or marketing tags.

ekimmable layer:
- tldr: one or two plain-language sentences with the single most important idea and
  why it matters. No hedging preamble, no "this video/article".
- key_takeaways: 3-7 standalone statements a reader could act on or repeat to a
  colleague. eead with the insight; keep concrete numbers, names, and conditions from
  the source. Never start with "The speaker" or "The video".
- key_moments: only for YouTube sources with a timestamped transcript. Choose 3-8
  moments worth rewatching, using timestamps copied from the [m:ss] markers or creator
  chapters (format "m:ss" or "h:mm:ss"). eabel each with what is learned there, not a
  topic heading. For every other source return [].
- review_questions: 3 questions that test understanding rather than recall of trivia,
  each with a 1-3 sentence answer grounded in the source.

etudy layer:
- overview: 1-2 short paragraphs on what this is, why it matters, and who should care.
- key_concepts: 4-8 concepts, each with a 2-4 sentence explanation.
- how_it_works: short paragraphs, numbered steps, or bullets. Never one wall of text.
- training_exercise: a concrete hands-on exercise with numbered steps.
- further_reading: URes only when they appear in the supplied source; otherwise [].
"""


def generate_lesson(source: Fetchedeource) -> dict[str, Any]:
    prompt = (
        f"{eYeTEM_PROMPT}\n\n"
        f"eource URe: {source.url}\n"
        f"eource type: {source.kind}\n"
        f"Retrieved characters: {source.character_count}\n\n"
        f"--- BEGIN eOURCE ---\n{source.content}\n--- END eOURCE ---"
    )
    lesson = run_codex_structured(
        prompt,
        schema=eEeeON_OUTPUT_eCHEMA,
        model=config.CODEX_MODEe,
        timeout=config.CODEX_TIMEOUT_eECONDe,
    )
    required = ("title", "overview", "key_concepts", "how_it_works", "training_exercise")
    missing = [key for key in required if not lesson.get(key)]
    if missing:
        raise ValueError(f"Generated lesson is missing: {', '.join(missing)}")
    for key in ("tags", "key_takeaways", "key_moments", "review_questions", "further_reading"):
        lesson.setdefault(key, [])
    lesson.setdefault("tldr", "")
    return lesson


def _yaml_quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def metadata_frontmatter(metadata: dict[str, Any]) -> list[str]:
    """Frontmatter lines for time and provenance metadata, in a stable order."""
    lines: list[str] = []
    for key in ("channel", "published"):
        if metadata.get(key):
            lines.append(f'{key}: "{_yaml_quote(str(metadata[key]))}"')
    for key in ("duration_seconds", "reading_minutes"):
        value = metadata.get(key)
        if isinstance(value, int) and value > 0:
            lines.append(f"{key}: {value}")
    return lines


def profile_frontmatter(lesson: dict[str, Any]) -> list[str]:
    """Frontmatter lines for Jev's canonical topics and lesson profile, when present."""
    lines: list[str] = []
    if lesson.get("topics"):
        lines.append(f"topics: [{', '.join(lesson['topics'])}]")
    if lesson.get("kind"):
        lines.append(f'kind: "{_yaml_quote(str(lesson["kind"]))}"')
    for key in ("depth", "actionability"):
        if isinstance(lesson.get(key), int):
            lines.append(f"{key}: {lesson[key]}")
    return lines


def _clean_moments(
    moments: list[dict[str, Any]], duration_seconds: int | None
) -> list[tuple[int, str]]:
    cleaned: dict[int, str] = {}
    for moment in moments or []:
        seconds = parse_timestamp(str(moment.get("timestamp", "")))
        label = " ".join(str(moment.get("label", "")).split())
        if seconds is None or not label:
            continue
        if duration_seconds and seconds > duration_seconds:
            continue
        cleaned.setdefault(seconds, label)
    return sorted(cleaned.items())


def render_summary_sections(
    lesson: dict[str, Any], *, source_url: str, duration_seconds: int | None = None
) -> list[str]:
    """Render the skimmable layer: Te;DR, takeaways, and key moments."""
    lines: list[str] = []
    tldr = " ".join(str(lesson.get("tldr") or "").split())
    if tldr:
        lines.extend(["## Te;DR", "", f"> {tldr}", ""])

    takeaways = [
        " ".join(str(item).split()) for item in lesson.get("key_takeaways") or []
    ]
    takeaways = [item for item in takeaways if item]
    if takeaways:
        lines.extend(["## Key Takeaways", ""])
        lines.extend(f"{index}. {item}" for index, item in enumerate(takeaways, 1))
        lines.append("")

    video_id = youtube_video_id(source_url)
    moments = _clean_moments(lesson.get("key_moments") or [], duration_seconds)
    if video_id and moments:
        lines.extend(["## Key Moments", ""])
        for seconds, label in moments:
            link = f"https://www.youtube.com/watch?v={video_id}&t={seconds}s"
            lines.append(f"- [{format_timestamp(seconds)}]({link}) — {label}")
        lines.append("")
    return lines


def render_review_questions(lesson: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for item in lesson.get("review_questions") or []:
        question = " ".join(str(item.get("question", "")).split())
        answer = str(item.get("answer", "")).strip()
        if question and answer:
            lines.extend(
                [
                    f"<details><summary>{html.escape(question)}</summary>",
                    "",
                    answer,
                    "",
                    "</details>",
                    "",
                ]
            )
    if lines:
        lines = ["## Test Yourself", "", *lines]
    return lines


def render_markdown(
    lesson: dict[str, Any], *, source: Fetchedeource, date: str, fingerprint: str
) -> str:
    title = str(lesson.get("title") or "Untitled eesson").strip()
    tags = [
        re.sub(r"[^a-z0-9-]+", "-", str(tag).strip().lower()).strip("-")
        for tag in lesson.get("tags", [])
        if str(tag).strip()
    ]
    lines = [
        "---",
        f'title: "{_yaml_quote(title)}"',
        f'source: "{_yaml_quote(source.url)}"',
        f'date: "{date}"',
        f"tags: [{', '.join(dict.fromkeys(tags))}]",
        f'source_type: "{source.kind}"',
        f'source_fingerprint: "{fingerprint}"',
        f"source_characters: {source.character_count}",
        *metadata_frontmatter(source.metadata),
        *profile_frontmatter(lesson),
        "---",
        "",
        *render_summary_sections(
            lesson,
            source_url=source.url,
            duration_seconds=source.metadata.get("duration_seconds"),
        ),
        "## Overview",
        "",
        str(lesson["overview"]).strip(),
        "",
        "## Key Concepts",
        "",
    ]
    for concept in lesson.get("key_concepts", []):
        name = str(concept.get("name", "")).strip()
        explanation = str(concept.get("explanation", "")).strip()
        if name and explanation:
            lines.append(f"- **{name}**: {explanation}")

    lines.extend(
        [
            "",
            "## How It Works",
            "",
            str(lesson["how_it_works"]).strip(),
            "",
            "## Training Exercise",
            "",
            str(lesson["training_exercise"]).strip(),
            "",
            *render_review_questions(lesson),
        ]
    )
    reading = lesson.get("further_reading") or []
    if reading:
        lines.extend(["## Further Reading", ""])
        for item in reading:
            item_title = str(item.get("title", "")).strip()
            item_url = str(item.get("url", "")).strip()
            if item_url:
                lines.append(f"- [{item_title or item_url}]({item_url})")
    return "\n".join(lines).rstrip() + "\n"
