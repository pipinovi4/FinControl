"""
Application step ordering & dynamic wizard rules.

This module defines:
---------------------
1. BASE_STEP_ORDER
   - the minimal skeleton of steps
   - additional steps (access_code, inn_ru, employment flows, etc.)
     are added dynamically in build_step_order()

2. ACCESS_CODE_PROMPTS
   - special localized text for the access code step
   - avoids duplication in locale files

3. MARITAL_OPTIONS
   - mapping of marital status options per language
   - used for validation / building keyboards

4. build_step_order(country_code)
   - returns the full list of steps, dynamically expanded
     depending on the user’s country and enabled FEATURES
"""

from __future__ import annotations


# ============================================================
# Application Wizard – Core Keys
# ============================================================

# Main user_data keys used during the wizard:
APP_FLOW  = "app_flow"   # whether user is currently inside the application flow
APP_STEPS = "steps"      # full ordered list of step keys
APP_IDX   = "idx"        # index of the current step
APP_ANS   = "answers"    # dictionary with collected answers


# ============================================================
# Base Step Order (Minimum Skeleton)
# ------------------------------------------------------------
# All steps that *may* appear in the flow go here.
# Some are inserted conditionally in build_step_order().
# ============================================================

BASE_STEP_ORDER = [
    "access_code",       # only for RU/BY/KZ countries (inserted first)
    "full_name",
    "phone",
    "telegram",          # inserted dynamically depending on FEATURES
    "email",
    "loan_amount",
    "id_number",         # country-specific meaning
    # RU → additional "inn_ru" inserted right after id_number
    "reg_address",
    "actual_address",
    "dob",
    "marital_status",
    "workplace",         # generic employment placeholder
]


# ============================================================
# Marital Status Options (per language)
# ============================================================

MARITAL_OPTIONS = {
    "en": ["Single", "Married", "Divorced", "Widowed"],
    "ru": ["Не женат / не замужем", "В браке", "В разводе", "Вдовец / вдова"],
}


# ============================================================
# Access Code Step – Prompt Texts
# ------------------------------------------------------------
# Not added to locale files to keep them clean.
# Language-specific multi-line prompts for this single step.
# ============================================================

ACCESS_CODE_PROMPTS = {
    "en": "🔐 Do you have a personal access code?\n\nEnter it below — optional. You can also type “No”.",
    "ru": "🔐 У вас есть персональный код доступа?\n\nВведите его ниже — необязательно. Можно написать «Нет».",
    "be": "🔐 У вас ёсць персанальны код доступу?\n\nУвядзіце яго ніжэй — неабавязкова.",
    "kk": "🔐 Жеке қолжетімділік кодыңыз бар ма?\n\nТөменде енгізіңіз — міндетті емес.",
    "hi": "🔐 क्या आपके पास व्यक्तिगत एक्सेस कोड है?\n\nनीचे दर्ज करें — वैकल्पिक.",
    "fr": "🔐 Avez-vous un code d’accès personnel ?\n\nSaisissez-le ci-dessous — facultatif.",
    "de": "🔐 Haben Sie einen persönlichen Zugangscode?\n\nUnten eingeben — optional.",
    "el": "🔐 Έχετε προσωπικό κωδικό πρόσβασης;\n\nΠληκτρολογήστε τον — προαιρετικό.",
    "ar": "🔐 هل لديك رمز وصول شخصي؟\n\nأدخله أدناه — اختياري.",
}


__all__ = [
    "APP_FLOW", "APP_STEPS", "APP_IDX", "APP_ANS",
    "BASE_STEP_ORDER",
    "MARITAL_OPTIONS",
    "ACCESS_CODE_PROMPTS",
]
