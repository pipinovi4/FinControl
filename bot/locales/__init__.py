from __future__ import annotations

# Core API
from .core import translate, register, L10N
from .common import WELCOME_BILINGUAL

# Action identifiers (used in handlers and keyboards)
BTN_SUPPORT        = "support"
BTN_ABOUT          = "about"
BTN_CHANGE_COUNTRY = "change_country"
BTN_MY_APPS        = "my_apps"
BTN_APPLY          = "apply"
BTN_BACK           = "back"

# ---------------------------------------------------------
# Re-export
# ---------------------------------------------------------

__all__ = [
    # Core API
    "translate",
    "register",
    "L10N",

    # Global UI snippets
    "WELCOME_BILINGUAL",

    # Button IDs
    "BTN_SUPPORT",
    "BTN_ABOUT",
    "BTN_CHANGE_COUNTRY",
    "BTN_MY_APPS",
    "BTN_APPLY",
    "BTN_BACK",
]
