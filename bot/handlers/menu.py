# handlers/menu.py

from __future__ import annotations

import os
from telegram import Update, InputMediaPhoto
from telegram.ext import ContextTypes

from core.logger import log
from locales import translate as t, WELCOME_BILINGUAL
from handlers.application.prompt import send_step_prompt, wipe_last_prompt
from keyboards import kb_regions, kb_countries, kb_main_menu, kb_about
from ui import safe_edit, replace_with_text, upsert_progress_panel, wipe_all_progress_panels, safe_delete, reset_ui
from wizard.engine import WizardEngine
from config.master_steps import MASTER_STEPS

from constants import (
    CB_START, CB_REGION, CB_COUNTRY, CB_MENU,
    LANG_BY_COUNTRY, COUNTRY_TITLE,
    ABOUT_PHOTO_MSG_ID, ABOUT_TEXT_MSG_ID,
)

from locales import (
    BTN_APPLY, BTN_SUPPORT, BTN_ABOUT,
    BTN_CHANGE_COUNTRY, BTN_MY_APPS, BTN_BACK
)


# ============================================================
# Cleanup helper for ABOUT section
# ============================================================
async def cleanup_about(chat, context: ContextTypes.DEFAULT_TYPE):
    """
    Deletes stored ABOUT media/text if they were previously sent.
    """
    photo_id = context.user_data.pop(ABOUT_PHOTO_MSG_ID, None)
    text_id = context.user_data.pop(ABOUT_TEXT_MSG_ID, None)

    for msg_id in (photo_id, text_id):
        if not msg_id:
            continue
        try:
            await chat.delete_message(msg_id)
        except Exception:
            pass


# ============================================================
# MAIN INLINE CALLBACK ROUTER
# ============================================================
async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = update.callback_query
    await q.answer()

    data = q.data or ""
    lang = context.user_data.get("lang", "en")

    # ---------------------------------------------------------
    # REGION SELECTED
    # ---------------------------------------------------------
    if data.startswith(CB_REGION):
        region_code = data.split(":", 1)[1]

        # 1️⃣ Якщо країна ще не обрана — показуємо Welcome
        if "country" not in context.user_data:
            text = WELCOME_BILINGUAL
        else:
            # 2️⃣ Якщо країна вже була вибрана — показуємо локалізований текст
            lang = context.user_data.get("lang", "en")
            text = t(lang, "bodies.back_to_region")

        await safe_edit(
            q,
            text,
            reply_markup=kb_countries(region_code),
            parse_mode="HTML",
        )
        return

    # ---------------------------------------------------------
    # COUNTRY SELECTED
    # ---------------------------------------------------------
    if data.startswith(CB_COUNTRY):
        country_code = data.split(":", 1)[1]

        context.user_data["country"] = country_code
        lang = LANG_BY_COUNTRY.get(country_code, "en")
        context.user_data["lang"] = lang

        # NEW L10N STRUCTURE
        text = (
            t(lang, "bodies.after_country_selected", country=COUNTRY_TITLE.get(country_code, country_code))
            + "\n\n"
            + t(lang, "titles.menu_title")
        )

        await safe_edit(
            q,
            text,
            reply_markup=kb_main_menu(lang),
            parse_mode="HTML",
        )

        return

    # ---------------------------------------------------------
    # MENU ACTIONS
    # ---------------------------------------------------------
    if not data.startswith(CB_MENU):
        return

    action = data.split(":", 1)[1]

    # ---------------------------------------------------------------
    # APPLY — start wizard flow
    # ---------------------------------------------------------------
    if action == BTN_APPLY:
        # Full UI reset (remove panels + prompt)
        await reset_ui(q, context)

        country = context.user_data.get("country", "US")
        lang = context.user_data.get("lang", "en")

        engine = WizardEngine(country=country, lang=lang, base_steps=MASTER_STEPS, debug=True)
        context.user_data["wizard"] = engine

        await upsert_progress_panel(q.message, context)

        # first step
        step = engine.current_step()

        await send_step_prompt(q.message, context, lang, country, step.key)

        return

    # ---------------------------------------------------------------
    # SUPPORT
    # ---------------------------------------------------------------
    if action == BTN_SUPPORT:
        await cleanup_about(q.message.chat, context)

        support_username = os.getenv("TELEGRAM_BOT_SUPPORT_USERNAME", "WorldFlowSupport")

        await safe_edit(
            q,
            t(lang, "bodies.support_text", support_username=support_username),
            reply_markup=kb_main_menu(lang),
            parse_mode="HTML"
        )
        return

    # ---------------------------------------------------------------
    # ABOUT
    # ---------------------------------------------------------------
    if action == BTN_ABOUT:
        await cleanup_about(q.message.chat, context)

        file_id = os.getenv("ABOUT_FILE_ID")

        caption = t(lang, "bodies.about_full")

        if file_id:
            try:
                msg = await q.edit_message_media(
                    InputMediaPhoto(
                        media=file_id,
                        caption=caption,
                        parse_mode="HTML",
                    ),
                    reply_markup=kb_about(lang),
                )
                context.user_data[ABOUT_PHOTO_MSG_ID] = msg.message_id
                return
            except Exception as e:
                log.warning(f"[ABOUT] Failed to replace media: {e}")

        msg = await safe_edit(
            q,
            caption,
            reply_markup=kb_about(lang),
            parse_mode="HTML",
        )

        context.user_data[ABOUT_TEXT_MSG_ID] = q.message.message_id
        return

    # ---------------------------------------------------------------
    # CHANGE COUNTRY
    # ---------------------------------------------------------------
    if action == BTN_CHANGE_COUNTRY:
        await cleanup_about(q.message.chat, context)

        # Локалізований текст!
        await safe_edit(
            q,
            t(lang, "bodies.back_to_region"),
            reply_markup=kb_regions(),
            parse_mode="HTML"
        )
        return

    # ---------------------------------------------------------------
    # MY APPLICATIONS (placeholder)
    # ---------------------------------------------------------------
    if action == BTN_MY_APPS:
        await safe_edit(
            q,
            t(lang, "bodies.my_apps_stub") + "\n\n" + t(lang, "titles.menu_title"),
            reply_markup=kb_main_menu(lang),
            parse_mode="HTML"
        )
        return

    # ---------------------------------------------------------------
    # BACK
    # ---------------------------------------------------------------
    if action == BTN_BACK:
        await replace_with_text(
            q,
            t(lang, "titles.menu_title"),
            reply_markup=kb_main_menu(lang),
            parse_mode="HTML"
        )
        return


__all__ = ["on_callback", "cleanup_about"]
