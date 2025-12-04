from telegram import Update
from telegram.ext import ContextTypes

from handlers.application.prompt import send_step_prompt, wipe_last_prompt
from handlers.application.finish import _finish_wizard
from ui.progress_panel import upsert_progress_panel, wipe_all_progress_panels
from wizard.engine import WizardEngine
from constants.callbacks import CB_BACK, CB_NEXT, CB_CANCEL
from keyboards import kb_main_menu
from locales import translate as t


async def handle_progress_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    wizard: WizardEngine = context.user_data.get("wizard")
    if not wizard:
        return

    # ---------------------------------------------------------
    # BACK
    # ---------------------------------------------------------
    if query.data == CB_BACK:

        if wizard.queue.index == 0:
            return

        success, step, _ = wizard.prev_step()
        if not success:
            return

        prev_value = wizard.queue.answers.get(step.key, {}).get("display")

        await wipe_last_prompt(query.message.chat, context)

        await send_step_prompt(
            query.message,
            context,
            wizard.lang,
            wizard.country,
            step.key,
            prefill=prev_value  # <<<<< ВСЕ, БІЛЬШЕ НІЧОГО НЕ ТРЕБА
        )

        await upsert_progress_panel(query.message, context)
        return

    # ---------------------------------------------------------
    # NEXT
    # ---------------------------------------------------------
    if query.data == CB_NEXT:

        # Заборона переходу на NEXT без відповіді
        step = wizard.current_step()
        if step.key not in wizard.queue.answers:
            return

        success, step, _ = wizard.next_step()
        if not success:
            return

        if wizard.is_finished():
            await _finish_wizard(update, context, wizard)
            return

        await wipe_last_prompt(query.message.chat, context)
        await send_step_prompt(query.message, context, wizard.lang, wizard.country, step.key)

        await upsert_progress_panel(query.message, context)
        return

    # ---------------------------------------------------------
    # CANCEL
    # ---------------------------------------------------------
    if query.data == CB_CANCEL:
        chat = query.message.chat

        # 1️⃣ Видаляємо Progress панелі
        await wipe_all_progress_panels(chat, context)

        # 2️⃣ Видаляємо останній prompt
        last_prompt_id = context.user_data.pop("last_prompt_msg_id", None)
        if last_prompt_id:
            try:
                await chat.delete_message(last_prompt_id)
            except:
                pass

        # 3️⃣ Очищаємо wizard
        context.user_data.pop("wizard", None)

        # 4️⃣ Повертаємо ГОЛОВНЕ МЕНЮ (без фейкових callback-ів)
        lang = context.user_data.get("lang", "en")

        await chat.send_message(
            text=t(lang, "titles.menu_title"),
            reply_markup=kb_main_menu(lang),
            parse_mode="HTML"
        )

        return

__all__ = [
    "handle_progress_callback",
]