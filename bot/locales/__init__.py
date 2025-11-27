from __future__ import annotations

from .core import translate, register
from .common import WELCOME_BILINGUAL, START_BTN

# Action ids (must match main.py)
BTN_SUPPORT        = "support"
BTN_ABOUT          = "about"
BTN_CHANGE_COUNTRY = "change_country"
BTN_MY_APPS        = "my_apps"
BTN_APPLY          = "apply"
BTN_BACK           = "back"

# import languages (registration side-effects)
from . import en  # noqa: F401
from . import ru  # noqa: F401
from . import de  # noqa: F401
from . import fr  # noqa: F401
from . import el  # noqa: F401
from . import ar  # noqa: F401
from . import hi  # noqa: F401

__all__ = [
    "translate", "register",

    "WELCOME_BILINGUAL", "START_BTN",

    "BTN_SUPPORT", "BTN_ABOUT", "BTN_CHANGE_COUNTRY", "BTN_MY_APPS", "BTN_APPLY", "BTN_BACK",

    "en", "ru", "de", "fr", "el", "ar", "hi"
]
