# handlers/application/prompts.py

from __future__ import annotations

from telegram import ReplyKeyboardRemove, ForceReply
from telegram.ext import ContextTypes

from ui.keyboard_builder import build_keyboard
from locales import L10N
from constants import LAST_PROMPT_MSG_ID


# =====================================================================
#   UNIVERSAL CLEANER FOR ALL PROMPTS
# =====================================================================
async def wipe_last_prompt(chat, context: ContextTypes.DEFAULT_TYPE):
    pid = context.user_data.pop(LAST_PROMPT_MSG_ID, None)
    if pid:
        try:
            await chat.delete_message(pid)
        except Exception:
            pass


async def wipe_all_prompts(chat, context: ContextTypes.DEFAULT_TYPE):
    """
    Clears ALL prompt messages tracked in prompt_ids[].
    This fixes the "old prompts remain forever" bug.
    """
    ids = context.user_data.pop("prompt_ids", [])
    for mid in ids:
        try:
            await chat.delete_message(mid)
        except Exception:
            pass

    # also remove last_prompt_id for safety
    pid = context.user_data.pop(LAST_PROMPT_MSG_ID, None)
    if pid:
        try:
            await chat.delete_message(pid)
        except Exception:
            pass


# =====================================================================
#   PROMPT TEXT RESOLUTION
# =====================================================================
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


# =====================================================================
#   MAIN PROMPT SENDER
# =====================================================================
async def send_step_prompt(
    msg,
    context: ContextTypes.DEFAULT_TYPE,
    lang: str,
    country: str,
    step_key: str,
    prefill: str | None = None,
):
    text = get_prompt(lang, country, step_key)

    # ===========================================================
    #   PREFILL MODE — used only before REFILLING a field in EDIT
    # ===========================================================
    if prefill:
        composed = (
            f"{text}\n\n"
            f"✏️ <b>Редактируйте предыдущее значение:</b>\n"
            f"<code>{prefill}</code>"
        )

        sent = await msg.chat.send_message(
            text=composed,
            parse_mode="HTML",
            reply_markup=ForceReply(input_field_placeholder=prefill),
        )

        # track last + full register
        context.user_data[LAST_PROMPT_MSG_ID] = sent.message_id

        arr = context.user_data.setdefault("prompt_ids", [])
        arr.append(sent.message_id)

        return sent

    # ===========================================================
    #   NORMAL MODE
    # ===========================================================
    kb = build_keyboard(lang, country, step_key)

    try:
        sent = await msg.chat.send_message(
            text=text,
            parse_mode="HTML",
            reply_markup=kb,
        )
    except Exception:
        sent = await msg.chat.send_message(
            text=text,
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove(),
        )

    # track last + full register
    context.user_data[LAST_PROMPT_MSG_ID] = sent.message_id

    arr = context.user_data.setdefault("prompt_ids", [])
    arr.append(sent.message_id)

    return sent


__all__ = [
    "send_step_prompt",
    "get_prompt",
    "wipe_last_prompt",
    "wipe_all_prompts",
]
