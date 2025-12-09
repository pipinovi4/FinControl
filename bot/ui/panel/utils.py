# ui/panel/utils.py
from locales import L10N

def html_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def short(val: str, limit: int = 64) -> str:
    s = str(val).strip()
    return s if len(s) <= limit else s[: limit - 1] + "…"

def resolve_text(lang: str, key: str) -> str:
    loc = L10N.get(lang, {})
    for ns in ("ui", "titles", "buttons", "common", "progress_panel"):
        block = loc.get(ns, {})
        if key in block:
            return block[key]
    return key

def resolve_label(lang: str, country: str, key: str) -> str:
    loc = L10N.get(lang, {})
    sbc = loc.get("steps_by_country", {})
    cfg = sbc.get(country, {}).get(key)
    if cfg and "label" in cfg:
        return cfg["label"]

    steps = loc.get("steps", {})
    cfg = steps.get(key)
    if cfg and "label" in cfg:
        return cfg["label"]

    return key
