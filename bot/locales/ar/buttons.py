from locales import BTN_SUPPORT, BTN_ABOUT, BTN_CHANGE_COUNTRY, BTN_MY_APPS, BTN_APPLY, BTN_BACK

BUTTONS = {
    "btn_apply": "📝 تقديم طلب",
    "btn_support": "🛟 الدعم",
    "btn_about": "ℹ️ من نحن",
    "btn_change_country": "🌐 تغيير الدولة",
    "btn_my_apps": "🗂 طلباتي",
    "btn_back": "↩ رجوع",

    "btn_website": "الموقع",
    "btn_tg_channel": "قناة تيليجرام",
    "btn_instagram": "إنستغرام",
    "btn_x": "X / تويتر",
    "btn_linkedin": "لينكدإن",
    "btn_youtube": "يوتيوب",
}

# تأكيد الأزرار aliases
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