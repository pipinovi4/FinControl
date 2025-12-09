from locales import BTN_SUPPORT, BTN_ABOUT, BTN_CHANGE_COUNTRY, BTN_MY_APPS, BTN_APPLY, BTN_BACK

BUTTONS = {
    "apply": "📝 Подать заявку",
    "support": "🛟 Поддержка",
    "about": "ℹ️ О нас",
    "change_country": "🌐 Изменить страну",
    "my_apps": "🗂 Мои заявки",
    "back": "⬅️ Назад",
    "next": "➡️ Вперед",
    "cancel": "❌ Отменить",
    "edit": "✏️ Изменить",
    "submit": "✅ Отправить",
    "return": "🔁 Вернуться",
    "choose_field": "🎯 Выбрать поле",
    "save": "💾 Сохранить",
}

# Алиасы кнопок
BUTTONS.update({
    BTN_SUPPORT: BUTTONS["support"],
    BTN_ABOUT: BUTTONS["about"],
    BTN_CHANGE_COUNTRY: BUTTONS["change_country"],
    BTN_MY_APPS: BUTTONS["my_apps"],
    BTN_APPLY: BUTTONS["apply"],
    BTN_BACK: BUTTONS["back"],
})

__all__ = [
    "BUTTONS"
]