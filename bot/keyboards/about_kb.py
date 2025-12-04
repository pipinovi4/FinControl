from __future__ import annotations
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from locales import translate as t, BTN_BACK
from .callback_kb import cb_menu


def kb_about(lang: str) -> InlineKeyboardMarkup:
    WEBSITE  = os.getenv("SOCIAL_WEBSITE",  "https://example.com")
    TG_CH    = os.getenv("SOCIAL_TG",       "https://t.me/worldflowcredit")
    INSTA    = os.getenv("SOCIAL_IG",       "https://instagram.com/worldflowcredit")
    X_TW     = os.getenv("SOCIAL_X",        "https://twitter.com/worldflowcredit")
    LINKEDIN = os.getenv("SOCIAL_LINKEDIN", "https://linkedin.com/company/worldflowcredit")
    YT       = os.getenv("SOCIAL_YT",       "https://youtube.com/@worldflowcredit")

    rows = [
        [
            InlineKeyboardButton(
                t(lang, "buttons.website"),
                url=WEBSITE
            ),
            InlineKeyboardButton(
                t(lang, "buttons.tg_channel"),
                url=TG_CH
            ),
        ],
        [
            InlineKeyboardButton(
                t(lang, "buttons.instagram"),
                url=INSTA
            ),
            InlineKeyboardButton(
                t(lang, "buttons.x"),
                url=X_TW
            ),
        ],
        [
            InlineKeyboardButton(
                t(lang, "buttons.linkedin"),
                url=LINKEDIN
            ),
            InlineKeyboardButton(
                t(lang, "buttons.youtube"),
                url=YT
            ),
        ],
        [
            InlineKeyboardButton(
                t(lang, "buttons.back"),
                callback_data=cb_menu(BTN_BACK)
            ),
        ],
    ]

    return InlineKeyboardMarkup(rows)
