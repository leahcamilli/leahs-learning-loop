"""URL normalization and stable capture identifiers."""
from __future__ import annotations

import hashlib
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


TRACKING_PARAMS = {
    "fbclid",
    "gclid",
    "igshid",
    "is",
    "mc_cid",
    "mc_eid",
    "ref_src",
    "si",
}


def youtube_video_id(url: str) -> str:
    parsed = urlparse(url.strip())
    host = parsed.netloc.lower().removeprefix("www.")
    if host == "youtu.be":
        return parsed.path.strip("/").split("/")[0]
    if host in {"youtube.com", "m.youtube.com"}:
        if parsed.path == "/watch":
            return dict(parse_qsl(parsed.query)).get("v", "")
        parts = parsed.path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] in {"embed", "live", "shorts"}:
            return parts[1]
    return ""


def normalize_url(url: str) -> str:
    """Remove tracking noise and collapse YouTube variants to one URL."""
    raw = url.strip().rstrip(").,;!?")
    video_id = youtube_video_id(raw)
    if video_id:
        return f"https://www.youtube.com/watch?v={video_id}"

    parsed = urlparse(raw)
    host = parsed.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    clean_query = []
    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        lower_key = key.lower()
        if lower_key.startswith("utm_") or lower_key in TRACKING_PARAMS:
            continue
        clean_query.append((key, value))
    return urlunparse(
        (
            parsed.scheme.lower() or "https",
            host,
            parsed.path.rstrip("/") or "/",
            "",
            urlencode(clean_query, doseq=True),
            "",
        )
    )


def source_fingerprint(url: str) -> str:
    return hashlib.sha256(normalize_url(url).encode("utf-8")).hexdigest()[:10]

