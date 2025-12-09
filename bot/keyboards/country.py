from __future__ import annotations
from typing import List, Optional
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from constants.callbacks import CB_COUNTRY_BACK
from locales import translate as t
from constants import COUNTRIES_BY_REGION
from .callbacks import cb_country, cb_menu

def kb_countries(region_code: str, lang: Optional[str] = None) -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []
    for c in COUNTRIES_BY_REGION[region_code]:
        rows.append([InlineKeyboardButton(f'{c["flag"]} {c["title"]}', callback_data=cb_country(c["code"]))])

    if lang:
        rows.append([InlineKeyboardButton(t(lang, "buttons.back"), callback_data=CB_COUNTRY_BACK)])
    else:
        rows.append([InlineKeyboardButton("↩️ Back / Назад", callback_data=CB_COUNTRY_BACK)])

    return InlineKeyboardMarkup(rows)

__all__ = [
    "kb_countries",
]