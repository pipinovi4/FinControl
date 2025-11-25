from __future__ import annotations
import os
from dataclasses import dataclass

# === Base application settings ===
# This dataclass stores all core environment-driven configuration
# values required by the bot. It ensures strict typing and immutability.
@dataclass(frozen=True)
class Settings:
    bot_token: str
    support_username: str
    app_name: str


def load_settings() -> Settings:
    """
    Loads all required environment variables for the bot.
    Raises an explicit error if a critical variable is missing.
    This function is executed once during application bootstrap.
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    support_username = os.getenv("SUPPORT_USERNAME", "WorldFlowSupport")
    app_name = os.getenv("APPLICATION_NAME", "WorldFlow Credit")

    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set. Put it in environment or .env")

    if not support_username:
        raise RuntimeError("SUPPORT_USERNAME is not set. Put it in environment or .env")

    return Settings(
        bot_token=token,
        support_username=support_username,
        app_name=app_name,
    )

# === High-level region definitions (UI section 1) ===
# These 4 global groups represent the main regional categories shown
# on the first onboarding step of the bot.
REGIONS = {
    "CIS": {"title": "🌏 СНГ / CIS", "code": "CIS"},
    "EU":  {"title": "🇪🇺 Европа / Europe", "code": "EU"},
    "NA":  {"title": "🌎 Северная Америка / North America", "code": "NA"},
    "AS":  {"title": "🌍 Азия / Asia", "code": "AS"},
}

# === List of countries inside each region (UI step 2) ===
# Each item contains:
# - flag: Display emoji for UI
# - title: Localized name of the country (for UI)
# - code: Internal country identifier
# - lang: Language code used to load translations for that country
COUNTRIES_BY_REGION = {
    "CIS": [
        {"flag": "🇷🇺", "title": "Россия",      "code": "RU", "lang": "ru"},
        {"flag": "🇧🇾", "title": "Беларусь",    "code": "BY", "lang": "be"},
        {"flag": "🇰🇿", "title": "Қазақстан",   "code": "KZ", "lang": "kk"},
    ],
    "EU": [
        {"flag": "🇩🇪", "title": "Deutschland", "code": "DE", "lang": "de"},
        {"flag": "🇫🇷", "title": "France",      "code": "FR", "lang": "fr"},
        {"flag": "🇬🇷", "title": "Ελλάδα",      "code": "GR", "lang": "el"},
        {"flag": "🇬🇧", "title": "United Kingdom","code": "GB","lang": "en"},
    ],
    "NA": [
        {"flag": "🇺🇸", "title": "United States","code": "US", "lang": "en"},
        {"flag": "🇨🇦", "title": "Canada",       "code": "CA", "lang": "en"},
    ],
    "AS": [
        {"flag": "🇮🇳", "title": "भारत (India)", "code": "IN", "lang": "hi"},
        {"flag": "🇦🇪", "title": "الإمارات (UAE)","code":"AE","lang":"ar"},
    ],
}

# === Mapping helpers for quick access ===
# LANG_BY_COUNTRY[country_code] → language code used for translations
LANG_BY_COUNTRY = {
    c["code"]: c["lang"]
    for region in COUNTRIES_BY_REGION.values()
    for c in region
}

# COUNTRY_TITLE[country_code] → "🇫🇷 France"
# Used in UI messages like "You selected France 🇫🇷"
COUNTRY_TITLE = {
    c["code"]: f'{c["flag"]} {c["title"]}'
    for region in COUNTRIES_BY_REGION.values()
    for c in region
}

# Export only what should be visible outside this module
__all__ = [
    "load_settings",
    "LANG_BY_COUNTRY", "COUNTRY_TITLE",
    "REGIONS", "COUNTRIES_BY_REGION"
]
