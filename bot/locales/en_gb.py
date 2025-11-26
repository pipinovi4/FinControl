from __future__ import annotations
from . import register, BTN_SUPPORT, BTN_ABOUT, BTN_CHANGE_COUNTRY, BTN_MY_APPS, BTN_APPLY, BTN_BACK

L10N_EN = {
    # Entry / country selection
    "prompt_choose_region": "🌍 Select the region for your application:",
    "prompt_choose_country": "🌍 Select your country of application.\n📄 The form will open in the correct language automatically.",
    "after_country_selected": "✅ Great, country selected.\nYou can now submit an application, learn more about the service, or adjust your settings.",
    "menu_title": "🧭 WorldFlow Credit — your financial navigator. Choose: apply, support, info, or your applications.",

    # Main menu buttons
    "btn_apply": "📝 Apply for a loan",
    "apply_text": "Let's begin. A personal access code is not required for your region.",
    "btn_support": "💬 Support",
    "btn_about": "ℹ️ About us",
    "btn_change_country": "🌍 Change country",
    "btn_my_apps": "📂 My applications",

    # Stubs / sections
    "my_applications_text": (
        "<b>📂 My applications</b>\n\n"
        "Your active applications will appear here: status, documents, comments, and direct chat with an adviser.\n"
    ),
    "my_apps_stub": "Your applications will appear here (soon).",

    "support_text": (
        "<b>💬 WorldFlow Credit Support</b>\n\n"
        "We’re here to make decisions faster:\n"
        "— resolve complex situations,\n"
        "— suggest optimal next steps,\n"
        "— connect you with the right specialist.\n\n"
        "📲 Your personal support channel: <b>@WorldFlowSupport</b>"
    ),

    "about_text": "WorldFlow Credit — international credit application service.",
    "back_to_region": (
        "<b>↩️ Change region and continue 🌐</b>\n\n"
        "💡 Select the country you are currently in — this way we’ll show you the most relevant products and forms."
    ),

    # Common nav buttons (for inline keyboards / links)
    "btn_back": "↩ Back",
    "btn_website": "Website",
    "btn_tg_channel": "Telegram channel",
    "btn_instagram": "Instagram",
    "btn_x": "X / Twitter",
    "btn_linkedin": "LinkedIn",
    "btn_youtube": "YouTube",

    # UI microcopy
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
        "return_to_menu": "🏠 Return to menu",
    },

    # Generic steps (common wording). No access_code here (only RU/BY/KZ per notes).
    "steps": {
        "full_name": (
            "✍️ Please enter your full name exactly as it appears in your passport/ID.\n\n"
            "ℹ️ Provide your answers directly in the messages to ensure the form is completed correctly."
        ),
        "phone": "📞 Enter your mobile number in international format (e.g., +1XXXXXXXXXX).",
        "email": "📧 Please enter your email address.",
        "telegram": "🤖 Please provide your Telegram account for contact.\n(format: @username)",
        "loan_amount": (
            "💰 Please enter the desired loan amount.\n"
            "Choose one of the options below or enter it manually.\n\n"
            "Buttons:\n"
            "💳 Maximum possible\n"
            "🤔 Not sure yet\n"
            "⏭ Skip this step"
        ),
        "id_number": "🆔 Enter your national ID number (country-specific).",
        "reg_address": "🏠 Enter your registered address (as in your ID).",
        "actual_address": "🏠 Enter your current residential address.\nIf it matches the registered one, type “Same”.",
        "dob": "📅 Enter your date of birth (MM/DD/YYYY).",
        "marital_status": (
            "💬 Please select your marital status.\n\n"
            "Buttons:\n"
            "• Single\n• Married\n• Divorced\n• Widowed"
        ),
        "workplace": "🏢 Enter the full name of your organization (place of work).",
    },

    # Per-country overrides (EN only for US and CA)
    "steps_by_country": {
        "US": {
            "phone": "📞 Please enter your mobile number in the format +1XXXXXXXXXX.",
            "id_number": "🆔 Step 6. Social Security Number (SSN)\nPlease provide your SSN (9 digits).",
            "dob": "📅 Please enter your date of birth in the format MM/DD/YYYY.",
            "actual_address": "🏠 Step 7. Residential address\nPlease provide your current residential address.",
        },
        "CA": {
            "phone": "📞 Please enter your mobile number in the format +1XXXXXXXXXX.",
            "id_number": "🆔 Step 6. Social Insurance Number (SIN)\nPlease provide your SIN (9 digits).",
            "dob": "📅 Please enter your date of birth in the format MM/DD/YYYY.",
            "actual_address": "🏠 Step 7. Residential address\nPlease provide your current residential address.",
        },
    },

    # Employment status chooser (US/CA/GB share English in notes; GB text lives in en_gb.py)
    "employment": {
        "status_prompt": (
            "🏢 Select your status:\n\n"
            "Buttons:\n"
            "👔 Employed\n"
            "📊 Business owner / Corporation\n"
            "💼 Self-employed\n"
            "🎓 Student\n"
            "👵 Retired\n"
            "🚫 Unemployed"
        ),

        # 👔 Employed flow
        "employee": {
            "employer_name": "🏢 Please enter the full name of your employer (company/organization).",
            "employer_reg_address": "🏢 Enter the official registered address of your employer.",
            "employer_actual_address": (
                "📍 Provide the actual workplace address.\nIf it matches the registered one, type “Same”."
            ),
            "job_title": "🧾 Please specify your job title.",
            "net_income": "💵 Enter your average monthly income (after taxes).",
            "proof_of_income": (
                "📑 Select an available proof of income option.\n\n"
                "Buttons:\n"
                "— Payslip\n— Bank statement\n— Employer certificate\n— Other"
            ),
            "employment_start_date": "📅 Please enter the date you started this job.",
            "industry": "🏭 Indicate the industry sector of your employer (e.g. IT, retail, construction, healthcare).",
        },

        # 📊 Business owner / Corporation flow
        "business_owner": {
            "business_name": "🏢 Please provide the full name of your business.",
            "registration_number": "🆔 Enter your official business registration number (e.g. EIN / Corporation Number).",
            "registration_date": "📅 Provide the date your business was registered.",
            "turnover": "💵 Enter your average monthly business turnover.",
            "credit_lines": "💳 Does your business have any active credit lines or bank limits? 👉 Yes / No",
            "tax_regime": "📑 Select your tax regime: Simplified / Corporate / Other.",
            "doc_upload": "📂 Upload a supporting document (bank statement or tax report, optional).",
        },

        # 💼 Self-employed flow
        "self_employed": {
            "activity_field": "📊 Please specify your field of activity (e.g. freelance, consulting, trade, services).",
            "net_income": "💵 Enter your average monthly income (after taxes).",
            "proof_of_income": (
                "📑 How can you provide proof of income?\n\n"
                "Buttons:\n"
                "— Bank statement\n"
                "— Client contracts\n"
                "— Tax return / IRS form\n"
                "— Other"
            ),
            "doc_upload": "📂 Upload a supporting document (if available).",
        },

        # 🎓 Student flow
        "student": {
            "institution": "🎓 Please provide the full name of your educational institution.",
            "dates": "📅 Enter your enrollment date and expected graduation date.",
            "study_type": "📚 Select your study type: Full-time / Part-time / Online.",
            "has_income": "💵 Do you currently have a source of income? 👉 Yes / No\n— If Yes → specify amount and provide proof.",
            "guarantor": "👥 Do you have a guarantor available? 👉 Yes / No",
        },

        # 👵 Retired flow
        "retired": {
            "pension": "👵 Please enter your monthly pension amount (after taxes).",
            "additional_income": "💵 Do you have any additional income? 👉 Yes / No\n— If Yes → specify source and amount.",
            "assets": "🏡 Do you own any assets (e.g. property, car)? 👉 Yes / No",
            "guarantor": (
                "👥 If needed, you may provide a guarantor:\n— Full name\n— Phone number\n— Relationship\n👉 If not, type “None”."
            ),
        },

        # 🚫 Unemployed flow
        "unemployed": {
            "regular_income": "💵 Do you have any regular source of income (e.g. rental, part-time work)? 👉 Yes / No\n— If Yes → specify source and amount.",
            "assets": "🏡 Do you own any assets (e.g. property, car)? 👉 Yes / No",
            "guarantor": (
                "👥 If needed, you may provide a guarantor:\n— Full name\n— Phone number\n— Relationship\n👉 If not, type “None”."
            ),
        },

        # 🔹 Additional block (for those who haven't answered above)
        "additional": {
            "assets": (
                "🏡 Do you own any assets?\n— Yes / No\n\n"
                "If Yes → specify the type (property, house, car, land, other).\n"
                "Optional: Are you open to a secured loan against the asset?"
            ),
            "extra_income": "💵 Do you have additional income? — Yes / No\nIf Yes → specify source and amount.",
            "emergency_contact": (
                "👥 Emergency contact (optional):\n— Full name, phone, relationship.\nYou may also choose “Skip”."
            ),
        },
    },

    # Credit reports upload (US / CA buttons per notes)
    "credit_reports": {
        "US": {
            "prompt": "📎 Please upload your credit report from any major bureau:",
            "buttons": [
                "Equifax (equifax.com)",
                "Experian (experian.com)",
                "TransUnion (transunion.com)"
            ],
            "ack_step": [
                "✅ File 1 received. Please attach more if needed.",
                "✅ All files received. Thank you!"
            ]
        },
        "CA": {
            "prompt": "📎 Please upload your credit report from:",
            "buttons": [
                "Equifax Canada (consumer.equifax.ca)",
                "TransUnion Canada (transunion.ca)"
            ],
            "ack_step": [
                "✅ File 1 received. Please attach more if needed.",
                "✅ All files received. Thank you!"
            ]
        },
    },

    # About (US/CA)
    "about_full": (
        "<b>🌍 WorldFlow Credit — a global fintech platform for lending.</b>\n\n"
        "We connect clients directly with banks, using digital solutions and the expertise of international brokers, analysts, "
        "and consultants. With us, the process becomes simple, transparent, and fast.\n\n"
        "💼 Our ecosystem brings together thousands of specialists and partners worldwide, working in the unified digital space "
        "of WorldFlow. We merge banking technology with financial consulting to ensure your applications are processed without barriers.\n\n"
        "<b>✅ We provide:</b>\n"
        "— 💳 online consumer, mortgage, and auto loans;\n"
        "— 💼 digital support for businesses (sole proprietors/companies), turnover growth, and deal support;\n"
        "— 📊 algorithms to prepare for credit scoring and boost approval chances;\n"
        "— 🤝 personal support at every stage — from application to disbursement.\n\n"
        "⚡ With WorldFlow Credit, you gain not just access to financial products, but a full digital banking tool, "
        "where every solution scales to your goals."
    ),

    # Labels for previews / summaries
    "labels": {
        "full_name": "Full name",
        "phone": "Phone",
        "email": "Email",
        "telegram": "Telegram",
        "loan_amount": "Loan amount",
        "id_number": "Identifier",
        "reg_address": "Registered address",
        "actual_address": "Current address",
        "dob": "Date of birth",
        "marital_status": "Marital status",
        "workplace": "Workplace",
        "employment_status": "Status",
        # Employee
        "employer_name": "Employer",
        "employer_reg_address": "Employer (registered address)",
        "employer_actual_address": "Employer (actual address)",
        "job_title": "Job title",
        "net_income": "Net monthly income",
        "proof_of_income": "Proof of income",
        "employment_start_date": "Employment start date",
        "industry": "Industry",
        # Business owner
        "business_name": "Business name",
        "registration_number": "Registration number",
        "registration_date": "Registration date",
        "turnover": "Monthly turnover",
        "credit_lines": "Credit lines",
        "tax_regime": "Tax regime",
        # Self-employed
        "activity_field": "Field of activity",
        # Student
        "institution": "Institution",
        "study_type": "Study type",
        "has_income": "Has income",
        "guarantor": "Guarantor",
        # Retired / Unemployed / Additional
        "additional_income": "Additional income",
        "assets": "Assets",
        "emergency_contact": "Emergency contact",
    },
}

# Map button constants
L10N_EN.update({
    BTN_SUPPORT: L10N_EN["btn_support"],
    BTN_ABOUT: L10N_EN["btn_about"],
    BTN_CHANGE_COUNTRY: L10N_EN["btn_change_country"],
    BTN_MY_APPS: L10N_EN["btn_my_apps"],
    BTN_APPLY: L10N_EN["btn_apply"],
    BTN_BACK: L10N_EN["btn_back"],
})

# Register locale
register("en", L10N_EN)

__all__ = ["L10N_EN"]
