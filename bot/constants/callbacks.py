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


# ------------------------------------------------------------
# Small helpers to generate consistent callback_data strings.
# These guarantee that callback formats remain stable and clean.
# ------------------------------------------------------------

def cb_region(code: str) -> str:
    """Build callback_data for region selection."""
    return f"{CB_REGION}{code}"

def cb_country(code: str) -> str:
    """Build callback_data for country selection."""
    return f"{CB_COUNTRY}{code}"

def cb_menu(action: str) -> str:
    """Build callback_data for menu actions."""
    return f"{CB_MENU}{action}"

__all__ = ["cb_region", "cb_country", "cb_menu"]