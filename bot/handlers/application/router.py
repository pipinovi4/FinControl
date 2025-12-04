from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes


from handlers.application import _finish_wizard
from handlers.application.prompt import send_step_prompt, wipe_last_prompt
from handlers.application.utils import resolve_canonical
from ui.progress_panel import upsert_progress_panel
from wizard.engine import WizardEngine
from locales import L10N


async def handle_application_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = update.message
    if not msg:
        return

    engine: WizardEngine = context.user_data.get("wizard")
    if not engine:
        return

    lang = engine.lang
    country = engine.country

    raw = msg.contact.phone_number if msg.contact else (msg.text or "").strip()
    step = engine.current_step()
    step_key = step.key

    locale = L10N.get(lang, {})
    steps = locale.get("steps", {})
    steps_by_country = locale.get("steps_by_country", {})

    # Pick correct config
    step_cfg = steps_by_country.get(country, {}).get(step_key, {}) or steps.get(step_key, {})

    value = resolve_canonical(step_cfg, raw)

    ok, status = engine.process_answer(
        key=step_key,
        raw_value=value["canonical"],
        display_value=value["display"]
    )

    # remove user's message
    try:
        await msg.delete()
    except:
        pass

    # ❌ INVALID INPUT — repeat same step
    if not ok:
        step = engine.current_step()

        # 💥 delete old prompt
        await wipe_last_prompt(msg.chat, context)

        await send_step_prompt(msg, context, lang, country, step.key)
        return

    # NEXT STEP
    success, step, _ = engine.next_step()

    # 💥 delete previous prompt before showing next
    await wipe_last_prompt(msg.chat, context)

    if engine.is_finished():
        await _finish_wizard(update, context, engine)
        return

    await upsert_progress_panel(msg, context)

    if step:
        await send_step_prompt(msg, context, lang, country, step.key)

__all__ = ["handle_application_message"]