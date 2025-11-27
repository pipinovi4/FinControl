"""
Application message router.

This module processes all user text/contact messages when the user
is inside the multi-step credit application wizard.

Responsibilities:
-----------------
1. Validate if the user is in APP_FLOW
2. Extract and normalize user input
3. Save the answer
4. Apply dynamic branching rules (employment + yes/no)
5. Maintain UI consistency:
     - delete previous prompts
     - delete service ticks
     - delete user message
     - update progress panel
6. Route to next step or finish the wizard

This router delegates:
- branching to application.branching
- finishing to application.finish
- prompt rendering to application.prompts
- normalization to application.saver
"""

from __future__ import annotations

from typing import Optional

from telegram import (
    Update,
    ReplyKeyboardRemove,
)
from telegram.ext import ContextTypes

# ----- Project imports -----
from constants import (
    APP_FLOW, APP_STEPS, APP_IDX, APP_ANS,
    LAST_PROMPT_MSG_ID, LAST_SERVICE_MSG_ID,
)
from locales import translate as t

# prompt engine
from .prompts import (
    get_prompt,
    send_step_prompt,
)

# answer normalization helpers
from .saver import (
    normalize_choice,
)

# branching engine
from .branching import apply_branching

# finalization
from .finish import finish_application

# UI helpers
from ui.progress_panel import upsert_progress_panel, wipe_all_progress_panels
from core.logger import log


# ====================================================================
# MAIN ROUTER
# ====================================================================
async def handle_application_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Main handler for user messages during the credit application wizard.
    """

    # -----------------------------------------------------------
    # 1) Wizard guard — ignore if not inside application flow
    # -----------------------------------------------------------
    if not context.user_data.get(APP_FLOW):
        return

    msg = update.message
    if not msg:
        return

    # Basic context
    country = context.user_data.get("country") or "US"
    lang = context.user_data.get("lang") or "en"

    steps = context.user_data.get(APP_STEPS, [])
    idx = context.user_data.get(APP_IDX, 0)
    answers = context.user_data.get(APP_ANS, {})

    if idx >= len(steps):
        return

    step_key = steps[idx]
    value: Optional[str] = None

    # -----------------------------------------------------------
    # 2) Phone contact case
    # -----------------------------------------------------------
    if step_key == "phone" and msg.contact:
        value = msg.contact.phone_number
        # Show small service checkmark
        svc = await msg.reply_text("✅")
        context.user_data[LAST_SERVICE_MSG_ID] = svc.message_id

    # -----------------------------------------------------------
    # 3) Manual input
    # -----------------------------------------------------------
    if value is None:
        text_input = (msg.text or "").strip()
        manual_button_text = t(lang, "ui.type_manually")

        # If user clicked "Type manually"
        if step_key == "phone" and text_input == manual_button_text:
            prompt = await msg.reply_text(
                get_prompt(lang, country, step_key),
                reply_markup=ReplyKeyboardRemove(),
            )
            context.user_data[LAST_PROMPT_MSG_ID] = prompt.message_id
            return

        value = text_input

    # -----------------------------------------------------------
    # 4) Normalize inputs (employment/marital remove emojis etc.)
    # -----------------------------------------------------------
    if step_key in {"employment_status", "marital_status"}:
        value = normalize_choice(value)

    # -----------------------------------------------------------
    # 5) Save answer
    # -----------------------------------------------------------
    answers[step_key] = value
    context.user_data[APP_ANS] = answers

    # -----------------------------------------------------------
    # 6) Cleanup previous UI artifacts
    # -----------------------------------------------------------
    await _cleanup_wizard_messages(msg, context)

    # -----------------------------------------------------------
    # 7) Apply dynamic branching logic
    # -----------------------------------------------------------
    steps = apply_branching(step_key, value, steps, idx)
    context.user_data[APP_STEPS] = steps

    # -----------------------------------------------------------
    # 8) Update progress panel
    # -----------------------------------------------------------
    await upsert_progress_panel(msg, context)

    # -----------------------------------------------------------
    # 9) Move to next step OR finish wizard
    # -----------------------------------------------------------
    idx += 1
    context.user_data[APP_IDX] = idx

    if idx >= len(steps):
        # Finished — run finalizer
        return await finish_application(msg, context, lang)

    # Send next step prompt
    sent = await send_step_prompt(msg, lang, country, steps[idx])
    if sent and hasattr(sent, "message_id"):
        context.user_data[LAST_PROMPT_MSG_ID] = sent.message_id


# ====================================================================
# Helper: cleanup prompt/service/user-message
# ====================================================================
async def _cleanup_wizard_messages(msg, context: ContextTypes.DEFAULT_TYPE):
    """Delete previous prompt, ticks and user's own message to keep wizard UI clean."""

    # previous prompt
    last_prompt_id = context.user_data.pop(LAST_PROMPT_MSG_ID, None)
    if last_prompt_id:
        try:
            await msg.chat.delete_message(last_prompt_id)
        except Exception as e:
            log.debug(f"Failed to delete last prompt: {e}")

    # previous small checkmark
    last_svc_id = context.user_data.pop(LAST_SERVICE_MSG_ID, None)
    if last_svc_id:
        try:
            await msg.chat.delete_message(last_svc_id)
        except Exception as e:
            log.debug(f"Failed to delete service tick: {e}")

    # delete the user's own message
    try:
        await msg.delete()
    except Exception:
        pass


__all__ = ["handle_application_message"]
