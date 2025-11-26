from __future__ import annotations

# ============================================================
# Centralized callback-data definitions used across the bot.
# Every callback sent by InlineKeyboard buttons must start
# with a stable prefix, so handlers can quickly route actions.
# ============================================================

# Fired when user presses the "Start" button → begins onboarding flow.
CB_START = "start_flow"

# Region selection prefix (example: "region:CIS")
CB_REGION = "region:"             # region:<REGION_CODE>

# Country selection prefix (example: "country:DE")
CB_COUNTRY = "country:"           # country:<COUNTRY_CODE>

# Main menu routing (example: "menu:support", "menu:about")
CB_MENU = "menu:"                 # menu:<action>

__all__ = [
    "CB_START", "CB_REGION", "CB_COUNTRY", "CB_MENU"
]