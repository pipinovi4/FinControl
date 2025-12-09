from __future__ import annotations
from typing import Optional
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from locales import translate as t
from constants import CB_EDIT, CB_SUBMIT, CB_CANCEL


def kb_review_panel(lang: Optional[str] = None) -> InlineKeyboardMarkup:
    if lang:
        edit = t(lang, "buttons.edit")
        cancel = t(lang, "buttons.cancel")
        submit = t(lang, "buttons.submit")
    else:
        edit = "✏️ Edit / Редактировать"
        cancel = "❌ Cancel / Отменить"
        submit = "✅ Submit / Подтвердить"

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(edit, callback_data=CB_EDIT)],
        [
            InlineKeyboardButton(cancel, callback_data=CB_CANCEL),
            InlineKeyboardButton(submit, callback_data=CB_SUBMIT),
        ]
    ])

__all__ = [
    "kb_review_panel",
]