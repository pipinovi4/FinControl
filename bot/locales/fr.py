from __future__ import annotations
from . import register, BTN_SUPPORT, BTN_ABOUT, BTN_CHANGE_COUNTRY, BTN_MY_APPS, BTN_APPLY, BTN_BACK

L10N_FR = {
    # Вхід і вибір країни
    "prompt_choose_region": "🌍 Sélectionnez la région pour votre demande :",
    "prompt_choose_country": "🌍 Sélectionnez votre pays :",
    "after_country_selected": (
        "✅ Parfait, pays sélectionné.\nVous pouvez maintenant soumettre une demande, en savoir plus sur le service ou modifier vos paramètres."
    ),
    "menu_title": (
        "🧭 WorldFlow Credit — votre navigateur financier. "
        "Choisissez : dépôt de demande, support, information ou vos dossiers."
    ),

    # Головне меню
    "btn_apply": "📝 Déposer une demande",
    "apply_text": "C’est parti. Un code d’accès personnel n’est pas requis pour votre région.",
    "btn_support": "💬 Support",
    "btn_about": "ℹ️ À propos",
    "btn_change_country": "🌐 Changer de pays",
    "btn_my_apps": "📂 Mes demandes",

    # Секції
    "my_applications_text": (
        "<b>📂 Mes demandes</b>\n\n"
        "Vos demandes actives apparaîtront ici : statut, documents, commentaires et chat direct avec un conseiller.\n"
    ),
    "my_apps_stub": "Vos demandes apparaîtront ici (bientôt).",

    "support_text": (
        "<b>💬 Assistance WorldFlow Credit</b>\n\n"
        "Nous sommes là pour accélérer vos décisions :\n"
        "— résoudre les situations complexes,\n"
        "— indiquer les meilleures étapes,\n"
        "— vous mettre en relation avec le bon spécialiste.\n\n"
        "📲 Votre canal d’assistance personnel : <b>@WorldFlowSupport</b>"
    ),

    "about_text": "WorldFlow Credit — service international de demande de crédit.",

    "back_to_region": (
        "<b>↩️ Changer de région et continuer 🌐</b>\n\n"
        "💡 Indiquez le pays où vous vous trouvez actuellement — "
        "ainsi nous vous proposerons les produits et formulaires les plus pertinents."
    ),

    # Кнопки навігації / соцмережі
    "btn_back": "↩ Retour",
    "btn_website": "Site web",
    "btn_tg_channel": "Chaîne Telegram",
    "btn_instagram": "Instagram",
    "btn_x": "X / Twitter",
    "btn_linkedin": "LinkedIn",
    "btn_youtube": "YouTube",

    # UI мікротексти
    "ui": {
        "preview_title": "Avancement de la demande",
        "step": "Champ",
        "status": "Statut",
        "value": "Valeur",
        "done": "✅ Terminé",
        "todo": "❌ À compléter",
        "share_phone": "📲 Partager le numéro (remplissage automatique via Telegram)",
        "type_manually": "✏️ Entrer manuellement",
        "completed_demo": "Le formulaire a été rempli avec succès ✅",
        "return_to_menu": "🏠 Retour au menu",
    },

    # Загальні кроки (базові, з fallback). Для FR дата — JJ/MM/AAAA
    "steps": {
        "full_name": (
            "✍️ Veuillez indiquer votre nom complet exactement comme il apparaît sur votre passeport/pièce d’identité.\n\n"
            "ℹ️ Saisissez vos réponses directement dans les messages afin d’assurer un remplissage correct."
        ),
        "phone": "📞 Indiquez votre numéro de mobile au format international (ex. +33XXXXXXXXX).",
        "email": "📧 Veuillez indiquer votre adresse e-mail.",
        "telegram": "🤖 Veuillez indiquer votre compte Telegram pour le contact.\n(au format @username)",
        "loan_amount": (
            "💰 Veuillez indiquer le montant du prêt souhaité.\n"
            "Choisissez une des options ci-dessous ou saisissez-le manuellement.\n\n"
            "Boutons :\n"
            "💳 Maximum possible\n"
            "🤔 Pas encore sûr(e)\n"
            "⏭ Passer cette étape"
        ),
        "id_number": "🆔 Indiquez votre identifiant national (spécifique au pays).",
        "reg_address": "🏠 Indiquez votre adresse enregistrée (selon votre pièce d’identité).",
        "actual_address": "🏠 Indiquez votre adresse actuelle.\nSi identique, tapez « Identique ».",
        "dob": "📅 Veuillez indiquer votre date de naissance (JJ/MM/AAAA).",
        "marital_status": (
            "💬 Veuillez sélectionner votre situation familiale.\n\n"
            "Boutons :\n"
            "• Célibataire\n• Marié(e)\n• Divorcé(e)\n• Veuf / Veuve"
        ),
        "workplace": "🏢 Indiquez le nom complet de votre employeur (entreprise/organisation).",
    },

    # Пер-країнові підказки (FR)
    "steps_by_country": {
        "FR": {
            "phone": "📞 Indiquez votre numéro de mobile au format +33XXXXXXXXX.",
            "id_number": "🆔 Indiquez votre numéro de sécurité sociale (INSEE).",
            "dob": "📅 Veuillez indiquer votre date de naissance au format JJ/MM/AAAA.",
            "actual_address": "🏠 Adresse de résidence\nVeuillez indiquer votre adresse actuelle.",
        }
    },

    # Статус зайнятості та гілки
    "employment": {
        "status_prompt": (
            "🏢 Sélectionnez votre statut :\n\n"
            "Boutons :\n"
            "👔 Salarié\n"
            "📊 Entrepreneur / Société\n"
            "💼 Travailleur indépendant\n"
            "🎓 Étudiant\n"
            "👵 Retraité\n"
            "🚫 Sans emploi"
        ),

        # 👔 Salarié
        "employee": {
            "employer_name": "🏢 Veuillez indiquer le nom complet de votre employeur.",
            "employer_reg_address": "🏢 Entrez l’adresse officielle enregistrée de votre employeur.",
            "employer_actual_address": "📍 Indiquez l’adresse réelle du lieu de travail.\nSi identique, tapez « Identique ».",
            "job_title": "🧾 Veuillez préciser votre poste.",
            "net_income": "💵 Indiquez votre revenu mensuel moyen (après impôts).",
            "proof_of_income": (
                "📑 Sélectionnez une option de justificatif de revenu.\n\n"
                "Boutons :\n"
                "— Fiche de paie\n— Relevé bancaire\n— Attestation de l’employeur\n— Autre"
            ),
            "employment_start_date": "📅 Veuillez indiquer la date de début de votre emploi.",
            "industry": "🏭 Indiquez le secteur d’activité de votre employeur (ex. informatique, commerce, construction, santé).",
        },

        # 📊 Entrepreneur / Société
        "business_owner": {
            "business_name": "🏢 Veuillez indiquer le nom complet de votre entreprise.",
            "registration_number": "🆔 Indiquez le numéro d’enregistrement (ex. SIREN/SIRET ou n° société).",
            "registration_date": "📅 Indiquez la date de création/enregistrement de l’entreprise.",
            "turnover": "💵 Indiquez votre chiffre d’affaires mensuel moyen.",
            "credit_lines": "💳 Votre entreprise dispose-t-elle de lignes de crédit actives ? 👉 Oui / Non",
            "tax_regime": "📑 Sélectionnez votre régime fiscal : Simplifié / Général / Autre.",
            "doc_upload": "📂 Téléchargez un document justificatif (relevé bancaire ou déclaration fiscale, optionnel).",
        },

        # 💼 Travailleur indépendant
        "self_employed": {
            "activity_field": "📊 Indiquez votre domaine d’activité (ex. freelance, conseil, commerce, services).",
            "net_income": "💵 Indiquez votre revenu mensuel moyen (après impôts).",
            "proof_of_income": (
                "📑 Comment pouvez-vous justifier vos revenus ?\n\n"
                "Boutons :\n"
                "— Relevé bancaire\n"
                "— Contrats clients\n"
                "— Déclaration fiscale\n"
                "— Autre"
            ),
            "doc_upload": "📂 Téléchargez un document justificatif (si disponible).",
        },

        # 🎓 Étudiant
        "student": {
            "institution": "🎓 Indiquez le nom complet de votre établissement d’enseignement.",
            "dates": "📅 Indiquez la date de début et la date prévue de fin des études.",
            "study_type": "📚 Forme d’études : Temps plein / Temps partiel / En ligne.",
            "has_income": "💵 Avez-vous une source de revenu ? 👉 Oui / Non\n— Si Oui → précisez le montant et fournissez un justificatif.",
            "guarantor": "👥 Disposez-vous d’un garant ? 👉 Oui / Non",
        },

        # 👵 Retraité
        "retired": {
            "pension": "👵 Indiquez le montant de votre pension mensuelle (après impôts).",
            "additional_income": "💵 Avez-vous un revenu supplémentaire ? 👉 Oui / Non\n— Si Oui → précisez la source et le montant.",
            "assets": "🏡 Possédez-vous des biens (ex. logement, voiture) ? 👉 Oui / Non",
            "guarantor": (
                "👥 Si nécessaire, vous pouvez indiquer un garant :\n"
                "— Nom complet\n— Téléphone\n— Relation\n👉 Si non, écrivez « Aucun »."
            ),
        },

        # 🚫 Sans emploi
        "unemployed": {
            "regular_income": "💵 Avez-vous une source de revenu régulière (ex. loyers, emploi à temps partiel) ? 👉 Oui / Non\n— Si Oui → précisez la source et le montant.",
            "assets": "🏡 Possédez-vous des biens (ex. logement, voiture) ? 👉 Oui / Non",
            "guarantor": (
                "👥 Si nécessaire, vous pouvez indiquer un garant :\n"
                "— Nom complet\n— Téléphone\n— Relation\n👉 Si non, écrivez « Aucun »."
            ),
        },

        # 🔹 Bloc « Supplémentaire »
        "additional": {
            "assets": (
                "🏡 Possédez-vous des biens ?\n— Oui / Non\n\n"
                "Si Oui → précisez le type (appartement, maison, voiture, terrain, autre).\n"
                "Optionnel : seriez-vous disposé(e) à envisager un prêt garanti par le bien ?"
            ),
            "extra_income": "💵 Avez-vous un revenu supplémentaire ? — Oui / Non\nSi Oui → précisez la source et le montant.",
            "emergency_contact": (
                "👥 Personne à contacter en cas d’urgence (optionnel) :\n"
                "— Nom complet, téléphone, relation.\nVous pouvez aussi « Passer »."
            ),
        },
    },

    # Завантаження кредитних звітів (FR)
    "credit_reports": {
        "FR": {
            "prompt": "📎 Veuillez téléverser votre attestation / rapport de crédit",
            "buttons": [
                "Banque de France – FICP (banque-france.fr)"
            ],
            "ack_step": [
                "✅ Fichier 1 reçu. Joignez d’autres fichiers si nécessaire.",
                "✅ Tous les fichiers ont été reçus. Merci !"
            ]
        }
    },

    # About (французька версія «Про нас»)
    "about_full": (
        "<b>🌍 WorldFlow Credit — une plateforme fintech mondiale dédiée au crédit.</b>\n\n"
        "Nous connectons les clients directement aux banques, grâce à des solutions digitales et à l’expertise d’un réseau international "
        "de courtiers, analystes et conseillers financiers. Avec nous, le processus devient simple, transparent et rapide.\n\n"
        "💼 Notre écosystème rassemble des milliers de spécialistes et de partenaires dans le monde entier, travaillant au sein de l’espace numérique WorldFlow. "
        "Nous associons technologie bancaire et conseil financier pour garantir un traitement fluide des demandes.\n\n"
        "<b>✅ Nous proposons :</b>\n"
        "— 💳 crédits à la consommation, hypothécaires et automobiles en ligne ;\n"
        "— 💼 accompagnement digital des entreprises (auto-entrepreneurs / sociétés), croissance du chiffre d’affaires et conformité ;\n"
        "— 📊 outils de préparation au scoring de crédit pour maximiser vos chances d’approbation ;\n"
        "— 🤝 suivi personnalisé à chaque étape — de la demande au financement.\n\n"
        "⚡️ <b>Avec WorldFlow Credit, vous accédez non seulement à des produits financiers, "
        "mais à un véritable outil de banque digitale, adapté à vos objectifs.</b>"
    ),

    # Ярлики для панелі прогресу / резюме
    "labels": {
        "full_name": "Nom complet",
        "phone": "Téléphone",
        "email": "E-mail",
        "telegram": "Telegram",
        "loan_amount": "Montant du prêt",
        "id_number": "Identifiant",
        "reg_address": "Adresse enregistrée",
        "actual_address": "Adresse actuelle",
        "dob": "Date de naissance",
        "marital_status": "État civil",
        "workplace": "Employeur",
        "employment_status": "Statut",

        # Employé
        "employer_name": "Employeur",
        "employer_reg_address": "Adresse (enregistrée)",
        "employer_actual_address": "Adresse (travail)",
        "job_title": "Poste",
        "net_income": "Revenu mensuel net",
        "proof_of_income": "Justificatif de revenu",
        "employment_start_date": "Date de début",
        "industry": "Secteur",

        # Entrepreneur
        "business_name": "Entreprise",
        "registration_number": "N° d’enregistrement",
        "registration_date": "Date d’enregistrement",
        "turnover": "CA mensuel",
        "credit_lines": "Lignes de crédit",
        "tax_regime": "Régime fiscal",

        # Indépendant
        "activity_field": "Domaine d’activité",

        # Étudiant
        "institution": "Établissement",
        "study_type": "Forme d’études",
        "has_income": "Source de revenu",
        "guarantor": "Garant",

        # Retraité / Sans emploi / Supplémentaire
        "additional_income": "Revenu supplémentaire",
        "assets": "Biens",
        "emergency_contact": "Contact d’urgence",
    },
}

# Прив’язка констант до текстів кнопок
L10N_FR.update({
    BTN_SUPPORT: L10N_FR["btn_support"],
    BTN_ABOUT: L10N_FR["btn_about"],
    BTN_CHANGE_COUNTRY: L10N_FR["btn_change_country"],
    BTN_MY_APPS: L10N_FR["btn_my_apps"],
    BTN_APPLY: L10N_FR["btn_apply"],
    BTN_BACK: L10N_FR["btn_back"],
})

# Реєстрація локалі
register("fr", L10N_FR)

__all__ = ["L10N_FR"]
