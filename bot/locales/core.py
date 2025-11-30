from __future__ import annotations

class L10NError(Exception):
    """Raised when translate() cannot resolve a key in any locale."""
    pass


L10N: dict[str, dict] = {}
_DEBUG = False


def enable_l10n_debug() -> None:
    global _DEBUG
    _DEBUG = True


def register(lang: str, data: dict) -> None:
    """Register or merge locale dictionary."""
    if _DEBUG:
        print(f"[L10N] Registering locale '{lang}' with {len(data)} keys")

    L10N[lang] = {**L10N.get(lang, {}), **data}


def _lang_map(lang: str) -> dict:
    """Return language map with fallback -> en."""
    if lang in L10N:
        return L10N[lang]
    return L10N.get("en", {})


def _get_dotted(m: dict, dotted: str):
    """Resolve dotted.key.paths inside nested dictionaries."""
    cur = m
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur if isinstance(cur, (str, int, float)) else None


def translate(lang: str, key: str, **kwargs) -> str:
    """
    Resolve locale key with fallback and format kwargs.
    Raises L10NError if nothing found.
    """
    m = _lang_map(lang)

    # direct key
    s = m.get(key)

    # dotted key (nested)
    if s is None:
        s = _get_dotted(m, key)

    # fallback → en
    if s is None:
        fallback_map = _lang_map("en")
        s = fallback_map.get(key) or _get_dotted(fallback_map, key)

    # completely missing → error or debug note
    if s is None:
        if _DEBUG:
            return f"[L10N-MISSING:{lang}:{key}]"
        raise L10NError(f"Missing translation key '{key}' for lang '{lang}'")

    # format
    try:
        return str(s).format(**kwargs)
    except Exception as ex:
        if _DEBUG:
            return f"[L10N-FORMAT-ERR:{lang}:{key}:{ex}]"
        raise

__all__ = [
    "translate",
    "register",
    "enable_l10n_debug",
    "L10N",
    "L10NError",
]
