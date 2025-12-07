from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest, Forbidden, TimedOut, RetryAfter, NetworkError

from handlers.application import _finish_wizard
from handlers.application.prompt import send_step_prompt, wipe_last_prompt
from handlers.application.utils import resolve_canonical
from ui.progress_panel import upsert_progress_panel
from wizard.engine import WizardEngine
from locales import L10N


async def handle_application_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    SAFE_EXCEPTIONS = (BadRequest, Forbidden, TimedOut, RetryAfter, NetworkError)

    msg = update.message
    if not msg:
        return

    engine: WizardEngine = context.user_data.get("wizard")
    if not engine:
        return

    lang = engine.lang
    country = engine.country

    # ---------------------------------------------------------
    # STEP META
    # ---------------------------------------------------------
    step = engine.current_step()
    if not step:
        return

    step_key = step.key

    locale = L10N.get(lang, {})
    steps = locale.get("steps", {})
    steps_by_country = locale.get("steps_by_country", {})

    # Pick correct config
    step_cfg = steps_by_country.get(country, {}).get(step_key, {}) or steps.get(step_key, {})

    # ---------------------------------------------------------
    # RAW INPUT (TEXT / CONTACT / FILE)
    # ---------------------------------------------------------

    # CASE 1 — CONTACT BUTTON (phone)
    if msg.contact and msg.contact.phone_number:
        raw = msg.contact.phone_number.strip()
        value = resolve_canonical(step_cfg, raw)
        raw_for_validation = value["canonical"]

    # CASE 2 — TEXT MESSAGE
    elif msg.text:
        raw = msg.text.strip()
        value = resolve_canonical(step_cfg, raw)
        raw_for_validation = value["canonical"]

    # CASE 3 — DOCUMENT (passport, PDF, etc.)
    elif msg.document:
        value = {
            "canonical": {
                "file_id": msg.document.file_id,
                "mime": msg.document.mime_type or "",
                "size": msg.document.file_size or 0,
                "name": msg.document.file_name or "Документ"
            },
            "display": msg.document.file_name or "Документ"
        }
        raw_for_validation = value["canonical"]

    # CASE 4 — PHOTO (Telegram always sends jpg)
    elif msg.photo:
        photo = msg.photo[-1]
        value = {
            "canonical": {
                "file_id": photo.file_id,
                "mime": "image/jpeg",
                "size": photo.file_size or 0,
                "name": "Фото"
            },
            "display": "Фото"
        }
        raw_for_validation = value["canonical"]

    # CASE 5 — fallback (nothing)
    else:
        raw = ""
        value = resolve_canonical(step_cfg, raw)
        raw_for_validation = value["canonical"]

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------
    valid, canonical, display = await engine.validate_input(step_key, raw_for_validation)

    if not valid:
        # delete user's message
        try:
            await msg.delete()
        except SAFE_EXCEPTIONS:
            pass

        # delete old error
        prev_err = context.user_data.get("last_error_msg")
        if prev_err:
            try:
                await prev_err.delete()
            except SAFE_EXCEPTIONS:
                pass

        # show new error
        err_msg = await msg.chat.send_message(display)
        context.user_data["last_error_msg"] = err_msg

        # repeat the same step
        await wipe_last_prompt(msg.chat, context)
        await send_step_prompt(msg, context, lang, country, step_key)
        return

    # VALID → delete previous error if exists
    prev_err = context.user_data.get("last_error_msg")
    if prev_err:
        try:
            await prev_err.delete()
        except SAFE_EXCEPTIONS:
            pass
        context.user_data["last_error_msg"] = None

    # Update canonical & display
    if canonical:
        value["canonical"] = canonical
    if display:
        value["display"] = display

    # ---------------------------------------------------------
    # SAVE ANSWER
    # ---------------------------------------------------------
    ok, status = engine.process_answer(
        key=step_key,
        raw_value=value["canonical"],
        display_value=value["display"],
    )

    # delete user's message
    try:
        await msg.delete()
    except SAFE_EXCEPTIONS:
        pass

    if not ok:
        await wipe_last_prompt(msg.chat, context)
        await send_step_prompt(msg, context, lang, country, step_key)
        return

    # ---------------------------------------------------------
    # NEXT STEP
    # ---------------------------------------------------------
    success, next_step, _ = engine.next_step()

    await wipe_last_prompt(msg.chat, context)

    if engine.is_finished():
        await _finish_wizard(update, context, engine)
        return

    await upsert_progress_panel(msg, context)

    if next_step:
        await send_step_prompt(msg, context, lang, country, next_step.key)


__all__ = ["handle_application_message"]
