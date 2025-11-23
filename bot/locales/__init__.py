from __future__ import annotations

# Action ids (must match main.py)
BTN_SUPPORT        = "support"
BTN_ABOUT          = "about"
BTN_CHANGE_COUNTRY = "change_country"
BTN_MY_APPS        = "my_apps"
BTN_APPLY          = "apply"
BTN_BACK           = "back"

_L10N: dict[str, dict] = {}

def _register(lang: str, data: dict) -> None:
    # merge (allow partial updates)
    _L10N[lang] = {**_L10N.get(lang, {}), **data}

def _lang_map(lang: str) -> dict:
    return _L10N.get(lang, _L10N.get("en", {}))

def _get_dotted(m: dict, dotted: str):
    cur = m
    for p in dotted.split("."):
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            return None
    return cur if isinstance(cur, (str, int, float)) else None

def t(lang: str, key: str, **kwargs) -> str:
    m = _lang_map(lang)
    s = m.get(key)
    if s is None:
        s = _get_dotted(m, key)
        if s is None:
            s = _lang_map("en").get(key, key)
    try:
        return str(s).format(**kwargs)
    except Exception:
        return str(s)

# import languages (registration side-effects)
from . import en  # noqa: F401
from . import ru  # noqa: F401
from . import de  # noqa: F401
from . import fr  # noqa: F401
from . import el  # noqa: F401
from . import ar  # noqa: F401
from . import hi  # noqa: F401
from . import be  # noqa: F401
from . import kk  # noqa: F401
