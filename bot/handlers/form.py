"""Conversation handler logic with validation & keyboards."""
from datetime import datetime

import httpx
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from questions import QUESTION_LIST
from utils import validators as v
from keyboards.main_menu import ASSETS_KB, FAMILY_KB
from config import BACKEND_URL

FORM = range(1)

# maps for per‑field validation and keyboards
auth_validators = {
    "email": v.email,
    "phone_number": v.phone,
    "reg_date": v.date_ddmmyyyy,
    "employment_date": v.date_ddmmyyyy,
    "amount": v.numeric,
}
field_keyboards = {
    "assets": ASSETS_KB,
    "family_status": FAMILY_KB,
}

# in‑memory buffer -> {tg_id: {field: value}}
user_buffer: dict[int, dict] = {}

async def start(update: Update, ctx: CallbackContext):
    ctx.user_data["step"] = 0
    user_buffer[update.effective_user.id] = {}
    first_key, first_text = QUESTION_LIST[0]
    kb = field_keyboards.get(first_key)
    await update.message.reply_text(first_text, reply_markup=kb if kb else None)
    return FORM

async def handle(update: Update, ctx: CallbackContext):
    uid = update.effective_user.id
    step = ctx.user_data.get("step", 0)
    key, _ = QUESTION_LIST[step]
    value = update.message.text.strip()

    # validation
    check = auth_validators.get(key)
    if check and not check(value):
        await update.message.reply_text("❌ Некорректное значение, попробуйте ещё раз.")
        return FORM

    user_buffer[uid][key] = value
    step += 1

    if step < len(QUESTION_LIST):
        ctx.user_data["step"] = step
        next_key, next_text = QUESTION_LIST[step]
        kb = field_keyboards.get(next_key)
        await update.message.reply_text(next_text, reply_markup=kb if kb else None)
        return FORM

    # form finished => compose payload
    data = user_buffer[uid]
    data.update(
        role="CLIENT",
        telegram_id=str(uid),
        telegram_username=update.effective_user.username or "",
        is_active=True,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
        report_files=[],
    )

    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(BACKEND_URL, json=data)
        if r.status_code in (200, 201):
            await update.message.reply_text("✅ Анкета отправлена успешно!")
        else:
            await update.message.reply_text(f"❌ Сервер ответил: {r.status_code}\n{r.text}")
    except Exception as exc:
        await update.message.reply_text(f"❌ Сбой при отправке: {exc}")

    return ConversationHandler.END

async def cancel(update: Update, ctx: CallbackContext):
    await update.message.reply_text("❌ Анкета отменена.")
    return ConversationHandler.END