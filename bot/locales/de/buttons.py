from locales import BTN_SUPPORT, BTN_ABOUT, BTN_CHANGE_COUNTRY, BTN_MY_APPS, BTN_APPLY, BTN_BACK

BUTTONS = {
    "btn_apply": "📝 Antrag stellen",
    "btn_support": "🛟 Support",
    "btn_about": "ℹ️ Über uns",
    "btn_change_country": "🌐 Land wechseln",
    "btn_my_apps": "🗂 Meine Anträge",
    "btn_back": "↩ Zurück",

    "btn_website": "Webseite",
    "btn_tg_channel": "Telegram-Kanal",
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

__all__ = [
    "BUTTONS"
]