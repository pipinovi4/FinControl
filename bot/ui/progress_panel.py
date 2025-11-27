# ui/progress_panel.py
"""
Fintech-style progress summary panel.

This module generates and maintains a dynamic "progress panel" — 
a multi-line HTML summary of:
    • completed steps
    • remaining steps
    • short preview of all answers

Used to give the user a clean real-time overview of the application wizard.

Functions provided:
-------------------
- progress_panel_html()      → builds the HTML panel
- upsert_progress_panel()    → creates or updates the panel in chat
- _wipe_all_progress_panels() → removes all panels from the chat

Internal helpers:
-----------------
- _html_escape()
- _short()
- _label()
- _track_panel_id()
- _cleanup_old_panels()
"""

from __future__ import annotations

from typing import List, Optional, Set
from telegram.ext import ContextTypes
from telegram import ReplyKeyboardRemove
from telegram.error import BadRequest, Forbidden, TelegramError

from locales import translate as t
from constants import (
    APP_STEPS, APP_ANS,
    PROGRESS_MSG_ID, PROGRESS_MSG_IDS,
)


# ============================================================
# Internal helpers
# ============================================================

def _html_escape(s: str) -> str:
    """Escape HTML-sensitive characters."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _short(val: str, limit: int = 64) -> str:
    """
    Truncate long values inside the panel.
    Example:
        "super long text ...." → "super long text…"
    """
    s = str(val).strip()
    return s if len(s) <= limit else s[: limit - 1] + "…"


def _label(lang: str, key: str) -> str:
    """
    Fetches a translated label for a given step key.
    Falls back to the raw key if no translation exists.
    """
    return t(lang, f"labels.{key}") or key


# ============================================================
# HTML panel generator
# ============================================================

def progress_panel_html(lang: str, steps: list[str], answers: dict) -> str:
    """
    Build the full HTML markup for the progress panel.

    Output structure:
        📊 Title
        ✓ Completed section
        ⏳ To-do section
    """
    title = t(lang, "ui.preview_title")
    done_h = t(lang, "ui.done")
    todo_h = t(lang, "ui.todo")

    done_lines, todo_lines = [], []

    for key in steps:
        label = _html_escape(_label(lang, key))
        raw_val = answers.get(key)

        # Determine if field is filled
        filled = (
            (isinstance(raw_val, str) and raw_val.strip() != "")
            or raw_val not in (None, "")
        )

        shown = "—" if not filled else _short(raw_val)
        shown = _html_escape(shown)

        line = f"• <b>{label}</b> — <code>{shown}</code>"

        if filled:
            done_lines.append(line)
        else:
            todo_lines.append(line)

    parts = [f"<b>📊 {title}</b>"]

    if done_lines:
        parts += [f"\n<b>{done_h}</b>", *done_lines]

    if todo_lines:
        parts += [f"\n<b>{todo_h}</b>", *todo_lines]

    return "\n".join(parts)


# ============================================================
# State helpers — tracking all panels
# ============================================================

def _track_panel_id(context: ContextTypes.DEFAULT_TYPE, mid: int) -> None:
    """
    Record a new panel message ID in user_data for cleanup management.
    """
    ids: List[int] = context.user_data.get(PROGRESS_MSG_IDS, [])
    if mid not in ids:
        ids.append(mid)
        context.user_data[PROGRESS_MSG_IDS] = ids


async def _cleanup_old_panels(msg, context: ContextTypes.DEFAULT_TYPE, keep: Set[int]) -> None:
    """
    Remove previous panels to avoid clutter:
    - keeps exactly the panel IDs passed in `keep`
    - deletes all others
    """
    ids: List[int] = context.user_data.get(PROGRESS_MSG_IDS, [])
    remain: List[int] = []

    for mid in ids:
        if mid in keep:
            remain.append(mid)
            continue

        try:
            await msg.chat.delete_message(mid)
        except (BadRequest, Forbidden):
            # message can't be deleted or already removed
            pass
        except TelegramError as e:
            # log other Telegram-level errors
            print(f"[progress_panel] TelegramError during cleanup: {e}")

    context.user_data[PROGRESS_MSG_IDS] = remain

# ============================================================
# Upsert main panel
# ============================================================

async def upsert_progress_panel(msg, context: ContextTypes.DEFAULT_TYPE):
    """
    Create or update the progress panel beneath the wizard.

    Behavior:
    ---------
    1. Try editing existing panel (faster, cleaner)
    2. If edit fails → delete old and send new panel
    3. Update internal tracking structures
    """
    lang = context.user_data.get("lang") or "en"
    steps: list[str] = context.user_data.get(APP_STEPS, [])
    answers: dict = context.user_data.get(APP_ANS, {})
    html = progress_panel_html(lang, steps, answers)

    pmid: Optional[int] = context.user_data.get(PROGRESS_MSG_ID)

    # Try updating
    if pmid:
        try:
            await msg.chat.edit_message_text(
                message_id=pmid,
                text=html,
                parse_mode="HTML"
            )
            _track_panel_id(context, pmid)
            await _cleanup_old_panels(msg, context, keep={pmid})
            return

        except (BadRequest, Forbidden):
            # message cannot be edited
            try:
                await msg.chat.delete_message(pmid)
            except (BadRequest, Forbidden):
                pass
            except TelegramError as e:
                print(f"[progress_panel] TelegramError on deleting stale panel: {e}")

        except TelegramError as e:
            print(f"[progress_panel] TelegramError on editing panel: {e}")

    # Send new panel
    sent = await msg.reply_text(
        html,
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove()
    )

    context.user_data[PROGRESS_MSG_ID] = sent.message_id
    _track_panel_id(context, sent.message_id)

    await _cleanup_old_panels(msg, context, keep={sent.message_id})


# ============================================================
# Full cleanup
# ============================================================

async def wipe_all_progress_panels(chat, context: ContextTypes.DEFAULT_TYPE):
    """
    Remove ALL progress panels from this chat.

    Used when:
    - user presses /start
    - restarting the application flow
    - switching country/region
    """
    ids: List[int] = context.user_data.get(PROGRESS_MSG_IDS, [])

    for mid in ids:
        try:
            await chat.delete_message(mid)
        except (BadRequest, Forbidden):
            pass
        except TelegramError as e:
            print(f"[progress_panel] TelegramError during wipe: {e}")

    context.user_data.pop(PROGRESS_MSG_IDS, None)
    context.user_data.pop(PROGRESS_MSG_ID, None)

__all__ = [
    "progress_panel_html",
    "upsert_progress_panel",
    "wipe_all_progress_panels",
]