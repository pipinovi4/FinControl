from __future__ import annotations
from locales import register, BTN_SUPPORT, BTN_ABOUT, BTN_CHANGE_COUNTRY, BTN_MY_APPS, BTN_APPLY, BTN_BACK

L10N_EN = {
    # ==== Menu, navigation, common ====
    "prompt_choose_region": "🌍 Select the region for your application:",
    "prompt_choose_country": "🌍 Select your country:",
    "after_country_selected": (
        "✅ Great, country selected.\n"
        "You can now submit an application, learn more about the service, or adjust your settings."
    ),
    "menu_title": "🧭 WorldFlow Credit — your financial navigator. Choose: apply, support, info, or your applications.",
    "btn_apply": "📝 Apply for a loan",
    "apply_text": "Let's begin. A personal access code can be entered at the first step.",
    "btn_support": "🛟 Support",
    "btn_about": "ℹ️ About us",
    "btn_change_country": "🌐 Change country",
    "btn_my_apps": "🗂 My applications",

    "my_applications_text": (
        "<b>🗂 My applications</b>\n\n"
        "Here you'll find your active applications: status, documents, comments, and chat with an expert.\n"
        "Tap “📝 Apply for a loan” to start."
    ),

    "support_text": (
        "<b>💬 WorldFlow Credit Support</b>\n\n"
        "We’re here to make decisions faster:\n"
        "— resolve complex situations,\n"
        "— suggest optimal next steps,\n"
        "— connect you with the right specialist.\n\n"
        "📲 Your personal support channel: <b>@{support_username}</b>"
    ),

    "about_text": "WorldFlow Credit — international credit application service.",
    "my_apps_stub": "Your applications will appear here (soon).",
    "back_to_region": (
        "<b>↩️ Change region and continue 🌐</b>\n\n"
        "💡 Select the country you are currently in — this way we’ll show the most relevant products and forms."
    ),
    "btn_back": "↩ Back",
    "btn_website": "Website",
    "btn_tg_channel": "Telegram channel",
    "btn_instagram": "Instagram",
    "btn_x": "X / Twitter",
    "btn_linkedin": "LinkedIn",
    "btn_youtube": "YouTube",

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
    },

    # ==== Core steps (universal) ====
    "steps": {
        # 0. Access code (enabled in logic only for RU/BY/KZ; text kept for parity)
        "access_code": (
            "🔐 Do you have a personal access code?\n\n"
            "Enter it below — we’ll activate individual terms available by special invitation."
        ),

        # 1. Full name
        "full_name": (
            "✍️ Please enter your full name exactly as it appears in your passport/ID.\n\n"
            "ℹ️ Provide your answers directly in the messages to ensure the form is completed correctly."
        ),

        # 2. Phone
        "phone": "📞 Enter your mobile number in international format (e.g., +1XXXXXXXXXX).",

        # 3. Email
        "email": "📧 Enter your email address.",

        # 4. Telegram
        "telegram_username": "🤖 Please provide your Telegram account for contact (format: @username).",

        # 5. Loan amount
        "loan_amount": (
            "💰 Please enter the desired loan amount.\n"
            "Choose one of the options below or enter it manually."
        ),

        # 6. National identifier (country-specific)
        "id_number": "🆔 Enter your national ID number (country-specific).",

        # 7–8. Addresses
        "reg_address": "🏠 Enter your registered address (as in your ID).",
        "actual_address": "🏠 Enter your current residential address.\nIf the same as registered — type “Same”.",

        # 9. Date of birth
        "dob": "📅 Enter your date of birth (YYYY-MM-DD).",

        # 10. Marital status
        "marital_status": (
            "💬 Please select your marital status.\n"
            "Options:\n• Single\n• Married\n• Divorced\n• Widowed"
        ),

        # 11. Employment status (branching)
        "employment_status": (
            "🏢 Select your status:\n"
            "👔 Employed\n"
            "📊 Business owner / Corporation\n"
            "💼 Self-employed\n"
            "🎓 Student\n"
            "👵 Retired\n"
            "🚫 Unemployed"
        ),

        # ==== Branch: Employed ====
        "emp_company_name": "🏢 Enter the full name of your employer (company/organization).",
        "emp_company_reg_address": "📍 Enter the official registered address of your employer.",
        "emp_company_actual_address": "📍 Provide the actual workplace address.\nIf same as registered — type “Same”.",
        "emp_job_title": "💼 Please specify your job title.",
        "emp_monthly_income_net": "💵 Enter your average monthly income (after taxes).",
        "emp_income_proof": (
            "📑 Select an available proof of income option.\n"
            "Options: Payslip / Bank statement / Employer certificate / Other"
        ),
        "emp_job_start_date": "📅 Please enter the date you started this job.",
        "emp_industry": "🏭 Indicate your employer’s industry (e.g., IT, retail, construction, healthcare).",

        # ==== Branch: Business owner / Corporation ====
        "biz_name": "🏢 Please provide the full name of your business.",
        "biz_reg_number": "🆔 Enter your official business registration number (e.g., EIN / Corporation Number).",
        "biz_reg_date": "📅 Provide the date your business was registered.",
        "biz_monthly_turnover": "💵 Enter your average monthly business turnover.",
        "biz_has_credit_lines": "💳 Does your business have any active credit lines or bank limits? 👉 Yes / No",
        "biz_tax_regime": "📑 Select your tax regime: Simplified / Corporate / Other.",
        "biz_upload_doc": "📂 Upload a supporting document (bank statement or tax report, optional).",

        # ==== Branch: Self-employed ====
        "self_activity_field": "📊 Please specify your field of activity (e.g., freelance, consulting, trade, services).",
        "self_monthly_income_net": "💵 Enter your average monthly income (after taxes).",
        "self_income_proof": (
            "📑 How can you provide proof of income?\n"
            "Options: Bank statement / Client contracts / Tax return / IRS form / Other"
        ),
        "self_upload_doc": "📂 Upload a supporting document (if available).",

        # ==== Branch: Student ====
        "stud_school_name": "🎓 Please provide the full name of your educational institution.",
        "stud_dates": "📅 Enter your enrolment date and expected graduation date.",
        "stud_study_type": "📚 Select your study type: Full-time / Part-time / Online.",
        "stud_has_income": "💵 Do you currently have a source of income? 👉 Yes / No\n— If Yes → specify amount and provide proof.",
        "stud_has_guarantor": "👥 Do you have a guarantor available? 👉 Yes / No",

        # ==== Branch: Retired ====
        "ret_pension_amount": "👵 Please enter your monthly pension amount (after taxes).",
        "ret_additional_income": "💵 Do you have any additional income? 👉 Yes / No\n— If Yes → specify source and amount.",
        "ret_assets_owned": "🏡 Do you own any assets (e.g., property, car)? 👉 Yes / No",
        "ret_guarantor_optional": (
            "👥 If needed, you may provide a guarantor:\n— Full name\n— Phone number\n— Relationship\n👉 If not, type “None”."
        ),

        # ==== Branch: Unemployed ====
        "unemp_regular_income": "💵 Do you have any regular source of income (e.g., rental, part-time work)? 👉 Yes / No\n— If Yes → specify source and amount.",
        "unemp_assets_owned": "🏡 Do you own any assets (e.g., property, car)? 👉 Yes / No",
        "unemp_guarantor_optional": (
            "👥 If needed, you may provide a guarantor:\n— Full name\n— Phone number\n— Relationship\n👉 If not, type “None”."
        ),

        # ==== Extra (universal, if not answered above) ====
        "extra_assets": "🏡 Do you have assets? 👉 Yes / No\n— If Yes → specify type (apartment, house, car, land, other).",
        "extra_assets_collateral": "🏦 Would you consider a collateral-backed loan (secured by your asset)? 👉 Yes / No",
        "extra_additional_income": "💵 Do you have any additional income? 👉 Yes / No\n— If Yes → specify source and amount.",
        "extra_emergency_contact": "☎️ Emergency contact: full name, phone, relationship (optional; you may skip).",

        # ==== Credit reports (US/CA only) ====
        "credit_report_us": (
            "📎 Please upload your credit report from any major bureau:\n"
            "— Equifax\n— Experian\n— TransUnion"
        ),
        "credit_report_ca": (
            "📎 Please upload your credit report from:\n"
            "— Equifax Canada\n— TransUnion Canada"
        ),

        # ==== Final ====
        "final_note": "✅ Thank you! Your data has been received. An expert will contact you shortly in chat.",
    },

    # ==== Country-specific overrides (North America only) ====
    "steps_by_country": {
        "US": {
            "phone": "📞 Enter your mobile number in the format +1XXXXXXXXXX.",
            "id_number": "🆔 Please provide your SSN (9 digits).",
            "dob": "📅 Enter your date of birth in the format MM/DD/YYYY.",
            "actual_address": "🏠 Enter your current residential address.",
        },
        "CA": {
            "phone": "📞 Enter your mobile number in the format +1XXXXXXXXXX.",
            "id_number": "🆔 Please provide your SIN (9 digits).",
            "dob": "📅 Enter your date of birth in the format MM/DD/YYYY.",
            "actual_address": "🏠 Enter your current residential address.",
        },
    },

    # ==== Labels (for preview/progress panel) ====
    "labels": {
        "access_code": "Access code",
        "full_name": "Full name",
        "phone": "Phone",
        "email": "Email",
        "telegram_username": "Telegram",
        "loan_amount": "Loan amount",
        "id_number": "Identifier",
        "reg_address": "Registered address",
        "actual_address": "Current address",
        "dob": "Date of birth",
        "marital_status": "Marital status",
        "employment_status": "Employment status",

        # Employed
        "emp_company_name": "Employer",
        "emp_company_reg_address": "Employer’s registered address",
        "emp_company_actual_address": "Workplace address",
        "emp_job_title": "Job title",
        "emp_monthly_income_net": "Monthly income (net)",
        "emp_income_proof": "Income proof",
        "emp_job_start_date": "Job start date",
        "emp_industry": "Industry",

        # Business owner / Corporation
        "biz_name": "Business name",
        "biz_reg_number": "Registration number",
        "biz_reg_date": "Business registration date",
        "biz_monthly_turnover": "Turnover/month",
        "biz_has_credit_lines": "Active credit lines",
        "biz_tax_regime": "Tax regime",
        "biz_upload_doc": "Supporting document",

        # Self-employed
        "self_activity_field": "Field of activity",
        "self_monthly_income_net": "Monthly income (net)",
        "self_income_proof": "Income proof",
        "self_upload_doc": "Supporting document",

        # Student
        "stud_school_name": "Educational institution",
        "stud_dates": "Study dates",
        "stud_study_type": "Study type",
        "stud_has_income": "Has income",
        "stud_has_guarantor": "Guarantor",

        # Retired
        "ret_pension_amount": "Pension/month (net)",
        "ret_additional_income": "Additional income",
        "ret_assets_owned": "Assets",
        "ret_guarantor_optional": "Guarantor (optional)",

        # Unemployed
        "unemp_regular_income": "Regular income",
        "unemp_assets_owned": "Assets",
        "unemp_guarantor_optional": "Guarantor (optional)",

        # Extra
        "extra_assets": "Assets (extra)",
        "extra_assets_collateral": "Collateral readiness",
        "extra_additional_income": "Additional income (extra)",
        "extra_emergency_contact": "Emergency contact",

        # Credit reports
        "credit_report_us": "Credit report (US)",
        "credit_report_ca": "Credit report (CA)",

        # Final
        "final_note": "Final message",

        # Legacy
        "workplace": "Workplace",
    },

    # ==== Extended “About us” (EN) ====
    "about_full": (
        "<b>🌍 WorldFlow Credit — a global fintech platform for lending.</b>\n\n"
        "We connect clients directly with banks, using digital solutions and the expertise of international brokers, "
        "analysts, and consultants. With us, the process becomes simple, transparent, and fast.\n\n"
        "💼 Our ecosystem brings together thousands of specialists and partners worldwide, working in the unified digital "
        "space of WorldFlow. We merge banking technology with financial consulting to ensure your applications are processed without barriers.\n\n"
        "<b>✅ We provide:</b>\n"
        "— 💳 online consumer, mortgage, and auto loans;\n"
        "— 💼 digital support for businesses (sole proprietors/companies), turnover growth, and deal support;\n"
        "— 📊 algorithms to prepare for credit scoring and boost approval chances;\n"
        "— 🤝 personal support at every stage — from application to disbursement.\n\n"
        "⚡️ <b>With WorldFlow Credit, you gain not just access to financial products, but a full digital banking tool where every solution scales to your goals.</b>"
    ),
}

# Button aliases
L10N_EN.update({
    BTN_SUPPORT: L10N_EN["btn_support"],
    BTN_ABOUT: L10N_EN["btn_about"],
    BTN_CHANGE_COUNTRY: L10N_EN["btn_change_country"],
    BTN_MY_APPS: L10N_EN["btn_my_apps"],
    BTN_APPLY: L10N_EN["btn_apply"],
    BTN_BACK: L10N_EN["btn_back"],
})

register("en", L10N_EN)

__all__ = ["L10N_EN"]
