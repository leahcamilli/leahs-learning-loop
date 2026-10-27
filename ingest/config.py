"""Configuration for the Telegram ingestion service."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env.local")
load_dotenv(REPO_ROOT / ".env")


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_TELEGRAM_USER_ID = int(os.getenv("ALLOWED_TELEGRAM_USER_ID", "0"))

# Lesson generation uses Codex CLI ChatGPT-plan auth (`codex login`), not API keys.
CODEX_BIN = os.getenv("CODEX_BIN", "codex")
CODEX_MODEL = os.getenv("CODEX_MODEL", "gpt-5.4")
CODEX_TIMEOUT_SECONDS = int(os.getenv("CODEX_TIMEOUT_SECONDS", "300"))

# Accept the former service's variable during migration; GITHUB_TOKEN is canonical.
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") or os.getenv("SECOND_BRAIN_GITHUB_TOKEN", "")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY", "leahcamilli/leahs-learning-loop")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "master")
SITE_URL = os.getenv(
    "LEARNING_LOOP_SITE_URL", "https://leahcamilli.github.io/leahs-learning-loop/"
)

CAPTURE_TIMEZONE = os.getenv("CAPTURE_TIMEZONE", "America/Chicago")
MIN_WEB_SOURCE_CHARS = int(os.getenv("MIN_WEB_SOURCE_CHARS", "800"))
MIN_YOUTUBE_SOURCE_CHARS = int(os.getenv("MIN_YOUTUBE_SOURCE_CHARS", "1500"))
YOUTUBE_FETCH_TIMEOUT_SECONDS = int(os.getenv("YOUTUBE_FETCH_TIMEOUT_SECONDS", "60"))

# Optional TypeSafe Jev judgments (source gate, grounding, topics, lesson profile).
# Leave TYPESAFE_API_KEY unset to capture exactly as before.
TYPESAFE_API_KEY = os.getenv("TYPESAFE_API_KEY", "").strip()
TYPESAFE_BASE_URL = os.getenv("TYPESAFE_BASE_URL", "https://api.typesafe.ai")
TYPESAFE_MODEL = os.getenv("TYPESAFE_MODEL", "jev-latest")
JEV_TIMEOUT_SECONDS = float(os.getenv("JEV_TIMEOUT_SECONDS", "30"))
# Reject a source before generation when P(substantive) falls below this.
JEV_SOURCE_MIN = float(os.getenv("JEV_SOURCE_MIN", "0.15"))
# Drop a takeaway or key moment when P(supported by the source) falls below this.
JEV_SUPPORT_MIN = float(os.getenv("JEV_SUPPORT_MIN", "0.3"))
# Assign a canonical topic when P(main subject) reaches this.
JEV_TOPIC_MIN = float(os.getenv("JEV_TOPIC_MIN", "0.5"))
# Ground takeaways only when the whole source fits; a truncated one would look unsupported.
JEV_MAX_SOURCE_CHARS = int(os.getenv("JEV_MAX_SOURCE_CHARS", "60000"))


def validate_runtime() -> None:
    """Fail once at startup with a concise list of missing settings."""
    from ingest.codex import validate_codex_runtime

    required = {
        "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
        "ALLOWED_TELEGRAM_USER_ID": ALLOWED_TELEGRAM_USER_ID,
        "GITHUB_TOKEN": GITHUB_TOKEN,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise RuntimeError(f"Missing required settings: {', '.join(missing)}")
    validate_codex_runtime()
