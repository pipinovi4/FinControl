from __future__ import annotations
from . import _register, BTN_SUPPORT, BTN_ABOUT, BTN_CHANGE_COUNTRY, BTN_MY_APPS, BTN_APPLY, BTN_BACK

L10N_EL = {
    "prompt_choose_region": "🌍 Επιλέξτε περιοχή για την αίτησή σας:",
    "prompt_choose_country": "🌍 Επιλέξτε χώρα:",
    "after_country_selected": "✅ Επιλέχθηκε χώρα: {country}\nΗ γλώσσα ορίστηκε αυτόματα.",
    "menu_title": "Πώς συνεχίζουμε;",
    "btn_apply": "📝 Υποβολή αίτησης",
    "apply_text": "Ξεκινάμε. Μπορείτε να εισαγάγετε προσωπικό κωδικό στο πρώτο βήμα.",
    "btn_support": "🛟 Υποστήριξη",
    "btn_about": "ℹ️ Σχετικά με εμάς",
    "btn_change_country": "🌐 Αλλαγή χώρας",
    "btn_my_apps": "🗂 Οι αιτήσεις μου",
    "support_text": "Γράψτε μας: @{support_username}",
    "about_text": "WorldFlow Credit — διεθνής υπηρεσία αιτήσεων πίστωσης.",
    "my_apps_stub": "Οι αιτήσεις σας θα εμφανιστούν εδώ (σύντομα).",
    "back_to_region": "↩️ Επιστροφή στην επιλογή περιοχής.",
    "btn_back": "↩ Πίσω",
    "btn_website": "Ιστότοπος",
    "btn_tg_channel": "Κανάλι Telegram",
    "btn_instagram": "Instagram",
    "btn_x": "X / Twitter",
    "btn_linkedin": "LinkedIn",
    "btn_youtube": "YouTube",

    "ui": {
        "preview_title": "Κατάσταση αίτησης",
        "step": "Πεδίο",
        "status": "Κατάσταση",
        "value": "Τιμή",
        "done": "✅ Ολοκληρώθηκε",
        "todo": "❌ Εκκρεμεί",
        "share_phone": "📲 Κοινοποίηση αριθμού",
        "type_manually": "✏️ Εισαγωγή χειροκίνητα",
        "completed_demo": "Η φόρμα συμπληρώθηκε με επιτυχία ✅",
    },

    "about_full": (
        "<b>WorldFlow Credit — Σχετικά με εμάς</b><br/><br/>"
        "Διεθνής πλατφόρμα αιτήσεων πίστωσης: τυποποιημένο KYC, αυτοματοποιημένοι έλεγχοι κινδύνου "
        "και ασφαλής προώθηση σε αδειοδοτημένους δανειοδότες.<br/><br/>"
        "• Διαφανείς όροι, χωρίς κρυφές χρεώσεις<br/>"
        "• Κρυπτογράφηση δεδομένων κατά τη μετάδοση και αποθήκευση<br/>"
        "• Γρήγορη αξιολόγηση μέσω πιστοποιημένων συνεργατών<br/>"
        "• Υποστήριξη στα αγγλικά και στις τοπικές γλώσσες"
    ),

    "steps_by_country": {
        "GR": {
            "phone": "📞 Εισαγάγετε τον αριθμό κινητού σε μορφή +30XXXXXXXXX.",
            "id_number": "🆔 Δηλώστε τον ΑΦΜ σας (Αριθμός Φορολογικού Μητρώου).",
            "dob": "📅 Δηλώστε την ημερομηνία γέννησης σε μορφή ΗΗ/ΜΜ/ΕΕΕΕ.",
        }
    },

    "labels": {
        "access_code": "Κωδικός πρόσβασης",
        "full_name": "Πλήρες όνομα",
        "phone": "Τηλέφωνο",
        "email": "Email",
        "loan_amount": "Ποσό δανείου",
        "id_number": "Αριθμός ταυτοποίησης",
        "inn_ru": "INN (μόνο Ρωσία)",
        "reg_address": "Διεύθυνση εγγραφής",
        "actual_address": "Τρέχουσα διεύθυνση",
        "dob": "Ημερομηνία γέννησης",
        "marital_status": "Οικογενειακή κατάσταση",
        "workplace": "Φορέας εργασίας",
    },
}

L10N_EL.update({
    BTN_SUPPORT: L10N_EL["btn_support"],
    BTN_ABOUT: L10N_EL["btn_about"],
    BTN_CHANGE_COUNTRY: L10N_EL["btn_change_country"],
    BTN_MY_APPS: L10N_EL["btn_my_apps"],
    BTN_APPLY: L10N_EL["btn_apply"],
    BTN_BACK: L10N_EL["btn_back"],
})
_register("el", L10N_EL)
