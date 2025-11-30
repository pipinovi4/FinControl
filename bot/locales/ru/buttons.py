from locales import BTN_SUPPORT, BTN_ABOUT, BTN_CHANGE_COUNTRY, BTN_MY_APPS, BTN_APPLY, BTN_BACK

BUTTONS = {
    "btn_apply": "📝 Подать заявку",
    "btn_support": "🛟 Поддержка",
    "btn_about": "ℹ️ О нас",
    "btn_change_country": "🌐 Изменить страну",
    "btn_my_apps": "🗂 Мои заявки",
    "btn_back": "↩ Назад",

    "btn_website": "Сайт",
    "btn_tg_channel": "Канал в Telegram",
    "btn_instagram": "Instagram",
    "btn_x": "X / Twitter",
    "btn_linkedin": "LinkedIn",
    "btn_youtube": "YouTube",
}

# Алиасы кнопок
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