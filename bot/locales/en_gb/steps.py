STEPS = {
    # Basic fields
    "full_name": (
        "✍️ Please enter your full name exactly as it appears in your passport/ID.\n\n"
        "ℹ️ Provide your answers directly in the messages to ensure the form is completed correctly."
    ),

    "phone": "📞 Enter your mobile number in international format (e.g., +44XXXXXXXXXX).",
    "email": "📧 Please enter your email address.",
    "loan_amount": (
        "💰 Please enter the desired loan amount.\n"
        "Choose one of the options below or enter it manually.\n\n"
        "Buttons:\n"
        "💳 Maximum possible\n"
        "🤔 Not sure yet\n"
        "⏭ Skip this step"
    ),
    "id_number": "🆔 Enter your national ID number.",
    "reg_address": "🏠 Enter your registered address.",
    "actual_address": (
        "🏠 Enter your current residential address.\n"
        "If it matches the registered one, type “Same”."
    ),
    "dob": "📅 Enter your date of birth (DD/MM/YYYY).",
    "marital_status": (
        "💬 Please select your marital status.\n\n"
        "• Single\n• Married\n• Divorced\n• Widowed"
    ),
    "workplace": "🏢 Enter the full name of your organization.",

    # Employment root
    "employment_status": (
        "🏢 Select your status:\n\n"
        "👔 Employed\n"
        "📊 Business owner / Corporation\n"
        "💼 Self-employed\n"
        "🎓 Student\n"
        "👵 Retired\n"
        "🚫 Unemployed"
    ),

    # EMPLOYED
    "employer_name": "🏢 Enter your employer’s full name.",
    "employer_reg_address": "🏢 Enter the official registered address of your employer.",
    "employer_actual_address": "📍 Provide the actual workplace address.",
    "job_title": "🧾 Your job title:",
    "net_income": "💵 Enter your monthly income (after taxes).",
    "proof_of_income": (
        "📑 Select your proof of income:\n"
        "— Payslip\n— Bank statement\n— Employer certificate\n— Other"
    ),
    "employment_start_date": "📅 Enter the date you started this job.",
    "industry": "🏭 Your employer’s industry:",

    # BUSINESS
    "business_name": "🏢 Enter your business name.",
    "registration_number": "🆔 Enter your business registration number.",
    "registration_date": "📅 Enter the business registration date.",
    "turnover": "💵 Monthly business turnover:",
    "credit_lines": "💳 Active credit lines? → Yes / No",
    "tax_regime": "📑 Your tax regime:",
    "doc_upload": "📂 Upload a supporting document.",

    # SELF-EMPLOYED
    "activity_field": "📊 Your field of activity:",
    # net_income reused
    # proof_of_income reused
    # doc_upload reused

    # STUDENT
    "institution": "🎓 Educational institution:",
    "dates": "📅 Enrollment date and expected graduation date:",
    "study_type": "📚 Study type: Full-time / Part-time / Online",
    "has_income": "💵 Do you have income? Yes / No",
    "guarantor": "👥 Do you have a guarantor? Yes / No",

    # RETIRED
    "pension": "👵 Monthly pension amount:",
    "additional_income": "💵 Any additional income?",
    "assets": "🏡 Do you own any assets?",
    # guarantor reused

    # UNEMPLOYED
    "regular_income": "💵 Any regular source of income?",
    # assets reused
    # guarantor reused

    # ADDITIONAL
    "extra_income": "💵 Do you have additional income?",
    "emergency_contact": "👥 Emergency contact (optional).",

    # CREDIT REPORTS
    "credit_report_us": "📎 Upload your US credit report.",
    "credit_report_ca": "📎 Upload your Canadian credit report.",

    "final_note": "✅ Thank you! An expert will contact you shortly.",
}

__all__ = ["STEPS"]
