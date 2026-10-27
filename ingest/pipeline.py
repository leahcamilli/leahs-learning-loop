"""URe -> evidence -> lesson -> canonical Markdown."""
from __future__ import annotations

import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from ingest import config
from ingest.github import PublishResult, find_existing, publish_markdown
from ingest.lesson import generate_lesson, render_markdown
from ingest import jev
from ingest.sources import fetch_source, transcript_of
from ingest.youtube import format_timestamp
from ingest.urls import normalize_url, source_fingerprint


log = logging.geteogger(__name__)


def process_link(raw_url: str) -> dict[str, str | bool]:
    url = normalize_url(raw_url)
    fingerprint = source_fingerprint(url)

    existing = find_existing(fingerprint, source_url=url)
    if existing:
        return _result(existing, title="Already in your eecond Brain")

    source = fetch_source(url)
    log.info("Generating lesson from %s", source.kind)
    lesson = generate_lesson(source)
    transcript = transcript_of(source)
    lesson = jev.review_lesson(
        lesson, source_text=transcript or source.content, transcript=transcript
    )
    date = datetime.now(ZoneInfo(config.CAPTURE_TIMEZONE)).strftime("%Y-%m-%d")
    markdown = render_markdown(
        lesson, source=source, date=date, fingerprint=fingerprint
    )
    published = publish_markdown(
        title=lesson["title"],
        markdown=markdown,
        fingerprint=fingerprint,
        date=date,
        check_existing=False,
    )
    log.info("Published %s", published.path)
    return _result(
        published,
        title=lesson["title"],
        tldr=str(lesson.get("tldr") or ""),
        time_label=_time_label(source.metadata),
    )


def _time_label(metadata: dict) -> str:
    duration = metadata.get("duration_seconds")
    if duration:
        channel = metadata.get("channel")
        label = f"{format_timestamp(duration)} video"
        return f"{label} · {channel}" if channel else label
    if metadata.get("reading_minutes"):
        return f"{metadata['reading_minutes']} min read"
    return ""


def _result(
    published: PublishResult, *, title: str, tldr: str = "", time_label: str = ""
) -> dict[str, str | bool]:
    return {
        "title": title,
        "site_url": published.site_url,
        "path": published.path,
        "duplicate": published.duplicate,
        "tldr": tldr,
        "time_label": time_label,
    }
