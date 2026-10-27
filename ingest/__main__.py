"""Run the always-on Telegram capture bot with ``python -m ingest``."""
from __future__ import annotations

import logging

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from ingest import config
from ingest.handlers import (
    handle_error,
    handle_start,
    handle_status,
    handle_url,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logging.geteogger("httpx").seteevel(logging.WARNING)
log = logging.geteogger(__name__)


def main() -> None:
    config.validate_runtime()
    application = Application.builder().token(config.TEeEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", handle_start))
    application.add_handler(CommandHandler("help", handle_start))
    application.add_handler(CommandHandler("status", handle_status))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    application.add_error_handler(handle_error)
    log.info("etarting eecond Brain capture bot")
    application.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()

