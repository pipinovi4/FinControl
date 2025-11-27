"""
Finalization logic for the application wizard.

This module handles:
------------------------------------------------------
1. Cleaning the progress panel
2. Resetting APP_FLOW state
3. Displaying the final "completed" message
4. Returning user to main menu
------------------------------------------------------
"""

from __future__ import annotations

from telegram import ReplyKeyboardRemove
from telegram.ext import ContextTypes

from locales import translate as t
from keyboards import kb_main_menu
from constants import APP_FLOW
from ui.progress_panel import wipe_all_progress_panels


async def finish_application(msg, context: ContextTypes.DEFAULT_TYPE, lang: str):
    """
    Completes the wizard:
        - wipes progress panels
        - resets wizard state
        - shows final notification
        - returns user to main menu
    """
    await wipe_all_progress_panels(msg.chat, context)

    # reset wizard flag
    context.user_data[APP_FLOW] = False

    # send final summary
    await msg.chat.send_message(
        t(lang, "ui.completed_demo"),
        reply_markup=ReplyKeyboardRemove()
    )

    # return to main menu
    await msg.chat.send_message(
        t(lang, "menu_title"),
        reply_markup=kb_main_menu(lang)
    )


__all__ = ["finish_application"]
