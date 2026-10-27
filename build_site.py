"""
Build a static HTML second-brain site from wiki/pages/*.md.
Output goes to the leahs-learning-loop repo as a single index.html
that can be hosted on GitHub Pages.

Usage:
    python build_site.py
    python build_site.py --out C:/path/to/output/index.html
"""
from __future__ import annotations

import argparse
import json
import logging
import re
from datetime import datetime
from markdown import markdown
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
WIKI_PAGES = HERE / "wiki" / "pages"
DEFAULT_OUT = HERE / "index.html"

GENERIC_TAGS = {"ai", "technology", "software", "tools", "automation"}
TITLE_STOP_WORDS = {
    "about", "after", "before", "building", "from", "into", "practical",
    "the", "their", "this", "understanding", "using", "what", "when",
    "where", "which", "with", "without", "your",
}


# ── Frontmatter parser ────────────────────────────────────────────────────────

def _parse_page(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8", errors="replace")

    # Split frontmatter from body
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)", text, re.DOTALL)
    if not fm_match:
        body = text.strip()
        fm_raw, body = "", body
    else:
        fm_raw, body = fm_match.group(1), fm_match.group(2).strip()

    def _fm(key: str, default: str = "") -> str:
        m = re.search(rf'^{key}:\s*"?([^"\n]+)"?\s*$', fm_raw, re.MULTILINE)
        return m.group(1).strip() if m else default

    def _fm_tags(key: str = "tags") -> list[str]:
        m = re.search(rf'^{key}:\s*\[([^\]]*)\]', fm_raw, re.MULTILINE)
        if not m:
            return []
        return [t.strip().strip('"').strip("'") for t in m.group(1).split(",") if t.strip()]

    title = _fm("title") or path.stem
    date  = _fm("date")
    source = _fm("source")
    tags  = _fm_tags()

    # Some newer pages use a markdown H1 plus inline metadata lines instead of
    # YAML frontmatter. Parse that fallback shape so the site can render both.
    if not fm_match:
      lines = body.splitlines()
      if lines and lines[0].startswith("# "):
        inferred_title = lines[0][2:].strip()
        cursor = 1

        while cursor < len(lines) and not lines[cursor].strip():
          cursor += 1

        inferred_date = ""
        inferred_source = ""
        inferred_tags: list[str] = []
        metadata_found = False

        while cursor < len(lines):
          line = lines[cursor].strip()
          if not line:
            cursor += 1
            break
          if line.startswith("Date:"):
            inferred_date = line.partition(":")[2].strip()
            metadata_found = True
          elif line.startswith("Source:"):
            inferred_source = line.partition(":")[2].strip()
            metadata_found = True
          elif line.startswith("Tags:"):
            inferred_tags = [tag.strip() for tag in line.partition(":")[2].split(",") if tag.strip()]
            metadata_found = True
          else:
            break
          cursor += 1

        if metadata_found:
          while cursor < len(lines) and not lines[cursor].strip():
            cursor += 1

          title = inferred_title or title
          date = inferred_date or date
          source = inferred_source or source
          tags = inferred_tags or tags
          body = "\n".join(lines[cursor:]).strip()

    if not body:
        return None

    # If frontmatter source is "personal notes", try to pull the real URL out of
    # the ## Personal Notes section (e.g. "Source: https://...") before stripping it.
    if source in ("personal notes", ""):
        url_match = re.search(
            r"## Personal Notes\b.*?(?:^Source:\s*)(https?://[^\s\n]+)",
            body, re.DOTALL | re.MULTILINE,
        )
        if url_match:
            source = url_match.group(1).strip()

    # Strip the ## Personal Notes section (contains raw email body / Notion links)
    body = re.sub(r"\n## Personal Notes\b.*?(?=\n## |\Z)", "", body, flags=re.DOTALL).strip()

    source_type = _fm("source_type") or _infer_source_type(source)
    minutes, estimated = _learning_minutes(
        source_type,
        duration_seconds=_fm_int(fm_raw, "duration_seconds"),
        reading_minutes=_fm_int(fm_raw, "reading_minutes"),
        source_characters=_fm_int(fm_raw, "source_characters"),
    )

    return {
        "id":     path.stem,
        "title":  title,
        "date":   date,
        "tags":   tags,
        "source": source,
        "source_type": source_type,
        "channel": _fm("channel"),
        "published": _fm("published"),
        "duration_seconds": _fm_int(fm_raw, "duration_seconds"),
        "minutes": minutes,
        "minutes_estimated": estimated,
        "tldr": _extract_tldr(body),
        "topics": _fm_tags("topics"),
        "kind": _fm("kind"),
        "depth": _fm_int(fm_raw, "depth"),
        "actionability": _fm_int(fm_raw, "actionability"),
        "content": body,
    }


def _fm_int(fm_raw: str, key: str) -> int | None:
    m = re.search(rf'^{key}:\s*"?(\d+)"?\s*$', fm_raw, re.MULTILINE)
    return int(m.group(1)) if m else None


def _infer_source_type(source: str) -> str:
    if re.match(r"^https?://(www\.|m\.)?(youtube\.com|youtu\.be)/", source):
        return "youtube"
    if re.match(r"^https?://(www\.)?github\.com/[^/]+/[^/]+", source):
        return "github"
    return "web" if source.startswith("http") else "notes"


def _learning_minutes(
    source_type: str,
    *,
    duration_seconds: int | None,
    reading_minutes: int | None,
    source_characters: int | None,
) -> tuple[float | None, bool]:
    """Time the source takes to consume: video length, or reading time for text."""
    if duration_seconds:
        return round(duration_seconds / 60, 1), False
    if reading_minutes:
        return float(reading_minutes), False
    if source_type in {"web", "github"} and source_characters:
        # ~230 words/minute at ~5.7 characters per word, including spaces.
        return float(max(1, round(source_characters / 1300))), True
    return None, False


def _extract_tldr(body: str) -> str:
    m = re.search(r"^## TL;DR\s*\n+((?:>.*\n?)+)", body, re.MULTILINE)
    if not m:
        return ""
    return " ".join(line.lstrip(">").strip() for line in m.group(1).splitlines()).strip()


def _title_tokens(title: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", title.lower())
        if len(token) > 2 and token not in TITLE_STOP_WORDS
    }


def add_related_articles(articles: list[dict], limit: int = 4) -> None:
    """Attach low-cost, explainable connections based on tags and title concepts."""
    for article in articles:
        article_tags = {tag.lower() for tag in article.get("tags", [])}
        meaningful_tags = article_tags - GENERIC_TAGS
        article_topics = set(article.get("topics", []))
        title_tokens = _title_tokens(article.get("title", ""))
        candidates: list[tuple[int, str, dict, list[str]]] = []

        for candidate in articles:
            if candidate["id"] == article["id"]:
                continue
            candidate_tags = {tag.lower() for tag in candidate.get("tags", [])}
            shared_tags = sorted(meaningful_tags & (candidate_tags - GENERIC_TAGS))
            shared_topics = sorted(article_topics & set(candidate.get("topics", [])))
            shared_words = title_tokens & _title_tokens(candidate.get("title", ""))
            if not shared_tags and not shared_topics and len(shared_words) < 2:
                continue
            score = len(shared_topics) * 6 + len(shared_tags) * 5 + len(shared_words) * 2
            shared_tags = sorted(set(shared_topics) | set(shared_tags))
            candidates.append((score, candidate.get("date", ""), candidate, shared_tags))

        candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
        article["related"] = [
            {
                "id": candidate["id"],
                "title": candidate["title"],
                "date": candidate.get("date", ""),
                "shared_tags": shared_tags,
            }
            for _, _, candidate, shared_tags in candidates[:limit]
        ]


# ── HTML template ─────────────────────────────────────────────────────────────

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Leah's Learning Loop</title>
<link rel="icon" type="image/png" href="apple-touch-icon.png"/>
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png"/>
<meta name="apple-mobile-web-app-title" content="Leah's Learning Loop"/>
<meta name="apple-mobile-web-app-capable" content="yes"/>
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"/>
<script src="https://cdn.jsdelivr.net/npm/marked@9/marked.min.js"></script>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:        #0d1117;
    --sidebar:   #161b22;
    --border:    #30363d;
    --text:      #e6edf3;
    --muted:     #8b949e;
    --accent:    #58a6ff;
    --accent2:   #3fb950;
    --card-bg:   #161b22;
    --card-hover:#1f2937;
    --tag-bg:    #21262d;
    --code-bg:   #1c2128;
    --sidebar-w: 340px;
  }

  html, body { height: 100%; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); font-size: 15px; line-height: 1.6; }

  /* ── Layout ── */
  .app { display: flex; height: 100vh; overflow: hidden; }

  /* ── Sidebar ── */
  .sidebar { width: var(--sidebar-w); min-width: var(--sidebar-w); background: var(--sidebar); border-right: 1px solid var(--border); display: flex; flex-direction: column; overflow: hidden; }

  .sidebar-header { padding: 20px 16px 12px; border-bottom: 1px solid var(--border); }
  .sidebar-header h1 { font-size: 16px; font-weight: 600; color: var(--text); letter-spacing: 0.3px; display: flex; align-items: center; gap: 10px; }
  .sidebar-header .brand-image { width: 44px; height: 44px; flex: 0 0 44px; object-fit: cover; border-radius: 50%; background: #fff; }
  .sidebar-header .count { font-size: 12px; color: var(--muted); margin-top: 2px; }

  .search-wrap { padding: 12px 16px; border-bottom: 1px solid var(--border); }
  .search-wrap input {
    width: 100%; background: var(--bg); border: 1px solid var(--border);
    border-radius: 6px; color: var(--text); padding: 7px 12px; font-size: 13px;
    outline: none; transition: border-color .15s;
  }
  .search-wrap input:focus { border-color: var(--accent); }
  .search-wrap input::placeholder { color: var(--muted); }

  .tags-wrap { padding: 10px 16px; border-bottom: 1px solid var(--border); display: flex; flex-wrap: wrap; gap: 6px; max-height: 90px; overflow-y: auto; }
  .tag-pill {
    background: var(--tag-bg); color: var(--muted); border: 1px solid var(--border);
    border-radius: 20px; padding: 2px 10px; font-size: 11px; cursor: pointer;
    transition: all .15s; user-select: none; white-space: nowrap;
  }
  .tag-pill:hover { border-color: var(--accent); color: var(--accent); }
  .tag-pill.topic, .art-tag.topic { border-color: var(--accent2); }
  .art-profile { margin-top: 8px; font-size: 13px; color: var(--accent2); }
  .tag-pill.active { background: var(--accent); color: #0d1117; border-color: var(--accent); font-weight: 600; }

  .article-list { flex: 1; overflow-y: auto; padding: 8px 0; }
  .article-list::-webkit-scrollbar { width: 4px; }
  .article-list::-webkit-scrollbar-track { background: transparent; }
  .article-list::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

  .article-card {
    padding: 12px 16px; cursor: pointer; border-left: 3px solid transparent;
    transition: background .12s, border-color .12s;
  }
  .article-card:hover { background: var(--card-hover); }
  .article-card.active { border-left-color: var(--accent); background: var(--card-hover); }
  .article-card .card-title { font-size: 13px; font-weight: 500; color: var(--text); line-height: 1.4; margin-bottom: 4px; }
  .article-card .card-meta { font-size: 11px; color: var(--muted); display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
  .article-card .card-tags { display: flex; gap: 4px; flex-wrap: wrap; margin-top: 5px; }
  .article-card .card-tag { background: var(--tag-bg); color: var(--muted); border-radius: 3px; padding: 1px 6px; font-size: 10px; }

  .no-results { padding: 24px 16px; color: var(--muted); font-size: 13px; text-align: center; }

  /* ── Main content ── */
  .main { flex: 1; overflow-y: auto; display: flex; flex-direction: column; }
  .main::-webkit-scrollbar { width: 6px; }
  .main::-webkit-scrollbar-track { background: transparent; }
  .main::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

  .welcome { flex: 1; overflow-y: auto; padding: 40px 48px; width: 100%; }

  .article-view { padding: 40px 48px; max-width: 820px; width: 100%; }

  .article-view .art-header { margin-bottom: 28px; padding-bottom: 20px; border-bottom: 1px solid var(--border); }
  .article-view .art-title { font-size: 26px; font-weight: 700; color: var(--text); line-height: 1.3; margin-bottom: 10px; }
  .article-view .art-source { margin-bottom: 8px; }
  .article-view .art-source a { color: var(--accent); text-decoration: none; font-size: 13px; }
  .article-view .art-source a:hover { text-decoration: underline; }
  .article-view .art-meta { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; font-size: 13px; color: var(--muted); }
  .art-tags { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 10px; }
  .art-tag { background: var(--tag-bg); color: var(--accent); border: 1px solid var(--border); border-radius: 20px; padding: 2px 10px; font-size: 12px; cursor: pointer; }
  .art-tag:hover { background: var(--accent); color: #0d1117; }

  .related-notes { margin-top: 36px; padding-top: 20px; border-top: 1px solid var(--border); }
  .related-notes h2 { font-size: 17px; margin-bottom: 10px; }
  .related-note { display: block; width: 100%; padding: 10px 12px; margin: 6px 0; text-align: left; color: var(--text); background: var(--card-bg); border: 1px solid var(--border); border-radius: 6px; cursor: pointer; }
  .related-note:hover { border-color: var(--accent); background: var(--card-hover); }
  .related-note-title { display: block; font-size: 13px; font-weight: 600; }
  .related-note-reason { display: block; margin-top: 2px; font-size: 11px; color: var(--muted); }

  /* ── Markdown styles ── */
  .md-body h1, .md-body h2, .md-body h3, .md-body h4 { color: var(--text); margin: 1.5em 0 .6em; line-height: 1.3; }
  .md-body h1 { font-size: 22px; } .md-body h2 { font-size: 18px; border-bottom: 1px solid var(--border); padding-bottom: 6px; }
  .md-body h3 { font-size: 16px; } .md-body h4 { font-size: 14px; color: var(--muted); }
  .md-body p { margin: .8em 0; color: var(--text); }
  .md-body a { color: var(--accent); text-decoration: none; }
  .md-body a:hover { text-decoration: underline; }
  .md-body ul, .md-body ol { margin: .8em 0 .8em 1.4em; }
  .md-body li { margin: .3em 0; }
  .md-body strong { color: var(--text); font-weight: 600; }
  .md-body em { color: var(--muted); font-style: italic; }
  .md-body code { background: var(--code-bg); border: 1px solid var(--border); border-radius: 4px; padding: 1px 6px; font-size: 13px; font-family: "SFMono-Regular", Consolas, monospace; color: #f0883e; }
  .md-body pre { background: var(--code-bg); border: 1px solid var(--border); border-radius: 8px; padding: 16px; overflow-x: auto; margin: 1em 0; }
  .md-body pre code { background: none; border: none; padding: 0; color: var(--text); font-size: 13px; }
  .md-body blockquote { border-left: 3px solid var(--accent); margin: 1em 0; padding: 4px 16px; color: var(--muted); background: var(--code-bg); border-radius: 0 6px 6px 0; }
  .md-body table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 14px; }
  .md-body th, .md-body td { border: 1px solid var(--border); padding: 8px 12px; }
  .md-body th { background: var(--code-bg); font-weight: 600; }
  .md-body hr { border: none; border-top: 1px solid var(--border); margin: 2em 0; }

  /* ── Sidebar tools ── */
  .sidebar-actions { display: flex; gap: 6px; margin-top: 10px; }
  .tool-btn { flex: 1; background: var(--bg); color: var(--text); border: 1px solid var(--border); border-radius: 6px; padding: 5px 8px; font-size: 12px; cursor: pointer; }
  .tool-btn:hover, .tool-btn.active { border-color: var(--accent); color: var(--accent); }
  .type-filter { display: flex; gap: 4px; padding: 8px 16px 0; }
  .type-btn { flex: 1; background: none; border: 1px solid var(--border); color: var(--muted); border-radius: 6px; padding: 3px 0; font-size: 11px; cursor: pointer; }
  .type-btn.active { background: var(--tag-bg); color: var(--text); border-color: var(--muted); }
  .card-tldr { font-size: 12px; color: var(--muted); margin: 2px 0 4px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
  .type-badge { font-size: 10px; letter-spacing: .3px; text-transform: uppercase; color: var(--muted); border: 1px solid var(--border); border-radius: 3px; padding: 0 5px; }

  /* ── Article extras ── */
  .video-embed { position: relative; margin: 0 0 24px; max-width: 480px; aspect-ratio: 16 / 9; background: #000; border-radius: 8px; overflow: hidden; border: 1px solid var(--border); }
  .video-embed img, .video-embed iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; object-fit: cover; }
  .video-embed button { position: absolute; inset: 0; width: 100%; background: none; border: 0; cursor: pointer; }
  .video-embed .play { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); background: rgba(13,17,23,.85); color: var(--text); border: 1px solid var(--border); border-radius: 999px; padding: 10px 18px; font-size: 14px; }
  .md-body blockquote.tldr { border-left-color: var(--accent2); color: var(--text); font-size: 16px; padding: 10px 16px; }
  .md-body a.moment { font-family: "SFMono-Regular", Consolas, monospace; font-size: 13px; }
  .md-body details { background: var(--card-bg); border: 1px solid var(--border); border-radius: 6px; padding: 8px 12px; margin: 8px 0; }
  .md-body details summary { cursor: pointer; font-weight: 600; }
  .md-body details[open] summary { margin-bottom: 6px; }

  /* ── Learning dashboard ── */
  .dash { padding: 40px 48px; max-width: 980px; width: 100%; }
  .dash h1 { font-size: 24px; margin-bottom: 4px; }
  .dash .sub { color: var(--muted); font-size: 13px; margin-bottom: 20px; }
  .dash .sub select { background: var(--bg); color: var(--text); border: 1px solid var(--border); border-radius: 4px; font-size: 12px; padding: 1px 4px; }
  .tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin-bottom: 28px; }
  .tile { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 14px 16px; }
  .tile .label { font-size: 12px; color: var(--muted); }
  .tile .value { font-size: 26px; font-weight: 700; margin-top: 2px; font-variant-numeric: tabular-nums; }
  .tile .hint { font-size: 11px; color: var(--muted); margin-top: 2px; }
  .panel { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 16px; margin-bottom: 16px; }
  .panel h2 { font-size: 14px; margin-bottom: 12px; }
  .panels { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }
  .cols { display: flex; align-items: flex-end; gap: 2px; height: 160px; border-bottom: 1px solid var(--border); }
  .col { flex: 1; height: 100%; display: flex; align-items: flex-end; position: relative; cursor: default; }
  .col .bar { width: 100%; background: var(--accent); border-radius: 4px 4px 0 0; min-height: 0; }
  .col:hover .bar { filter: brightness(1.25); }
  .col-labels { display: flex; gap: 2px; margin-top: 4px; }
  .col-labels span { flex: 1; font-size: 10px; color: var(--muted); text-align: center; white-space: nowrap; overflow: hidden; }
  .hbar { display: grid; grid-template-columns: minmax(90px, 38%) 1fr auto; gap: 8px; align-items: center; font-size: 12px; margin: 5px 0; }
  .hbar .name { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .hbar .track { height: 10px; }
  .hbar .fill { height: 100%; background: var(--accent); border-radius: 0 4px 4px 0; }
  .hbar .val { color: var(--muted); font-variant-numeric: tabular-nums; }
  .hbar.clickable { cursor: pointer; } .hbar.clickable:hover .name { color: var(--accent); }
  .tip { position: fixed; pointer-events: none; background: #010409; border: 1px solid var(--border); border-radius: 6px; padding: 6px 9px; font-size: 12px; color: var(--text); z-index: 10; display: none; }
  .note { font-size: 12px; color: var(--muted); margin-top: 8px; }
  .note code { background: var(--code-bg); padding: 1px 5px; border-radius: 4px; }

  /* ── Sidebar footer ── */
  .sidebar-footer { padding: 12px 16px; border-top: 1px solid var(--border); font-size: 12px; color: var(--muted); display: flex; flex-direction: column; gap: 6px; }
  .sidebar-footer a { color: var(--muted); text-decoration: none; display: flex; align-items: center; gap: 6px; transition: color .15s; }
  .sidebar-footer a:hover { color: var(--accent); }
  .sidebar-footer-row { display: flex; gap: 12px; }

  /* ── Mobile back button ── */
  .mobile-back { display: none; }

  /* ── Responsive ── */
  @media (max-width: 768px) {
    .app { flex-direction: column; height: 100dvh; }

    /* Default mobile: show sidebar full-screen, hide main */
    .sidebar {
      width: 100%; min-width: unset; height: 100%;
      border-right: none; border-bottom: none;
      display: flex;
    }
    .main { display: none; }

    /* When an article is open: hide sidebar, show main full-screen */
    .app.article-open .sidebar { display: none; }
    .app.article-open .main { display: flex; flex-direction: column; height: 100%; overflow-y: auto; }

    /* Back button */
    .mobile-back {
      display: flex; align-items: center; gap: 8px;
      padding: 12px 16px; border-bottom: 1px solid var(--border);
      background: var(--sidebar); color: var(--accent);
      font-size: 14px; cursor: pointer; flex-shrink: 0;
    }
    .mobile-back:hover { color: var(--text); }

    .article-view, .dash { padding: 20px 16px; }
    .article-view .art-title { font-size: 20px; }
  }
</style>
</head>
<body>
<div class="app">
  <aside class="sidebar">
    <div class="sidebar-header">
      <h1><img class="brand-image" src="apple-touch-icon.png" alt=""/> Leah's Learning Loop</h1>
      <div class="count" id="count"></div>
      <div class="sidebar-actions">
        <button class="tool-btn" id="stats-btn" title="Learning time dashboard">&#128202; Learning</button>
        <button class="tool-btn" id="resurface-btn" title="Open a random note you captured 2+ weeks ago">&#127922; Resurface</button>
      </div>
    </div>
    <div class="search-wrap">
      <input id="search" type="text" placeholder="Search articles..." autocomplete="off"/>
    </div>
    <div class="type-filter" id="types"></div>
    <div class="tags-wrap" id="tags"></div>
    <div class="article-list" id="list"></div>
    <div class="sidebar-footer">
      <a href="https://github.com/leahcamilli/leahs-learning-loop" target="_blank" rel="noopener">
        <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
        View on GitHub
      </a>
      <div class="sidebar-footer-row">
        <a href="https://steviesimsii.github.io/Deepwater_Daily/" target="_blank" rel="noopener">
          <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C8 0 2.5 6.5 2.5 10a5.5 5.5 0 0011 0C13.5 6.5 8 0 8 0z"/></svg>
          Deepwater
        </a>
        <a href="https://steviesimsii.github.io/AiNewsDaily/" target="_blank" rel="noopener">
          <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0l1.6 5.4 5.4 1.6-5.4 1.6L8 14l-1.6-5.4L1 7l5.4-1.6z"/></svg>
          AI &amp; ML
        </a>
        <a href="https://steviesimsii.github.io/Nola_Daily/" target="_blank" rel="noopener">
          <svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor"><path d="M8 1a7 7 0 100 14A7 7 0 008 1zM0 8a8 8 0 1116 0A8 8 0 010 8zm9-3.5a1 1 0 11-2 0 1 1 0 012 0zm-.25 3a.75.75 0 00-1.5 0v3a.75.75 0 001.5 0v-3z"/></svg>
          Nola Daily
        </a>
      </div>
    </div>
  </aside>
  <main class="main" id="main">
    <div class="welcome md-body" id="welcome-content">__README_HTML__</div>
  </main>
</div>

<div class="tip" id="tip"></div>
<script id="articles-data" type="application/json">__ARTICLES_JSON__</script>

<script>
const ARTICLES = JSON.parse(document.getElementById("articles-data").textContent);

// ── State ─────────────────────────────────────────────────────────────────────
let activeId     = null;
let activeTag    = null;
let activeType   = null;
let activeKind   = null;
const KINDS = { tutorial: "Tutorial", "deep-dive": "Deep dive", news: "News", opinion: "Opinion", demo: "Demo", interview: "Interview" };
const DEPTH = ["Headline", "Overview", "Practical", "Expert"];
const ACTION = ["Awareness", "Ideas for later", "Try this week", "Apply today"];
const topicsOf = a => (a.topics && a.topics.length ? a.topics : a.tags) || [];
let searchQuery  = "";
const TYPES = { youtube: "Video", web: "Article", github: "Repo", notes: "Note" };
const WELCOME_HTML = document.getElementById("main").innerHTML;

// ── Tag index ─────────────────────────────────────────────────────────────────
const tagCounts = {}, topicCounts = {};
ARTICLES.forEach(a => {
  (a.tags || []).forEach(t => { tagCounts[t] = (tagCounts[t] || 0) + 1; });
  (a.topics || []).forEach(t => { topicCounts[t] = (topicCounts[t] || 0) + 1; });
});
const byCount = counts => Object.entries(counts).sort((a, b) => b[1] - a[1]).map(e => e[0]);
const canonicalTopics = new Set(Object.keys(topicCounts));
const allTags = [
  ...byCount(topicCounts),
  ...byCount(tagCounts).filter(t => tagCounts[t] >= 4 && !canonicalTopics.has(t)),
];

// ── Render tags ───────────────────────────────────────────────────────────────
function renderTags() {
  const wrap = document.getElementById("tags");
  wrap.innerHTML = allTags.map(t =>
    `<span class="tag-pill${activeTag === t ? " active" : ""}${canonicalTopics.has(t) ? " topic" : ""}" data-tag="${t}">${t}</span>`
  ).join("");
  wrap.querySelectorAll(".tag-pill").forEach(el => el.addEventListener("click", () => {
    activeTag = activeTag === el.dataset.tag ? null : el.dataset.tag;
    renderTags(); renderList();
  }));
}

// ── Type filter ───────────────────────────────────────────────────────────────
function renderTypes() {
  const present = Object.keys(TYPES).filter(t => ARTICLES.some(a => a.source_type === t));
  const wrap = document.getElementById("types");
  wrap.innerHTML = [null, ...present].map(t =>
    `<button class="type-btn${activeType === t ? " active" : ""}" data-type="${t || ""}">${t ? TYPES[t] + "s" : "All"}</button>`
  ).join("");
  wrap.querySelectorAll(".type-btn").forEach(el => el.addEventListener("click", () => {
    activeType = el.dataset.type || null;
    renderTypes(); renderList();
  }));
}

// ── Filter articles ───────────────────────────────────────────────────────────
function filtered() {
  const q = searchQuery.toLowerCase();
  return ARTICLES.filter(a => {
    if (activeTag && !(a.tags || []).includes(activeTag) && !(a.topics || []).includes(activeTag)) return false;
    if (activeType && a.source_type !== activeType) return false;
    if (activeKind && a.kind !== activeKind) return false;
    if (q && ![a.title, a.content, a.channel || ""].some(text => text.toLowerCase().includes(q))) return false;
    return true;
  });
}

// ── Render list ───────────────────────────────────────────────────────────────
function renderList() {
  const list = document.getElementById("list");
  const items = filtered();
  document.getElementById("count").innerHTML = `${items.length} of ${ARTICLES.length} articles` +
    (activeKind ? ` · ${KINDS[activeKind]} <a href="#" id="clear-kind">clear</a>` : "");
  const clearKind = document.getElementById("clear-kind");
  if (clearKind) clearKind.addEventListener("click", e => { e.preventDefault(); activeKind = null; renderList(); });
  if (!items.length) { list.innerHTML = `<div class="no-results">No articles found</div>`; return; }
  list.innerHTML = items.map(a => `
    <div class="article-card${a.id === activeId ? " active" : ""}" data-id="${a.id}">
      <div class="card-title">${escHtml(a.title)}</div>
      ${a.tldr ? `<div class="card-tldr">${escHtml(a.tldr)}</div>` : ""}
      <div class="card-meta">
        <span class="type-badge">${TYPES[a.source_type] || "Note"}</span>
        ${a.kind && KINDS[a.kind] ? `<span class="type-badge">${KINDS[a.kind]}</span>` : ""}
        <span>${fmtDate(a.date)}</span>
        ${a.channel ? `<span>· ${escHtml(a.channel)}</span>`
          : a.source && a.source !== "personal notes" ? `<span>· ${escHtml(friendlySource(a.source))}</span>` : ""}
        ${a.minutes ? `<span>· ${timeLabel(a)}</span>` : ""}
      </div>
      ${a.tags && a.tags.length ? `<div class="card-tags">${a.tags.map(t => `<span class="card-tag">${t}</span>`).join("")}</div>` : ""}
    </div>`).join("");
  list.querySelectorAll(".article-card").forEach(el => el.addEventListener("click", () => openArticle(el.dataset.id)));
}

// ── Mobile helpers ────────────────────────────────────────────────────────────
function isMobile() { return window.innerWidth <= 768; }

function showList() {
  activeId = null;
  document.getElementById("stats-btn").classList.remove("active");
  document.querySelector(".app").classList.remove("article-open");
  window.location.hash = "";
  renderList();
}

// ── Open article ──────────────────────────────────────────────────────────────
function openArticle(id) {
  const a = ARTICLES.find(x => x.id === id);
  if (!a) return;
  activeId = id;
  document.getElementById("stats-btn").classList.remove("active");
  renderList();
  const videoId = youtubeId(a.source);

  const sourceHtml = a.source && a.source !== "personal notes"
    ? `<div class="art-source"><a href="${escHtml(a.source)}" target="_blank" rel="noopener">↗ Link to Source</a></div>`
    : "";

  const tagsHtml = [...(a.topics || []).map(t => [t, " topic"]), ...(a.tags || []).filter(t => !(a.topics || []).includes(t)).map(t => [t, ""])]
    .map(([t, cls]) => `<span class="art-tag${cls}" data-tag="${t}">${t}</span>`).join("");
  const profile = [a.kind && KINDS[a.kind], a.depth != null && DEPTH[a.depth], a.actionability != null && ACTION[a.actionability]].filter(Boolean);

  const bodyHtml = marked.parse(a.content || "");

  const relatedHtml = (a.related || []).length
    ? `<div class="related-notes"><h2>Related Notes</h2>${a.related.map(item => `
        <button class="related-note" data-related-id="${escHtml(item.id)}">
          <span class="related-note-title">${escHtml(item.title)}</span>
          <span class="related-note-reason">${item.shared_tags.length ? `Shared topics: ${item.shared_tags.map(escHtml).join(", ")}` : "Related concepts"}</span>
        </button>`).join("")}</div>`
    : "";

  const backBtn = isMobile()
    ? `<div class="mobile-back" id="back-btn">&#8592; All Articles</div>`
    : "";

  document.getElementById("main").innerHTML = `
    ${backBtn}
    <div class="article-view">
      <div class="art-header">
        <div class="art-title">${escHtml(a.title)}</div>
        ${sourceHtml}
        <div class="art-meta">
          <span class="type-badge">${TYPES[a.source_type] || "Note"}</span>
          <span>Captured ${fmtDate(a.date)}</span>
          ${a.channel ? `<span>${escHtml(a.channel)}</span>` : ""}
          ${a.minutes ? `<span>&#9201; ${timeLabel(a)}</span>` : ""}
          ${a.published ? `<span>Published ${fmtDate(a.published)}</span>` : ""}
        </div>
        ${profile.length ? `<div class="art-profile" title="Judged by TypeSafe Jev">${profile.join(" · ")}</div>` : ""}
        ${tagsHtml ? `<div class="art-tags">${tagsHtml}</div>` : ""}
      </div>
      ${videoId ? `<div class="video-embed" id="video">
          <img src="https://i.ytimg.com/vi/${encodeURIComponent(videoId)}/hqdefault.jpg" alt="" loading="lazy"/>
          <button aria-label="Play video"><span class="play">&#9654; Play here</span></button>
        </div>` : ""}
      <div class="md-body">${bodyHtml}</div>
      ${relatedHtml}
    </div>`;

  if (isMobile()) {
    document.querySelector(".app").classList.add("article-open");
    document.getElementById("back-btn").addEventListener("click", showList);
  }

  document.getElementById("main").querySelectorAll(".art-tag").forEach(el =>
    el.addEventListener("click", () => {
      activeTag = activeTag === el.dataset.tag ? null : el.dataset.tag;
      renderTags(); renderList();
    })
  );

  document.getElementById("main").querySelectorAll(".related-note").forEach(el =>
    el.addEventListener("click", () => openArticle(el.dataset.relatedId))
  );

  // Highlight the TL;DR and let key moments seek the embedded player.
  document.getElementById("main").querySelectorAll(".md-body h2").forEach(h => {
    if (h.textContent.trim() === "TL;DR" && h.nextElementSibling && h.nextElementSibling.tagName === "BLOCKQUOTE")
      h.nextElementSibling.classList.add("tldr");
  });
  if (videoId) {
    document.querySelector("#video button").addEventListener("click", () => playAt(videoId, 0));
    document.getElementById("main").querySelectorAll(".md-body a[href]").forEach(link => {
      const m = link.getAttribute("href").match(/[?&]t=(\d+)s?/);
      if (!m || youtubeId(link.href) !== videoId) return;
      link.classList.add("moment");
      link.addEventListener("click", e => { e.preventDefault(); playAt(videoId, +m[1]); });
    });
  }

  window.location.hash = id;
  document.getElementById("main").scrollTop = 0;
}

function playAt(videoId, seconds) {
  const box = document.getElementById("video");
  box.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${encodeURIComponent(videoId)}?autoplay=1&start=${seconds}"
    allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen title="Video player"></iframe>`;
  box.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// ── Learning dashboard ────────────────────────────────────────────────────────
function storageGet(key, fallback) {
  try { return localStorage.getItem(key) || fallback; } catch { return fallback; }
}
function storageSet(key, value) {
  try { localStorage.setItem(key, value); } catch {}
}

function effectiveMinutes(a, speed) {
  if (!a.minutes) return 0;
  return a.source_type === "youtube" ? a.minutes / speed : a.minutes;
}

function fmtHours(minutes) {
  if (minutes < 60) return `${Math.round(minutes)}m`;
  const h = Math.floor(minutes / 60), m = Math.round(minutes % 60);
  return m ? `${h}h ${m}m` : `${h}h`;
}

function weekStart(dateStr) {
  const d = new Date(dateStr + "T00:00:00");
  d.setDate(d.getDate() - ((d.getDay() + 6) % 7));
  return d;
}
function isoDay(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

function hbars(rows, total, opts = {}) {
  if (!rows.length) return `<div class="note">Nothing yet.</div>`;
  const max = Math.max(...rows.map(r => r.value)) || 1;
  return rows.map(r => `
    <div class="hbar${opts.clickable ? " clickable" : ""}" data-key="${escHtml(r.key)}" data-tip="${escHtml(r.tip)}">
      <span class="name">${escHtml(r.label)}</span>
      <span class="track"><div class="fill" style="width:${(r.value / max * 100).toFixed(1)}%"></div></span>
      <span class="val">${escHtml(r.valueLabel)}</span>
    </div>`).join("");
}

function groupMinutes(items, keyFn, speed) {
  const map = {};
  items.forEach(a => (keyFn(a) || []).forEach(k => {
    map[k] = map[k] || { minutes: 0, count: 0 };
    map[k].minutes += effectiveMinutes(a, speed);
    map[k].count += 1;
  }));
  return Object.entries(map).map(([key, v]) => ({ key, ...v }));
}

function showStats() {
  activeId = null;
  renderList();
  document.getElementById("stats-btn").classList.add("active");
  const speed = parseFloat(storageGet("sb-speed", "1")) || 1;
  const timed = ARTICLES.filter(a => a.minutes);
  const total = timed.reduce((sum, a) => sum + effectiveMinutes(a, speed), 0);

  const today = new Date();
  const thisWeek = isoDay(weekStart(isoDay(today)));
  const monthPrefix = isoDay(today).slice(0, 7);
  const sumWhere = pred => timed.filter(pred).reduce((sum, a) => sum + effectiveMinutes(a, speed), 0);
  const weekMinutes = sumWhere(a => a.date && isoDay(weekStart(a.date)) === thisWeek);
  const monthMinutes = sumWhere(a => (a.date || "").startsWith(monthPrefix));

  // Last 12 weeks, oldest first.
  const weeks = [];
  for (let i = 11; i >= 0; i--) {
    const d = weekStart(isoDay(today)); d.setDate(d.getDate() - 7 * i);
    weeks.push({ key: isoDay(d), minutes: 0, count: 0 });
  }
  ARTICLES.forEach(a => {
    if (!a.date) return;
    const w = weeks.find(x => x.key === isoDay(weekStart(a.date)));
    if (w) { w.minutes += effectiveMinutes(a, speed); w.count += 1; }
  });
  const activeWeeks = new Set(ARTICLES.filter(a => a.date).map(a => isoDay(weekStart(a.date))));
  let streak = 0;
  for (const d = weekStart(isoDay(today)); activeWeeks.has(isoDay(d)); d.setDate(d.getDate() - 7)) streak++;
  const maxWeek = Math.max(...weeks.map(w => w.minutes)) || 1;
  const weekLabel = k => { const [, m, d] = k.split("-"); return `${+m}/${+d}`; };

  const byType = groupMinutes(ARTICLES, a => [a.source_type], speed)
    .sort((a, b) => b.minutes - a.minutes)
    .map(r => ({ key: r.key, label: TYPES[r.key] + "s", value: r.minutes, valueLabel: fmtHours(r.minutes),
      tip: `${r.count} captured · ${fmtHours(r.minutes)} of known time` }));
  const channels = groupMinutes(ARTICLES.filter(a => a.channel), a => [a.channel], speed)
    .sort((a, b) => b.minutes - a.minutes).slice(0, 8)
    .map(r => ({ key: r.key, label: r.key, value: r.minutes, valueLabel: fmtHours(r.minutes), tip: `${r.count} videos` }));
  const kinds = groupMinutes(ARTICLES.filter(a => KINDS[a.kind]), a => [a.kind], speed)
    .filter(r => r.minutes > 0).sort((a, b) => b.minutes - a.minutes)
    .map(r => ({ key: "kind:" + r.key, label: KINDS[r.key], value: r.minutes, valueLabel: fmtHours(r.minutes), tip: `${r.count} notes` }));
  const profiled = ARTICLES.filter(a => a.kind).length;
  const topics = groupMinutes(ARTICLES, topicsOf, speed)
    .filter(r => r.minutes > 0)
    .sort((a, b) => b.minutes - a.minutes).slice(0, 10)
    .map(r => ({ key: r.key, label: r.key, value: r.minutes, valueLabel: fmtHours(r.minutes), tip: `${r.count} notes` }));

  const videos = ARTICLES.filter(a => a.source_type === "youtube");
  const videosTimed = videos.filter(a => a.duration_seconds).length;
  const estimated = timed.filter(a => a.minutes_estimated).length;

  const backBtn = isMobile() ? `<div class="mobile-back" id="back-btn">&#8592; All Articles</div>` : "";
  document.getElementById("main").innerHTML = `
    ${backBtn}
    <div class="dash">
      <h1>Learning time</h1>
      <div class="sub">Time is the length of what you captured: video runtime, and reading time for articles and repos.
        I watch videos at <select id="speed">${[1, 1.25, 1.5, 1.75, 2].map(v =>
          `<option value="${v}"${v === speed ? " selected" : ""}>${v}×</option>`).join("")}</select></div>
      <div class="tiles">
        <div class="tile"><div class="label">Total learning time</div><div class="value">${fmtHours(total)}</div>
          <div class="hint">across ${timed.length} timed notes</div></div>
        <div class="tile"><div class="label">This week</div><div class="value">${fmtHours(weekMinutes)}</div>
          <div class="hint">${weeks[weeks.length - 1].count} captured</div></div>
        <div class="tile"><div class="label">This month</div><div class="value">${fmtHours(monthMinutes)}</div>
          <div class="hint">${ARTICLES.filter(a => (a.date || "").startsWith(monthPrefix)).length} captured</div></div>
        <div class="tile"><div class="label">Weekly streak</div><div class="value">${streak}</div>
          <div class="hint">consecutive weeks with a capture</div></div>
      </div>
      <div class="panel">
        <h2>Learning time per week</h2>
        <div class="cols">${weeks.map(w => `<div class="col" data-tip="Week of ${weekLabel(w.key)}: ${fmtHours(w.minutes)} · ${w.count} captured">
          <div class="bar" style="height:${(w.minutes / maxWeek * 100).toFixed(1)}%"></div></div>`).join("")}</div>
        <div class="col-labels">${weeks.map((w, i) => `<span>${i % 2 ? "" : weekLabel(w.key)}</span>`).join("")}</div>
      </div>
      <div class="panels">
        <div class="panel"><h2>By format</h2>${hbars(byType, total, { clickable: true })}</div>
        <div class="panel"><h2>Top channels</h2>${channels.length ? hbars(channels, total)
          : `<div class="note">Channels appear once video metadata is captured.</div>`}</div>
        <div class="panel"><h2>Top topics by time</h2>${hbars(topics, total, { clickable: true })}</div>
        <div class="panel"><h2>What kind of learning</h2>${kinds.length ? hbars(kinds, total, { clickable: true })
          : `<div class="note">Appears once lessons are profiled by Jev (<code>python -m ingest.backfill --jev-only</code>).</div>`}</div>
      </div>
      <div class="note">Coverage: ${videosTimed} of ${videos.length} videos have a known length${estimated ? `; ${estimated} article times are estimated from captured text` : ""}.
        ${profiled ? `${profiled} of ${ARTICLES.length} notes have Jev topics and profile.` : ""}
        ${videosTimed < videos.length ? `Fill the gaps on the capture host with <code>python -m ingest.backfill --metadata-only</code>.` : ""}</div>
    </div>`;

  const main = document.getElementById("main");
  main.scrollTop = 0;
  if (isMobile()) {
    document.querySelector(".app").classList.add("article-open");
    document.getElementById("back-btn").addEventListener("click", showList);
  }
  document.getElementById("speed").addEventListener("change", e => { storageSet("sb-speed", e.target.value); showStats(); });
  const tip = document.getElementById("tip");
  main.querySelectorAll("[data-tip]").forEach(el => {
    el.addEventListener("mousemove", e => {
      tip.textContent = el.dataset.tip; tip.style.display = "block";
      tip.style.left = Math.min(e.clientX + 12, window.innerWidth - tip.offsetWidth - 8) + "px";
      tip.style.top = (e.clientY + 12) + "px";
    });
    el.addEventListener("mouseleave", () => { tip.style.display = "none"; });
  });
  main.querySelectorAll(".panel .hbar.clickable").forEach(el => el.addEventListener("click", () => {
    tip.style.display = "none";
    if (TYPES[el.dataset.key]) { activeType = el.dataset.key; renderTypes(); }
    else if (el.dataset.key.startsWith("kind:")) { activeKind = el.dataset.key.slice(5); }
    else { activeTag = el.dataset.key; renderTags(); }
    renderList();
    if (isMobile()) showList();
  }));
  window.location.hash = "stats";
}

function resurface() {
  const cutoff = new Date(); cutoff.setDate(cutoff.getDate() - 14);
  const pool = ARTICLES.filter(a => a.date && a.date <= isoDay(cutoff));
  const choices = pool.length ? pool : ARTICLES;
  if (choices.length) openArticle(choices[Math.floor(Math.random() * choices.length)].id);
}

document.getElementById("stats-btn").addEventListener("click", showStats);
document.getElementById("resurface-btn").addEventListener("click", resurface);
document.addEventListener("keydown", e => {
  if (e.key === "/" && document.activeElement.tagName !== "INPUT" && document.activeElement.tagName !== "SELECT") {
    e.preventDefault(); document.getElementById("search").focus();
  }
});

// ── Search ────────────────────────────────────────────────────────────────────
document.getElementById("search").addEventListener("input", e => {
  searchQuery = e.target.value;
  renderList();
});

// ── Helpers ───────────────────────────────────────────────────────────────────
const SOURCE_NAMES = {
  "github.com":          "GitHub",
  "gist.github.com":     "GitHub Gist",
  "docs.github.com":     "GitHub Docs",
  "youtu.be":            "YouTube",
  "youtube.com":         "YouTube",
  "linkedin.com":        "LinkedIn",
  "open.substack.com":   "Substack",
  "substack.com":        "Substack",
  "x.com":               "X / Twitter",
  "twitter.com":         "X / Twitter",
  "hbr.org":             "Harvard Business Review",
  "claude.ai":           "Claude",
  "claude.com":          "Claude / Anthropic",
  "anthropic.com":       "Anthropic",
  "docs.anthropic.com":  "Anthropic Docs",
  "notion.so":           "Notion",
  "medium.com":          "Medium",
  "dev.to":              "DEV Community",
  "stackoverflow.com":   "Stack Overflow",
  "microsoft.com":       "Microsoft",
  "learn.microsoft.com": "Microsoft Learn",
  "docs.microsoft.com":  "Microsoft Docs",
  "techcommunity.microsoft.com": "Microsoft Tech Community",
  "powerappstools.com":  "Power Apps Tools",
  "tabulareditor.com":   "Tabular Editor",
  "npmjs.com":           "npm",
  "pypi.org":            "PyPI",
};

function friendlySource(url) {
  try {
    const host = new URL(url).hostname.replace(/^www\./, "");
    // Check exact match first, then check if host ends with a known domain
    if (SOURCE_NAMES[host]) return SOURCE_NAMES[host];
    for (const [domain, name] of Object.entries(SOURCE_NAMES)) {
      if (host.endsWith("." + domain) || host === domain) return name;
    }
    // Fallback: capitalise the root domain (e.g. "vercel.com" → "Vercel")
    const root = host.split(".").slice(-2, -1)[0] || host;
    return root.charAt(0).toUpperCase() + root.slice(1);
  } catch {
    return url;
  }
}

function youtubeId(url) {
  try {
    const u = new URL(url);
    const host = u.hostname.replace(/^(www|m)\./, "");
    if (host === "youtu.be") return u.pathname.slice(1).split("/")[0];
    if (host === "youtube.com") {
      if (u.pathname === "/watch") return u.searchParams.get("v") || "";
      const parts = u.pathname.split("/").filter(Boolean);
      if (["embed", "live", "shorts"].includes(parts[0])) return parts[1] || "";
    }
  } catch {}
  return "";
}

function timeLabel(a) {
  const m = Math.round(a.minutes);
  const amount = m >= 60 ? fmtHours(m) : `${m} min`;
  if (a.source_type === "youtube") return `${amount} video`;
  return `${a.minutes_estimated ? "~" : ""}${amount} read`;
}

function fmtDate(d) {
  if (!d) return "";
  const [y, m, day] = d.split("-");
  return `${m}-${day}-${y}`;
}

function escHtml(s) {
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
}

// ── Welcome (README) ──────────────────────────────────────────────────────────
function showWelcome() {
  // On mobile, stay on the list view — README is desktop-only landing
  if (isMobile()) return;
  document.getElementById("main").innerHTML = WELCOME_HTML;
}

// ── Init ──────────────────────────────────────────────────────────────────────
renderTypes();
renderTags();
renderList();

// Open article from URL hash on load, otherwise show README
const hash = window.location.hash.slice(1);
if (hash === "stats") {
  showStats();
} else if (hash && ARTICLES.find(a => a.id === hash)) {
  openArticle(hash);
} else {
  showWelcome();
}
</script>
</body>
</html>
"""


# ── Build ─────────────────────────────────────────────────────────────────────

def build(out_path: Path) -> None:
    if not WIKI_PAGES.exists():
        log.error("Wiki pages directory not found: %s", WIKI_PAGES)
        return

    md_files = sorted(WIKI_PAGES.glob("*.md"), key=lambda p: p.name)
    md_files = [f for f in md_files if f.name != ".gitkeep"]

    articles = []
    for path in md_files:
        page = _parse_page(path)
        if page:
            articles.append(page)

    # Sort newest first
    articles.sort(key=lambda a: a.get("date", ""), reverse=True)
    add_related_articles(articles)

    log.info("Loaded %d articles from %s", len(articles), WIKI_PAGES)

    articles_json = json.dumps(articles, ensure_ascii=False, indent=2)
    articles_json = articles_json.replace("<", "\\u003c")

    readme_path = HERE / "README.md"
    readme_text = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    readme_html = markdown(readme_text, extensions=["fenced_code", "tables"])

    html = HTML_TEMPLATE.replace("__ARTICLES_JSON__", articles_json)
    html = html.replace("__README_HTML__", readme_html)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    log.info("Built: %s  (%d KB)", out_path, out_path.stat().st_size // 1024)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Leah's Learning Loop static site.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help=f"Output path (default: {DEFAULT_OUT})")
    args = parser.parse_args()
    build(args.out)


if __name__ == "__main__":
    main()
