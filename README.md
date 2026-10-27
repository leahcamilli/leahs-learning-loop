# Leah's Learning Loop

One repository and one workflow for capturing, developing, searching, and publishing durable knowledge.

The live site is [Leah's Learning Loop](https://leahcamilli.github.io/leahs-learning-loop/). The original project is [Stevie's Second Brain](https://steviesimsii.github.io/Second_Brain/).

## The Workflow

```text
Send a link to Telegram
        ↓
Normalize the URL and check for duplicates
        ↓
Retrieve source evidence
  • YouTube timestamped transcript + length, channel, chapters
  • GitHub metadata, README, and file tree
  • Readable article content
        ↓
Reject thin sources instead of inventing a lesson
  (+ optional TypeSafe Jev check: is this worth learning from?)
        ↓
Generate a lesson with Codex (ChatGPT plan auth):
TL;DR · key takeaways · key moments · study notes · self-test
        ↓
Optional Jev review: drop unsupported takeaways and off-target
key moments; assign canonical topics, kind, depth, actionability
        ↓
Commit canonical Markdown to wiki/pages/
        ↓
GitHub Actions rebuilds the searchable site
        ↓
Telegram returns the TL;DR, the video length, and the direct link
```

Markdown is the source of truth. Notion, email, and OpenAI Platform API keys are not part of the pipeline.

## Repository Layout

```text
leahs-learning-loop/
├── ingest/                  # Always-on Telegram capture service
│   ├── __main__.py          # python -m ingest
│   ├── sources.py           # GitHub, YouTube, and web acquisition
│   ├── codex.py             # Codex CLI + ChatGPT monthly-plan auth
│   ├── lesson.py            # Grounded lesson generation
│   ├── github.py            # Idempotent Markdown publishing
│   └── requirements.txt     # Bot runtime dependencies
├── wiki/pages/              # Canonical lesson Markdown
├── build_site.py            # Searchable static-site generator
├── index.html               # Generated GitHub Pages site
├── tests/                   # Ingestion and knowledge-linking tests
└── docs/OPERATIONS.md       # Mac mini setup and daily operations
```

## Intelligence That Compounds

Every new capture stores stable metadata with the lesson:

- normalized source URL
- source type and evidence size
- a URL fingerprint used for deduplication
- reusable topic tags
- capture date
- time to consume it: video length (plus channel and publish date) or reading time

## Every Lesson Has Two Layers

- **Skim (30 seconds):** a TL;DR, 3-7 key takeaways, and, for videos, timestamped
  key moments that play right on the page.
- **Study (5 minutes):** overview, key concepts, how it works, a hands-on exercise,
  and *Test Yourself* questions with hidden answers.

## TypeSafe Jev Judgments (optional)

Codex writes lessons; [TypeSafe](https://typesafe.ai)'s Jev model supplies fast, typed
judgments that code acts on. Set `TYPESAFE_API_KEY` in `.env.local` to enable them:

| Judgment | Primitive | What code does with it |
| --- | --- | --- |
| Is the source substantive? | Noul | Rejects consent walls, stubs, and ads before a Codex run |
| Is each takeaway supported by the source? | Noul per takeaway | Drops unsupported takeaways |
| Does each key moment's transcript window match its label? | Noul per moment | Drops off-target timestamps |
| Which canonical topics is this about? | Noul per topic in `ingest/topics.py` | Writes `topics:`, used for learning time by topic and related notes |
| What kind of source is it? | Choice | Writes `kind:` (tutorial, deep dive, news, opinion, demo, interview) |
| How deep, and how actionable? | Score ×2 | Writes `depth:` and `actionability:` (0-3) |

Everything is one request per capture after generation, plus one small request before
it. Without a key, or if TypeSafe is unreachable, capture works exactly as before.
Thresholds (`JEV_SOURCE_MIN`, `JEV_SUPPORT_MIN`, `JEV_TOPIC_MIN`) are starting points;
tune them against your own captures.

## Learning Time

The **📊 Learning** view totals the time behind your captures: this week, this month,
a 12-week trend, your weekly capture streak, and time by format, channel, and topic.
Set your usual playback speed there so 1.5× viewers aren't over-counted. **🎲 Resurface**
opens a random note from two or more weeks ago, and `/` jumps to search.

The site automatically connects each lesson to related notes using shared topics and title concepts. This is deliberately transparent and inexpensive: no vector database is needed for the first intelligence layer.

The next natural layer is retrieval over the Markdown collection for a Telegram `/ask` command. The canonical files are already structured to support that without another content store.

## Run the Site Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python build_site.py
```

Open `index.html` after the build.

## Run the Telegram Capture Bot

```bash
# One-time on the Mac mini host
npm install -g @openai/codex
codex login   # Sign in with ChatGPT (monthly plan), not an API key

source .venv/bin/activate
python -m pip install -r ingest/requirements.txt
cp .env.example .env.local
# Fill in Telegram and GitHub values. Leave OPENAI_API_KEY unset.
python -m ingest
```

Lesson generation calls `codex exec` and reuses `~/.codex/auth.json` from `codex login`, so usage follows your ChatGPT/Codex plan limits.

Only one instance should poll a Telegram bot token at a time. The Mac mini is the permanent host; use a separate Telegram bot token for development.

See [docs/OPERATIONS.md](docs/OPERATIONS.md) for `launchd`, updates, logs, and migration from the former `LinkToNotionLessons` service.

## Content Format

Lessons are normal Markdown with YAML frontmatter:

```md
---
title: "A durable lesson title"
source: "https://example.com/source"
date: "2026-07-16"
tags: [agents, retrieval, knowledge-management]
source_type: "web"
source_fingerprint: "d8c66f8213"
source_characters: 18420
channel: "Example Channel"      # videos only
published: "2026-07-10"         # videos only
duration_seconds: 1843          # videos only
reading_minutes: 12             # articles and repos
topics: [ai-agents, mcp]        # canonical topics (Jev)
kind: "tutorial"                # Jev
depth: 2                        # 0 headline … 3 expert (Jev)
actionability: 3                # 0 awareness … 3 apply today (Jev)
---

## TL;DR
## Key Takeaways
## Key Moments                  # videos only
## Overview
## Key Concepts
## How It Works
## Training Exercise
## Test Yourself
## Further Reading
...
```

You can also write or edit files in `wiki/pages/` manually. Pushing them to `master` rebuilds the site.

## Design Principles

- One canonical store: Git-tracked Markdown.
- Capture should be easier than postponing the note.
- Weak evidence should fail visibly.
- Generated knowledge should remain inspectable and editable.
- Intelligence should grow from the corpus without locking it into a proprietary store.
- Lesson generation uses ChatGPT-plan Codex auth, not Platform API billing.
