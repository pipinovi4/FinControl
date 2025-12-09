# ui/safe_io.py
from __future__ import annotations
from typing import Optional

from telegram import Message
from telegram.error import BadRequest, Forbidden, TelegramError

from core.logger import log


async def _try_delete_message(message: Message):
    """Safely delete a message (ignore all safe exceptions)."""
    try:
        await message.delete()
    except (BadRequest, Forbidden):
        pass
    except TelegramError as e:
        log.debug(f"[safe_delete] TelegramError while deleting: {e}")


# ---------------------------------------------------------------------
# SAFE EDIT (universal)
# ---------------------------------------------------------------------
async def safe_edit(q, text: str, reply_markup=None, parse_mode: Optional[str] = None):
    """
    Edit a text or caption safely. If edit fails → delete and send new.
    """
    m: Message = q.message

    is_media = any([
        m.photo, m.video, m.animation, m.document
    ])

    try:
        if is_media:
            await q.edit_message_caption(
                caption=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
        else:
            await q.edit_message_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
        return

    except (BadRequest, Forbidden, TelegramError) as e:
        log.debug(f"[safe_edit] Failed to edit → fallback: {e}")

    await _try_delete_message(m)

    await m.chat.send_message(
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode,
    )


# ---------------------------------------------------------------------
# Replace message with NEW — always delete + send
# ---------------------------------------------------------------------
async def replace_with_text(q, text: str, reply_markup=None, parse_mode=None):
    m: Message = q.message
    await _try_delete_message(m)

    await m.chat.send_message(
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode,
    )


# ---------------------------------------------------------------------
# Safe delete single callback message
# ---------------------------------------------------------------------
async def safe_delete(q):
    await _try_delete_message(q.message)


# ---------------------------------------------------------------------
# Reset UI – in new architecture:
# delete the pressed message + clear panel_ids
# ---------------------------------------------------------------------
async def reset_ui(q, context):
    chat = q.message.chat

    # delete the pressed callback message
    await _try_delete_message(q.message)

    # clean all panel messages (BasePanel mechanics)
    panel_ids = context.user_data.get("panel_ids", [])
    for mid in panel_ids:
        try:
            await chat.delete_message(mid)
        except Exception:
            pass

    context.user_data["panel_ids"] = []

__all__ = [
    "safe_delete",
    "safe_edit",
    "replace_with_text",
    "reset_ui",
]