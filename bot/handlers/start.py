# handlers/start.py
"""
Start command handler.

This module contains the logic for the /start command:
- clears user session state,
- wipes progress panels,
- shows the welcome text,
- displays the Start keyboard.

It uses shared UI helpers and constants from ui/ and constants/.
"""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

# --- Project imports ---
from ..locales import WELCOME_BILINGUAL        # i18n welcome text (Markdown)
from ..keyboards.start_kb import kb_start      # "▶ Start" inline keyboard

from ..ui import safe_edit, wipe_all_progress_panels

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command.

    Responsibilities:
    -----------------
    1. Fully clears user_data — resets application state.
    2. Removes any existing progress panels (UI cleanup).
    3. Sends the bilingual welcome message.
    4. Displays the Start button (inline keyboard).

    Notes:
    ------
    - update.message.exists → user typed /start manually → reply_text().
    - update.callback_query.exists → /start triggered from previous message or fallback → safe_edit().
    - safe_edit() automatically handles cases where the message is a photo/video.
    """

    # 1️⃣ Wipe all UI panels from previous session (if user existed)
    if update.effective_chat:
        await wipe_all_progress_panels(update.effective_chat, context)

    # 2️⃣ Reset all conversation context (country, lang, wizard state etc.)
    context.user_data.clear()

    # 3️⃣ Display welcome text + start button
    if update.message:
        # /start was typed normally
        await update.message.reply_text(
            WELCOME_BILINGUAL,
            parse_mode="Markdown",
            reply_markup=kb_start()
        )
    else:
        # /start triggered from callback or from a media message — must use safe_edit
        await safe_edit(
            update.callback_query,
            WELCOME_BILINGUAL,
            reply_markup=kb_start(),
            parse_mode="Markdown"
        )


__all__ = ["cmd_start"]