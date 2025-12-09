"""
WorldFlow Credit — Telegram bot bootstrap.
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

from core.settings import load_settings
from core.logger import setup_logging, log

# Handlers
from handlers.start import cmd_start
from handlers.menu import on_callback
from handlers.application.router_selector import get_router
from jobs import cleanup_user_data
from locales.ru import L10N_RU


# ============================================================
# 🔥 Global error handler
# ============================================================
async def error_handler(update, context):
    error = context.error

    # What caused the error?
    if update:
        if update.message:
            origin = f"message from user {update.message.from_user.id}"
        elif update.callback_query:
            origin = f"callback '{update.callback_query.data}' from user {update.callback_query.from_user.id}"
        else:
            origin = "unknown update type"
    else:
        origin = "update = None"

    try:
        raise error
    except (BadRequest, Forbidden):
        log.warning(f"[TG Warning] ({origin}) → {error}")
    except TelegramError:
        log.error(f"[TelegramError] ({origin}) → {error}")
    except Exception:
        log.error(f"[Unhandled Exception] ({origin})", exc_info=True)

# ============================================================
# 🔧 New unified message dispatcher
# ============================================================
async def handle_user_message(update, context):
    """
    Universal router for all user messages (text/file/contact/photo).
    Uses 3-mode router system:
    - ProgressRouter
    - EditRouter
    - ReviewRouter
    """
    router = get_router(update, context)
    if not router:
        return None

    msg = update.message
    if not msg:
        return None

    # File or photo
    if msg.document or msg.photo:
        return await router.on_file()

    # Text/contact
    return await router.on_text()


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

    # ALL callback buttons = handled inside menu.on_callback
    app.add_handler(CallbackQueryHandler(on_callback))

    # Wizard text/contact/file inputs → NEW universal router
    app.add_handler(
        MessageHandler(
            filters.ALL & ~filters.COMMAND,
            handle_user_message
        )
    )

    # Global errors
    app.add_error_handler(error_handler)

    # cleanup job
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
