"""
Branching engine for the multi-step application wizard.

This module contains all dynamic step-insertion logic:
----------------------------------------------------------------
1. Employment status:
      - inserts entire branch (Employed, Self-employed, Student...)
2. Conditional Yes/No steps:
      - income_present      → add income_net_monthly, income_proof
      - additional_income   → add additional_income_details
      - assets_owned        → add assets_details
      - regular_income      → add regular_income_details
----------------------------------------------------------------

Router delegates branching to this module to remain clean.
"""

from __future__ import annotations
from typing import List

from ...constants import STATUS_BRANCH_STEPS
from .saver import is_yes     # reuse normalized yes/no check


# ================================================================
# Main branching engine
# ================================================================
def apply_branching(step_key: str, value: str, steps: List[str], idx: int) -> List[str]:
    """
    Apply all branching rules based on the current step input.

    Returns:
        new list of steps (maybe unchanged)
    """

    # ------------------------------------------------------------
    # 1) Employment status → insert full branch
    # ------------------------------------------------------------
    if step_key == "employment_status":
        norm = normalize_employment(value)
        branch = STATUS_BRANCH_STEPS.get(norm)

        if branch:
            # insert branch right after the current step
            return steps[:idx + 1] + branch + steps[idx + 1:]

    # ------------------------------------------------------------
    # 2) Conditional Yes/No branches
    # ------------------------------------------------------------
    if step_key == "income_present" and is_yes(value):
        return steps[:idx + 1] + ["income_net_monthly", "income_proof"] + steps[idx + 1:]

    if step_key == "additional_income" and is_yes(value):
        return steps[:idx + 1] + ["additional_income_details"] + steps[idx + 1:]

    if step_key == "assets_owned" and is_yes(value):
        return steps[:idx + 1] + ["assets_details"] + steps[idx + 1:]

    if step_key == "regular_income" and is_yes(value):
        return steps[:idx + 1] + ["regular_income_details"] + steps[idx + 1:]

    return steps


# ================================================================
# Employment normalization table
# ================================================================
_EMPLOYMENT_MAP = {
    # EN
    "Employed": "Employed",
    "Business owner / Corporation": "Business owner / Corporation",
    "Self-employed": "Self-employed",
    "Student": "Student",
    "Retired": "Retired",
    "Unemployed": "Unemployed",

    # DE
    "Angestellt": "Employed",
    "Unternehmer / GmbH": "Business owner / Corporation",
    "Selbstständig": "Self-employed",
    "Rentner": "Retired",
    "Arbeitslos": "Unemployed",

    # RU
    "Работаю по найму": "Employed",
    "ИП / ООО": "Business owner / Corporation",
    "Самозанятый": "Self-employed",
    "Студент": "Student",
    "Пенсионер": "Retired",
    "Безработный": "Unemployed",
}


def normalize_employment(raw: str) -> str:
    """Normalize employment values across languages and emoji/no-emoji versions."""
    cleaned = raw.strip()
    # strip emoji prefixes (also handled in saver._normalize_choice)
    if cleaned[:2] in ("👔", "📊", "💼", "🎓", "👵", "🚫"):
        cleaned = cleaned[2:].strip()

    return _EMPLOYMENT_MAP.get(cleaned, cleaned)


__all__ = ["apply_branching", "normalize_employment"]
