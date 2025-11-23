from __future__ import annotations
from . import _register, BTN_SUPPORT, BTN_ABOUT, BTN_CHANGE_COUNTRY, BTN_MY_APPS, BTN_APPLY, BTN_BACK

L10N_FR = {
    "prompt_choose_region": "🌍 Sélectionnez la région pour votre demande :",
    "prompt_choose_country": "🌍 Sélectionnez votre pays :",
    "after_country_selected": "✅ Pays sélectionné : {country}\nLa langue a été réglée automatiquement.",
    "menu_title": "Que souhaitez-vous faire ensuite ?",
    "btn_apply": "📝 Déposer une demande",
    "apply_text": "C’est parti. Un code d’accès personnel peut être saisi à la première étape.",
    "btn_support": "🛟 Support",
    "btn_about": "ℹ️ À propos",
    "btn_change_country": "🌐 Changer de pays",
    "btn_my_apps": "🗂 Mes demandes",
    "support_text": "Écrivez-nous : @{support_username}",
    "about_text": "WorldFlow Credit — service international de demande de crédit.",
    "my_apps_stub": "Vos demandes apparaîtront ici (bientôt).",
    "back_to_region": "↩️ Retour à la sélection de région.",
    "btn_back": "↩ Retour",
    "btn_website": "Site web",
    "btn_tg_channel": "Chaîne Telegram",
    "btn_instagram": "Instagram",
    "btn_x": "X / Twitter",
    "btn_linkedin": "LinkedIn",
    "btn_youtube": "YouTube",

    "ui": {
        "preview_title": "Avancement de la demande",
        "step": "Champ",
        "status": "Statut",
        "value": "Valeur",
        "done": "✅ Terminé",
        "todo": "❌ À compléter",
        "share_phone": "📲 Partager le numéro",
        "type_manually": "✏️ Entrer manuellement",
        "completed_demo": "Le formulaire a été rempli avec succès ✅",
    },

    "about_full": (
        "<b>WorldFlow Credit — À propos</b><br/><br/>"
        "Plateforme internationale de demande de crédit : KYC standardisé, contrôles de risque automatisés "
        "et acheminement sécurisé vers des prêteurs agréés.<br/><br/>"
        "• Conditions transparentes, sans frais cachés<br/>"
        "• Données chiffrées en transit et au repos<br/>"
        "• Instruction rapide via des partenaires vérifiés<br/>"
        "• Support en anglais et langues locales"
    ),

    "steps_by_country": {
        "FR": {
            "phone": "📞 Indiquez votre numéro de mobile au format +33XXXXXXXXX.",
            "id_number": "🆔 Indiquez votre numéro de sécurité sociale (INSEE).",
            "dob": "📅 Veuillez indiquer votre date de naissance au format JJ/MM/AAAA.",
        }
    },

    "labels": {
        "access_code": "Code d’accès",
        "full_name": "Nom complet",
        "phone": "Téléphone",
        "email": "E-mail",
        "loan_amount": "Montant du prêt",
        "id_number": "Identifiant",
        "inn_ru": "INN (Russie uniquement)",
        "reg_address": "Adresse enregistrée",
        "actual_address": "Adresse actuelle",
        "dob": "Date de naissance",
        "marital_status": "État civil",
        "workplace": "Employeur",
    },
}

L10N_FR.update({
    BTN_SUPPORT: L10N_FR["btn_support"],
    BTN_ABOUT: L10N_FR["btn_about"],
    BTN_CHANGE_COUNTRY: L10N_FR["btn_change_country"],
    BTN_MY_APPS: L10N_FR["btn_my_apps"],
    BTN_APPLY: L10N_FR["btn_apply"],
    BTN_BACK: L10N_FR["btn_back"],
})
_register("fr", L10N_FR)
