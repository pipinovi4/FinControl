# ============================================================
# Step Order Configuration for the Application Wizard
#
# This module defines:
#   • The base sequence of input fields (steps).
#   • Feature toggles controlling optional steps.
#   • Country-specific rules (e.g., RU-specific INN).
#   • Employment-status branching logic.
#   • Dynamic Yes/No sub-steps (income, assets, etc.).
#
# The build_step_order() function is the single source of truth
# for assembling the final step sequence per user country.
#
# This system allows:
#   • Per-country customization.
#   • Per-language step prompts (via /locales).
#   • Dynamic branching inside the wizard depending on answers.
# ============================================================


# ------------------------------------------------------------
# Base step sequence.
#
# Important:
#   • Some steps are injected conditionally via FEATURES[]
#   • RU/BY/KZ add "access_code" at the beginning
#   • RU adds "inn_ru" after id_number
#   • Branch-specific steps (employment paths) are added later
#
# This is the minimal skeleton before conditional injection.
# ------------------------------------------------------------
BASE_STEP_ORDER = [
    # access_code — added dynamically for RU/BY/KZ
    "full_name",
    "phone",
    "email",
    # "telegram" is inserted later if ASK_TELEGRAM = True
    "loan_amount",
    "id_number",  # national ID (SSN/SIN/NIN/Steuer-ID/Emirates ID/PAN/etc.)
    # RU inserts "inn_ru" after this step
    "reg_address",
    "actual_address",
    "dob",
    "marital_status",
    # "employment_status" inserted later if ASK_EMPLOYMENT = True
    # Employment sub-steps inserted dynamically at runtime
]


# ------------------------------------------------------------
# Feature toggles controlling optional steps.
#
# Turning these off allows:
#   • Simpler onboarding for A/B tests
#   • Country-specific onboarding flows
#   • Bot "lite mode" for quick MVP deployments
# ------------------------------------------------------------
FEATURES = {
    # Adds the "telegram" field after email
    "ASK_TELEGRAM": True,

    # Adds the employment-status switcher after marital_status
    # and enables all branching logic
    "ASK_EMPLOYMENT": True,

    # Enables the final "credit_report" step for selected countries
    "ASK_CREDIT_REPORT": True,
}


# ------------------------------------------------------------
# Countries that require a "credit_report" step at the end.
# Typically these are jurisdictions with strong credit bureau systems.
# ------------------------------------------------------------
CREDIT_REPORT_COUNTRIES = {
    "RU", "BY", "KZ",  # CIS region
    "US", "CA",        # North America
    "GB", "DE", "FR", "GR",  # Europe
    "IN", "AE",        # Asia
}


# ------------------------------------------------------------
# Employment-status branching logic.
#
# Each key corresponds to a normalized employment status
# (localized variants resolved earlier in the pipeline).
#
# The values define a list of additional steps inserted
# immediately after the "employment_status" step.
#
# Each of these step keys must exist in locales under:
#   labels.<key>
#   steps.<key>
#   or steps_by_country.<CC>.<key>
# ------------------------------------------------------------
STATUS_BRANCH_STEPS = {
    "Employed": [
        "employer_name",
        "employer_reg_address",
        "employer_actual_address",
        "job_title",
        "income_net_monthly",
        "income_proof",
        "employment_start_date",
        "employer_industry",
    ],

    "Business owner / Corporation": [
        "business_name",
        "business_reg_number",
        "business_reg_date",
        "business_turnover_monthly",
        "business_credit_lines",
        "business_tax_regime",
        "business_doc_upload",
    ],

    "Self-employed": [
        "activity_field",
        "income_net_monthly",
        "income_proof",
        "supporting_doc_upload",
    ],

    "Student": [
        "university_name",
        "study_dates",
        "study_mode",
        "income_present",      # Yes → inject income fields dynamically
        "guarantor_available", # Yes/No
    ],

    "Retired": [
        "pension_amount",
        "additional_income",   # Yes → add additional_income_details
        "assets_owned",        # Yes → add assets_details
        "guarantor_optional",
    ],

    "Unemployed": [
        "regular_income",      # Yes → add regular_income_details
        "assets_owned",        # Yes → add assets_details
        "guarantor_optional",
    ],
}


# ------------------------------------------------------------
# Text for the special RU/BY/KZ "access_code" step.
# Locales override is optional, so we define defaults here.
# ------------------------------------------------------------
ACCESS_CODE_PROMPTS = {
    "en": "🔐 Do you have a personal access code?\n\nEnter it below — optional. You can also type “No”.",
    "ru": "🔐 У вас есть персональный код доступа?\n\nВведите его ниже — необязательно. Можно написать «Нет».",
}


# ------------------------------------------------------------
# Main step-building function.
#
# Returns the final list of steps depending on:
#   • Base sequence
#   • Country-specific logic
#   • Enabled FEATURES[]
#
# This is called once after the user selects their country.
# ------------------------------------------------------------
def build_step_order(country_code: str) -> list[str]:
    steps = BASE_STEP_ORDER.copy()

    # Insert Telegram username field
    if FEATURES["ASK_TELEGRAM"]:
        steps.insert(steps.index("loan_amount"), "telegram")

    # Insert access_code for RU/BY/KZ
    if country_code in {"RU", "BY", "KZ"}:
        steps.insert(0, "access_code")

    # Insert RU-specific INN (tax ID)
    if country_code == "RU":
        i = steps.index("id_number") + 1
        steps.insert(i, "inn_ru")

    # Insert employment_status selector
    if FEATURES["ASK_EMPLOYMENT"]:
        j = steps.index("marital_status") + 1
        steps.insert(j, "employment_status")

    # Add credit_report at the end if required
    if FEATURES["ASK_CREDIT_REPORT"] and country_code in CREDIT_REPORT_COUNTRIES:
        steps.append("credit_report")

    return steps

__all__ = [
    "BASE_STEP_ORDER",
    "FEATURES",
    "CREDIT_REPORT_COUNTRIES",
    "STATUS_BRANCH_STEPS",
    "ACCESS_CODE_PROMPTS",
    "build_step_order"
]