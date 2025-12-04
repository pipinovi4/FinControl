STEPS = {

    # ----------------------
    # ACCESS CODE
    # ----------------------
    "access_code": {
        "label": "Code personnel",
        "prompt": (
            "🔐 Avez-vous un code d’accès personnel ?\n\n"
            "Saisissez-le ci-dessous — nous activerons vos conditions individuelles."
        ),
        "quick": None,
    },

    # ----------------------
    # BASIC
    # ----------------------
    "full_name": {
        "label": "Nom complet",
        "prompt": (
            "✍️ Veuillez indiquer votre nom complet exactement comme indiqué "
            "sur votre passeport/pièce d'identité."
        ),
        "quick": None,
    },

    "phone": {
        "label": "Téléphone",
        "prompt": "📞 Indiquez votre numéro de téléphone.",
        "quick": [
            {"key": "TELEGRAM_PHONE", "type": "contact", "text": "📱 Utiliser le numéro Telegram"},
        ],
    },

    "email": {
        "label": "Email",
        "prompt": "📧 Indiquez votre adresse e-mail.",
        "quick": None,
    },

    "telegram": {
        "label": "Compte Telegram",
        "prompt": "🤖 Indiquez votre username Telegram au format @username.",
        "quick": None,
    },

    "loan_amount": {
        "label": "Montant du prêt",
        "prompt": (
            "💰 Indiquez le montant du prêt souhaité.\n"
            "Choisissez une option ci-dessous ou saisissez le montant manuellement."
        ),
        "quick": [
            {"key": "MAX",     "text": "💳 Maximum possible"},
            {"key": "UNKNOWN", "text": "🤔 Je ne sais pas encore"},
            {"key": "SKIP",    "text": "⏭ Passer l’étape"},
        ],
    },

    "id_number": {
        "label": "Identifiant national",
        "prompt": "🆔 Indiquez votre identifiant national.",
        "quick": None,
    },

    "reg_address": {
        "label": "Adresse enregistrée",
        "prompt": "🏠 Indiquez votre adresse enregistrée.",
        "quick": None,
    },

    "actual_address": {
        "label": "Adresse actuelle",
        "prompt": "🏠 Indiquez votre adresse actuelle. Si identique — écrivez « Identique ».",
        "quick": None,
    },

    "dob": {
        "label": "Date de naissance",
        "prompt": "📅 Indiquez votre date de naissance (JJ/MM/AAAA).",
        "quick": None,
    },

    # ----------------------
    # MARITAL STATUS
    # ----------------------
    "marital_status": {
        "label": "Situation familiale",
        "prompt": "💬 Sélectionnez votre situation familiale.",
        "quick": [
            {"key": "single",   "text": "Célibataire"},
            {"key": "married",  "text": "Marié(e)"},
            {"key": "divorced", "text": "Divorcé(e)"},
            {"key": "widowed",  "text": "Veuf / Veuve"},
        ],
    },

    # ----------------------
    # EMPLOYMENT STATUS
    # ----------------------
    "employment_status": {
        "label": "Statut professionnel",
        "prompt": "🏢 Sélectionnez votre statut.",
        "quick": [
            {"key": "Employed",                     "text": "Salarié"},
            {"key": "Business owner / Corporation", "text": "Entrepreneur / Société"},
            {"key": "Self-employed",                "text": "Indépendant"},
            {"key": "Student",                      "text": "Étudiant"},
            {"key": "Retired",                      "text": "Retraité"},
            {"key": "Unemployed",                   "text": "Sans emploi"},
        ],
    },

    # ----------------------
    # EMPLOYED BRANCH
    # ----------------------
    "employer_name": {
        "label": "Employeur",
        "prompt": "🏢 Indiquez le nom complet de votre employeur.",
        "quick": None,
    },
    "employer_reg_address": {
        "label": "Adresse légale",
        "prompt": "📍 Indiquez l'adresse légale de l’entreprise.",
        "quick": None,
    },
    "employer_actual_address": {
        "label": "Adresse réelle",
        "prompt": "📍 Indiquez l'adresse réelle de votre lieu de travail (ou « Identique »).",
        "quick": None,
    },
    "job_title": {
        "label": "Poste",
        "prompt": "💼 Indiquez votre poste.",
        "quick": None,
    },
    "income_net_monthly": {
        "label": "Revenu mensuel (net)",
        "prompt": "💵 Indiquez votre revenu mensuel net.",
        "quick": None,
    },
    "income_proof": {
        "label": "Justificatif de revenu",
        "prompt": "📑 Choisissez un type de justificatif de revenu.",
        "quick": [
            {"key": "2NDFL",    "text": "Fiche de paie"},
            {"key": "BANK",     "text": "Relevé bancaire"},
            {"key": "EMPLOYER", "text": "Attestation employeur"},
            {"key": "OTHER",    "text": "Autre"},
        ],
    },
    "employment_start_date": {
        "label": "Date de début",
        "prompt": "📅 Indiquez votre date de début d’emploi.",
        "quick": None,
    },
    "employer_industry": {
        "label": "Secteur",
        "prompt": "🏭 Indiquez le secteur d’activité de votre employeur.",
        "quick": None,
    },

    # ----------------------
    # BUSINESS BRANCH
    # ----------------------
    "business_name": {
        "label": "Entreprise",
        "prompt": "🏢 Indiquez le nom de votre entreprise.",
        "quick": None,
    },
    "business_reg_number": {
        "label": "Numéro d’enregistrement",
        "prompt": "🆔 Indiquez le numéro d’enregistrement de votre entreprise.",
        "quick": None,
    },
    "business_reg_date": {
        "label": "Date d’enregistrement",
        "prompt": "📅 Indiquez la date d’enregistrement de votre entreprise.",
        "quick": None,
    },
    "business_turnover_monthly": {
        "label": "Chiffre d’affaires mensuel",
        "prompt": "💵 Indiquez votre chiffre d’affaires mensuel.",
        "quick": None,
    },
    "business_credit_lines": {
        "label": "Lignes de crédit",
        "prompt": "💳 Avez-vous des lignes de crédit ?",
        "quick": [
            {"key": "Yes", "text": "Oui"},
            {"key": "No",  "text": "Non"},
        ],
    },
    "business_tax_regime": {
        "label": "Régime fiscal",
        "prompt": "📑 Sélectionnez votre régime fiscal.",
        "quick": [
            {"key": "Simplified", "text": "Simplifié"},
            {"key": "General",    "text": "Général"},
            {"key": "Other",      "text": "Autre"},
        ],
    },
    "business_doc_upload": {
        "label": "Documents d’entreprise",
        "prompt": "📂 Téléversez un document justificatif si possible.",
        "quick": None,
    },

    # ----------------------
    # SELF-EMPLOYED
    # ----------------------
    "activity_field": {
        "label": "Domaine d’activité",
        "prompt": "📊 Indiquez votre domaine d’activité.",
        "quick": None,
    },
    "supporting_doc_upload": {
        "label": "Document justificatif",
        "prompt": "📂 Téléversez un document si disponible.",
        "quick": None,
    },

    # ----------------------
    # STUDENT BRANCH
    # ----------------------
    "university_name": {
        "label": "Établissement",
        "prompt": "🎓 Indiquez le nom complet de votre établissement.",
        "quick": None,
    },
    "study_dates": {
        "label": "Période d’études",
        "prompt": "📅 Indiquez les dates de début et de fin d’études.",
        "quick": None,
    },
    "study_mode": {
        "label": "Type d’étude",
        "prompt": "📚 Sélectionnez votre type d’étude.",
        "quick": [
            {"key": "Full-time", "text": "Temps plein"},
            {"key": "Part-time", "text": "Temps partiel"},
            {"key": "Online",    "text": "En ligne"},
        ],
    },
    "income_present": {
        "label": "Revenu disponible",
        "prompt": "💵 Avez-vous un revenu ?",
        "quick": [
            {"key": "Yes", "text": "Oui"},
            {"key": "No",  "text": "Non"},
        ],
    },
    "income_amount": {
        "label": "Montant du revenu",
        "prompt": "💵 Indiquez le montant de votre revenu.",
        "quick": None,
    },
    "guarantor_available": {
        "label": "Garant",
        "prompt": "👥 Avez-vous un garant ?",
        "quick": [
            {"key": "Yes", "text": "Oui"},
            {"key": "No",  "text": "Non"},
        ],
    },
    "guarantor_fullname": {
        "label": "Nom du garant",
        "prompt": "👤 Indiquez le nom complet du garant.",
        "quick": None,
    },
    "guarantor_phone": {
        "label": "Téléphone du garant",
        "prompt": "📞 Indiquez le numéro du garant.",
        "quick": None,
    },
    "guarantor_relation": {
        "label": "Lien",
        "prompt": "👥 Indiquez votre lien avec le garant.",
        "quick": None,
    },

    # ----------------------
    # RETIRED
    # ----------------------
    "pension_amount": {
        "label": "Pension",
        "prompt": "👵 Indiquez le montant de votre pension.",
        "quick": None,
    },
    "additional_income": {
        "label": "Revenu supplémentaire",
        "prompt": "💵 Avez-vous un revenu supplémentaire ?",
        "quick": [
            {"key": "Yes", "text": "Oui"},
            {"key": "No",  "text": "Non"},
        ],
    },
    "assets_owned": {
        "label": "Biens possédés",
        "prompt": "🏡 Possédez-vous des biens ?",
        "quick": [
            {"key": "Yes", "text": "Oui"},
            {"key": "No",  "text": "Non"},
        ],
    },
    "guarantor_optional": {
        "label": "Garant (optionnel)",
        "prompt": "👥 Indiquez les données du garant si nécessaire.",
        "quick": None,
    },

    # ----------------------
    # UNEMPLOYED
    # ----------------------
    "regular_income": {
        "label": "Revenu régulier",
        "prompt": "💵 Avez-vous un revenu régulier ?",
        "quick": [
            {"key": "Yes", "text": "Oui"},
            {"key": "No",  "text": "Non"},
        ],
    },

    # ----------------------
    # CREDIT REPORTS
    # ----------------------
    "credit_report_ru": {
        "label": "Rapports de crédit RF",
        "prompt": "📎 Téléversez vos rapports de crédit (3 fichiers).",
        "quick": None,
    },
    "credit_report_by": {
        "label": "Rapport de crédit (BY)",
        "prompt": "📎 Téléversez le rapport de crédit.",
        "quick": None,
    },
    "credit_report_kz": {
        "label": "Rapport de crédit (KZ)",
        "prompt": "📎 Téléversez le rapport de crédit.",
        "quick": None,
    },
}

__all__ = ["STEPS"]
