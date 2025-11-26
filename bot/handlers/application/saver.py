"""
Application input normalisation helpers.

This module provides small, targeted utilities used by the wizard:
-----------------------------------------------------------------
- _normalize_choice() → cleans emoji-prefixed options (employment, marital)
- _is_yes()           → robust multilingual "Yes" detector

These functions keep input handling consistent across all steps.
"""

from __future__ import annotations

# ============================================================
# Normalization Helpers
# ============================================================

def normalize_choice(text: str) -> str:
    """
    Normalize user choices that may start with emoji/visual prefixes.

    Example:
        "👔 Employed" → "Employed"
        "📊 Business owner / Corporation" → "Business owner / Corporation"

    Why it's needed:
    ----------------
    The keyboards for employment_status or marital_status sometimes
    contain emoji icons for visual styling. User replies back the
    entire button text — this function strips the visual prefix.
    """
    s = (text or "").strip()
    if not s:
        return s

    # Emoji prefixes used in our UI buttons
    emoji_prefixes = ("👔", "📊", "💼", "🎓", "👵", "🚫")

    if s[:2] in emoji_prefixes:
        return s[2:].strip()

    return s


def is_yes(text: str) -> bool:
    """
    Detects whether the user's reply means "Yes" across multiple languages.

    Supports:
    ---------
    English:   yes
    Russian:   да
    French:    oui
    German:    ja
    Spanish:   sí
    Arabic:    نعم
    Japanese:  はい / はい。
    Turkish:   evet
    Hindi:     हाँ

    *Comparison is case-insensitive and trims whitespace.*
    """
    if not text:
        return False

    s = text.strip().lower()

    yes_set = {
        "yes", "да", "oui", "ja", "sí",
        "نعم", "はい", "はい。", "evet",
        "हाँ",
    }

    return s in yes_set


# ============================================================
# Public API
# ============================================================
__all__ = [
    "normalize_choice",
    "is_yes",
]
