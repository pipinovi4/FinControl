STEPS = {

    # ----------------------
    # ACCESS CODE
    # ----------------------
    "access_code": {
        "label": "Personal code",
        "prompt": (
            "🔐 Do you have a personal access code?\n\n"
            "Enter it below — we will activate your individual conditions."
        ),
        "quick": None,
    },

    # ----------------------
    # BASIC
    # ----------------------
    "full_name": {
        "label": "Full name",
        "prompt": "✍️ Enter your full name exactly as in your passport/ID.",
        "quick": None,
    },

    "phone": {
        "label": "Phone number",
        "prompt": "📞 Enter your phone number.",
        "quick": [
            {"key": "TELEGRAM_PHONE", "type": "contact", "text": "📱 Use Telegram number"},
        ],
    },

    "email": {
        "label": "Email",
        "prompt": "📧 Enter your email address.",
        "quick": None,
    },

    "telegram": {
        "label": "Telegram account",
        "prompt": "🤖 Enter your Telegram username in the format @username.",
        "quick": None,
    },

    "loan_amount": {
        "label": "Loan amount",
        "prompt": (
            "💰 Enter the desired loan amount.\n"
            "Choose an option below or type the amount manually."
        ),
        "quick": [
            {"key": "MAX",     "text": "💳 Maximum possible"},
            {"key": "UNKNOWN", "text": "🤔 Not sure yet"},
            {"key": "SKIP",    "text": "⏭ Skip step"},
        ],
    },

    "id_number": {
        "label": "Identification number",
        "prompt": "🆔 Enter your national identification number.",
        "quick": None,
    },

    "reg_address": {
        "label": "Registered address",
        "prompt": "🏠 Enter your registered address.",
        "quick": None,
    },

    "actual_address": {
        "label": "Actual address",
        "prompt": "🏠 Enter your actual address. If the same — type “Same”.",
        "quick": None,
    },

    "dob": {
        "label": "Date of birth",
        "prompt": "📅 Enter your date of birth (DD/MM/YYYY).",
        "quick": None,
    },

    # ----------------------
    # MARITAL STATUS
    # ----------------------
    "marital_status": {
        "label": "Marital status",
        "prompt": "💬 Select your marital status.",
        "quick": [
            {"key": "single",   "text": "Single"},
            {"key": "married",  "text": "Married"},
            {"key": "divorced", "text": "Divorced"},
            {"key": "widowed",  "text": "Widowed"},
        ],
    },

    # ----------------------
    # EMPLOYMENT STATUS
    # ----------------------
    "employment_status": {
        "label": "Employment status",
        "prompt": "🏢 Select your employment status.",
        "quick": [
            {"key": "Employed",                     "text": "Employed"},
            {"key": "Business owner / Corporation", "text": "Business owner / Corporation"},
            {"key": "Self-employed",                "text": "Self-employed"},
            {"key": "Student",                      "text": "Student"},
            {"key": "Retired",                      "text": "Retired"},
            {"key": "Unemployed",                   "text": "Unemployed"},
        ],
    },

    # ----------------------
    # EMPLOYED BRANCH
    # ----------------------
    "employer_name": {
        "label": "Employer",
        "prompt": "🏢 Enter the full name of your employer.",
        "quick": None,
    },
    "employer_reg_address": {
        "label": "Registered address",
        "prompt": "📍 Enter the legal registered address of the employer.",
        "quick": None,
    },
    "employer_actual_address": {
        "label": "Actual work address",
        "prompt": "📍 Enter the actual workplace address (or “Same”).",
        "quick": None,
    },
    "job_title": {
        "label": "Job title",
        "prompt": "💼 Enter your job title.",
        "quick": None,
    },
    "income_net_monthly": {
        "label": "Monthly income (net)",
        "prompt": "💵 Enter your net monthly income.",
        "quick": None,
    },
    "income_proof": {
        "label": "Income proof",
        "prompt": "📑 Select your income proof.",
        "quick": [
            {"key": "2NDFL",    "text": "Payslip"},
            {"key": "BANK",     "text": "Bank statement"},
            {"key": "EMPLOYER", "text": "Employer certificate"},
            {"key": "OTHER",    "text": "Other"},
        ],
    },
    "employment_start_date": {
        "label": "Employment start date",
        "prompt": "📅 Enter the date when you started this job.",
        "quick": None,
    },
    "employer_industry": {
        "label": "Industry",
        "prompt": "🏭 Enter the employer’s industry sector.",
        "quick": None,
    },

    # ----------------------
    # BUSINESS BRANCH
    # ----------------------
    "business_name": {
        "label": "Business name",
        "prompt": "🏢 Enter your business name.",
        "quick": None,
    },
    "business_reg_number": {
        "label": "Registration number",
        "prompt": "🆔 Enter your business registration number.",
        "quick": None,
    },
    "business_reg_date": {
        "label": "Registration date",
        "prompt": "📅 Enter the business registration date.",
        "quick": None,
    },
    "business_turnover_monthly": {
        "label": "Monthly turnover",
        "prompt": "💵 Enter your average monthly turnover.",
        "quick": None,
    },
    "business_credit_lines": {
        "label": "Credit lines",
        "prompt": "💳 Do you have active credit lines?",
        "quick": [
            {"key": "Yes", "text": "Yes"},
            {"key": "No",  "text": "No"},
        ],
    },
    "business_tax_regime": {
        "label": "Tax regime",
        "prompt": "📑 Select your tax regime.",
        "quick": [
            {"key": "Simplified", "text": "Simplified"},
            {"key": "General",    "text": "General"},
            {"key": "Other",      "text": "Other"},
        ],
    },
    "business_doc_upload": {
        "label": "Business documents",
        "prompt": "📂 Upload a supporting document if possible.",
        "quick": None,
    },

    # ----------------------
    # SELF-EMPLOYED
    # ----------------------
    "activity_field": {
        "label": "Activity field",
        "prompt": "📊 Enter your activity field.",
        "quick": None,
    },
    "supporting_doc_upload": {
        "label": "Supporting document",
        "prompt": "📂 Upload a supporting document (if available).",
        "quick": None,
    },

    # ----------------------
    # STUDENT BRANCH
    # ----------------------
    "university_name": {
        "label": "Educational institution",
        "prompt": "🎓 Enter the full name of your educational institution.",
        "quick": None,
    },
    "study_dates": {
        "label": "Study period",
        "prompt": "📅 Enter the start and end dates of your studies.",
        "quick": None,
    },
    "study_mode": {
        "label": "Study mode",
        "prompt": "📚 Select your mode of study.",
        "quick": [
            {"key": "Full-time", "text": "Full-time"},
            {"key": "Part-time", "text": "Part-time"},
            {"key": "Online",    "text": "Online"},
        ],
    },
    "income_present": {
        "label": "Income",
        "prompt": "💵 Do you have income?",
        "quick": [
            {"key": "Yes", "text": "Yes"},
            {"key": "No",  "text": "No"},
        ],
    },
    "income_amount": {
        "label": "Income amount",
        "prompt": "💵 Enter your income amount.",
        "quick": None,
    },
    "guarantor_available": {
        "label": "Guarantor",
        "prompt": "👥 Do you have a guarantor?",
        "quick": [
            {"key": "Yes", "text": "Yes"},
            {"key": "No",  "text": "No"},
        ],
    },
    "guarantor_fullname": {
        "label": "Guarantor full name",
        "prompt": "👤 Enter the guarantor’s full name.",
        "quick": None,
    },
    "guarantor_phone": {
        "label": "Guarantor phone",
        "prompt": "📞 Enter the guarantor’s phone number.",
        "quick": None,
    },
    "guarantor_relation": {
        "label": "Relation",
        "prompt": "👥 Enter your relationship to the guarantor.",
        "quick": None,
    },

    # ----------------------
    # RETIRED
    # ----------------------
    "pension_amount": {
        "label": "Pension",
        "prompt": "👵 Enter your monthly pension amount.",
        "quick": None,
    },
    "additional_income": {
        "label": "Additional income",
        "prompt": "💵 Do you have any additional income?",
        "quick": [
            {"key": "Yes", "text": "Yes"},
            {"key": "No",  "text": "No"},
        ],
    },
    "assets_owned": {
        "label": "Assets",
        "prompt": "🏡 Do you own any assets?",
        "quick": [
            {"key": "Yes", "text": "Yes"},
            {"key": "No",  "text": "No"},
        ],
    },
    "guarantor_optional": {
        "label": "Guarantor (optional)",
        "prompt": "👥 Enter guarantor details if necessary.",
        "quick": None,
    },

    # ----------------------
    # UNEMPLOYED
    # ----------------------
    "regular_income": {
        "label": "Regular income",
        "prompt": "💵 Do you have a regular income source?",
        "quick": [
            {"key": "Yes", "text": "Yes"},
            {"key": "No",  "text": "No"},
        ],
    },

    # ----------------------
    # CREDIT REPORTS
    # ----------------------
    "credit_report_ru": {
        "label": "Credit reports (RU)",
        "prompt": "📎 Upload your RU credit reports (3 files).",
        "quick": None,
    },
    "credit_report_by": {
        "label": "Credit report (BY)",
        "prompt": "📎 Upload your BY credit report.",
        "quick": None,
    },
    "credit_report_kz": {
        "label": "Credit report (KZ)",
        "prompt": "📎 Upload your KZ credit report.",
        "quick": None,
    },
}

__all__ = ["STEPS"]
