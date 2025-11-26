from __future__ import annotations

import os
from telegram import (
    Update,
    InputMediaPhoto,
)
from telegram.ext import ContextTypes

# --- Project-wide imports ---
from ..constants import (
    CB_START, CB_REGION, CB_COUNTRY, CB_MENU,
    LANG_BY_COUNTRY, COUNTRY_TITLE,
    APP_FLOW, APP_STEPS, APP_IDX, APP_ANS,
    LAST_PROMPT_MSG_ID,
    ABOUT_PHOTO_MSG_ID, ABOUT_TEXT_MSG_ID,
    build_step_order,
)

from ..locales import (
    translate as t,
    WELCOME_BILINGUAL,
    BTN_APPLY, BTN_SUPPORT, BTN_ABOUT,
    BTN_CHANGE_COUNTRY, BTN_MY_APPS,
    BTN_BACK,
)

from ..keyboards import (
    kb_regions,
    kb_countries,
    kb_main_menu,
    kb_about,
)

from ..handlers.application.prompts import send_step_prompt
from ..ui import safe_edit, replace_with_text, upsert_progress_panel, wipe_all_progress_panels

from ..core.logger import log


# ============================================================
# Internal helper: remove previously sent "About Us" media/text
# ============================================================
async def _cleanup_about(chat, context: ContextTypes.DEFAULT_TYPE):
    """
    Deletes the previously sent About photo and About text message
    if they exist in user_data. Helps avoid media clutter when user
    reopens About multiple times.
    """
    photo_id = context.user_data.pop(ABOUT_PHOTO_MSG_ID, None)
    text_id = context.user_data.pop(ABOUT_TEXT_MSG_ID, None)

    for mid in (photo_id, text_id):
        if mid:
            try:
                await chat.delete_message(mid)
            except Exception:
                pass


# ============================================================
# Callback router: processes all inline keyboard actions
# ============================================================
async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Main callback handler for all inline keyboard actions.
    Routes user navigation across:
      - Start
      - Region selection
      - Country selection
      - Main menu actions
      - Application (wizard) start
      - Misc sections (About, Support, My Apps)
    """
    q = update.callback_query
    await q.answer()

    data = q.data or ""
    lang = context.user_data.get("lang") or "en"

    # ------------------------------
    # User pressed "Start"
    # ------------------------------
    if data == CB_START:
        # reset UI
        await wipe_all_progress_panels(q.message.chat, context)

        await safe_edit(
            q,
            WELCOME_BILINGUAL,
            reply_markup=kb_regions(),
            parse_mode="HTML"
        )
        return

    # ------------------------------
    # Region selected
    # ------------------------------
    if data.startswith(CB_REGION):
        region_code = data.split(":", 1)[1]
        await safe_edit(
            q,
            WELCOME_BILINGUAL,
            reply_markup=kb_countries(region_code),
            parse_mode="Markdown"
        )
        return

    # ------------------------------
    # Country selected
    # ------------------------------
    if data.startswith(CB_COUNTRY):
        country_code = data.split(":", 1)[1]

        context.user_data["country"] = country_code
        lang = LANG_BY_COUNTRY.get(country_code, "en")
        context.user_data["lang"] = lang

        text = t(lang, "after_country_selected",
                  country=COUNTRY_TITLE.get(country_code, country_code))
        text += "\n\n" + t(lang, "menu_title")

        await safe_edit(q, text, reply_markup=kb_main_menu(lang))
        return

    # ------------------------------
    # Menu actions
    # ------------------------------
    if data.startswith(CB_MENU):
        action = data.split(":", 1)[1]

        # --------------------------------------------------------
        # 1) APPLY → Starting the credit wizard
        # --------------------------------------------------------
        if action == BTN_APPLY:
            country = context.user_data.get("country") or "US"
            lang = context.user_data.get("lang") or "en"

            steps = build_step_order(country)

            # initialize wizard state
            context.user_data[APP_FLOW] = True
            context.user_data[APP_STEPS] = steps
            context.user_data[APP_IDX] = 0
            context.user_data[APP_ANS] = {}

            await safe_edit(q, t(lang, "apply_text"))

            # show progress panel
            await upsert_progress_panel(q.message, context)

            # send first step prompt
            sent_prompt = await send_step_prompt(q.message, lang, country, steps[0])

            if sent_prompt and hasattr(sent_prompt, "message_id"):
                context.user_data[LAST_PROMPT_MSG_ID] = sent_prompt.message_id

            return

        # --------------------------------------------------------
        # 2) SUPPORT
        # --------------------------------------------------------
        if action == BTN_SUPPORT:
            await _cleanup_about(q.message.chat, context)
            support_username = os.getenv("TELEGRAM_BOT_SUPPORT_USERNAME", "WorldFlowSupport")
            txt = t(lang, "support_text", support_username=support_username)
            await safe_edit(q, txt, reply_markup=kb_main_menu(lang), parse_mode="HTML")
            return
        # --------------------------------------------------------
        # 3) ABOUT
        # --------------------------------------------------------
        if action == BTN_ABOUT:
            await _cleanup_about(q.message.chat, context)

            file_id = os.getenv("ABOUT_FILE_ID", "")
            if file_id:
                try:
                    await q.edit_message_media(
                        media=InputMediaPhoto(
                            media=file_id,
                            caption=t(lang, "about_full"),
                            parse_mode="HTML"
                        ),
                        reply_markup=kb_about(lang),
                    )
                    return
                except Exception as e:
                    log.warning("edit_message_media failed: %s", e)

            # fallback (text)
            await safe_edit(
                q,
                t(lang, "about_full"),
                reply_markup=kb_about(lang),
                parse_mode="HTML",
            )
            return

        # --------------------------------------------------------
        # 4) CHANGE COUNTRY
        # --------------------------------------------------------
        if action == BTN_CHANGE_COUNTRY:
            await safe_edit(
                q,
                t(lang, "back_to_region"),
                reply_markup=kb_regions(),
                parse_mode="HTML",
            )
            return

        # --------------------------------------------------------
        # 5) MY APPLICATIONS (stub)
        # --------------------------------------------------------
        if action == BTN_MY_APPS:
            await safe_edit(
                q,
                t(lang, "my_apps_stub") + "\n\n" + t(lang, "menu_title"),
                reply_markup=kb_main_menu(lang)
            )
            return

        # --------------------------------------------------------
        # 6) BACK
        # --------------------------------------------------------
        if action == BTN_BACK:
            await replace_with_text(
                q,
                t(lang, "menu_title"),
                reply_markup=kb_main_menu(lang)
            )
            return


# Export public symbols
__all__ = [
    "on_callback",
    "_cleanup_about",
]