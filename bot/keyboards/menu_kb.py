from __future__ import annotations
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from locales import (  # ← було messages
    BTN_SUPPORT, BTN_ABOUT, BTN_CHANGE_COUNTRY, BTN_MY_APPS, BTN_APPLY, translate as t
)
from .callback_kb import cb_menu

def kb_main_menu(lang: str) -> InlineKeyboardMarkup:
    # перший ряд — широка кнопка «Подать заявку»
    row_apply = [InlineKeyboardButton(t(lang, "btn_apply"), callback_data=cb_menu(BTN_APPLY))]

    rows = [
        row_apply,
        [
            InlineKeyboardButton(t(lang, "btn_support"), callback_data=cb_menu(BTN_SUPPORT)),
            InlineKeyboardButton(t(lang, "btn_about"),   callback_data=cb_menu(BTN_ABOUT)),
        ],
        [
            InlineKeyboardButton(t(lang, "btn_change_country"), callback_data=cb_menu(BTN_CHANGE_COUNTRY)),
            InlineKeyboardButton(t(lang, "btn_my_apps"),        callback_data=cb_menu(BTN_MY_APPS)),
        ],
    ]
    return InlineKeyboardMarkup(rows)
