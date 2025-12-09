from constants import CB_COUNTRY, CB_REGION, CB_MENU

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

__all__ = [
    "cb_region",
    "cb_country",
    "cb_menu",
]