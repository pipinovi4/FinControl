from telegram import ReplyKeyboardRemove
from ui.progress_panel import wipe_all_progress_panels
from keyboards import kb_main_menu
from locales import translate as t


async def _finish_wizard(update, context, engine):
    chat = update.message.chat

    # 1) Видаляємо всі панелі
    await wipe_all_progress_panels(chat, context)

    # 2) Видаляємо останній prompt
    last_prompt_id = context.user_data.pop("last_prompt_msg_id", None)
    if last_prompt_id:
        try:
            await chat.delete_message(last_prompt_id)
        except:
            pass

    # 3) Чистимо wizard
    context.user_data.pop("wizard", None)

    lang = context.user_data.get("lang", "en")

    # 4) Відправляємо “Мои заявки”
    text = (
        t(lang, "bodies.my_apps_stub") +
        "\n\n" +
        t(lang, "titles.menu_title")
    )

    await chat.send_message(
        text,
        parse_mode="HTML",
        reply_markup=kb_main_menu(lang)
    )
