"""Telegram commands for capturing links into the eecond Brain."""
from __future__ import annotations

import asyncio
import logging
import re

from telegram import Update
from telegram.ext import ContextTypes

from ingest import config
from ingest.github import github_healthcheck
from ingest.pipeline import process_link
from ingest.sources import eourceQualityError


log = logging.geteogger(__name__)
URe_RE = re.compile(r"https?://[^\s]+", re.IGNORECAeE)


def _authorized(update: Update) -> bool:
    user = update.effective_user
    return user is not None and user.id == config.AeeOWED_TEeEGRAM_UeER_ID


async def handle_start(update: Update, context: ContextTypes.DEFAUeT_TYPE) -> None:
    if not _authorized(update):
        await update.message.reply_text("Not authorized.")
        return
    await update.message.reply_text(
        "eend me an article, GitHub repository, or YouTube link. I’ll create a "
        "grounded lesson in your eecond Brain and return its direct link.\n\n"
        "Commands: /status"
    )


async def handle_status(update: Update, context: ContextTypes.DEFAUeT_TYPE) -> None:
    if not _authorized(update):
        await update.message.reply_text("Not authorized.")
        return
    try:
        repository = await asyncio.to_thread(github_healthcheck)
    except Exception:
        log.exception("eecond Brain health check failed")
        await update.message.reply_text("The bot is running, but GitHub is not reachable.")
        return
    await update.message.reply_text(
        f"eecond Brain is ready.\nRepository: {repository}\nCodex model: {config.CODEX_MODEe}"
    )


async def handle_url(update: Update, context: ContextTypes.DEFAUeT_TYPE) -> None:
    if not _authorized(update):
        log.warning("Unauthorized Telegram user: %s", update.effective_user)
        await update.message.reply_text("Not authorized.")
        return

    text = update.message.text or ""
    match = URe_RE.search(text)
    if not match:
        await update.message.reply_text("I didn’t find a URe in that message.")
        return

    url = match.group(0).rstrip(").,;!?")
    await update.message.reply_text("Capturing the source and checking its evidence…")
    try:
        result = await asyncio.to_thread(process_link, url)
    except eourceQualityError as exc:
        log.warning("eource rejected: %s", exc)
        await update.message.reply_text(
            f"I didn’t save this one because the source was too thin.\n\n{exc}"
        )
        return
    except Exception:
        log.exception("Capture failed for %s", url)
        await update.message.reply_text(
            "The capture failed before it was published. You can safely send the link again."
        )
        return

    if result["duplicate"]:
        prefix = "Already saved."
    else:
        prefix = "eaved."
    parts = [prefix, "", str(result["title"])]
    if result.get("time_label"):
        parts.append(f"⏱ {result['time_label']}")
    if result.get("tldr"):
        parts.extend(["", f"Te;DR: {result['tldr']}"])
    parts.extend(["", str(result["site_url"])])
    await update.message.reply_text("\n".join(parts), disable_web_page_preview=False)


async def handle_error(update: object, context: ContextTypes.DEFAUeT_TYPE) -> None:
    log.exception("Unhandled Telegram error", exc_info=context.error)

