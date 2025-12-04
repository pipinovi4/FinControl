# ui/safe_io.py

from __future__ import annotations
from typing import Optional

from telegram import Message
from telegram.error import BadRequest, Forbidden, TelegramError

from core.logger import log
from ui import wipe_all_progress_panels

async def _try_delete_message(message: Message):
    try:
        await message.delete()
    except (BadRequest, Forbidden):
        pass
    except TelegramError as e:
        log.debug(f"[safe_delete] TelegramError while deleting: {e}")


async def safe_edit(q, text: str, reply_markup=None, parse_mode: Optional[str] = None):
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


async def replace_with_text(q, text: str, reply_markup=None, parse_mode=None):
    m: Message = q.message
    await _try_delete_message(m)

    await m.chat.send_message(
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode,
    )


async def safe_delete(q):
    await _try_delete_message(q.message)


async def reset_ui(q, context):
    chat = q.message.chat

    await _try_delete_message(q.message)

    try:
        await wipe_all_progress_panels(chat, context)
    except Exception as e:
        log.debug(f"[reset_ui] Cannot wipe panels: {e}")

    # cleanup_about тут більше НЕ викликаємо
    # це буде робити menu.py (UI logic)
