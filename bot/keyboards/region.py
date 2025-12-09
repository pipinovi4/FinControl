from __future__ import annotations
from typing import List, Optional
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from constants import REGIONS, CB_MENU
from .callbacks import cb_region, cb_menu
from locales import translate as t, BTN_BACK


def kb_regions(lang: Optional[str] = None) -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []
    for code in ("CIS", "EU", "NA", "AS"):
        rows.append([InlineKeyboardButton(REGIONS[code]["title"], callback_data=cb_region(code))])

    if lang:
        rows.append([InlineKeyboardButton(t(lang, "buttons.back"), callback_data=cb_menu(BTN_BACK))])

    return InlineKeyboardMarkup(rows)

__all__ = [
    "kb_regions",
]