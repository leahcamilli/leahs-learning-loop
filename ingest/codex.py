"""ChatGPT/Codex monthly-plan auth for lesson generation.

Uses the official Codex CLI (`codex exec`) so requests bill against the
signed-in ChatGPT plan via ``~/.codex/auth.json`` from ``codex login``.
No OpenAI Platform API key is required.
"""
from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from ingest import config


log = logging.getLogger(__name__)

LESSON_OUTPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "title",
        "tags",
        "tldr",
        "key_takeaways",
        "key_moments",
        "review_questions",
        "overview",
        "key_concepts",
        "how_it_works",
        "training_exercise",
        "further_reading",
    ],
    "properties": {
        "title": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}},
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
        "overview": {"type": "string"},
        "key_concepts": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["name", "explanation"],
                "properties": {
                    "name": {"type": "string"},
                    "explanation": {"type": "string"},
                },
            },
        },
        "how_it_works": {"type": "string"},
        "training_exercise": {"type": "string"},
        "further_reading": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["title", "url"],
                "properties": {
                    "title": {"type": "string"},
                    "url": {"type": "string"},
                },
            },
        },
    },
}


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def auth_json_path() -> Path:
    return codex_home() / "auth.json"


def resolve_codex_bin() -> str:
    configured = (config.CODEX_BIN or "codex").strip() or "codex"
    if os.path.sep in configured or configured.startswith("."):
        path = Path(configured).expanduser()
        if path.is_file() and os.access(path, os.X_OK):
            return str(path)
        raise RuntimeError(f"CODEX_BIN is not an executable file: {configured}")
    found = shutil.which(configured)
    if found:
        return found
    raise RuntimeError(
        f"Codex CLI `{configured}` not found on PATH. "
        "Install with `npm install -g @openai/codex`, then run `codex login`."
    )


def ensure_chatgpt_auth() -> Path:
    """Require a ChatGPT-managed Codex auth cache from `codex login`."""
    path = auth_json_path()
    if not path.is_file():
        raise RuntimeError(
            f"Codex ChatGPT auth not found at {path}. "
            "On the Mac mini run: `codex login` and sign in with your ChatGPT plan."
        )
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Could not read Codex auth cache {path}: {exc}") from exc

    tokens = payload.get("tokens") if isinstance(payload, dict) else None
    access = ""
    refresh = ""
    if isinstance(tokens, dict):
        access = str(tokens.get("access_token") or "")
        refresh = str(tokens.get("refresh_token") or "")
    auth_mode = str(payload.get("auth_mode") or "") if isinstance(payload, dict) else ""

    if not access or not refresh:
        raise RuntimeError(
            f"Codex auth at {path} is missing ChatGPT tokens. "
            "Run `codex login` and choose Sign in with ChatGPT (not an API key)."
        )
    if auth_mode and auth_mode not in {"chatgpt", "chatgptAuthTokens"}:
        raise RuntimeError(
            f"Codex auth_mode is `{auth_mode}`; expected ChatGPT plan auth. "
            "Run `codex login` and sign in with ChatGPT."
        )
    return path


def validate_codex_runtime() -> None:
    resolve_codex_bin()
    ensure_chatgpt_auth()


def run_codex_structured(
    prompt: str,
    *,
    schema: dict[str, Any],
    model: str | None = None,
    timeout: int | None = None,
) -> dict[str, Any]:
    """Run `codex exec` with ChatGPT auth and return schema-validated JSON."""
    binary = resolve_codex_bin()
    ensure_chatgpt_auth()
    model = model or config.CODEX_MODEL
    timeout = config.CODEX_TIMEOUT_SECONDS if timeout is None else timeout

    with tempfile.TemporaryDirectory(prefix="secondbrain-codex-") as tmp:
        tmp_path = Path(tmp)
        schema_path = tmp_path / "schema.json"
        output_path = tmp_path / "lesson.json"
        schema_path.write_text(json.dumps(schema), encoding="utf-8")

        command = [
            binary,
            "exec",
            "--ephemeral",
            "--skip-git-repo-check",
            "--color",
            "never",
            "-s",
            "read-only",
            "-m",
            model,
            "--output-schema",
            str(schema_path),
            "-o",
            str(output_path),
            "-",
        ]
        log.info("Invoking Codex CLI model=%s", model)
        try:
            completed = subprocess.run(
                command,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise TimeoutError(
                f"Codex lesson generation timed out after {timeout}s"
            ) from exc

        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout or "").strip()
            if len(detail) > 1200:
                detail = detail[-1200:]
            raise RuntimeError(
                f"Codex exec failed (exit {completed.returncode}). {detail}"
            )

        if not output_path.is_file():
            raise RuntimeError("Codex exec finished without writing structured output")

        try:
            payload = json.loads(output_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Codex returned invalid JSON: {exc}") from exc
        if not isinstance(payload, dict):
            raise ValueError("Codex structured output must be a JSON object")
        return payload
