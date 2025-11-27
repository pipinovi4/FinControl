from __future__ import annotations
from locales import register, BTN_SUPPORT, BTN_ABOUT, BTN_CHANGE_COUNTRY, BTN_MY_APPS, BTN_APPLY, BTN_BACK

L10N_DE = {
    # --------- Menü / Basistexte ---------
    "prompt_choose_region": "🌍 Wählen Sie die Region für Ihren Antrag:",
    "prompt_choose_country": "🌍 Wählen Sie Ihr Land:",
    "after_country_selected": (
        "✅ Perfekt, Land ausgewählt.\n"
        "Sie können nun einen Antrag stellen, mehr über den Service erfahren oder Ihre Einstellungen ändern."
    ),
    "menu_title": (
        "🧭 WorldFlow Credit — Ihr Finanznavigator. "
        "Wählen Sie: Antrag, Support, Informationen oder Meine Anträge."
    ),

    "btn_apply": "📝 Antrag stellen",
    "apply_text": "Legen wir los. Einen persönlichen Code können Sie im ersten Schritt eingeben.",
    "btn_support": "🛟 Support",
    "btn_about": "ℹ️ Über uns",
    "btn_change_country": "🌐 Land wechseln",
    "btn_my_apps": "🗂 Meine Anträge",

    "my_applications_text": (
        "<b>🗂 Meine Anträge</b>\n\n"
        "Hier erscheinen Ihre aktiven Anträge: Status, Dokumente, Kommentare und Chat mit einem Experten.\n"
    ),

    "support_text": (
        "<b>💬 WorldFlow Credit Support</b>\n\n"
        "Wir sind für Sie da, damit Entscheidungen schneller getroffen werden:\n"
        "— wir lösen komplexe Situationen,\n"
        "— zeigen optimale nächste Schritte,\n"
        "— verbinden Sie mit dem passenden Spezialisten.\n\n"
        "📲 Ihr persönlicher Support-Kanal: <b>@WorldFlowSupport</b>"
    ),

    "about_text": "WorldFlow Credit — internationaler Kredit-Antragsservice.",
    "my_apps_stub": "Ihre Anträge erscheinen hier (bald).",

    "back_to_region": (
        "<b>↩️ Region wechseln und fortfahren 🌐</b>\n\n"
        "💡 Geben Sie das Land an, in dem Sie sich gerade befinden — "
        "so zeigen wir Ihnen die relevantesten Produkte und Formulare."
    ),

    "btn_back": "↩ Zurück",
    "btn_website": "Webseite",
    "btn_tg_channel": "Telegram-Kanal",
    "btn_instagram": "Instagram",
    "btn_x": "X / Twitter",
    "btn_linkedin": "LinkedIn",
    "btn_youtube": "YouTube",

    # --------- UI ---------
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
        "back_to_menu": "↩ Zurück zum Menü",
        "skip_step": "⏭ Überspringen",
    },

    # --------- Ausführlicher „Über uns“-Block ---------
    "about_full": (
        "<b>🌍 WorldFlow Credit — eine globale Fintech-Plattform für Kreditlösungen.</b>\n\n"
        "Wir verbinden Kunden direkt mit Banken, durch digitale Lösungen und die Expertise internationaler Broker, Analysten und Berater. "
        "Mit uns wird der Prozess einfach, transparent und schnell.\n\n"
        "💼 Unser Ökosystem umfasst Tausende von Spezialisten und Partnern weltweit, die im digitalen Raum von WorldFlow zusammenarbeiten. "
        "Wir kombinieren Bankentechnologien mit Finanzberatung, damit Ihre Anträge ohne Hindernisse bearbeitet werden.\n\n"
        "<b>✅ Wir bieten:</b>\n"
        "— 💳 Online-Kredite für Konsum, Immobilien und Fahrzeuge;\n"
        "— 💼 digitale Unterstützung für Unternehmen (Einzelunternehmer / GmbH), Umsatzwachstum und Geschäftsbegleitung;\n"
        "— 📊 Algorithmen zur Vorbereitung auf Bonitätsscoring zur Steigerung der Genehmigungschancen;\n"
        "— 🤝 persönliche Begleitung in jeder Phase — von der Antragstellung bis zur Auszahlung.\n\n"
        "⚡️ <b>Mit WorldFlow Credit erhalten Sie nicht nur Zugang zu Finanzprodukten, "
        "sondern ein vollständiges digitales Banking-Tool, das Ihre Ziele unterstützt.</b>"
    ),

    # --------- Formularschritte (universelle Prompts) ---------
    "steps": {
        # Hinweis: Der Access-Code-Schritt gilt laut Notizen nur für RU/BY/KZ.
        # Wir hinterlegen Texte generisch; die Logik blendet ihn für DE aus.
        "access_code_intro": (
            "🔐 Haben Sie einen persönlichen Zugangscode?\n\n"
            "Geben Sie ihn unten ein — wir aktivieren priorisierte Bearbeitung und individuelle Konditionen."
        ),
        "access_code_checking": "⏳ Code wird geprüft…",
        "access_code_ok": (
            "✅ Code akzeptiert.\n\n"
            "Individuelle Konditionen aktiviert: priorisierte Bearbeitung und personalisierte Antragsparameter."
        ),
        "access_code_bad": (
            "❌ Code nicht erkannt.\n"
            "Bitte prüfen Sie die Eingabe oder fahren Sie ohne Code fort."
        ),
        "continue_without_code": "➡️ Ohne Code fortfahren",

        # Vollständiger Name
        "full_name": (
            "✍️ Bitte geben Sie Ihren vollständigen Namen genau wie im Reisepass/Ausweis angegeben ein.\n\n"
            "ℹ️ Geben Sie Ihre Antworten direkt in den Nachrichten ein, damit das Formular korrekt ausgefüllt wird."
        ),

        # Telefon / E-Mail / Telegram
        "phone": (
            "📞 Bitte geben Sie Ihre Mobilnummer im Format +49XXXXXXXXXX ein.\n\n"
            "📲 Sie können:\n— Ihre Nummer teilen (automatisch aus Telegram)\n— Manuell eingeben"
        ),
        "email": "📧 Bitte geben Sie Ihre E-Mail-Adresse ein.",
        "telegram": "🤖 Bitte geben Sie Ihren Telegram-Account für die Kontaktaufnahme an. (im Format @username)",

        # Kreditsumme
        "loan_amount": (
            "💰 Bitte geben Sie den gewünschten Kreditbetrag ein.\n"
            "Wählen Sie eine der Optionen unten oder geben Sie den Betrag manuell ein."
        ),
        "loan_amount_options": {
            "max": "💳 Maximal möglich",
            "not_sure": "🤔 Noch unsicher",
            "skip": "⏭ Überspringen",
        },

        # ID / Steuernummer (DE)
        "id_number_de": (
            "Schritt 6. Steuer-Identifikationsnummer (Steuer-ID)\n"
            "🆔 Bitte geben Sie Ihre Steuer-ID ein (11 Ziffern)."
        ),

        # Adresse
        "residential_address_de": (
            "Schritt 7. Wohnadresse\n"
            "🏠 Bitte geben Sie Ihre aktuelle Wohnadresse an."
        ),

        # Geburtsdatum
        "dob_de": "📅 Bitte geben Sie Ihr Geburtsdatum im Format TT.MM.JJJJ ein.",

        # Familienstand
        "marital_status": "💬 Bitte wählen Sie Ihren Familienstand aus.",
        "marital_status_options": [
            "Ledig",
            "Verheiratet",
            "Geschieden",
            "Verwitwet",
        ],

        # Beschäftigungsstatus
        "employment_title": "🏢 Wählen Sie Ihren Status:",
        "employment_options": [
            "👔 Angestellt",
            "📊 Unternehmer / GmbH",
            "💼 Selbstständig",
            "🎓 Student",
            "👵 Rentner",
            "🚫 Arbeitslos",
        ],

        # ---- Branch: Angestellt
        "employee_employer_name": "Bitte geben Sie den vollständigen Namen Ihres Arbeitgebers an.",
        "employee_registered_address": "Geben Sie die offizielle registrierte Adresse Ihres Arbeitgebers an.",
        "employee_actual_address": (
            "Geben Sie die tatsächliche Arbeitsadresse an.\nFalls identisch, schreiben Sie „Gleich“."
        ),
        "employee_job_title": "Bitte geben Sie Ihre Position im Unternehmen an.",
        "employee_income": "Geben Sie Ihr durchschnittliches monatliches Einkommen (nach Steuern) an.",
        "employee_income_proof": "Wählen Sie eine verfügbare Option zum Nachweis Ihres Einkommens.",
        "employee_income_proof_options": [
            "Gehaltsabrechnung",
            "Kontoauszug",
            "Arbeitgeberbescheinigung",
            "Andere",
        ],
        "employee_job_start_date": "Bitte geben Sie das Datum Ihres Beschäftigungsbeginns an.",
        "employee_industry": "Bitte geben Sie die Branche Ihres Arbeitgebers an (z. B. IT, Einzelhandel, Bauwesen).",

        # ---- Branch: Unternehmer / GmbH (Business owner)
        "biz_name": "Bitte geben Sie den vollständigen Namen Ihres Unternehmens an.",
        "biz_reg_number": "Geben Sie die Registrierungsnummer Ihres Unternehmens ein (Handelsregister-Nr. oder Steuer-ID).",
        "biz_reg_date": "Geben Sie das Datum der Unternehmensgründung an.",
        "biz_turnover": "Geben Sie den durchschnittlichen monatlichen Umsatz an.",
        "biz_credit_lines": "Hat Ihr Unternehmen aktive Kreditlinien oder Banklimits? 👉 Ja / Nein",
        "biz_tax_regime": "Wählen Sie Ihr Steuersystem: Vereinfacht / Allgemein / Anderes.",
        "biz_doc_upload": "📂 Laden Sie ein unterstützendes Dokument hoch (optional).",

        # ---- Branch: Selbstständig
        "self_field": "Bitte geben Sie Ihr Tätigkeitsfeld an (z. B. Freiberufler, Handel, Dienstleistungen).",
        "self_income": "Geben Sie Ihr durchschnittliches monatliches Einkommen (nach Steuern) an.",
        "self_income_proof": "Wie können Sie Ihr Einkommen nachweisen?",
        "self_income_proof_options": [
            "Kontoauszug",
            "Verträge mit Kunden",
            "Steuerbescheid",
            "Andere",
        ],
        "self_doc_upload": "📂 Laden Sie ein Nachweisdokument hoch (falls verfügbar).",

        # ---- Branch: Student
        "student_institution": "Bitte geben Sie den vollständigen Namen Ihrer Bildungseinrichtung an.",
        "student_dates": "Geben Sie das Beginn- und voraussichtliche Abschlussdatum an.",
        "student_study_type": "Wählen Sie Ihre Studienform: Vollzeit / Teilzeit / Online.",
        "student_has_income": "Haben Sie derzeit eine Einkommensquelle? 👉 Ja / Nein",
        "student_income_details": "Falls Ja — Betrag angeben und Nachweis hochladen.",
        "student_guarantor": "Haben Sie einen Bürgen? 👉 Ja / Nein",

        # ---- Branch: Rentner
        "retired_pension": "Bitte geben Sie Ihre monatliche Rente an (nach Steuern).",
        "retired_add_income": "Haben Sie zusätzliches Einkommen? 👉 Ja / Nein",
        "retired_add_income_details": "Falls Ja — Quelle und Betrag angeben.",
        "retired_assets": "Besitzen Sie Vermögenswerte (z. B. Wohnung, Auto)? 👉 Ja / Nein",
        "retired_guarantor": (
            "Falls nötig, können Sie einen Bürgen angeben:\n— Vollständiger Name\n— Telefonnummer\n— Beziehung\n👉 Wenn nicht, schreiben Sie „Keiner“."
        ),

        # ---- Branch: Arbeitslos
        "unemployed_regular_income": "Haben Sie regelmäßige Einkommensquellen (z. B. Mieteinnahmen, Nebenjobs)? 👉 Ja / Nein",
        "unemployed_regular_income_details": "Falls Ja — Quelle und Betrag angeben.",
        "unemployed_assets": "Besitzen Sie Vermögenswerte (z. B. Wohnung, Auto)? 👉 Ja / Nein",
        "unemployed_guarantor": (
            "Falls nötig, können Sie einen Bürgen angeben:\n— Vollständiger Name\n— Telefonnummer\n— Beziehung\n👉 Wenn nicht, schreiben Sie „Keiner“."
        ),

        # ---- Zusatzblock (falls oben noch nicht abgefragt)
        "extra_block_title": "➕ Zusätzliche Informationen",
        "extra_assets": (
            "🏡 Gibt es Vermögenswerte?\n— Ja / Nein\n— Falls Ja → Art angeben (Wohnung, Haus, Auto, Grundstück, anderes).\n"
            "— Optional: Sind Sie bereit, ein Darlehen mit Besicherung durch Vermögen zu prüfen?"
        ),
        "extra_income": (
            "💵 Gibt es zusätzliches Einkommen?\n— Ja / Nein\n— Falls Ja → Quelle + Betrag angeben."
        ),
        "extra_emergency_contact": (
            "👥 Notfall-Kontaktperson:\n— Vollständiger Name\n— Telefon\n— Beziehung\n👉 Kann übersprungen werden."
        ),

        # ---- Kreditbericht (Deutschland)
        "credit_report_prompt_de": "📎 Bitte laden Sie Ihre SCHUFA-Auskunft hoch.",
        "credit_report_sources_de": [
            "SCHUFA (https://schufa.de/)"
        ],
        "upload_ack_1ofN": "✅ Datei {i}/{n} erhalten. Bitte weitere Datei anhängen.",
        "upload_all_received": "✅ Alle Dateien erhalten. Vielen Dank!",
    },

    # --------- Länderspezifische Formate ---------
    "steps_by_country": {
        "DE": {
            "phone": "📞 Bitte geben Sie Ihre Handynummer im Format +49XXXXXXXXXX ein.",
            "id_number": "🆔 Bitte geben Sie Ihre Steuer-ID ein (11 Ziffern).",
            "dob": "📅 Bitte geben Sie Ihr Geburtsdatum im Format TT.MM.JJJJ ein.",
            "address": "🏠 Wohnadresse (Straße, Nr., PLZ, Ort).",
        }
    },

    # --------- Labels (Schlüssel für gespeicherte Werte) ---------
    "labels": {
        "access_code": "Zugangscode",
        "full_name": "Vollständiger Name",
        "phone": "Telefon",
        "email": "E-Mail",
        "telegram": "Telegram",
        "loan_amount": "Kreditsumme",
        "id_number": "Steuer-ID",
        "reg_address": "Meldeadresse",
        "actual_address": "Aktuelle Adresse",
        "dob": "Geburtsdatum",
        "marital_status": "Familienstand",
        "employment_status": "Beschäftigungsstatus",

        # Angestellt
        "employer_name": "Arbeitgeber",
        "employer_reg_address": "Arbeitgeber-Adresse (registriert)",
        "employer_actual_address": "Arbeitsadresse (tatsächlich)",
        "job_title": "Position",
        "monthly_income": "Monatliches Einkommen (netto)",
        "income_proof": "Einkommensnachweis",
        "job_start_date": "Beschäftigungsbeginn",
        "employer_industry": "Branche des Arbeitgebers",

        # Unternehmen
        "biz_name": "Unternehmensname",
        "biz_reg_number": "Registrierungsnummer",
        "biz_reg_date": "Gründungsdatum",
        "biz_turnover": "Durchschnittlicher Monatsumsatz",
        "biz_credit_lines": "Kreditlinien",
        "biz_tax_regime": "Steuersystem",
        "biz_doc": "Unterstützendes Dokument (optional)",

        # Selbstständig
        "self_field": "Tätigkeitsfeld",
        "self_income": "Monatliches Einkommen (netto)",
        "self_income_proof": "Einkommensnachweis",
        "self_doc": "Nachweisdokument (optional)",

        # Student
        "student_institution": "Bildungseinrichtung",
        "student_enroll_date": "Beginn",
        "student_grad_date": "Vorauss. Abschluss",
        "student_study_type": "Studienform",
        "student_has_income": "Einkommensquelle",
        "student_income_amount": "Einkommensbetrag",
        "student_income_proof": "Nachweis",
        "student_has_guarantor": "Bürge",

        # Rentner
        "pension_amount": "Rente (monatlich, netto)",
        "retired_extra_income": "Zusätzliches Einkommen",
        "retired_assets": "Vermögenswerte",
        "retired_guarantor": "Bürge",

        # Arbeitslos
        "unemployed_regular_income": "Regelmäßiges Einkommen",
        "unemployed_assets": "Vermögen",
        "unemployed_guarantor": "Bürge",

        # Zusatz
        "assets": "Vermögen",
        "asset_types": "Vermögensarten",
        "is_ready_collateral": "Bereit für besichertes Darlehen",
        "extra_income": "Zusätzliches Einkommen",
        "emergency_contact": "Notfall-Kontakt",
    },
}

# Button-Mapping
L10N_DE.update({
    BTN_SUPPORT: L10N_DE["btn_support"],
    BTN_ABOUT: L10N_DE["btn_about"],
    BTN_CHANGE_COUNTRY: L10N_DE["btn_change_country"],
    BTN_MY_APPS: L10N_DE["btn_my_apps"],
    BTN_APPLY: L10N_DE["btn_apply"],
    BTN_BACK: L10N_DE["btn_back"],
})

register("de", L10N_DE)

__all__ = ["L10N_DE"]
