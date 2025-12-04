STEPS = {

    # ----------------------
    # ACCESS CODE
    # ----------------------
    "access_code": {
        "label": "Κωδικός πρόσβασης",
        "prompt": (
            "🔐 Διαθέτετε προσωπικό κωδικό πρόσβασης;\n\n"
            "Πληκτρολογήστε τον — θα ενεργοποιήσουμε προνομιακές συνθήκες."
        ),
        "quick": None,
    },

    "access_code_checking": {
        "label": "Έλεγχος κωδικού",
        "prompt": "⏳ Έλεγχος κωδικού…",
        "quick": None,
    },

    "access_code_ok": {
        "label": "Κωδικός αποδεκτός",
        "prompt": "✅ Ο κωδικός έγινε δεκτός.",
        "quick": None,
    },

    "access_code_bad": {
        "label": "Μη έγκυρος κωδικός",
        "prompt": "❌ Ο κωδικός δεν αναγνωρίστηκε.",
        "quick": None,
    },

    "continue_without_code": {
        "label": "Συνέχεια χωρίς κωδικό",
        "prompt": "➡️ Συνέχεια χωρίς κωδικό",
        "quick": None,
    },

    # ----------------------
    # BASIC
    # ----------------------
    "full_name": {
        "label": "Πλήρες όνομα",
        "prompt": "✍️ Εισαγάγετε το πλήρες όνομά σας όπως στο διαβατήριο.",
        "quick": None,
    },

    "phone": {
        "label": "Τηλέφωνο",
        "prompt": (
            "📞 Εισαγάγετε αριθμό κινητού σε μορφή +30XXXXXXXXXX.\n"
            "Μπορείτε να μοιραστείτε αριθμό ή να τον εισαγάγετε χειροκίνητα."
        ),
        "quick": None,
    },

    "email": {
        "label": "Email",
        "prompt": "📧 Εισαγάγετε email.",
        "quick": None,
    },

    "loan_amount": {
        "label": "Ποσό δανείου",
        "prompt": "💰 Εισαγάγετε το επιθυμητό ποσό δανείου.",
        "quick": [
            {"key": "MAX",     "text": "💳 Μέγιστο δυνατό"},
            {"key": "NOT_SURE","text": "🤔 Δεν είμαι σίγουρος/η"},
            {"key": "SKIP",    "text": "⏭ Παράλειψη"},
        ],
    },

    "id_number": {
        "label": "ΑΦΜ",
        "prompt": "🆔 Εισαγάγετε ΑΦΜ (9 ψηφία).",
        "quick": None,
    },

    "reg_address": {
        "label": "Διεύθυνση κατοικίας",
        "prompt": "🏠 Εισαγάγετε διεύθυνση κατοικίας.",
        "quick": None,
    },

    "dob": {
        "label": "Ημερομηνία γέννησης",
        "prompt": "📅 Εισαγάγετε ημερομηνία σε μορφή ΗΗ/ΜΜ/ΕΕΕΕ.",
        "quick": None,
    },

    # ----------------------
    # MARITAL STATUS
    # ----------------------
    "marital_status": {
        "label": "Οικογενειακή κατάσταση",
        "prompt": "💬 Επιλέξτε οικογενειακή κατάσταση.",
        "quick": [
            {"key": "single",   "text": "Άγαμος / Άγαμη"},
            {"key": "married",  "text": "Παντρεμένος / Παντρεμένη"},
            {"key": "divorced", "text": "Διαζευγμένος / Διαζευγμένη"},
            {"key": "widowed",  "text": "Χήρος / Χήρα"},
        ],
    },

    # ----------------------
    # EMPLOYMENT
    # ----------------------
    "employment_status": {
        "label": "Κατάσταση απασχόλησης",
        "prompt": "🏢 Επιλέξτε κατάσταση απασχόλησης:",
        "quick": [
            {"key": "Employed", "text": "👔 Μισθωτός"},
            {"key": "Business owner / Corporation", "text": "📊 Επιχειρηματίας / Εταιρεία"},
            {"key": "Self-employed", "text": "💼 Ελεύθερος επαγγελματίας"},
            {"key": "Student", "text": "🎓 Φοιτητής/τρια"},
            {"key": "Retired", "text": "👵 Συνταξιούχος"},
            {"key": "Unemployed", "text": "🚫 Άνεργος"},
        ],
    },

    # ----------------------
    # EMPLOYED BRANCH
    # ----------------------
    "employer_name": {
        "label": "Εργοδότης",
        "prompt": "🏢 Όνομα εργοδότη.",
        "quick": None,
    },

    "employer_reg_address": {
        "label": "Εγγεγραμμένη διεύθυνση",
        "prompt": "📍 Εγγεγραμμένη διεύθυνση εργοδότη.",
        "quick": None,
    },

    "employer_actual_address": {
        "label": "Πραγματική διεύθυνση",
        "prompt": "📍 Πραγματική διεύθυνση εργασίας.",
        "quick": None,
    },

    "job_title": {
        "label": "Θέση εργασίας",
        "prompt": "💼 Θέση στην εταιρεία.",
        "quick": None,
    },

    "income_net_monthly": {
        "label": "Μηνιαίο εισόδημα",
        "prompt": "💵 Μηνιαίο καθαρό εισόδημα.",
        "quick": None,
    },

    "income_proof": {
        "label": "Απόδειξη εισοδήματος",
        "prompt": "📑 Επιλέξτε απόδειξη εισοδήματος.",
        "quick": [
            {"key": "PAYSLIP",   "text": "Μισθοδοσία"},
            {"key": "BANK",      "text": "Τραπεζικό αντίγραφο"},
            {"key": "EMPLOYER",  "text": "Βεβαίωση εργοδότη"},
            {"key": "OTHER",     "text": "Άλλο"},
        ],
    },

    "employment_start_date": {
        "label": "Έναρξη εργασίας",
        "prompt": "📅 Ημερομηνία έναρξης εργασίας.",
        "quick": None,
    },

    "employer_industry": {
        "label": "Κλάδος",
        "prompt": "🏭 Κλάδος εργοδότη.",
        "quick": None,
    },

    # ----------------------
    # BUSINESS
    # ----------------------
    "business_name": {
        "label": "Επιχείρηση",
        "prompt": "🏢 Όνομα επιχείρησης.",
        "quick": None,
    },
    "business_reg_number": {
        "label": "Αριθμός εγγραφής",
        "prompt": "🆔 Αριθμός εγγραφής.",
        "quick": None,
    },
    "business_reg_date": {
        "label": "Ημερομηνία ίδρυσης",
        "prompt": "📅 Ημερομηνία ίδρυσης.",
        "quick": None,
    },
    "business_turnover_monthly": {
        "label": "Κύκλος εργασιών",
        "prompt": "💵 Μέσος μηνιαίος κύκλος εργασιών.",
        "quick": None,
    },
    "business_credit_lines": {
        "label": "Πιστωτικές γραμμές",
        "prompt": "💳 Πιστωτικές γραμμές; Ναι/Όχι",
        "quick": [
            {"key": "Yes", "text": "Ναι"},
            {"key": "No",  "text": "Όχι"},
        ],
    },
    "business_tax_regime": {
        "label": "Φορολογικό καθεστώς",
        "prompt": "📑 Φορολογικό καθεστώς.",
        "quick": None,
    },
    "business_doc_upload": {
        "label": "Έγγραφα",
        "prompt": "📂 Ανέβασμα εγγράφου (προαιρετικό).",
        "quick": None,
    },

    # ----------------------
    # SELF-EMPLOYED
    # ----------------------
    "activity_field": {
        "label": "Τομέας",
        "prompt": "📊 Τομέας δραστηριότητας.",
        "quick": None,
    },

    "supporting_doc_upload": {
        "label": "Έγγραφο",
        "prompt": "📂 Έγγραφο (προαιρετικό).",
        "quick": None,
    },

    # ----------------------
    # STUDENT
    # ----------------------
    "university_name": {
        "label": "Ίδρυμα",
        "prompt": "🎓 Εκπαιδευτικό ίδρυμα.",
        "quick": None,
    },

    "study_dates": {
        "label": "Περίοδος σπουδών",
        "prompt": "📅 Έναρξη & αποφοίτηση.",
        "quick": None,
    },

    "study_mode": {
        "label": "Μορφή σπουδών",
        "prompt": "📚 Μορφή σπουδών.",
        "quick": None,
    },

    "income_present": {
        "label": "Εισόδημα",
        "prompt": "💵 Πηγή εισοδήματος; Ναι/Όχι",
        "quick": None,
    },

    "income_amount": {
        "label": "Ποσό εισοδήματος",
        "prompt": "💵 Ποσό & απόδειξη.",
        "quick": None,
    },

    "guarantor_available": {
        "label": "Εγγυητής",
        "prompt": "👥 Εγγυητής; Ναι/Όχι",
        "quick": None,
    },

    # ----------------------
    # RETIRED
    # ----------------------
    "pension_amount": {
        "label": "Σύνταξη",
        "prompt": "👵 Μηνιαία σύνταξη.",
        "quick": None,
    },

    "additional_income": {
        "label": "Έξτρα εισόδημα",
        "prompt": "💵 Έξτρα εισόδημα; Ναι/Όχι",
        "quick": None,
    },

    "assets_owned": {
        "label": "Περιουσία",
        "prompt": "🏡 Περιουσιακά στοιχεία;",
        "quick": None,
    },

    # ----------------------
    # CREDIT REPORT
    # ----------------------
    "credit_report_gr": {
        "label": "Πιστωτική αναφορά",
        "prompt": "📎 Ανέβασμα πιστωτικής αναφοράς.",
        "quick": None,
    },
}

__all__ = ["STEPS"]
