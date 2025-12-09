from __future__ import annotations
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from locales import (
    BTN_SUPPORT, BTN_ABOUT, BTN_CHANGE_COUNTRY, BTN_MY_APPS, BTN_APPLY,
    translate as t
)
from .callbacks import cb_menu


def kb_main_menu(lang: str) -> InlineKeyboardMarkup:
    # перший ряд — широка кнопка «Подати заявку»
    row_apply = [
        InlineKeyboardButton(
            t(lang, "buttons.apply"),
            callback_data=cb_menu(BTN_APPLY)
        )
    ]

    rows = [
        row_apply,

        [
            InlineKeyboardButton(
                t(lang, "buttons.support"),
                callback_data=cb_menu(BTN_SUPPORT)
            ),
            InlineKeyboardButton(
                t(lang, "buttons.about"),
                callback_data=cb_menu(BTN_ABOUT)
            ),
        ],

        [
            InlineKeyboardButton(
                t(lang, "buttons.change_country"),
                callback_data=cb_menu(BTN_CHANGE_COUNTRY)
            ),
            InlineKeyboardButton(
                t(lang, "buttons.my_apps"),
                callback_data=cb_menu(BTN_MY_APPS)
            ),
        ],
    ]

    return InlineKeyboardMarkup(rows)

__all__ = [
    "kb_main_menu",
]