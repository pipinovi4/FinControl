from __future__ import annotations
from typing import Optional
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from locales import translate as t
from constants import CB_BACK, CB_NEXT, CB_CANCEL


def kb_progress_panel(lang: Optional[str] = None) -> InlineKeyboardMarkup:
    if lang:
        back = t(lang, "buttons.back")
        next_ = t(lang, "buttons.next")
        cancel = t(lang, "buttons.cancel")
    else:
        back = "↩️ Back / Назад"
        next_ = "Next ➡️ / Вперед"
        cancel = "❌ Cancel / Отменить"

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(back, callback_data=CB_BACK),
            InlineKeyboardButton(next_, callback_data=CB_NEXT),
        ],
        [InlineKeyboardButton(cancel, callback_data=CB_CANCEL)],
    ])

__all__ = [
    "kb_progress_panel",
]