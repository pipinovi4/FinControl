from __future__ import annotations
from typing import List
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from ..constants import REGIONS
from .callback_kb import cb_region

def kb_regions() -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []
    for code in ("CIS", "EU", "NA", "AS"):
        rows.append([InlineKeyboardButton(REGIONS[code]["title"], callback_data=cb_region(code))])
    return InlineKeyboardMarkup(rows)
