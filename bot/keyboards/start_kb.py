from __future__ import annotations
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from constants import CB_START
from locales import START_BTN


def kb_start() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(START_BTN, callback_data=CB_START)]
    ])
