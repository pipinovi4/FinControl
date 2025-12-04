from datetime import UTC, datetime
from telegram import Update
from telegram.ext import ContextTypes

async def stamp_user_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Middleware: кожна взаємодія оновлює _ts у user_data.
    Працює для:
    • message
    • callback_query
    • command
    """

    context.user_data["_ts"] = datetime.now(UTC)

__all__ = ["stamp_user_context"]