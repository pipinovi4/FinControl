# handlers/application/prompts.py

from __future__ import annotations

from telegram import ReplyKeyboardRemove, ForceReply
from ui.keyboard_builder import build_keyboard
from locales import L10N
from telegram.ext import ContextTypes
from constants import LAST_PROMPT_MSG_ID


async def wipe_last_prompt(chat, context: ContextTypes.DEFAULT_TYPE):
    pid = context.user_data.pop(LAST_PROMPT_MSG_ID, None)
    if not pid:
        return

    try:
        await chat.delete_message(pid)
    except Exception:
        pass


def get_prompt(lang: str, country: str, step_key: str) -> str:
    locale = L10N.get(lang, {})
    steps = locale.get("steps", {})
    steps_by_country = locale.get("steps_by_country", {})

    cfg = steps_by_country.get(country, {}).get(step_key)
    if cfg and "prompt" in cfg:
        return cfg["prompt"]

    cfg = steps.get(step_key)
    if cfg and "prompt" in cfg:
        return cfg["prompt"]

    return f"[{step_key}]"


async def send_step_prompt(
    msg,
    context,
    lang: str,
    country: str,
    step_key: str,
    prefill: str | None = None,
):
    text = get_prompt(lang, country, step_key)

    # ---------------------------------------------------------
    # CASE 1 — Prefilled input (ForceReply hack)
    # ---------------------------------------------------------
    if prefill:
        composed = (
            f"{text}\n\n"
            f"✏️ <b>Редактируйте предыдущее значение:</b>\n"
            f"<code>{prefill}</code>"
        )

        sent = await msg.chat.send_message(
            text=composed,
            parse_mode="HTML",
            reply_markup=ForceReply(input_field_placeholder=prefill)
        )

        context.user_data[LAST_PROMPT_MSG_ID] = sent.message_id
        return sent

    # ---------------------------------------------------------
    # CASE 2 — Normal prompt with keyboard
    # ---------------------------------------------------------
    kb = build_keyboard(lang, country, step_key)

    try:
        sent = await msg.chat.send_message(
            text=text,
            reply_markup=kb,
            parse_mode="HTML",
        )
    except Exception:
        sent = await msg.chat.send_message(
            text=text,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="HTML",
        )

    context.user_data[LAST_PROMPT_MSG_ID] = sent.message_id
    return sent


__all__ = ["send_step_prompt", "get_prompt", "wipe_last_prompt"]
