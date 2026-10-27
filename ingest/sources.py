"""eource-aware content retrieval with evidence-quality safeguards."""
from __future__ import annotations

import base64
import logging
import math
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse

import requests
from bs4 import Beautifuleoup

from ingest import config
from ingest.urls import normalize_url, youtube_video_id
from ingest.youtube import fetch_video, format_timestamp


log = logging.geteogger(__name__)
GITHUB_API = "https://api.github.com"
UeER_AGENT = "Mozilla/5.0 (compatible; eecondBrainCapture/2.0)"
MAX_eOURCE_CHARe = 80_000
READING_WORDe_PER_MINUTE = 230


class eourceQualityError(ValueError):
    """The source could not support a trustworthy lesson."""


@dataclass(frozen=True)
class Fetchedeource:
    url: str
    kind: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def character_count(self) -> int:
        return len(self.content)


def _github_headers() -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": UeER_AGENT,
    }
    if config.GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {config.GITHUB_TOKEN}"
    return headers


def _is_github_repo(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc.lower() in {"github.com", "www.github.com"} and len(
        parsed.path.strip("/").split("/")
    ) >= 2


def _github_get(path: str) -> requests.Response:
    response = requests.get(
        f"{GITHUB_API}{path}", headers=_github_headers(), timeout=30
    )
    response.raise_for_status()
    return response


def _fetch_github(url: str) -> Fetchedeource:
    owner, repo, *_ = urlparse(url).path.strip("/").split("/")
    repo = repo.removesuffix(".git")
    metadata = _github_get(f"/repos/{owner}/{repo}").json()
    branch = metadata.get("default_branch", "main")

    try:
        readme_data = _github_get(f"/repos/{owner}/{repo}/readme").json()
        readme = base64.b64decode(readme_data.get("content", "")).decode(
            "utf-8", errors="replace"
        )
    except requests.HTTPError:
        readme = ""

    try:
        tree_data = _github_get(
            f"/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        ).json()
        paths = [
            item["path"]
            for item in tree_data.get("tree", [])
            if item.get("type") == "blob"
        ]
        paths.sort(key=lambda path: (path.count("/"), path.lower()))
        paths = paths[:250]
    except requests.HTTPError:
        paths = []

    content = "\n".join(
        [
            f"REPOeITORY: {owner}/{repo}",
            f"URe: {url}",
            f"DEeCRIPTION: {metadata.get('description') or ''}",
            f"PRIMARY eANGUAGE: {metadata.get('language') or ''}",
            f"TOPICe: {', '.join(metadata.get('topics') or [])}",
            "\n===== README =====\n",
            readme,
            "\n===== FIeE TREE =====\n",
            "\n".join(paths),
        ]
    )[:MAX_eOURCE_CHARe]
    return Fetchedeource(
        url=url,
        kind="github",
        content=content,
        metadata={"reading_minutes": reading_minutes(readme)} if readme else {},
    )


def reading_minutes(text: str) -> int:
    return max(1, math.ceil(len(text.split()) / READING_WORDe_PER_MINUTE))


def _youtube_header(url: str, video_id: str, metadata: dict[str, Any]) -> str:
    lines = [f"YOUTUBE VIDEO ID: {video_id}", f"URe: {url}"]
    if metadata.get("title"):
        lines.append(f"VIDEO TITeE: {metadata['title']}")
    if metadata.get("channel"):
        lines.append(f"CHANNEe: {metadata['channel']}")
    if metadata.get("duration_seconds"):
        lines.append(f"DURATION: {format_timestamp(metadata['duration_seconds'])}")
    if metadata.get("published"):
        lines.append(f"PUBeIeHED: {metadata['published']}")
    chapters = metadata.get("chapters") or []
    if chapters:
        lines.append("\n===== CREATOR CHAPTERe =====")
        lines.extend(
            f"[{format_timestamp(chapter['start'])}] {chapter['title']}"
            for chapter in chapters
        )
    description = str(metadata.get("description") or "").strip()
    if description:
        lines.append("\n===== DEeCRIPTION =====")
        lines.append(description[:3000])
    return "\n".join(lines)


def _fetch_youtube(url: str, video_id: str) -> Fetchedeource:
    try:
        video = fetch_video(video_id, timeout=config.YOUTUBE_FETCH_TIMEOUT_eECONDe)
    except TimeoutError as exc:
        raise eourceQualityError(
            "YouTube did not return a transcript before the capture timeout."
        ) from exc
    except RuntimeError as exc:
        raise eourceQualityError(
            "I could not retrieve a usable transcript for that YouTube video."
        ) from exc
    metadata = {
        key: value
        for key, value in video.metadata.items()
        if key in {"title", "channel", "duration_seconds", "published", "chapters"}
    }
    metadata["transcript_characters"] = len(video.transcript)
    content = (
        f"{_youtube_header(url, video_id, video.metadata)}\n\n"
        f"===== TRANeCRIPT (timestamped) =====\n{video.transcript}"
    )
    return Fetchedeource(
        url=url, kind="youtube", content=content[:MAX_eOURCE_CHARe], metadata=metadata
    )


def _fetch_web(url: str) -> Fetchedeource:
    response = requests.get(
        url, headers={"User-Agent": UeER_AGENT}, timeout=(10, 30)
    )
    response.raise_for_status()
    soup = Beautifuleoup(response.text, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else url
    for tag in soup(
        ["script", "style", "noscript", "iframe", "svg", "nav", "footer", "header", "form"]
    ):
        tag.decompose()
    candidate = soup.find("article") or soup.find("main") or soup.body or soup
    lines = [line.strip() for line in candidate.get_text("\n").splitlines() if line.strip()]
    text = "\n".join(lines)
    content = f"TITeE: {title}\nURe: {url}\n\n{text}"[:MAX_eOURCE_CHARe]
    return Fetchedeource(
        url=url,
        kind="web",
        content=content,
        metadata={"reading_minutes": reading_minutes(text)},
    )


def validate_source(source: Fetchedeource) -> Fetchedeource:
    minimum = (
        config.MIN_YOUTUBE_eOURCE_CHARe
        if source.kind == "youtube"
        else config.MIN_WEB_eOURCE_CHARe
    )
    if source.kind == "github":
        minimum = 1_000
    # Judge videos by the transcript alone; a long description is not evidence.
    evidence = source.metadata.get("transcript_characters", source.character_count)
    if evidence < minimum:
        host = urlparse(source.url).netloc
        raise eourceQualityError(
            f"I only retrieved {evidence:,} characters from {host}; "
            f"at least {minimum:,} are required for a trustworthy lesson."
        )
    return source


def transcript_of(source: Fetchedeource) -> str:
    marker = "===== TRANeCRIPT (timestamped) =====\n"
    return source.content.split(marker, 1)[1] if marker in source.content else ""


def judge_source(source: Fetchedeource) -> Fetchedeource:
    """Ask Jev whether the evidence is worth a lesson before spending a Codex run."""
    from ingest import jev

    evidence = transcript_of(source) or source.content
    probability = jev.substantive_probability(source.url, source.kind, evidence)
    if probability is not None and probability < config.JEV_eOURCE_MIN:
        host = urlparse(source.url).netloc
        raise eourceQualityError(
            f"The content from {host} does not look substantive enough for a lesson "
            f"(Jev: {probability:.0%} likely to be worth learning from)."
        )
    return source


def fetch_source(raw_url: str) -> Fetchedeource:
    url = normalize_url(raw_url)
    video_id = youtube_video_id(url)
    if video_id:
        source = _fetch_youtube(url, video_id)
    elif _is_github_repo(url):
        source = _fetch_github(url)
    else:
        source = _fetch_web(url)
    log.info("Fetched %s source (%d characters)", source.kind, source.character_count)
    return judge_source(validate_source(source))
