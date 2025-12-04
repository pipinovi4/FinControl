from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

# Project imports
from locales import WELCOME_BILINGUAL
from keyboards import kb_regions

from ui import safe_edit
from core.logger import log


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /start command — resets the session, UI, and wizard state.

    Behaviour:
    ----------
    • Clears ALL user_data (wizard, country, lang, steps, answers)
    • Removes all UI progress panels
    • Sends welcome message with START button
    • Works both for text message and callback_query
    """
    msg = update.message
    cq = update.callback_query

    log.info("[Start] /start called — resetting session")

    # Reset session
    context.user_data.clear()

    # Prepare text
    text = WELCOME_BILINGUAL

    # Remove any UI panels from past sessions
    if msg:
        await msg.reply_text(
            text,
            reply_markup=kb_regions(),
            parse_mode="HTML",
        )
    else:
        await safe_edit(
            cq,
            text,
            reply_markup=kb_regions(),
            parse_mode="HTML",
        )

    log.debug("[Start] Session reset complete")


__all__ = ["cmd_start"]