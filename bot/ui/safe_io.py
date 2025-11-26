# ui/safe_io.py
"""
Safe message editing utilities.

This module provides two key helpers used across the bot:
---------------------------------------------------------
- safe_edit()        — safely edits a message (handles media, text, fallbacks)
- replace_with_text() — deletes message and sends a clean text replacement

Both functions use narrowed Telegram exceptions:
    BadRequest     → message can't be edited/deleted (invalid or outdated)
    Forbidden      → insufficient permissions
    TelegramError  → other telegram-level errors (logged)
"""

from __future__ import annotations

from typing import Optional
from telegram.error import BadRequest, Forbidden, TelegramError
from telegram import Message

from ..core.logger import log


# =====================================================================
# Safe message editing (text OR caption)
# =====================================================================

async def safe_edit(q, text: str, reply_markup=None, parse_mode: Optional[str] = None):
    """
    Safely edit the message associated with this callback:

    Behavior:
    ---------
    - If message contains media → edits caption
    - Otherwise → edits text
    - If edit fails:
         → delete message (if possible)
         → send a fresh new one

    This prevents:
    - "message is not modified"
    - "message can't be edited"
    - "message to edit not found"
    """

    m: Message = q.message

    is_media = bool(
        getattr(m, "photo", None)
        or getattr(m, "video", None)
        or getattr(m, "document", None)
        or getattr(m, "animation", None)
    )

    try:
        if is_media:
            await q.edit_message_caption(
                caption=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
        else:
            await q.edit_message_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
        return

    except BadRequest as e:
        log.debug(f"[safe_edit] BadRequest: {e}. Falling back to delete+send.")

    except Forbidden as e:
        log.debug(f"[safe_edit] Forbidden: {e}. Falling back to delete+send.")

    except TelegramError as e:
        log.debug(f"[safe_edit] TelegramError: {e}. Falling back to delete+send.")

    # Fallback — delete message
    try:
        await m.delete()
    except (BadRequest, Forbidden):
        pass
    except TelegramError as e:
        log.debug(f"[safe_edit] TelegramError while deleting stale message: {e}")

    # Send new message
    await m.chat.send_message(
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )


# =====================================================================
# Hard replace: delete message → send a clean new one
# =====================================================================

async def replace_with_text(q, text: str, reply_markup=None, parse_mode=None):
    """
    Deletes the original message and sends a clean new text message.

    Used when:
    - media messages must be replaced with text
    - switching views (e.g., from About to Menu)
    - UI refreshes that must not preserve old messages
    """

    m: Message = q.message

    try:
        await m.delete()
    except (BadRequest, Forbidden):
        pass
    except TelegramError as e:
        log.debug(f"[replace_with_text] TelegramError on delete: {e}")

    await m.chat.send_message(
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )


__all__ = [
    "safe_edit",
    "replace_with_text",
]
