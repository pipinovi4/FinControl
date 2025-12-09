from __future__ import annotations
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from locales import translate as t, BTN_BACK
from .callbacks import cb_menu


def kb_support(lang: str) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                t(lang, "buttons.back"),
                callback_data=cb_menu(BTN_BACK)
            ),
        ],
    ]

    return InlineKeyboardMarkup(rows)

__all__ = [
    "kb_support",
]