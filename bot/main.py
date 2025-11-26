"""
Telegram bot bootstrap for WorldFlow Credit.

This module is the entrypoint of the entire bot:
- loads settings
- initializes logging
- builds the Telegram Application
- registers handlers
- starts polling

Architecture notes:
-------------------
• clean separation: startup logic ONLY
• business logic lives in handlers/
• settings loaded once
• logging initialized globally before Application is created
"""

from __future__ import annotations

# Telegram framework
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

# Project imports
from bot.core.settings import load_settings
from bot.core.logger import setup_logging, log

# Handlers
from bot.handlers.start import cmd_start
from bot.handlers.menu import on_callback
from bot.handlers.application import handle_application_message


# =====================================================================
# Factory: Build Application instance
# =====================================================================
def build_app() -> Application:
    """
    Create and configure a Telegram Application instance.

    Steps:
    ------
    1) Load config via load_settings()
    2) Initialize Application (builder pattern)
    3) Register all handlers

    Returns:
        Ready-to-run Application instance
    """

    # Load .env / config
    settings = load_settings()

    # Create bot instance
    app = (
        Application
        .builder()
        .token(settings.bot_token)
        .build()
    )

    # ========== Command handlers ==========
    app.add_handler(CommandHandler("start", cmd_start))

    # ========== Inline keyboard callbacks ==========
    app.add_handler(CallbackQueryHandler(on_callback))

    # ========== Application wizard routing ==========
    app.add_handler(
        MessageHandler(
            filters.TEXT | filters.CONTACT,
            handle_application_message
        )
    )

    return app


# =====================================================================
# Entrypoint
# =====================================================================
def main() -> None:
    """
    Start the Telegram bot:
    • initialize logging
    • build Application
    • start polling
    """

    # 🔥 Initialize logging BEFORE anything else
    setup_logging()

    log.info("Bootstrapping WorldFlow Credit bot...")

    app = build_app()
    log.info("🚀 WorldFlow Credit bot started (polling mode)")

    app.run_polling(
        allowed_updates=["message", "callback_query"]
    )


__all__ = ["build_app", "main"]


if __name__ == "__main__":
    main()
