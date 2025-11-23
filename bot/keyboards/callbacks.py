from __future__ import annotations

# Single place for callback data
CB_START = "start_flow"
CB_REGION = "region:"            # region:<REGION_CODE>
CB_COUNTRY = "country:"          # country:<COUNTRY_CODE>
CB_MENU = "menu:"                # menu:<action>

def cb_region(code: str) -> str:
    return f"{CB_REGION}{code}"

def cb_country(code: str) -> str:
    return f"{CB_COUNTRY}{code}"

def cb_menu(action: str) -> str:
    return f"{CB_MENU}{action}"
