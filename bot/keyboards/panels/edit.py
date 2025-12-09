from __future__ import annotations
from typing import Optional
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from locales import translate as t
from constants.callbacks import CB_SAVE, CB_GOTO, CB_CANCEL


def kb_edit_panel(lang: Optional[str] = None) -> InlineKeyboardMarkup:
    if lang:
        save = t(lang, "buttons.save")
        choose = t(lang, "buttons.choose_field")
        cancel = t(lang, "buttons.cancel")
    else:
        choose = "🔽 Choose field / Выбрать поле"
        save = "💾 Save / Сохранить"
        cancel = "❌ Cancel / Отменить"

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(choose, callback_data=CB_GOTO + "menu")],
        [InlineKeyboardButton(cancel, callback_data=CB_CANCEL), InlineKeyboardButton(save, callback_data=CB_SAVE)],
    ])
