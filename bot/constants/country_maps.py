# ============================================================
# Regions & Countries configuration
#
# This module defines:
#   1) The list of supported geographic regions.
#   2) The countries inside each region.
#   3) Language mappings for every country code.
#   4) Human-readable country titles with flags.
#
# These structures are used for:
#   • Region -> country selection in onboarding.
#   • Locale auto-selection for each user.
#   • Keyboard generation and language routing.
#
# All locale-specific text (step prompts, buttons, messages)
# is defined under /locales. These constants only define
# structural geography and language defaults.
# ============================================================


# -----------------------------
# High-level region definitions
# -----------------------------
REGIONS = {
    "CIS": {"title": "🌐 CIS / СНГ", "code": "CIS"},
    "EU":  {"title": "🇪🇺 Europe / Европа", "code": "EU"},
    "NA":  {"title": "🗽 North America / Северная Америка", "code": "NA"},
    "AS":  {"title": "🏯 Asia / Азия", "code": "AS"},
}


# -------------------------------------------------------------
# Countries available inside each region.
# Each entry defines:
#   • flag  – emoji flag (used in keyboards)
#   • title – country name in local language
#   • code  – standardized ISO-like country identifier
#   • lang  – default UI language for applicants
#
# These language codes correspond to /locales/<lang>.py files.
# -------------------------------------------------------------
COUNTRIES_BY_REGION = {
    "CIS": [
        {"flag": "🇷🇺", "title": "Россия",      "code": "RU", "lang": "ru"},
        {"flag": "🇧🇾", "title": "Беларусь",    "code": "BY", "lang": "ru"},
        {"flag": "🇰🇿", "title": "Қазақстан",   "code": "KZ", "lang": "ru"},
    ],
    "EU": [
        {"flag": "🇩🇪", "title": "Deutschland", "code": "DE", "lang": "de"},
        {"flag": "🇫🇷", "title": "France",      "code": "FR", "lang": "fr"},
        {"flag": "🇬🇷", "title": "Ελλάδα",      "code": "GR", "lang": "el"},
        {"flag": "🇬🇧", "title": "United Kingdom", "code": "GB", "lang": "en"},
    ],
    "NA": [
        {"flag": "🇺🇸", "title": "United States", "code": "US", "lang": "en"},
        {"flag": "🇨🇦", "title": "Canada",        "code": "CA", "lang": "en"},
    ],
    "AS": [
        {"flag": "🇮🇳", "title": "भारत (India)", "code": "IN", "lang": "hi"},
        {"flag": "🇦🇪", "title": "الإمارات (UAE)", "code": "AE", "lang": "ar"},
    ],
}


# -------------------------------------------------------------
# Automatically generated helper maps:
#
# LANG_BY_COUNTRY["DE"] -> "de"
# COUNTRY_TITLE["DE"]   -> "🇩🇪 Deutschland"
#
# These mappings make it easy to:
#   • detect UI language per user
#   • reuse a consistent country title everywhere
# -------------------------------------------------------------
LANG_BY_COUNTRY = {
    c["code"]: c["lang"]
    for region in COUNTRIES_BY_REGION.values()
    for c in region
}

COUNTRY_TITLE = {
    c["code"]: f'{c["flag"]} {c["title"]}'
    for region in COUNTRIES_BY_REGION.values()
    for c in region
}

__all__ = [
    "REGIONS",
    "COUNTRIES_BY_REGION",
    "LANG_BY_COUNTRY",
    "COUNTRY_TITLE",
]