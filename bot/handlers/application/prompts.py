"""
Application Wizard — Step Prompt Builder

This module contains:
---------------------
1. get_prompt(lang, country, step_key)
   - Returns the correct localized prompt text for a given step.
   - Uses country-specific overrides, base steps, and fallback logic.

2. send_step_prompt(...)
   - Sends a Telegram message for the current step.
   - Builds ReplyKeyboardMarkup dynamically per step type.
   - Supports:
        • phone (contact share)
        • marital_status (parsed options)
        • employment_status (parsed options)
        • loan_amount (auto-options when available)

3. _parse_options_block(text)
   - Extracts clean button options from multi-line localized blocks.
   - Removes icons, headers, long lines, and duplicates.

This file is the “brain” responsible for generating
the correct UI per wizard step.
"""

from __future__ import annotations

from typing import List

from telegram import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

# --- Project imports ---
from ...locales import translate as t
from ...constants.step_order import ACCESS_CODE_PROMPTS


# ============================================================================
# Option block parser
# ============================================================================

def _parse_options_block(block: str | None) -> List[str]:
    """
    Extract clean selectable options from a localized multi-line text block.

    Removes:
    - headers
    - decorative icons
    - long lines (labels, notes, etc.)
    - duplicates

    Returns:
        List[str] — unique, clean button labels.
    """
    if not block:
        return []

    res: List[str] = []

    for line in block.splitlines():
        raw = line.strip()
        if not raw:
            continue

        # Ignore headers (Labels, “Buttons”, “Options”, etc.)
        if any(marker in raw for marker in (
            "Кнопки", "Buttons", "Optionen", "Boutons",
            "Κουμπιά", "الأزرار", "Options", "Варианты",
            "Варыянты", "Таңдау", "Επιλογές", "الخيارات"
        )):
            continue

        # Skip long non-option lines (usually descriptions)
        if any(ch in raw for ch in (":", "—", "•", "⋅")) and len(raw) > 20:
            continue

        # Remove emoji prefixes
        if raw[:2] in ("👔", "📊", "💼", "🎓", "👵", "🚫", "💳", "🤔", "⏭"):
            raw = raw[2:].strip()

        # Filter garbage
        if 0 < len(raw) <= 48:
            res.append(raw)

    # Unique while preserving order
    uniq = []
    for x in res:
        if x not in uniq:
            uniq.append(x)

    return uniq


# ============================================================================
# Prompt selection
# ============================================================================

def get_prompt(lang: str, country: str, step_key: str) -> str:
    """
    Resolve the correct text for the step prompt in this order:

    Priority:
    ---------
    1) Country-specific override → steps_by_country.<CC>.<key>
    2) Base step text → steps.<key>
    3) Special cases:
          - access_code
          - inn_ru (RU only)
    4) Fallback → "[step_key]"
    """
    # Country-specific (highest priority)
    country_key = f"steps_by_country.{country}.{step_key}"
    s = t(lang, country_key)
    if s != country_key:
        return s

    # Base step
    base_key = f"steps.{step_key}"
    s = t(lang, base_key)
    if s != base_key:
        return s

    # Special-case: Access code
    if step_key == "access_code":
        return ACCESS_CODE_PROMPTS.get(lang, ACCESS_CODE_PROMPTS["en"])

    # Special-case: RU-only INN field
    if step_key == "inn_ru":
        return "🔢 Укажите ваш ИНН (10 или 12 цифр)."

    # Fallback
    return f"[{step_key}]"


# ============================================================================
# Prompt message sender
# ============================================================================

async def send_step_prompt(qmsg_or_upd, lang: str, country: str, step_key: str):
    """
    Sends the UI prompt for the given step.

    Automatically constructs:
      - reply keyboards (share phone, marital status, employment status, etc.)
      - fallback plain text for free input fields.

    Args:
        qmsg_or_upd:
            Telegram Update.message or callback.message
        lang:
            User language
        country:
            User country code (for localized fields)
        step_key:
            Wizard step identifier ("phone", "marital_status", etc.)
    """
    text = get_prompt(lang, country, step_key)
    reply_markup = None

    # -----------------------------------------------------
    # Phone number → ask for contact or manual input
    # -----------------------------------------------------
    if step_key == "phone":
        share = t(lang, "ui.share_phone")
        manual = t(lang, "ui.type_manually")

        reply_markup = ReplyKeyboardMarkup(
            [
                [KeyboardButton(share, request_contact=True)],
                [KeyboardButton(manual)],
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

    # -----------------------------------------------------
    # Marital status → auto-parse block
    # -----------------------------------------------------
    elif step_key == "marital_status":
        options = _parse_options_block(t(lang, "steps.marital_status"))
        if not options:
            options = ["Single", "Married", "Divorced", "Widowed"]

        reply_markup = ReplyKeyboardMarkup(
            [[KeyboardButton(opt)] for opt in options],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

    # -----------------------------------------------------
    # Employment status → parsed block with emoji support
    # -----------------------------------------------------
    elif step_key == "employment_status":
        options = _parse_options_block(t(lang, "steps.employment_status"))
        if not options:
            options = [
                "👔 Employed",
                "📊 Business owner / Corporation",
                "💼 Self-employed",
                "🎓 Student",
                "👵 Retired",
                "🚫 Unemployed",
            ]

        reply_markup = ReplyKeyboardMarkup(
            [[KeyboardButton(opt)] for opt in options],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

    # -----------------------------------------------------
    # Loan amount → parsed options if provided by locale
    # -----------------------------------------------------
    elif step_key == "loan_amount":
        options = _parse_options_block(t(lang, "steps.loan_amount"))
        if options:
            reply_markup = ReplyKeyboardMarkup(
                [[KeyboardButton(opt)] for opt in options],
                resize_keyboard=True,
                one_time_keyboard=True,
            )

    # -----------------------------------------------------
    # Credit report → free input (links auto-detected)
    # other fields → free text
    # -----------------------------------------------------

    # Accept both Update.message and Update.callback_query.message
    if hasattr(qmsg_or_upd, "reply_text"):
        return await qmsg_or_upd.reply_text(text, reply_markup=reply_markup)

    return await qmsg_or_upd.chat.send_message(text=text, reply_markup=reply_markup)


# ============================================================================
# Export public API
# ============================================================================

__all__ = [
    "send_step_prompt",
    "get_prompt",
    "_parse_options_block",
]
