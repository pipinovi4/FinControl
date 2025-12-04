"""
WorldFlow Credit — Telegram bot bootstrap.

Responsibilities:
-----------------
✓ load settings
✓ configure logging
✓ build Application
✓ register handlers
✓ start polling
"""

from __future__ import annotations

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from telegram.error import BadRequest, Forbidden, TelegramError

# Project imports
from core.settings import load_settings
from core.logger import setup_logging, log
from handlers.application.callbacks import handle_progress_callback

# Handlers
from handlers.start import cmd_start
from handlers.menu import on_callback
from handlers.application import handle_application_message
from jobs import cleanup_user_data
from locales.ru import L10N_RU


# ============================================================
# 🔥 Global error handler
# ============================================================
async def error_handler(update, context):
    try:
        raise context.error
    except (BadRequest, Forbidden):
        log.warning(f"[TG Warning] {context.error}")
    except TelegramError as e:
        log.error(f"[TelegramError] {e}")
    except Exception as e:
        log.error(f"[Unhandled Exception] {e}", exc_info=True)


# ============================================================
# 🔧 Build Application
# ============================================================
def build_app() -> Application:

    settings = load_settings()

    app = (
        Application.builder()
        .token(settings.bot_token)
        .build()
    )

    # Commands
    app.add_handler(CommandHandler("start", cmd_start))

    # Wizard navigation callbacks
    app.add_handler(CallbackQueryHandler(handle_progress_callback, pattern="^nav:"))

    # Menu, country select, etc.
    app.add_handler(CallbackQueryHandler(on_callback))

    # Wizard text/contact messages
    app.add_handler(
        MessageHandler(
            filters.TEXT | filters.CONTACT,
            handle_application_message
        )
    )

    # Global errors
    app.add_error_handler(error_handler)

    # jobqueue
    app.job_queue.run_repeating(cleanup_user_data, interval=1800)


    return app


# ============================================================
# 🚀 Entrypoint
# ============================================================
def main() -> None:

    setup_logging()

    log.info("Bootstrapping WorldFlow Credit bot...")

    app = build_app()

    log.info("🚀 Bot started (polling mode)")

    app.run_polling(
        allowed_updates=["message", "callback_query"]
    )

if __name__ == "__main__":
    print(L10N_RU)
    main()
