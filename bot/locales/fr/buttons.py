from locales import (
    BTN_SUPPORT,
    BTN_ABOUT,
    BTN_CHANGE_COUNTRY,
    BTN_MY_APPS,
    BTN_APPLY,
    BTN_BACK,
)

BUTTONS = {
    "btn_apply": "📝 Déposer une demande",
    "btn_support": "💬 Support",
    "btn_about": "ℹ️ À propos",
    "btn_change_country": "🌐 Changer de pays",
    "btn_my_apps": "📂 Mes demandes",
    "btn_back": "↩ Retour",
    "btn_website": "Site web",
    "btn_tg_channel": "Chaîne Telegram",
    "btn_instagram": "Instagram",
    "btn_x": "X / Twitter",
    "btn_linkedin": "LinkedIn",
    "btn_youtube": "YouTube",
}

BUTTONS.update({
    BTN_SUPPORT: BUTTONS["btn_support"],
    BTN_ABOUT: BUTTONS["btn_about"],
    BTN_CHANGE_COUNTRY: BUTTONS["btn_change_country"],
    BTN_MY_APPS: BUTTONS["btn_my_apps"],
    BTN_APPLY: BUTTONS["btn_apply"],
    BTN_BACK: BUTTONS["btn_back"],
})

__all__ = ["BUTTONS"]
