"""
constants/__init__.py
=====================

Centralized re-export hub for all bot-wide constants.

This module aggregates multiple constant groups from different files
(app_state, callbacks, country_maps, step_order) and exposes them via
a single import path:

    from constants import SOME_CONSTANT

Why this exists:
----------------
• Keeps imports clean across the entire project.
• Prevents long, messy multi-line imports in handlers.
• Makes refactoring easier — internal file structure can change without
  touching the consumer code.
• Ensures all constant-like definitions live in one logical namespace.

All exported symbols are explicitly listed in __all__, so nothing
leaks unintentionally and autocompletion remains clean.
"""

# Application flow state keys
from .app_state import (
    APP_FLOW, APP_STEPS, APP_IDX, APP_ANS,
    PROGRESS_MSG_ID, PROGRESS_MSG_IDS,
    LAST_SERVICE_MSG_ID, LAST_PROMPT_MSG_ID,
    ABOUT_PHOTO_MSG_ID, ABOUT_TEXT_MSG_ID,
)

# Callback helpers
from .callbacks import cb_region, cb_country, cb_menu

# Country/region mappings
from .country_maps import (
    REGIONS, COUNTRIES_BY_REGION,
    LANG_BY_COUNTRY, COUNTRY_TITLE,
)

# Step ordering & branching logic
from .step_order import (
    BASE_STEP_ORDER, FEATURES,
    CREDIT_REPORT_COUNTRIES, STATUS_BRANCH_STEPS,
    ACCESS_CODE_PROMPTS, build_step_order,
)

__all__ = [
    # application flow state
    "APP_FLOW", "APP_STEPS", "APP_IDX", "APP_ANS",
    "PROGRESS_MSG_ID", "PROGRESS_MSG_IDS",
    "LAST_SERVICE_MSG_ID", "LAST_PROMPT_MSG_ID",
    "ABOUT_PHOTO_MSG_ID", "ABOUT_TEXT_MSG_ID",

    # callback builders
    "cb_region", "cb_country", "cb_menu",

    # country/region maps
    "REGIONS", "COUNTRIES_BY_REGION",
    "LANG_BY_COUNTRY", "COUNTRY_TITLE",

    # step ordering system
    "BASE_STEP_ORDER", "FEATURES",
    "CREDIT_REPORT_COUNTRIES", "STATUS_BRANCH_STEPS",
    "ACCESS_CODE_PROMPTS", "build_step_order",
]
