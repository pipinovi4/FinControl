from keyboards import kb_main_menu
from locales import translate as t
from ui.panel.review import ReviewPanel
from ui.panel import CleanerPanel
from handlers.application.prompt import wipe_all_prompts
from telegram.error import BadRequest, Forbidden


async def _finish_wizard(update, context):
    chat = update.message.chat

    # ===============================================================
    # 1) Видаляємо ВСІ прогресс-панелі
    # ===============================================================
    try:
        cleaner = CleanerPanel(context)
        await cleaner.wipe_all(chat)
    except Exception:
        pass

    # ===============================================================
    # 2) Видаляємо ВСІ промпти
    # ===============================================================
    try:
        await wipe_all_prompts(chat, context)
    except Exception:
        pass

    # ===============================================================
    # 3) Видаляємо ВСІ error bubbles перед фіналом
    # ===============================================================
    error_keys = [
        "edit_error_msg",
        "edit_file_msg",
        "progress_error_msg",
        "enum_error_msg",
        "last_error_msg",   # ← ДОДАТИ ЦЕ
    ]

    for key in error_keys:
        msg_obj = context.user_data.pop(key, None)
        if msg_obj:
            try:
                await msg_obj.delete()
            except (BadRequest, Forbidden):
                pass
            except Exception:
                pass


    # ===============================================================
    # 4) Скидаємо технічні ключі
    # ===============================================================
    for k in ["panel_id", "panel_ids", "panel_mode"]:
        context.user_data.pop(k, None)

    # ===============================================================
    # 5) Переходимо в REVIEW
    # ===============================================================
    context.user_data["panel_mode"] = "review"

    wizard = context.user_data.get("wizard")
    if not wizard:
        lang = context.user_data.get("lang", "en")
        return await chat.send_message(
            t(lang, "titles.menu_title"),
            reply_markup=kb_main_menu(lang),
            parse_mode="HTML"
        )

    # Починаємо з першого поля
    wizard.queue.index = 0

    # ===============================================================
    # 6) Рендеримо ReviewPanel
    # ===============================================================
    panel = ReviewPanel(context, wizard)
    await panel.upsert(update.message)

    return None
