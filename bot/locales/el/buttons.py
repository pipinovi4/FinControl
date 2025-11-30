from locales import (
    BTN_SUPPORT, BTN_ABOUT, BTN_CHANGE_COUNTRY, BTN_MY_APPS, BTN_APPLY, BTN_BACK
)

BUTTONS = {
    "btn_apply": "📝 Υποβολή αίτησης",
    "btn_support": "🛟 Υποστήριξη",
    "btn_about": "ℹ️ Σχετικά με εμάς",
    "btn_change_country": "🌐 Αλλαγή χώρας",
    "btn_my_apps": "🗂 Οι αιτήσεις μου",
    "btn_back": "↩ Πίσω",

    "btn_website": "Ιστότοπος",
    "btn_tg_channel": "Κανάλι Telegram",
    "btn_instagram": "Instagram",
    "btn_x": "X / Twitter",
    "btn_linkedin": "LinkedIn",
    "btn_youtube": "YouTube",
}

# Aliases
BUTTONS.update({
    BTN_SUPPORT: BUTTONS["btn_support"],
    BTN_ABOUT: BUTTONS["btn_about"],
    BTN_CHANGE_COUNTRY: BUTTONS["btn_change_country"],
    BTN_MY_APPS: BUTTONS["btn_my_apps"],
    BTN_APPLY: BUTTONS["btn_apply"],
    BTN_BACK: BUTTONS["btn_back"],
})

__all__ = ["BUTTONS"]
