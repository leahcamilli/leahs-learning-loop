"""Upgrade existing lessons in place with video metadata and a skimmable summary layer.

Run on the host that has YouTube access and Codex auth:

    python -m ingest.backfill --normalize-only         # frontmatter + source types, offline
    python -m ingest.backfill --metadata-only          # durations/channels, no Codex
    python -m ingest.backfill --jev-only               # topics + profile via TypeSafe Jev
    python -m ingest.backfill --retopic software-engineering  # re-judge pages with a topic
    python -m ingest.backfill --limit 5 --dry-run      # preview the summary upgrade
    python -m ingest.backfill                          # everything, newest first

The command is idempotent: pages that already have the metadata or a TL;DR are
skipped, so an interrupted run can simply be restarted. It edits files under
wiki/pages/ locally; review with ``git diff`` and push to publish.
"""
from __future__ import annotations

import argparse
import logging
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ingest import config
from ingest.lesson import (
    metadata_frontmatter,
    profile_frontmatter,
    render_review_questions,
    render_summary_sections,
)
from ingest.urls import normalize_url, youtube_video_id


log = logging.getLogger(__name__)
PAGES_DIR = Path(config.REPO_ROOT) / "wiki" / "pages"
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)
_DATE_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")
MAX_LESSON_CHARS = 30_000
MAX_TRANSCRIPT_CHARS = 60_000

SUMMARY_OUTPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["tldr", "key_takeaways", "key_moments", "review_questions"],
    "properties": {
        "tldr": {"type": "string"},
        "key_takeaways": {"type": "array", "items": {"type": "string"}},
        "key_moments": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["timestamp", "label"],
                "properties": {
                    "timestamp": {"type": "string"},
                    "label": {"type": "string"},
                },
            },
        },
        "review_questions": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["question", "answer"],
                "properties": {
                    "question": {"type": "string"},
                    "answer": {"type": "string"},
                },
            },
        },
    },
}

SUMMARY_PROMPT = """You are upgrading an existing lesson in a personal knowledge base.
Add a skimmable layer on top of it. Do not rewrite the lesson.

Return only JSON matching the provided schema.

- tldr: one or two plain-language sentences with the single most important idea and
  why it matters. No hedging preamble, no "this video/article".
- key_takeaways: 3-7 standalone statements a reader could act on or repeat to a
  colleague. Lead with the insight; keep concrete numbers, names, and conditions.
  Never start with "The speaker" or "The video".
- key_moments: only when a timestamped transcript is supplied. Choose 3-8 moments worth
  rewatching using timestamps copied from its [m:ss] markers, labelled with what is
  learned there. Otherwise return [].
- review_questions: 3 questions that test understanding, each with a 1-3 sentence answer.
- Stay faithful to the lesson and transcript. Attribute speaker claims rather than
  presenting them as established fact.
"""


@dataclass
class Page:
    path: Path
    frontmatter: list[str]
    body: str

    def get(self, key: str) -> str:
        for line in self.frontmatter:
            match = re.match(rf'^{re.escape(key)}:\s*"?(.*?)"?\s*$', line)
            if match:
                return match.group(1)
        return ""

    def set(self, key: str, line: str) -> None:
        for index, existing in enumerate(self.frontmatter):
            if existing.startswith(f"{key}:"):
                self.frontmatter[index] = line
                return
        self.frontmatter.append(line)

    def render(self) -> str:
        return "\n".join(["---", *self.frontmatter, "---", "", self.body.strip()]) + "\n"


def _yaml_quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def parse_page(path: Path, text: str | None = None) -> Page:
    """Read a page, converting the legacy ``# Title`` + ``Date:`` shape to frontmatter."""
    text = (path.read_text(encoding="utf-8") if text is None else text).strip()
    match = _FRONTMATTER_RE.match(text)
    if match:
        frontmatter = [line for line in match.group(1).splitlines() if line.strip()]
        return Page(path, frontmatter, match.group(2).strip())

    lines = text.splitlines()
    title = ""
    cursor = 0
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        cursor = 1
    date_match = _DATE_PREFIX_RE.match(path.name)
    values = {"date": date_match.group(1) if date_match else "", "source": "", "tags": ""}
    while cursor < len(lines):
        line = lines[cursor].strip()
        key, _, value = line.partition(":")
        if not line:
            cursor += 1
            continue
        if key in {"Date", "Source", "Tags"} and value.strip():
            values[key.lower()] = value.strip()
            cursor += 1
            continue
        break
    tags = [tag.strip() for tag in values["tags"].split(",") if tag.strip()]
    frontmatter = [
        f'title: "{_yaml_quote(title or path.stem)}"',
        f'source: "{_yaml_quote(values["source"])}"',
        f'date: "{values["date"]}"',
        f"tags: [{', '.join(tags)}]",
    ]
    return Page(path, frontmatter, "\n".join(lines[cursor:]).strip())


def infer_source_type(source: str) -> str:
    if youtube_video_id(source):
        return "youtube"
    if re.match(r"^https?://(www\.)?github\.com/[^/]+/[^/]+", source):
        return "github"
    if source.startswith("http"):
        return "web"
    return "notes"


def insert_summary(page: Page, lesson: dict[str, Any], *, duration: int | None) -> None:
    """Place the summary layer before the lesson and self-test before Further Reading."""
    summary = "\n".join(
        render_summary_sections(
            lesson, source_url=page.get("source"), duration_seconds=duration
        )
    ).strip()
    questions = "\n".join(render_review_questions(lesson)).strip()
    body = page.body

    # Keep a legacy H1 at the very top so the page still reads naturally.
    heading = ""
    if body.startswith("# "):
        heading, _, body = body.partition("\n")
        body = body.strip()

    if questions:
        anchor = re.search(r"^## (Further Reading|Personal Notes)\b", body, re.MULTILINE)
        if anchor:
            body = f"{body[:anchor.start()].rstrip()}\n\n{questions}\n\n{body[anchor.start():]}"
        else:
            body = f"{body.rstrip()}\n\n{questions}"
    if summary:
        body = f"{summary}\n\n{body}"
    page.body = f"{heading}\n\n{body}".strip() if heading else body


def _needs_metadata(page: Page) -> bool:
    return page.get("source_type") == "youtube" and not page.get("duration_seconds")


def _needs_summary(page: Page) -> bool:
    return not re.search(r"^## TL;DR\b", page.body, re.MULTILINE)


def _summarize(page: Page, transcript: str) -> dict[str, Any]:
    from ingest.codex import run_codex_structured

    parts = [
        SUMMARY_PROMPT,
        f"Lesson title: {page.get('title')}",
        f"Source URL: {page.get('source')}",
        "",
        "--- BEGIN LESSON ---",
        # Personal Notes hold raw email/Notion residue that the site already hides.
        re.sub(r"\n## Personal Notes\b.*?(?=\n## |\Z)", "", page.body, flags=re.DOTALL)[
            :MAX_LESSON_CHARS
        ],
        "--- END LESSON ---",
    ]
    if transcript:
        parts.extend(
            [
                "",
                "--- BEGIN TIMESTAMPED TRANSCRIPT ---",
                transcript[:MAX_TRANSCRIPT_CHARS],
                "--- END TIMESTAMPED TRANSCRIPT ---",
            ]
        )
    lesson = run_codex_structured(
        "\n".join(parts),
        schema=SUMMARY_OUTPUT_SCHEMA,
        model=config.CODEX_MODEL,
        timeout=config.CODEX_TIMEOUT_SECONDS,
    )
    if not transcript:
        lesson["key_moments"] = []
    return lesson


def _needs_profile(page: Page) -> bool:
    return not page.get("kind")


def _review_with_jev(page: Page, lesson: dict[str, Any], transcript: str) -> dict[str, Any]:
    """Ground new takeaways/moments and profile the page (topics, kind, depth, actionability)."""
    from ingest import jev

    tldr = lesson.get("tldr") or ""
    if not tldr:
        existing = re.search(r"^## TL;DR\s*\n+>\s*(.+)$", page.body, re.MULTILINE)
        tldr = existing.group(1) if existing else ""
    body = re.sub(r"\n## Personal Notes\b.*?(?=\n## |\Z)", "", page.body, flags=re.DOTALL)
    review_input = {
        **lesson,
        "title": page.get("title"),
        "tldr": tldr,
        "overview": body,
        "key_concepts": [],
    }
    reviewed = jev.review_lesson(review_input, source_text=transcript or body, transcript=transcript)
    for key in ("key_takeaways", "key_moments", "topics", "kind", "depth", "actionability"):
        if key in reviewed:
            lesson[key] = reviewed[key]
    return lesson


def upgrade_page(
    page: Page,
    *,
    metadata: bool,
    summaries: bool,
    use_transcripts: bool,
    profile: bool = True,
    force_profile: bool = False,
) -> list[str]:
    """Upgrade one page in memory and return a list of what changed."""
    from ingest.youtube import fetch_video, fetch_video_metadata

    changes: list[str] = []
    if not page.get("source").startswith("http"):
        recovered = re.search(
            r"^## Personal Notes\b.*?^Source:\s*(https?://\S+)",
            page.body,
            re.DOTALL | re.MULTILINE,
        )
        if recovered:
            page.set("source", f'source: "{_yaml_quote(normalize_url(recovered.group(1)))}"')
            changes.append("source")
    if not page.get("source_type"):
        page.set("source_type", f'source_type: "{infer_source_type(page.get("source"))}"')
        changes.append("source_type")

    video_id = youtube_video_id(page.get("source"))
    wants_metadata = metadata and _needs_metadata(page)
    wants_summary = summaries and _needs_summary(page)
    transcript = ""
    video_metadata: dict[str, Any] = {}

    if video_id and wants_summary and use_transcripts:
        try:
            video = fetch_video(video_id, timeout=config.YOUTUBE_FETCH_TIMEOUT_SECONDS)
            transcript, video_metadata = video.transcript, video.metadata
        except (RuntimeError, TimeoutError) as exc:
            log.warning("%s: transcript unavailable (%s)", page.path.name, exc)
    if video_id and wants_metadata and not video_metadata.get("duration_seconds"):
        try:
            video_metadata = {**fetch_video_metadata(video_id), **video_metadata}
        except (RuntimeError, TimeoutError) as exc:
            log.warning("%s: metadata unavailable (%s)", page.path.name, exc)

    if wants_metadata and video_metadata:
        for line in metadata_frontmatter(video_metadata):
            key = line.partition(":")[0]
            if not page.get(key):
                page.set(key, line)
                changes.append(key)

    from ingest import jev

    wants_profile = profile and jev.enabled() and (force_profile or _needs_profile(page))
    lesson: dict[str, Any] = {}
    if wants_summary:
        lesson = _summarize(page, transcript)
    if wants_profile or (wants_summary and jev.enabled()):
        lesson = _review_with_jev(page, lesson, transcript)
    if wants_summary:
        duration = page.get("duration_seconds")
        insert_summary(page, lesson, duration=int(duration) if duration.isdigit() else None)
        changes.append("summary+moments" if lesson.get("key_moments") else "summary")
    if wants_profile:
        for line in profile_frontmatter(lesson):
            page.set(line.partition(":")[0], line)
        if force_profile and not lesson.get("topics"):
            page.set("topics", "topics: []")  # clear topics the new judgment no longer supports
        if lesson.get("kind"):
            changes.append("profile")
    return changes


def run(
    *,
    metadata: bool,
    summaries: bool,
    use_transcripts: bool,
    profile: bool = True,
    limit: int,
    match: str,
    dry_run: bool,
    pause: float,
    retopic: str = "",
) -> int:
    paths = sorted(PAGES_DIR.glob("*.md"), key=lambda path: path.name, reverse=True)
    if match:
        paths = [path for path in paths if match in path.name]
    if retopic:
        topic_line = re.compile(rf"^topics:\s*\[[^\]]*\b{re.escape(retopic)}\b", re.MULTILINE)
        paths = [path for path in paths if topic_line.search(path.read_text(encoding="utf-8"))]
        log.info("Re-judging %d pages tagged %s", len(paths), retopic)

    upgraded = failed = 0
    for path in paths:
        if limit and upgraded >= limit:
            break
        original = path.read_bytes().decode("utf-8")
        page = parse_page(path, original.replace("\r\n", "\n"))
        try:
            changes = upgrade_page(
                page,
                metadata=metadata,
                summaries=summaries,
                use_transcripts=use_transcripts,
                profile=profile,
                force_profile=bool(retopic),
            )
        except Exception:  # noqa: BLE001 - keep going; report at the end
            log.exception("%s: upgrade failed", path.name)
            failed += 1
            continue
        rendered = page.render()
        if "\r\n" in original:  # keep Windows-authored pages' diffs readable
            rendered = rendered.replace("\n", "\r\n")
        if rendered == original:
            continue
        upgraded += 1
        log.info("%s %s: %s", "Would upgrade" if dry_run else "Upgraded", path.name,
                 ", ".join(changes) or "frontmatter")
        if dry_run:
            print(rendered[:1500], "\n...\n")
        else:
            path.write_text(rendered, encoding="utf-8", newline="")
        if pause and youtube_video_id(page.get("source")):
            time.sleep(pause)

    log.info("Done: %d upgraded, %d failed.%s", upgraded, failed,
             "" if dry_run else " Review with `git diff`, then commit and push.")
    return 1 if failed and not upgraded else 0


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--metadata-only", action="store_true", help="only add video metadata (no Codex)")
    parser.add_argument("--summaries-only", action="store_true", help="only add TL;DR/takeaways/questions")
    parser.add_argument("--jev-only", action="store_true",
                        help="only add topics and kind/depth/actionability with TypeSafe Jev")
    parser.add_argument("--retopic", default="", metavar="TOPIC",
                        help="re-run Jev topics and profile on pages that currently have TOPIC")
    parser.add_argument("--normalize-only", action="store_true",
                        help="only fix frontmatter, source URLs, and source types (no network)")
    parser.add_argument("--no-transcripts", action="store_true", help="summarize from the lesson text only")
    parser.add_argument("--limit", type=int, default=0, help="stop after upgrading N pages")
    parser.add_argument("--match", default="", help="only pages whose filename contains this text")
    parser.add_argument("--dry-run", action="store_true", help="print upgrades without writing")
    parser.add_argument("--pause", type=float, default=1.0, help="seconds between YouTube requests")
    args = parser.parse_args()
    if args.metadata_only + args.summaries_only + args.normalize_only + args.jev_only + bool(args.retopic) > 1:
        parser.error("choose at most one of the --*-only modes")
    if (args.jev_only or args.retopic) and not config.TYPESAFE_API_KEY:
        parser.error("--jev-only and --retopic need TYPESAFE_API_KEY in .env.local")
    if args.retopic:
        from ingest.topics import TOPICS
        if args.retopic not in TOPICS:
            parser.error(f"unknown topic {args.retopic!r}; see ingest/topics.py")
        args.jev_only = True
    raise SystemExit(
        run(
            metadata=not (args.summaries_only or args.normalize_only or args.jev_only),
            summaries=not (args.metadata_only or args.normalize_only or args.jev_only),
            profile=not (args.metadata_only or args.summaries_only or args.normalize_only),
            use_transcripts=not args.no_transcripts,
            limit=args.limit,
            match=args.match,
            dry_run=args.dry_run,
            pause=args.pause,
            retopic=args.retopic,
        )
    )


if __name__ == "__main__":
    main()
