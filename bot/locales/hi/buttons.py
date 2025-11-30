from locales import (
    BTN_SUPPORT,
    BTN_ABOUT,
    BTN_CHANGE_COUNTRY,
    BTN_MY_APPS,
    BTN_APPLY,
    BTN_BACK,
)

BUTTONS = {
    "btn_apply": "📝 ऋण के लिए आवेदन करें",
    "btn_support": "🛟 सहायता",
    "btn_about": "ℹ️ हमारे बारे में",
    "btn_change_country": "🌐 देश बदलें",
    "btn_my_apps": "🗂 मेरे आवेदन",
    "btn_back": "↩ वापस",
    "btn_website": "वेबसाइट",
    "btn_tg_channel": "टेलीग्राम चैनल",
    "btn_instagram": "इंस्टाग्राम",
    "btn_x": "X / ट्विटर",
    "btn_linkedin": "लिंक्डइन",
    "btn_youtube": "यूट्यूब",
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
