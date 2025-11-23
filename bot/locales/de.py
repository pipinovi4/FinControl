from __future__ import annotations
from . import _register, BTN_SUPPORT, BTN_ABOUT, BTN_CHANGE_COUNTRY, BTN_MY_APPS, BTN_APPLY, BTN_BACK

L10N_DE = {
    "prompt_choose_region": "🌍 Wählen Sie die Region für Ihren Antrag:",
    "prompt_choose_country": "🌍 Wählen Sie Ihr Land:",
    "after_country_selected": "✅ Land ausgewählt: {country}\nDie Sprache wurde automatisch eingestellt.",
    "menu_title": "Wie möchten Sie fortfahren?",
    "btn_apply": "📝 Antrag stellen",
    "apply_text": "Legen wir los. Einen persönlichen Code können Sie im ersten Schritt eingeben.",
    "btn_support": "🛟 Support",
    "btn_about": "ℹ️ Über uns",
    "btn_change_country": "🌐 Land ändern",
    "btn_my_apps": "🗂 Meine Anträge",
    "support_text": "Schreiben Sie uns: @{support_username}",
    "about_text": "WorldFlow Credit — internationaler Kredit-Antragsservice.",
    "my_apps_stub": "Ihre Anträge erscheinen hier (bald).",
    "back_to_region": "↩️ Zur Regionsauswahl.",
    "btn_back": "↩ Zurück",
    "btn_website": "Webseite",
    "btn_tg_channel": "Telegram-Kanal",
    "btn_instagram": "Instagram",
    "btn_x": "X / Twitter",
    "btn_linkedin": "LinkedIn",
    "btn_youtube": "YouTube",

    "ui": {
        "preview_title": "Antragsstatus",
        "step": "Feld",
        "status": "Status",
        "value": "Wert",
        "done": "✅ Erledigt",
        "todo": "❌ Offen",
        "share_phone": "📲 Nummer teilen",
        "type_manually": "✏️ Manuell eingeben",
        "completed_demo": "Das Formular wurde erfolgreich ausgefüllt ✅",
    },

    "about_full": (
        "<b>WorldFlow Credit — Über uns</b><br/><br/>"
        "Grenzüberschreitende Antragsplattform: standardisiertes KYC, automatisierte Risiko-Checks "
        "und sichere Weiterleitung an lizenzierte Kreditgeber.<br/><br/>"
        "• Transparente Konditionen, keine versteckten Gebühren<br/>"
        "• Verschlüsselung bei Übertragung & Speicherung<br/>"
        "• Schnelle Prüfung über verifizierte Partner<br/>"
        "• Support auf Englisch und in Landessprachen"
    ),

    "steps_by_country": {
        "DE": {
            "phone": "📞 Bitte geben Sie Ihre Handynummer im Format +49XXXXXXXXXX ein.",
            "id_number": "🆔 Bitte geben Sie Ihre Steuer-ID ein.",
            "dob": "📅 Bitte geben Sie Ihr Geburtsdatum im Format TT.MM.JJJJ ein.",
        }
    },
    "labels": {
        "access_code": "Zugangscode",
        "full_name": "Vollständiger Name",
        "phone": "Telefon",
        "email": "E-Mail",
        "loan_amount": "Kreditsumme",
        "id_number": "Steuer-ID",
        "inn_ru": "INN (nur Russland)",
        "reg_address": "Meldeadresse",
        "actual_address": "Aktuelle Adresse",
        "dob": "Geburtsdatum",
        "marital_status": "Familienstand",
        "workplace": "Arbeitgeber",
    },
}

# generic steps fallback are taken from English; DE has country specifics above.

L10N_DE.update({
    BTN_SUPPORT: L10N_DE["btn_support"],
    BTN_ABOUT: L10N_DE["btn_about"],
    BTN_CHANGE_COUNTRY: L10N_DE["btn_change_country"],
    BTN_MY_APPS: L10N_DE["btn_my_apps"],
    BTN_APPLY: L10N_DE["btn_apply"],
    BTN_BACK: L10N_DE["btn_back"],
})
_register("de", L10N_DE)
