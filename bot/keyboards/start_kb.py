from __future__ import annotations
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from locales import START_BTN   # ← було messages
from .callbacks import CB_START

def kb_start() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(START_BTN, callback_data=CB_START)]
    ])
