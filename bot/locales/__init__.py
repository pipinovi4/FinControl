from __future__ import annotations

# Core API
from .core import translate, register, _L10N
from .common import WELCOME_BILINGUAL, START_BTN

# Action identifiers (used in handlers and keyboards)
BTN_SUPPORT        = "support"
BTN_ABOUT          = "about"
BTN_CHANGE_COUNTRY = "change_country"
BTN_MY_APPS        = "my_apps"
BTN_APPLY          = "apply"
BTN_BACK           = "back"

# ---------------------------------------------------------
# Importing all locales (registration happens inside each)
# ---------------------------------------------------------

# Important: explicit imports to trigger `register(lang, data)`
from .en     import L10N_EN
from .ru     import L10N_RU
from .de     import L10N_DE
from .fr     import L10N_FR
from .el     import L10N_EL
from .ar     import L10N_AR
from .hi     import L10N_HI
from .en_gb  import L10N_EN_GB

# ---------------------------------------------------------
# Re-export
# ---------------------------------------------------------

__all__ = [
    # Core API
    "translate",
    "register",
    "_L10N",

    # Global UI snippets
    "WELCOME_BILINGUAL",
    "START_BTN",

    # Button IDs
    "BTN_SUPPORT",
    "BTN_ABOUT",
    "BTN_CHANGE_COUNTRY",
    "BTN_MY_APPS",
    "BTN_APPLY",
    "BTN_BACK",

    # Locales (exposed for debugging)
    "L10N_EN",
    "L10N_EN_GB",
    "L10N_RU",
    "L10N_DE",
    "L10N_FR",
    "L10N_EL",
    "L10N_AR",
    "L10N_HI",
]
