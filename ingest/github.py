"""Idempotent publishing to the canonical Leah's Learning Loop Markdown collection."""
from __future__ import annotations

import base64
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

from ingest import config
from ingest.urls import normalize_url


API = "https://api.github.com"
PAGES_PATH = "wiki/pages"


@dataclass(frozen=True)
class PublishResult:
    page_id: str
    path: str
    site_url: str
    duplicate: bool = False


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {config.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")[:72] or "untitled"


def _site_url(page_id: str) -> str:
    return f"{config.SITE_URL.rstrip('/')}/#{page_id}"


def build_page_id(title: str, fingerprint: str, date: str) -> str:
    return f"{date}-{_slugify(title)}-{fingerprint}"


def _find_local_source(source_url: str) -> PublishResult | None:
    """Cover legacy pages created before URL fingerprints were added."""
    normalized_source = normalize_url(source_url)
    pages = Path(config.REPO_ROOT) / PAGES_PATH
    for path in pages.glob("*.md"):
        head = "\n".join(path.read_text(encoding="utf-8", errors="replace").splitlines()[:20])
        match = re.search(r'^source:\s*"?([^"\n]+)"?\s*$', head, re.MULTILINE)
        if match and normalize_url(match.group(1)) == normalized_source:
            return PublishResult(path.stem, str(path.relative_to(config.REPO_ROOT)), _site_url(path.stem), True)
    return None


def find_existing(fingerprint: str, source_url: str = "") -> PublishResult | None:
    if source_url:
        local_match = _find_local_source(source_url)
        if local_match:
            return local_match

    response = requests.get(
        f"{API}/repos/{config.GITHUB_REPOSITORY}/git/trees/{config.GITHUB_BRANCH}",
        params={"recursive": "1"},
        headers=_headers(),
        timeout=30,
    )
    response.raise_for_status()
    suffix = f"-{fingerprint}.md"
    for item in response.json().get("tree", []):
        path = item.get("path", "")
        if path.startswith(f"{PAGES_PATH}/") and path.endswith(suffix):
            page_id = path.rsplit("/", 1)[-1].removesuffix(".md")
            return PublishResult(page_id, path, _site_url(page_id), duplicate=True)
    return None


def publish_markdown(
    *,
    title: str,
    markdown: str,
    fingerprint: str,
    date: str | None = None,
    check_existing: bool = True,
) -> PublishResult:
    if check_existing:
        existing = find_existing(fingerprint)
        if existing:
            return existing

    capture_date = date or datetime.now(ZoneInfo(config.CAPTURE_TIMEZONE)).strftime(
        "%Y-%m-%d"
    )
    page_id = build_page_id(title, fingerprint, capture_date)
    path = f"{PAGES_PATH}/{page_id}.md"
    response = requests.put(
        f"{API}/repos/{config.GITHUB_REPOSITORY}/contents/{path}",
        headers=_headers(),
        timeout=30,
        json={
            "message": f"lesson: {title}",
            "content": base64.b64encode(markdown.encode("utf-8")).decode("ascii"),
            "branch": config.GITHUB_BRANCH,
        },
    )
    response.raise_for_status()
    return PublishResult(page_id, path, _site_url(page_id))


def github_healthcheck() -> str:
    response = requests.get(
        f"{API}/repos/{config.GITHUB_REPOSITORY}", headers=_headers(), timeout=15
    )
    response.raise_for_status()
    return response.json().get("full_name", config.GITHUB_REPOSITORY)
