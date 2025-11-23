from __future__ import annotations
import logging
import os
from dataclasses import dataclass
from typing import List, Optional, Set

from dotenv import load_dotenv
from telegram import (
    Update, InputMediaPhoto,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
)
from telegram.ext import (
    Application, CommandHandler, ContextTypes,
    CallbackQueryHandler, MessageHandler, filters,
)

# Load .env once at startup
load_dotenv()

# ===== Logging =====
logging.basicConfig(
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("worldflow")

# ===== Locales =====
from locales import t  # i18n

# ===== Callback data keys =====
CB_START = "start_flow"
CB_REGION = "region:"
CB_COUNTRY = "country:"
CB_MENU = "menu:"

BTN_SUPPORT        = "support"
BTN_ABOUT          = "about"
BTN_CHANGE_COUNTRY = "change_country"
BTN_MY_APPS        = "my_apps"
BTN_APPLY          = "apply"
BTN_BACK           = "back"

# ===== Settings =====
@dataclass(frozen=True)
class Settings:
    bot_token: str
    support_username: str
    app_name: str

def load_settings() -> Settings:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")
    return Settings(
        bot_token=token,
        support_username=os.getenv("SUPPORT_USERNAME", "WorldFlowSupport"),
        app_name=os.getenv("APPLICATION_NAME", "WorldFlow Credit"),
    )

# ===== Regions & Countries =====
REGIONS = {
    "CIS": {"title": "🌐 СНГ / CIS", "code": "CIS"},
    "EU":  {"title": "🇪🇺 Europe",   "code": "EU"},
    "NA":  {"title": "🗽 North America", "code": "NA"},
    "AS":  {"title": "🏯 Asia", "code": "AS"},
}

COUNTRIES_BY_REGION = {
    "CIS": [
        {"flag": "🇷🇺", "title": "Россия",    "code": "RU", "lang": "ru"},
        {"flag": "🇧🇾", "title": "Беларусь",  "code": "BY", "lang": "be"},
        {"flag": "🇰🇿", "title": "Қазақстан", "code": "KZ", "lang": "kk"},
    ],
    "EU": [
        {"flag": "🇩🇪", "title": "Deutschland", "code": "DE", "lang": "de"},
        {"flag": "🇫🇷", "title": "France",      "code": "FR", "lang": "fr"},
        {"flag": "🇬🇷", "title": "Ελλάδα",      "code": "GR", "lang": "el"},
        {"flag": "🇬🇧", "title": "United Kingdom", "code": "GB", "lang": "en"},
    ],
    "NA": [
        {"flag": "🇺🇸", "title": "United States", "code": "US", "lang": "en"},
        {"flag": "🇨🇦", "title": "Canada",        "code": "CA", "lang": "en"},
    ],
    "AS": [
        {"flag": "🇮🇳", "title": "भारत (India)", "code": "IN", "lang": "hi"},
        {"flag": "🇦🇪", "title": "الإمارات (UAE)", "code": "AE", "lang": "ar"},
    ],
}

LANG_BY_COUNTRY = {c["code"]: c["lang"] for region in COUNTRIES_BY_REGION.values() for c in region}
COUNTRY_TITLE   = {c["code"]: f'{c["flag"]} {c["title"]}' for region in COUNTRIES_BY_REGION.values() for c in region}

# ===== Static UI =====
WELCOME_BILINGUAL = (
    "*Let’s get you started*\n\n"
    "▶ To continue, select your country and start the application.\n\n"
    "🌍 Indicate the country for your application.\n"
    "📄 The form and language will adjust automatically.\n"
    
    "\n— — — — — — — — — —\n\n"
    
    "*Начнём оформление*\n\n"
    "▶ Чтобы продолжить, выберите страну и начните оформление.\n\n"
    "🌍 Укажите страну для подачи заявки.\n"
    "📄 Анкета и язык настроятся автоматически."
)

# ===== Keyboards =====
def kb_start() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("▶ Start", callback_data=CB_START)]])

def cb_region(code: str) -> str:  return f"{CB_REGION}{code}"
def cb_country(code: str) -> str: return f"{CB_COUNTRY}{code}"
def cb_menu(action: str) -> str:  return f"{CB_MENU}{action}"

def kb_regions() -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []
    for code in ("CIS", "EU", "NA", "AS"):
        rows.append([InlineKeyboardButton(REGIONS[code]["title"], callback_data=cb_region(code))])
    return InlineKeyboardMarkup(rows)

def kb_countries(region_code: str) -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []
    for c in COUNTRIES_BY_REGION[region_code]:
        rows.append([InlineKeyboardButton(f'{c["flag"]} {c["title"]}', callback_data=cb_country(c["code"]))])
    rows.append([InlineKeyboardButton("↩️ Back / Назад", callback_data=CB_START)])
    return InlineKeyboardMarkup(rows)

def kb_main_menu(lang: str) -> InlineKeyboardMarkup:
    row_apply = [InlineKeyboardButton(t(lang, "btn_apply"), callback_data=cb_menu(BTN_APPLY))]
    rows = [
        row_apply,
        [
            InlineKeyboardButton(t(lang, "btn_support"), callback_data=cb_menu(BTN_SUPPORT)),
            InlineKeyboardButton(t(lang, "btn_about"),   callback_data=cb_menu(BTN_ABOUT)),
        ],
        [
            InlineKeyboardButton(t(lang, "btn_change_country"), callback_data=cb_menu(BTN_CHANGE_COUNTRY)),
            InlineKeyboardButton(t(lang, "btn_my_apps"),        callback_data=cb_menu(BTN_MY_APPS)),
        ],
    ]
    return InlineKeyboardMarkup(rows)

def kb_about(lang: str) -> InlineKeyboardMarkup:
    WEBSITE  = os.getenv("SOCIAL_WEBSITE",  "https://example.com")
    TG_CH    = os.getenv("SOCIAL_TG",       "https://t.me/worldflowcredit")
    INSTA    = os.getenv("SOCIAL_IG",       "https://instagram.com/worldflowcredit")
    X_TW     = os.getenv("SOCIAL_X",        "https://twitter.com/worldflowcredit")
    LINKEDIN = os.getenv("SOCIAL_LINKEDIN", "https://linkedin.com/company/worldflowcredit")
    YT       = os.getenv("SOCIAL_YT",       "https://youtube.com/@worldflowcredit")

    rows = [
        [InlineKeyboardButton(t(lang, "btn_website"), url=WEBSITE), InlineKeyboardButton(t(lang, "btn_tg_channel"), url=TG_CH)],
        [InlineKeyboardButton(t(lang, "btn_instagram"), url=INSTA), InlineKeyboardButton(t(lang, "btn_x"), url=X_TW)],
        [InlineKeyboardButton(t(lang, "btn_linkedin"), url=LINKEDIN), InlineKeyboardButton(t(lang, "btn_youtube"), url=YT)],
        [InlineKeyboardButton(t(lang, "btn_back"), callback_data=cb_menu(BTN_BACK))],
    ]
    return InlineKeyboardMarkup(rows)

# ===== Application (wizard) state =====
APP_FLOW  = "app_flow"
APP_STEPS = "steps"
APP_IDX   = "idx"
APP_ANS   = "answers"

BASE_STEP_ORDER = [
    "access_code",
    "full_name",
    "phone",
    "email",
    "loan_amount",
    "id_number",
    "reg_address",
    "actual_address",
    "dob",
    "marital_status",
    "workplace",
]

# ===== Fintech-style progress panel helpers =====
PROGRESS_MSG_ID   = "progress_msg_id"     # last (for edit)
PROGRESS_MSG_IDS  = "progress_msg_ids"    # ALL created (for cleanup)
LAST_PROMPT_MSG_ID  = "last_prompt_msg_id"
LAST_SERVICE_MSG_ID = "last_service_msg_id"

def _html_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def _short(val: str, limit: int = 64) -> str:
    s = val.strip()
    return s if len(s) <= limit else s[:limit - 1] + "…"

def _label(lang: str, key: str) -> str:
    return t(lang, f"labels.{key}") or key

def build_step_order(country_code: str) -> list[str]:
    steps = BASE_STEP_ORDER.copy()
    if country_code == "RU":
        i = steps.index("id_number") + 1
        steps.insert(i, "inn_ru")
    return steps

ACCESS_CODE_PROMPTS = {
    "en": "🔐 Do you have a personal access code?\n\nEnter it below — optional. You can also type “No”.",
    "ru": "🔐 У вас есть персональный код доступа?\n\nВведите его ниже — необязательно. Можно написать «Нет».",
}

def get_prompt(lang: str, country: str, step_key: str) -> str:
    country_key = f"steps_by_country.{country}.{step_key}"
    s = t(lang, country_key)
    if s != country_key:
        return s
    base_key = f"steps.{step_key}"
    s = t(lang, base_key)
    if s != base_key:
        return s
    if step_key == "access_code": return ACCESS_CODE_PROMPTS.get(lang, ACCESS_CODE_PROMPTS["en"])
    if step_key == "inn_ru":      return "🔢 Укажите ваш ИНН (10 или 12 цифр)."
    return f"[{step_key}]"

def progress_panel_html(lang: str, steps: list[str], answers: dict) -> str:
    title  = t(lang, "ui.preview_title")
    done_h = t(lang, "ui.done")
    todo_h = t(lang, "ui.todo")

    done_lines, todo_lines = [], []
    for key in steps:
        label = _html_escape(_label(lang, key))
        raw_val = answers.get(key)
        filled = (isinstance(raw_val, str) and raw_val.strip() != "") or (raw_val not in (None, ""))
        shown = "—" if not filled else _short(str(raw_val))
        shown = _html_escape(shown)
        line = f"• <b>{label}</b> — <code>{shown}</code>"
        (done_lines if filled else todo_lines).append(line)

    parts = [f"<b>📊 {title}</b>"]
    if done_lines: parts += [f"\n<b>{done_h}</b>", *done_lines]
    if todo_lines: parts += [f"\n<b>{todo_h}</b>", *todo_lines]
    return "\n".join(parts)

def _track_panel_id(context: ContextTypes.DEFAULT_TYPE, mid: int) -> None:
    ids: List[int] = context.user_data.get(PROGRESS_MSG_IDS, [])
    if mid not in ids:
        ids.append(mid)
        context.user_data[PROGRESS_MSG_IDS] = ids

async def _cleanup_old_panels(msg, context: ContextTypes.DEFAULT_TYPE, keep: Set[int]) -> None:
    ids: List[int] = context.user_data.get(PROGRESS_MSG_IDS, [])
    remain: List[int] = []
    for mid in ids:
        if mid in keep:
            remain.append(mid)
            continue
        try:
            await msg.chat.delete_message(mid)
        except Exception:
            pass
    context.user_data[PROGRESS_MSG_IDS] = remain

async def upsert_progress_panel(msg, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang") or "en"
    steps: list[str] = context.user_data.get(APP_STEPS, [])
    answers: dict = context.user_data.get(APP_ANS, {})
    html = progress_panel_html(lang, steps, answers)

    pmid: Optional[int] = context.user_data.get(PROGRESS_MSG_ID)
    if pmid:
        try:
            await msg.chat.edit_message_text(message_id=pmid, text=html, parse_mode="HTML")
            _track_panel_id(context, pmid)
            await _cleanup_old_panels(msg, context, keep={pmid})
            return
        except Exception as e:
            # cannot edit — delete stale and replace
            try:
                await msg.chat.delete_message(pmid)
            except Exception:
                pass

    sent = await msg.reply_text(html, parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
    context.user_data[PROGRESS_MSG_ID] = sent.message_id
    _track_panel_id(context, sent.message_id)
    await _cleanup_old_panels(msg, context, keep={sent.message_id})

# ===== Safe editor for media/text messages =====
async def safe_edit(q, text: str, reply_markup=None, parse_mode: Optional[str] = None):
    """
    Edits the current message safely:
    - if it's a media message -> edit caption
    - else -> edit text
    Fallback: delete message and send a new one.
    """
    m = q.message
    is_media = bool(getattr(m, "photo", None) or getattr(m, "video", None) or
                    getattr(m, "document", None) or getattr(m, "animation", None))
    try:
        if is_media:
            await q.edit_message_caption(caption=text, reply_markup=reply_markup, parse_mode=parse_mode)
        else:
            await q.edit_message_text(text=text, reply_markup=reply_markup, parse_mode=parse_mode)
        return
    except Exception as e:
        log.debug("safe_edit: primary edit failed, fallback to delete+send. %s", e)
        try:
            await m.delete()
        except Exception:
            pass
        await m.chat.send_message(text=text, reply_markup=reply_markup, parse_mode=parse_mode)

async def replace_with_text(q, text, reply_markup=None, parse_mode=None):
    m = q.message
    try:
        await m.delete()
    except Exception:
        pass
    await m.chat.send_message(text=text, reply_markup=reply_markup, parse_mode=parse_mode)

# ===== Bot handlers =====
async def send_step_prompt(qmsg_or_upd, lang: str, country: str, step_key: str):
    text = get_prompt(lang, country, step_key)
    reply_markup = None

    if step_key == "phone":
        share = t(lang, "ui.share_phone")
        manual = t(lang, "ui.type_manually")
        reply_markup = ReplyKeyboardMarkup(
            [[KeyboardButton(share, request_contact=True)],
             [KeyboardButton(manual)]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    elif step_key == "marital_status":
        options = []
        base = t(lang, "steps.marital_status")
        for line in (base or "").splitlines():
            opt = line.strip(" ••\t")
            if opt and "•" not in opt and ":" not in opt and "💬" not in opt and len(opt) <= 32:
                if any(k in opt for k in ("Варианты", "Варыянты", "Таңдау", "Options", "Optionen", "Options :", "Επιλογές", "الخيارات")):
                    continue
                options.append(opt)
        if not options:
            options = ["Single", "Married", "Divorced", "Widowed"]
        reply_markup = ReplyKeyboardMarkup([[KeyboardButton(opt)] for opt in options],
                                           resize_keyboard=True,
                                           one_time_keyboard=True)

    if hasattr(qmsg_or_upd, "reply_text"):
        return await qmsg_or_upd.reply_text(text, reply_markup=reply_markup)
    else:
        return await qmsg_or_upd.chat.send_message(text=text, reply_markup=reply_markup)

async def _wipe_all_progress_panels(chat, context: ContextTypes.DEFAULT_TYPE):
    ids: List[int] = context.user_data.get(PROGRESS_MSG_IDS, [])
    for mid in ids:
        try:
            await chat.delete_message(mid)
        except Exception:
            pass
    context.user_data.pop(PROGRESS_MSG_IDS, None)
    context.user_data.pop(PROGRESS_MSG_ID, None)

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # wipe any previous UI from this chat
    if update.effective_chat:
        await _wipe_all_progress_panels(update.effective_chat, context)

    context.user_data.clear()
    if update.message:
        await update.message.reply_text(WELCOME_BILINGUAL, parse_mode="Markdown", reply_markup=kb_start())
    else:
        # could be triggered by callback from a media message, so use safe_edit
        await safe_edit(update.callback_query, WELCOME_BILINGUAL, reply_markup=kb_start(), parse_mode="Markdown")

async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    q = update.callback_query
    await q.answer()
    data = q.data or ""
    lang = context.user_data.get("lang") or "en"

    if data == CB_START:
        # starting over → cleanup panels too
        await _wipe_all_progress_panels(q.message.chat, context)
        await safe_edit(q, WELCOME_BILINGUAL, reply_markup=kb_regions(), parse_mode="Markdown")
        return

    if data.startswith(CB_REGION):
        region_code = data.split(":", 1)[1]
        await safe_edit(q, WELCOME_BILINGUAL, reply_markup=kb_countries(region_code), parse_mode="Markdown")
        return

    if data.startswith(CB_COUNTRY):
        country_code = data.split(":", 1)[1]
        context.user_data["country"] = country_code
        lang = LANG_BY_COUNTRY.get(country_code, "en")
        context.user_data["lang"] = lang

        text = t(lang, "after_country_selected", country=COUNTRY_TITLE.get(country_code, country_code))
        text += "\n\n" + t(lang, "menu_title")
        await safe_edit(q, text, reply_markup=kb_main_menu(lang))
        return

    if data.startswith(CB_MENU):
        action = data.split(":", 1)[1]
        if action == BTN_APPLY:
            country = context.user_data.get("country") or "US"
            lang = context.user_data.get("lang") or "en"
            steps = build_step_order(country)
            context.user_data[APP_FLOW] = True
            context.user_data[APP_STEPS] = steps
            context.user_data[APP_IDX] = 0
            context.user_data[APP_ANS] = {}

            await safe_edit(q, t(lang, "apply_text"))
            await upsert_progress_panel(q.message, context)

            sent_prompt = await send_step_prompt(q.message, lang, country, steps[0])
            if sent_prompt and hasattr(sent_prompt, "message_id"):
                context.user_data[LAST_PROMPT_MSG_ID] = sent_prompt.message_id
            return

        if action == BTN_SUPPORT:
            support_username = os.getenv("SUPPORT_USERNAME", "WorldFlowSupport")
            txt = t(lang, "support_text", support_username=support_username) + "\n\n" + t(lang, "menu_title")
            await safe_edit(q, txt, reply_markup=kb_main_menu(lang))
            return

        if action == BTN_ABOUT:
            file_id = os.getenv("ABOUT_FILE_ID", "AgACAgIAAxkBAAMlaMaGKun818899Ofq-VykTYr2ZgsAAmDzMRtEzDlKa-c7JNW7ODkBAAMCAAN5AAM2BA")
            if file_id:
                try:
                    await q.edit_message_media(
                        media=InputMediaPhoto(media=file_id, caption=t(lang, "about_full"), parse_mode="HTML"),
                        reply_markup=kb_about(lang),
                    )
                    return
                except Exception as e:
                    log.warning("edit_message_media failed: %s", e)

            # Fallback to text (use safe_edit in case previous is media)
            await safe_edit(q, t(lang, "about_full"), reply_markup=kb_about(lang), parse_mode="Markdown")
            return

        if action == BTN_CHANGE_COUNTRY:
            await safe_edit(q, t(lang, "back_to_region"), reply_markup=kb_regions())
            return

        if action == BTN_MY_APPS:
            await safe_edit(q, t(lang, "my_apps_stub") + "\n\n" + t(lang, "menu_title"), reply_markup=kb_main_menu(lang))
            return

        if action == BTN_BACK:
            await replace_with_text(q, t(lang, "menu_title"), reply_markup=kb_main_menu(lang))
            return

async def handle_application_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get(APP_FLOW):
        return

    msg = update.message
    if not msg:
        return

    country = context.user_data.get("country") or "US"
    lang = context.user_data.get("lang") or "en"
    steps: list[str] = context.user_data.get(APP_STEPS, [])
    idx: int = context.user_data.get(APP_IDX, 0)
    answers: dict = context.user_data.get(APP_ANS, {})

    if idx >= len(steps):
        return

    step_key = steps[idx]
    value = None

    # Handle phone contact share
    if step_key == "phone" and msg.contact:
        value = msg.contact.phone_number
        svc = await msg.reply_text("✅")
        context.user_data[LAST_SERVICE_MSG_ID] = svc.message_id

    if value is None:
        text = (msg.text or "").strip()
        manual = t(lang, "ui.type_manually")
        # If user chose manual entry, re-send prompt without keyboard
        if step_key == "phone" and (text == manual or "Ввести вручную" in text or "Manuell" in text or "Entrer" in text):
            prompt = await msg.reply_text(get_prompt(lang, country, step_key), reply_markup=ReplyKeyboardRemove())
            context.user_data[LAST_PROMPT_MSG_ID] = prompt.message_id
            return
        value = text

    # Save answer
    answers[step_key] = value
    context.user_data[APP_ANS] = answers

    # Cleanup: previous bot prompt & service ticks
    last_prompt_id = context.user_data.pop(LAST_PROMPT_MSG_ID, None)
    if last_prompt_id:
        try: await msg.chat.delete_message(last_prompt_id)
        except Exception: pass

    last_svc_id = context.user_data.pop(LAST_SERVICE_MSG_ID, None)
    if last_svc_id:
        try: await msg.chat.delete_message(last_svc_id)
        except Exception: pass

    # Try to delete user's message
    try: await msg.delete()
    except Exception: pass

    # Update single progress panel (and cleanup old ones)
    await upsert_progress_panel(msg, context)

    # Next step
    idx += 1
    context.user_data[APP_IDX] = idx

    if idx >= len(steps):
        # finish: remove the panel and reset
        await _wipe_all_progress_panels(msg.chat, context)
        context.user_data[APP_FLOW] = False
        await msg.chat.send_message(t(lang, "ui.completed_demo"), reply_markup=ReplyKeyboardRemove())
        await msg.chat.send_message(t(lang, "menu_title"), reply_markup=kb_main_menu(lang))
        return

    sent_prompt = await send_step_prompt(msg, lang, country, steps[idx])
    if sent_prompt and hasattr(sent_prompt, "message_id"):
        context.user_data[LAST_PROMPT_MSG_ID] = sent_prompt.message_id

# ===== App bootstrap =====
def build_app() -> Application:
    settings = load_settings()
    app = Application.builder().token(settings.bot_token).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.TEXT | filters.CONTACT, handle_application_message))
    return app

def main() -> None:
    app = build_app()
    log.info("WorldFlow Credit bot started")
    app.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    main()
