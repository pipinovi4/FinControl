"""
Application step ordering & dynamic wizard rules.

This module defines:
---------------------
1. BASE_STEP_ORDER
   - the minimal skeleton of steps
   - additional steps (access_code, inn_ru, employment flows, etc.)
     are added dynamically in build_step_order()

2. ACCESS_CODE_PROMPTS
   - special localized text for the access code step
   - avoids duplication in locale files

3. MARITAL_OPTIONS
   - mapping of marital status options per language
   - used for validation / building keyboards

4. build_step_order(country_code)
   - returns the full list of steps, dynamically expanded
     depending on the user’s country and enabled FEATURES
"""

from __future__ import annotations


# ============================================================
# Application Wizard – Core Keys
# ============================================================

# Main user_data keys used during the wizard:
APP_FLOW  = "app_flow"   # whether user is currently inside the application flow
APP_STEPS = "steps"      # full ordered list of step keys
APP_IDX   = "idx"        # index of the current step
APP_ANS   = "answers"    # dictionary with collected answers


__all__ = [
    "APP_FLOW", "APP_STEPS", "APP_IDX", "APP_ANS",
]