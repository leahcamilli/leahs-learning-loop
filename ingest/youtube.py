"""Hard-bounded YouTube transcript and metadata retrieval.

The transcript library does not expose an overall network deadline. Running it in a
short-lived child process lets the bot stop a DNS or socket stall reliably.
"""
from __future__ import annotations

import json
import re
import socket
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


WATCH_URL = "https://www.youtube.com/watch?v={video_id}"
OEMBED_URL = "https://www.youtube.com/oembed"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
# Group transcript snippets into short timestamped paragraphs so the lesson can
# cite key moments without doubling the prompt size.
PARAGRAPH_SECONDS = 30
_CHAPTER_RE = re.compile(
    r"^\s*[\(\[]?((?:\d{1,2}:)?\d{1,2}:\d{2})[\)\]]?\s*[-–—:|]?\s*(.+?)\s*$"
)


@dataclass(frozen=True)
class VideoEvidence:
    transcript: str
    metadata: dict[str, Any] = field(default_factory=dict)


def format_timestamp(seconds: float) -> str:
    total = max(0, int(seconds))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def parse_timestamp(value: str) -> int | None:
    """Parse ``h:mm:ss`` / ``m:ss`` into seconds; ``None`` when malformed."""
    parts = str(value).strip().split(":")
    if not 2 <= len(parts) <= 3 or not all(part.isdigit() for part in parts):
        return None
    seconds = 0
    for part in parts:
        seconds = seconds * 60 + int(part)
    return seconds


def parse_chapters(description: str) -> list[dict[str, Any]]:
    """Read creator chapters from a description (YouTube requires a 0:00 start)."""
    chapters: list[dict[str, Any]] = []
    for line in (description or "").splitlines():
        match = _CHAPTER_RE.match(line)
        if not match:
            continue
        start = parse_timestamp(match.group(1))
        if start is None:
            continue
        if chapters and start <= chapters[-1]["start"]:
            continue
        chapters.append({"start": start, "title": match.group(2)})
    if len(chapters) < 2 or chapters[0]["start"] != 0:
        return []
    return chapters


def _extract_json_object(html: str, marker: str) -> dict[str, Any]:
    index = html.find(marker)
    if index < 0:
        return {}
    start = html.find("{", index + len(marker))
    if start < 0:
        return {}
    try:
        value, _ = json.JSONDecoder().raw_decode(html, start)
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def parse_watch_page(html: str) -> dict[str, Any]:
    """Extract stable metadata from a watch page's ``ytInitialPlayerResponse``."""
    player = _extract_json_object(html, "ytInitialPlayerResponse")
    details = player.get("videoDetails") or {}
    microformat = (player.get("microformat") or {}).get("playerMicroformatRenderer") or {}
    metadata: dict[str, Any] = {}

    if details.get("title"):
        metadata["title"] = str(details["title"])
    if details.get("author"):
        metadata["channel"] = str(details["author"])
    if str(details.get("lengthSeconds", "")).isdigit():
        metadata["duration_seconds"] = int(details["lengthSeconds"])
    if str(details.get("viewCount", "")).isdigit():
        metadata["view_count"] = int(details["viewCount"])
    published = str(microformat.get("publishDate") or microformat.get("uploadDate") or "")
    if published:
        metadata["published"] = published[:10]
    if microformat.get("category"):
        metadata["category"] = str(microformat["category"])
    description = str(details.get("shortDescription") or "")
    if description:
        metadata["description"] = description
        chapters = parse_chapters(description)
        if chapters:
            metadata["chapters"] = chapters
    return metadata


def timestamped_transcript(segments: list[tuple[float, float, str]]) -> str:
    """Render ``(start, duration, text)`` snippets as ``[m:ss]`` paragraphs."""
    paragraphs: list[str] = []
    current: list[str] = []
    paragraph_start = 0.0
    for start, _, text in segments:
        text = " ".join(str(text).split())
        if not text:
            continue
        if current and start - paragraph_start >= PARAGRAPH_SECONDS:
            paragraphs.append(f"[{format_timestamp(paragraph_start)}] {' '.join(current)}")
            current = []
        if not current:
            paragraph_start = start
        current.append(text)
    if current:
        paragraphs.append(f"[{format_timestamp(paragraph_start)}] {' '.join(current)}")
    return "\n".join(paragraphs)


def _snippet(item: Any) -> tuple[float, float, str]:
    if isinstance(item, dict):
        return (
            float(item.get("start", 0) or 0),
            float(item.get("duration", 0) or 0),
            str(item.get("text", "")),
        )
    return (
        float(getattr(item, "start", 0) or 0),
        float(getattr(item, "duration", 0) or 0),
        str(getattr(item, "text", "")),
    )


def _fetch_segments(video_id: str) -> list[tuple[float, float, str]]:
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    if hasattr(api, "fetch"):
        transcript = api.fetch(video_id, languages=["en"])
    else:  # Compatibility with pre-1.0 releases.
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    return [_snippet(item) for item in transcript]


def _fetch_metadata(video_id: str) -> dict[str, Any]:
    """Best-effort metadata; a missing field never blocks a capture."""
    import requests

    headers = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}
    metadata: dict[str, Any] = {}
    try:
        response = requests.get(
            WATCH_URL.format(video_id=video_id),
            headers=headers,
            cookies={"CONSENT": "YES+1"},
            timeout=(4, 8),
        )
        response.raise_for_status()
        metadata = parse_watch_page(response.text)
    except Exception as exc:  # noqa: BLE001 - metadata is optional evidence
        print(f"watch page metadata unavailable: {exc}", file=sys.stderr)

    if not metadata.get("title") or not metadata.get("channel"):
        try:
            response = requests.get(
                OEMBED_URL,
                params={"url": WATCH_URL.format(video_id=video_id), "format": "json"},
                headers=headers,
                timeout=(3, 5),
            )
            response.raise_for_status()
            payload = response.json()
            metadata.setdefault("title", str(payload.get("title") or ""))
            metadata.setdefault("channel", str(payload.get("author_name") or ""))
        except Exception as exc:  # noqa: BLE001
            print(f"oEmbed metadata unavailable: {exc}", file=sys.stderr)
    return {key: value for key, value in metadata.items() if value not in ("", None)}


def _fetch_direct(video_id: str, *, metadata_only: bool = False) -> dict[str, Any]:
    # This Mac's resolver can prefer an unreachable IPv6 route for YouTube while
    # IPv4 is healthy. Keep the isolated worker on the reliable address family.
    from urllib3.util import connection as urllib3_connection

    urllib3_connection.allowed_gai_family = lambda: socket.AF_INET
    if metadata_only:
        return {"transcript": "", "metadata": _fetch_metadata(video_id)}

    # The transcript is the evidence; fetch it before spending budget on metadata.
    segments = _fetch_segments(video_id)
    metadata = _fetch_metadata(video_id)
    if segments and "duration_seconds" not in metadata:
        # The last caption's end is a close lower bound when the page is unreadable.
        start, duration, _ = segments[-1]
        metadata["duration_seconds"] = int(start + duration)
    return {"transcript": timestamped_transcript(segments), "metadata": metadata}


def _run_worker(args: list[str], timeout: int) -> dict[str, Any]:
    try:
        process = subprocess.run(
            [sys.executable, "-m", "ingest.youtube", *args],
            cwd=Path(__file__).resolve().parent.parent,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise TimeoutError(f"YouTube retrieval timed out after {timeout} seconds") from exc

    if process.returncode != 0:
        raise RuntimeError(process.stderr.strip() or "YouTube retrieval failed")
    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("YouTube worker returned invalid output") from exc
    return payload if isinstance(payload, dict) else {}


def fetch_video(video_id: str, *, timeout: int = 60) -> VideoEvidence:
    payload = _run_worker([video_id], timeout)
    transcript = str(payload.get("transcript", "")).strip()
    if not transcript:
        raise RuntimeError("YouTube transcript was empty")
    return VideoEvidence(transcript=transcript, metadata=dict(payload.get("metadata") or {}))


def fetch_video_metadata(video_id: str, *, timeout: int = 30) -> dict[str, Any]:
    payload = _run_worker([video_id, "--metadata-only"], timeout)
    return dict(payload.get("metadata") or {})


def main() -> None:
    args = sys.argv[1:]
    metadata_only = "--metadata-only" in args
    args = [arg for arg in args if arg != "--metadata-only"]
    if len(args) != 1:
        raise SystemExit("usage: python -m ingest.youtube VIDEO_ID [--metadata-only]")
    try:
        payload = _fetch_direct(args[0], metadata_only=metadata_only)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2) from exc
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
