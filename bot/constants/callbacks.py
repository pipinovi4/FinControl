from __future__ import annotations

# ============================================================
# Centralized callback-data definitions used across the bot.
# Every callback sent by InlineKeyboard buttons must start
# with a stable prefix, so handlers can quickly route actions.
# ============================================================

# Region selection prefix (example: "region:CIS")
CB_REGION = "region:"             # region:<REGION_CODE>

# Country selection prefix (example: "country:DE")
CB_COUNTRY = "country:"           # country:<COUNTRY_CODE>

CB_COUNTRY_BACK = "country_back"

# Main menu routing (example: "menu:support", "menu:about")
CB_MENU = "menu:"                 # menu:<action>

CB_BACK = "nav:back"
CB_NEXT = "nav:next"
CB_CANCEL = "nav:cancel"

__all__ = [
    "CB_REGION", "CB_COUNTRY", "CB_MENU", "CB_BACK", "CB_NEXT", "CB_CANCEL", "CB_COUNTRY_BACK",
]