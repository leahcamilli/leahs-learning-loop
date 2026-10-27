"""TypeSafe Jev judgments: source gate, summary grounding, topics, and lesson profile.

Codex writes the lesson; Jev supplies fast, typed judgments that code acts on.
Everything here is optional: without TYPESAFE_API_KEY the pipeline behaves exactly
as before, and a Jev failure never blocks a capture.

API contract (TypeSafe HTTP API v1): POST {base}/v1/systemone with
``{"state": ..., "model": ..., "questions": {name: question}}``; answers come back
keyed by the same names as ``noul`` / ``choice`` / ``score`` objects.
"""
from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass, field
from typing import Any

import requests

from ingest import config
from ingest.topics import TOPIC_MIN_OVERRIDES, TOPICS
from ingest.youtube import parse_timestamp


log = logging.getLogger(__name__)
RETRY_STATUSES = {429, 500, 502, 503, 504}
MAX_ATTEMPTS = 3
TOPICS_PER_LESSON = 4
_TRANSCRIPT_LINE_RE = re.compile(r"^\[((?:\d+:)?\d{1,2}:\d{2})\]\s*(.*)$")

KINDS: dict[str, str] = {
    "tutorial": "Step-by-step teaching of how to do something with a tool, technique, or workflow.",
    "deep-dive": "In-depth explanation of how or why something works, its internals, or trade-offs.",
    "news": "Announcement, release, or update: mainly reports what changed or was launched.",
    "opinion": "Argument, commentary, prediction, or strategic perspective from the author.",
    "demo": "Shows a product, project, or build in action without teaching the steps.",
    "interview": "Conversation, podcast, or panel among several people.",
}
DEPTH_LEVELS = [
    "Headline: reports what happened with little explanation.",
    "Overview: explains the ideas without implementation detail.",
    "Practical: shows how to use or apply it with concrete steps or examples.",
    "Expert: detailed internals, trade-offs, or advanced techniques.",
]
ACTIONABILITY_LEVELS = [
    "Nothing to try: background awareness only.",
    "Ideas worth considering later.",
    "Something concrete a reader could try this week.",
    "Directly applicable today with clear steps.",
]


class JevError(RuntimeError):
    """The TypeSafe API could not answer."""


def enabled() -> bool:
    return bool(config.TYPESAFE_API_KEY)


# ── Transport ─────────────────────────────────────────────────────────────────

def ask(state: Any, questions: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Send one System One request and return the raw answers keyed by question name."""
    if not questions:
        return {}
    body = {"state": state, "model": config.TYPESAFE_MODEL, "questions": questions}
    headers = {
        "Authorization": f"Bearer {config.TYPESAFE_API_KEY}",
        "Accept": "application/json",
    }
    url = f"{config.TYPESAFE_BASE_URL.rstrip('/')}/v1/systemone"
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.post(
                url, json=body, headers=headers, timeout=config.JEV_TIMEOUT_SECONDS
            )
        except requests.RequestException as exc:
            if attempt == MAX_ATTEMPTS:
                raise JevError(f"TypeSafe request failed: {type(exc).__name__}") from exc
            time.sleep(2 ** (attempt - 1))
            continue
        if response.status_code in RETRY_STATUSES and attempt < MAX_ATTEMPTS:
            retry_after = response.headers.get("retry-after", "")
            time.sleep(float(retry_after) if retry_after.isdigit() else 2 ** (attempt - 1))
            continue
        if response.status_code >= 400:
            # Never echo headers; the body is a short validation or error message.
            raise JevError(f"TypeSafe returned {response.status_code}: {response.text[:200]}")
        answers = response.json().get("answers")
        if not isinstance(answers, dict):
            raise JevError("TypeSafe response had no answers")
        usage = response.json().get("usage") or {}
        log.info("Jev answered %d questions (%s input tokens)", len(answers), usage.get("input_tokens", "?"))
        return answers
    raise JevError("TypeSafe request failed")


def noul(instructions: Any, *, true: str | None = None, false: str | None = None) -> dict[str, Any]:
    question: dict[str, Any] = {"type": "noul", "instructions": instructions}
    if true or false:
        question["criteria"] = {"true": true, "false": false}
    return question


def choice(instructions: Any, criteria: dict[str, str | None]) -> dict[str, Any]:
    return {"type": "choice", "instructions": instructions, "criteria": criteria}


def score(instructions: Any, levels: list[str]) -> dict[str, Any]:
    return {"type": "score", "instructions": instructions, "criteria": levels}


def _key(prefix: str, name: str | int) -> str:
    """Question names are for code only; keep them to safe identifier characters."""
    return f"{prefix}_{re.sub(r'[^a-z0-9]+', '_', str(name).lower()).strip('_')}"


# ── Source gate ───────────────────────────────────────────────────────────────

def substantive_probability(url: str, kind: str, content: str) -> float | None:
    """Probability the retrieved source is worth a lesson; ``None`` when Jev is unavailable."""
    if not enabled():
        return None
    state = {"url": url, "source_type": kind, "excerpt": content[:12_000]}
    question = noul(
        "`excerpt` is substantive content a person could learn from.",
        true=(
            "It explains ideas, techniques, events, or opinions in enough detail to learn "
            "from, even when informal, spoken, or promotional in tone."
        ),
        false=(
            "It is a stub, cookie or consent wall, login or error page, bare advertisement, "
            "song lyrics, or mostly navigation and boilerplate with little to learn."
        ),
    )
    try:
        answers = ask(state, {"substantive": question})
    except JevError as exc:
        log.warning("Jev source gate skipped: %s", exc)
        return None
    return float(answers["substantive"]["noul"])


# ── Lesson review ─────────────────────────────────────────────────────────────

@dataclass
class LessonReview:
    topics: list[tuple[str, float]] = field(default_factory=list)
    kind: str | None = None
    depth: int | None = None
    actionability: int | None = None
    takeaway_support: list[float] | None = None
    moment_support: list[float] | None = None


def transcript_window(transcript: str, seconds: int, *, before: int = 15, after: int = 90) -> str:
    """Text of the ``[m:ss]`` paragraphs that overlap a moment's neighbourhood."""
    lines: list[str] = []
    for line in transcript.splitlines():
        match = _TRANSCRIPT_LINE_RE.match(line.strip())
        if not match:
            continue
        start = parse_timestamp(match.group(1))
        if start is not None and seconds - before - 30 <= start <= seconds + after:
            lines.append(line.strip())
    return "\n".join(lines)


def build_review_request(
    lesson: dict[str, Any], *, source_text: str, transcript: str = ""
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    """State and questions for one request; independent questions run in parallel."""
    takeaways = [str(item) for item in lesson.get("key_takeaways") or [] if str(item).strip()]
    moments = []
    for moment in lesson.get("key_moments") or []:
        seconds = parse_timestamp(str(moment.get("timestamp", "")))
        window = transcript_window(transcript, seconds) if transcript and seconds is not None else ""
        if window:
            moments.append({"timestamp": moment["timestamp"], "label": moment.get("label", ""), "transcript_excerpt": window})

    ground = bool(takeaways) and 0 < len(source_text) <= config.JEV_MAX_SOURCE_CHARS
    if takeaways and not ground:
        log.info("Jev grounding skipped: source is %d characters", len(source_text))
    state: dict[str, Any] = {
        "lesson": {
            "title": lesson.get("title", ""),
            "tldr": lesson.get("tldr", ""),
            "overview": str(lesson.get("overview", ""))[:4000],
            "key_concepts": [c.get("name", "") for c in lesson.get("key_concepts") or []],
        },
        "source": {"excerpt": source_text if ground else source_text[:12_000]},
    }
    questions: dict[str, dict[str, Any]] = {}

    for slug, description in TOPICS.items():
        questions[_key("topic", slug)] = noul(
            f"The lesson in `lesson` is substantially about this topic: {description}",
            true="The topic is one of the lesson's main subjects.",
            false="The topic is absent or only mentioned in passing.",
        )
    questions["kind"] = choice(
        "What kind of source is summarized in `lesson` (see `source.excerpt`)?", dict(KINDS)
    )
    questions["depth"] = score("How deep does the source in `source.excerpt` go?", DEPTH_LEVELS)
    questions["actionability"] = score(
        "How directly can a reader act on the lesson in `lesson`?", ACTIONABILITY_LEVELS
    )

    if ground:
        state["takeaways"] = takeaways
        for index in range(len(takeaways)):
            questions[_key("takeaway", index)] = noul(
                f"The statement `takeaways[{index}]` is supported by `source.excerpt`.",
                true="The source states or clearly implies it, including any numbers or names it uses.",
                false="The source contradicts it, never addresses it, or it adds specifics the source does not contain.",
            )
    if moments:
        state["moments"] = moments
        for index in range(len(moments)):
            questions[_key("moment", index)] = noul(
                f"`moments[{index}].transcript_excerpt` covers what `moments[{index}].label` describes.",
                true="The excerpt discusses that point.",
                false="The excerpt is about something else.",
            )
    return state, questions


def parse_review(
    answers: dict[str, dict[str, Any]], *, takeaway_count: int, moment_count: int
) -> LessonReview:
    review = LessonReview()
    for slug in TOPICS:
        answer = answers.get(_key("topic", slug))
        threshold = TOPIC_MIN_OVERRIDES.get(slug, config.JEV_TOPIC_MIN)
        if answer and answer.get("noul", 0) >= threshold:
            review.topics.append((slug, float(answer["noul"])))
    review.topics.sort(key=lambda item: item[1], reverse=True)
    review.topics = review.topics[:TOPICS_PER_LESSON]

    if "kind" in answers:
        review.kind = answers["kind"].get("choice")
    for name in ("depth", "actionability"):
        if name in answers and answers[name].get("score") is not None:
            setattr(review, name, int(round(float(answers[name]["score"]))))
    if takeaway_count and _key("takeaway", 0) in answers:
        review.takeaway_support = [
            float(answers.get(_key("takeaway", i), {}).get("noul", 1.0)) for i in range(takeaway_count)
        ]
    if moment_count and _key("moment", 0) in answers:
        review.moment_support = [
            float(answers.get(_key("moment", i), {}).get("noul", 1.0)) for i in range(moment_count)
        ]
    return review


def apply_review(lesson: dict[str, Any], review: LessonReview, *, transcript: str = "") -> dict[str, Any]:
    """Drop unsupported takeaways and moments; attach topics and the lesson profile."""
    threshold = config.JEV_SUPPORT_MIN
    if review.takeaway_support is not None:
        takeaways = [str(item) for item in lesson.get("key_takeaways") or [] if str(item).strip()]
        kept = [item for item, p in zip(takeaways, review.takeaway_support) if p >= threshold]
        if len(kept) < len(takeaways):
            log.info("Jev dropped %d unsupported takeaway(s)", len(takeaways) - len(kept))
        lesson["key_takeaways"] = kept
    if review.moment_support is not None:
        # Only moments that had a transcript window were judged; keep the same order.
        judged = [
            moment for moment in lesson.get("key_moments") or []
            if transcript and parse_timestamp(str(moment.get("timestamp", ""))) is not None
            and transcript_window(transcript, parse_timestamp(str(moment["timestamp"])))
        ]
        dropped = {
            id(moment) for moment, p in zip(judged, review.moment_support) if p < threshold
        }
        if dropped:
            log.info("Jev dropped %d off-target key moment(s)", len(dropped))
        lesson["key_moments"] = [m for m in lesson.get("key_moments") or [] if id(m) not in dropped]
    lesson["topics"] = [slug for slug, _ in review.topics]
    if review.kind:
        lesson["kind"] = review.kind
    if review.depth is not None:
        lesson["depth"] = review.depth
    if review.actionability is not None:
        lesson["actionability"] = review.actionability
    return lesson


def review_lesson(
    lesson: dict[str, Any], *, source_text: str, transcript: str = ""
) -> dict[str, Any]:
    """Run the review when Jev is configured; otherwise return the lesson unchanged."""
    if not enabled():
        return lesson
    state, questions = build_review_request(lesson, source_text=source_text, transcript=transcript)
    try:
        answers = ask(state, questions)
    except JevError as exc:
        log.warning("Jev review skipped: %s", exc)
        return lesson
    review = parse_review(
        answers,
        takeaway_count=len(state.get("takeaways", [])),
        moment_count=len(state.get("moments", [])),
    )
    return apply_review(lesson, review, transcript=transcript)
