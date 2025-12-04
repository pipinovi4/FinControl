STEPS = {

    # ----------------------
    # ACCESS CODE
    # ----------------------
    "access_code": {
        "label": "Zugangscode",
        "prompt": (
            "🔐 Haben Sie einen persönlichen Zugangscode?\n\n"
            "Geben Sie ihn unten ein — priorisierte Bearbeitung und individuelle Konditionen."
        ),
        "quick": None,
    },

    "access_code_checking": {
        "label": "Codeprüfung",
        "prompt": "⏳ Code wird geprüft…",
        "quick": None,
    },

    "access_code_ok": {
        "label": "Code akzeptiert",
        "prompt": "✅ Code akzeptiert. Individuelle Konditionen aktiviert.",
        "quick": None,
    },

    "access_code_bad": {
        "label": "Code ungültig",
        "prompt": "❌ Code nicht erkannt.",
        "quick": None,
    },

    "continue_without_code": {
        "label": "Ohne Code fortfahren",
        "prompt": "➡️ Ohne Code fortfahren",
        "quick": None,
    },

    # ----------------------
    # BASIC
    # ----------------------
    "full_name": {
        "label": "Vollständiger Name",
        "prompt": "✍️ Bitte geben Sie Ihren vollständigen Namen wie im Reisepass/Ausweis ein.",
        "quick": None,
    },

    "phone": {
        "label": "Telefonnummer",
        "prompt": (
            "📞 Bitte geben Sie Ihre Mobilnummer im Format +49XXXXXXXXXX ein.\n\n"
            "📲 Nummer teilen oder manuell eingeben."
        ),
        "quick": None,
    },

    "email": {
        "label": "E-Mail",
        "prompt": "📧 Bitte geben Sie Ihre E-Mail-Adresse ein.",
        "quick": None,
    },

    "loan_amount": {
        "label": "Kreditbetrag",
        "prompt": "💰 Gewünschten Kreditbetrag eingeben oder Option wählen.",
        "quick": [
            {"key": "MAX", "text": "💳 Maximal möglich"},
            {"key": "NOT_SURE", "text": "🤔 Noch unsicher"},
            {"key": "SKIP", "text": "⏭ Überspringen"},
        ],
    },

    "id_number_de": {
        "label": "Steuer-ID",
        "prompt": "🆔 Bitte geben Sie Ihre Steuer-Identifikationsnummer ein (11 Ziffern).",
        "quick": None,
    },

    "residential_address_de": {
        "label": "Wohnadresse",
        "prompt": "🏠 Aktuelle Wohnadresse eingeben.",
        "quick": None,
    },

    "dob_de": {
        "label": "Geburtsdatum",
        "prompt": "📅 Geburtsdatum TT.MM.JJJJ.",
        "quick": None,
    },

    # ----------------------
    # MARITAL STATUS
    # ----------------------
    "marital_status": {
        "label": "Familienstand",
        "prompt": "💬 Familienstand wählen:",
        "quick": [
            {"key": "single", "text": "Ledig"},
            {"key": "married", "text": "Verheiratet"},
            {"key": "divorced", "text": "Geschieden"},
            {"key": "widowed", "text": "Verwitwet"},
        ],
    },

    # ----------------------
    # EMPLOYMENT STATUS
    # ----------------------
    "employment_title": {
        "label": "Beschäftigungsstatus",
        "prompt": "🏢 Beschäftigungsstatus wählen:",
        "quick": [
            {"key": "Employed", "text": "👔 Angestellt"},
            {"key": "Business owner / Corporation", "text": "📊 Unternehmer / GmbH"},
            {"key": "Self-employed", "text": "💼 Selbstständig"},
            {"key": "Student", "text": "🎓 Student"},
            {"key": "Retired", "text": "👵 Rentner"},
            {"key": "Unemployed", "text": "🚫 Arbeitslos"},
        ],
    },

    # ----------------------
    # EMPLOYED BRANCH
    # ----------------------
    "employee_employer_name": {
        "label": "Arbeitgeber",
        "prompt": "Arbeitgeber (vollständiger Name).",
        "quick": None,
    },
    "employee_registered_address": {
        "label": "Registrierte Adresse",
        "prompt": "Registrierte Adresse des Arbeitgebers.",
        "quick": None,
    },
    "employee_actual_address": {
        "label": "Arbeitsadresse",
        "prompt": "Tatsächliche Arbeitsadresse.",
        "quick": None,
    },
    "employee_job_title": {
        "label": "Position",
        "prompt": "Position im Unternehmen.",
        "quick": None,
    },
    "employee_income": {
        "label": "Einkommen (netto)",
        "prompt": "Durchschnittliches Monatseinkommen (netto).",
        "quick": None,
    },
    "employee_income_proof": {
        "label": "Einkommensnachweis",
        "prompt": "Nachweisoption wählen.",
        "quick": [
            {"key": "PAYSLIP", "text": "Gehaltsabrechnung"},
            {"key": "BANK", "text": "Kontoauszug"},
            {"key": "EMPLOYER", "text": "Arbeitgeberbescheinigung"},
            {"key": "OTHER", "text": "Andere"},
        ],
    },
    "employee_job_start_date": {
        "label": "Beschäftigungsbeginn",
        "prompt": "Beschäftigungsbeginn.",
        "quick": None,
    },
    "employee_industry": {
        "label": "Branche",
        "prompt": "Branche (z. B. IT, Handel, Bau).",
        "quick": None,
    },

    # ----------------------
    # BUSINESS
    # ----------------------
    "biz_name": {
        "label": "Unternehmensname",
        "prompt": "Unternehmensname.",
        "quick": None,
    },
    "biz_reg_number": {
        "label": "Registrierungsnummer",
        "prompt": "Registrierungsnummer.",
        "quick": None,
    },
    "biz_reg_date": {
        "label": "Gründungsdatum",
        "prompt": "Gründungsdatum.",
        "quick": None,
    },
    "biz_turnover": {
        "label": "Monatlicher Umsatz",
        "prompt": "Monatlicher Umsatz.",
        "quick": None,
    },
    "biz_credit_lines": {
        "label": "Kreditlinien",
        "prompt": "Kreditlinien vorhanden?",
        "quick": [
            {"key": "Yes", "text": "Ja"},
            {"key": "No", "text": "Nein"},
        ],
    },
    "biz_tax_regime": {
        "label": "Steuersystem",
        "prompt": "Steuersystem.",
        "quick": None,
    },
    "biz_doc_upload": {
        "label": "Dokument",
        "prompt": "Unterstützendes Dokument hochladen (optional).",
        "quick": None,
    },

    # ----------------------
    # SELF-EMPLOYED
    # ----------------------
    "self_field": {
        "label": "Tätigkeitsfeld",
        "prompt": "Tätigkeitsfeld.",
        "quick": None,
    },
    "self_income": {
        "label": "Einkommen (netto)",
        "prompt": "Monatliches Einkommen (netto).",
        "quick": None,
    },
    "self_income_proof": {
        "label": "Einkommensnachweis",
        "prompt": "Wie können Sie Ihr Einkommen nachweisen?",
        "quick": [
            {"key": "BANK", "text": "Kontoauszug"},
            {"key": "CONTRACTS", "text": "Verträge"},
            {"key": "TAX", "text": "Steuerbescheid"},
            {"key": "OTHER", "text": "Andere"},
        ],
    },
    "self_doc_upload": {
        "label": "Dokument",
        "prompt": "Dokument hochladen (optional).",
        "quick": None,
    },

    # ----------------------
    # STUDENT
    # ----------------------
    "student_institution": {
        "label": "Bildungseinrichtung",
        "prompt": "Bildungseinrichtung (vollständiger Name).",
        "quick": None,
    },
    "student_dates": {
        "label": "Studienzeitraum",
        "prompt": "Beginn & voraussichtlicher Abschluss.",
        "quick": None,
    },
    "student_study_type": {
        "label": "Studienform",
        "prompt": "Studienform.",
        "quick": None,
    },
    "student_has_income": {
        "label": "Einkommen",
        "prompt": "Gibt es Einkommen?",
        "quick": [
            {"key": "Yes", "text": "Ja"},
            {"key": "No", "text": "Nein"},
        ],
    },
    "student_income_details": {
        "label": "Einkommensdetails",
        "prompt": "Falls Ja — Betrag & Nachweis.",
        "quick": None,
    },
    "student_guarantor": {
        "label": "Bürge",
        "prompt": "Haben Sie einen Bürgen?",
        "quick": None,
    },

    # ----------------------
    # RETIRED
    # ----------------------
    "retired_pension": {
        "label": "Rente",
        "prompt": "Monatliche Rente (netto).",
        "quick": None,
    },
    "retired_add_income": {
        "label": "Zusätzliches Einkommen",
        "prompt": "Zusätzliches Einkommen?",
        "quick": None,
    },
    "retired_add_income_details": {
        "label": "Details",
        "prompt": "Falls Ja — Quelle + Betrag.",
        "quick": None,
    },
    "retired_assets": {
        "label": "Vermögenswerte",
        "prompt": "Vermögenswerte?",
        "quick": None,
    },
    "retired_guarantor": {
        "label": "Bürge",
        "prompt": "Bürge (optional).",
        "quick": None,
    },

    # ----------------------
    # UNEMPLOYED
    # ----------------------
    "unemployed_regular_income": {
        "label": "Regelmäßiges Einkommen",
        "prompt": "Regelmäßiges Einkommen?",
        "quick": None,
    },
    "unemployed_regular_income_details": {
        "label": "Details",
        "prompt": "Falls Ja — Quelle und Betrag.",
        "quick": None,
    },
    "unemployed_assets": {
        "label": "Vermögenswerte",
        "prompt": "Vermögenswerte?",
        "quick": None,
    },
    "unemployed_guarantor": {
        "label": "Bürge",
        "prompt": "Bürge (optional).",
        "quick": None,
    },

    # ----------------------
    # EXTRA
    # ----------------------
    "extra_assets": {
        "label": "Vermögenswerte",
        "prompt": "Vermögenswerte?",
        "quick": None,
    },
    "extra_income": {
        "label": "Zusätzliches Einkommen",
        "prompt": "Zusätzliches Einkommen?",
        "quick": None,
    },
    "extra_emergency_contact": {
        "label": "Notfallkontakt",
        "prompt": "Notfallkontakt.",
        "quick": None,
    },

    # ----------------------
    # SCHUFA
    # ----------------------
    "credit_report_prompt_de": {
        "label": "SCHUFA",
        "prompt": "📎 SCHUFA-Auskunft hochladen.",
        "quick": None,
    },
}
