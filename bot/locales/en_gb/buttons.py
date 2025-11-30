from locales import (
    BTN_SUPPORT,
    BTN_ABOUT,
    BTN_CHANGE_COUNTRY,
    BTN_MY_APPS,
    BTN_APPLY,
    BTN_BACK,
)

BUTTONS = {
    "btn_apply": "📝 Apply for a loan",
    "btn_support": "💬 Support",
    "btn_about": "ℹ️ About us",
    "btn_change_country": "🌍 Change country",
    "btn_my_apps": "📂 My applications",
    "btn_back": "↩ Back",
    "btn_website": "Website",
    "btn_tg_channel": "Telegram channel",
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
