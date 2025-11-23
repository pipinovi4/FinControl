from __future__ import annotations
from . import _register, BTN_SUPPORT, BTN_ABOUT, BTN_CHANGE_COUNTRY, BTN_MY_APPS, BTN_APPLY, BTN_BACK

L10N_EN = {
    "prompt_choose_region": "🌍 Select the region for your application:",
    "after_country_selected": "✅ Country selected: {country}\nLanguage has been set automatically.",
    "menu_title": "What would you like to do next?",
    "btn_apply": "📝 Submit application",
    "apply_text": "Let's begin. A personal access code can be entered on the first step.",
    "btn_support": "🛟 Support",
    "btn_about": "ℹ️ About us",
    "btn_change_country": "🌐 Change country",
    "btn_my_apps": "🗂 My applications",
    "support_text": "Message us: @{support_username}",
    "about_text": "WorldFlow Credit — international credit application service.",
    "my_apps_stub": "Your applications will appear here (soon).",
    "back_to_region": "↩️ Back to region selection.",
    "btn_back": "↩ Back",
    "btn_website": "Website",
    "btn_tg_channel": "Telegram channel",
    "btn_instagram": "Instagram",
    "btn_x": "X / Twitter",
    "btn_linkedin": "LinkedIn",
    "btn_youtube": "YouTube",

    "ui": {
        "preview_title": "Application progress",
        "step": "Field",
        "status": "Status",
        "value": "Value",
        "done": "✅ Completed",
        "todo": "❌ Not filled",
        "share_phone": "📲 Share number (auto-fill from Telegram)",
        "type_manually": "✏️ Enter manually",
        "completed_demo": "The form has been successfully completed ✅",
    },

    "steps": {
        "access_code": (
            "🔐 Do you have a personal access code?\n\n"
            "Enter it below — and we’ll activate individual terms available only by special invitation."
        ),
        "full_name": (
            "✍️ Please enter your full name exactly as it appears in your passport.\n\n"
            "ℹ️ Enter all answers directly in messages — this ensures the form is completed correctly."
        ),
        "phone": "📞 Enter your mobile number in international format (e.g., +1XXXXXXXXXX).",
        "email": "📧 Enter your email address.",
        "loan_amount": "💰 Enter the desired loan amount.",
        "id_number": "🆔 Enter your national ID number (country-specific).",
        "reg_address": "🏠 Enter your registered residential address (as in your ID).",
        "actual_address": "🏠 Enter your current residential address.\nIf it is the same as your registered address — write “Same”.",
        "dob": "📅 Enter your date of birth (YYYY-MM-DD).",
        "marital_status": (
            "💬 Select your marital status.\nOptions:\n• Single\n• Married\n• Divorced\n• Widowed"
        ),
        "workplace": "🏢 Enter the full name of your organization (place of work).",
        "inn_ru": "🔢 Enter your INN (10 or 12 digits).",
    },

    "about_full": (
        "<b>WorldFlow Credit — About Us</b><br/><br/>"
        "We are a cross-border credit application platform that standardizes KYC, automates risk checks, "
        "and securely routes applications to licensed lenders.<br/><br/>"
        "• Transparent terms, no hidden fees<br/>"
        "• Data encrypted in transit & at rest<br/>"
        "• Fast underwriting via verified partners<br/>"
        "• Support in English & local languages"
    ),

    "steps_by_country": {
        "US": {
            "phone": "📞 Enter your mobile number in the format +1XXXXXXXXXX.",
            "id_number": "🆔 Enter your SSN (Social Security Number).",
            "dob": "📅 Enter your date of birth in the format MM/DD/YYYY.",
        },
        "CA": {
            "phone": "📞 Enter your mobile number in the format +1XXXXXXXXXX.",
            "id_number": "🆔 Enter your SIN (Social Insurance Number).",
            "dob": "📅 Enter your date of birth in the format YYYY-MM-DD.",
        },
        "GB": {
            "phone": "📞 Enter your mobile number in the format +44XXXXXXXXXX.",
            "id_number": "🆔 Enter your NINo (National Insurance Number).",
            "dob": "📅 Enter your date of birth in the format DD/MM/YYYY.",
        },
        "IN": {
            "phone": "📞 Enter your mobile number in the format +91XXXXXXXXXX.",
            "id_number": "🆔 Enter your Aadhaar Number.",
            "dob": "📅 Enter your date of birth in the format DD-MM-YYYY.",
        },
        "AE": {
            "phone": "📞 Enter your mobile number in the format +971XXXXXXXXX.",
            "id_number": "🆔 Enter your UAE ID card number.",
            "dob": "📅 Enter your date of birth in the format DD/MM/YYYY.",
        },
        "DE": {
            "phone": "📞 Bitte geben Sie Ihre Handynummer im Format +49XXXXXXXXXX ein.",
            "id_number": "🆔 Bitte geben Sie Ihre Steuer-ID ein.",
            "dob": "📅 Bitte geben Sie Ihr Geburtsdatum im Format TT.MM.JJJJ ein.",
        },
        "FR": {
            "phone": "📞 Indiquez votre numéro de mobile au format +33XXXXXXXXX.",
            "id_number": "🆔 Indiquez votre numéro de sécurité sociale (INSEE).",
            "dob": "📅 Veuillez indiquer votre date de naissance au format JJ/MM/AAAA.",
        },
        "GR": {
            "phone": "📞 Εισαγάγετε τον αριθμό κινητού τηλεφώνου σε μορφή +30XXXXXXXXX.",
            "id_number": "🆔 Δηλώστε τον ΑΦΜ σας (Αριθμός Φορολογικού Μητρώου).",
            "dob": "📅 Δηλώστε την ημερομηνία γέννησης σε μορφή ΗΗ/ΜΜ/ΕΕΕΕ.",
        },
    },

    "labels": {
        "access_code": "Access code",
        "full_name": "Full name",
        "phone": "Phone",
        "email": "Email",
        "loan_amount": "Loan amount",
        "id_number": "Identifier",
        "inn_ru": "INN (Russia only)",
        "reg_address": "Registered address",
        "actual_address": "Current address",
        "dob": "Date of birth",
        "marital_status": "Marital status",
        "workplace": "Workplace",
    },
}

L10N_EN.update({
    BTN_SUPPORT: L10N_EN["btn_support"],
    BTN_ABOUT: L10N_EN["btn_about"],
    BTN_CHANGE_COUNTRY: L10N_EN["btn_change_country"],
    BTN_MY_APPS: L10N_EN["btn_my_apps"],
    BTN_APPLY: L10N_EN["btn_apply"],
    BTN_BACK: L10N_EN["btn_back"],
})
_register("en", L10N_EN)
