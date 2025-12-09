# # ui/progress.py
# """
# Fintech-style progress summary panel with nested L10N architecture.
# """
#
# from __future__ import annotations
#
# from typing import List, Set
# from telegram.ext import ContextTypes
# from telegram.error import BadRequest, Forbidden, TelegramError
# from telegram import (
#     InlineKeyboardMarkup,
#     InlineKeyboardButton,
# )
#
# from core.logger import log
# from locales import L10N
# from constants import PROGRESS_MSG_ID, PROGRESS_MSG_IDS
# from constants.callbacks import CB_BACK, CB_NEXT, CB_CANCEL
# from wizard import Step
#
#
# # ============================================================
# # Helpers
# # ============================================================
#
# def _html_escape(s: str) -> str:
#     return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
#
#
# def _short(val: str, limit: int = 64) -> str:
#     s = str(val).strip()
#     return s if len(s) <= limit else s[: limit - 1] + "…"
#
#
# # ============================================================
# # L10N label resolvers
# # ============================================================
#
# def resolve_text(lang: str, key: str) -> str:
#     """
#     Fetch: ui[key], titles[key], buttons[key], common[key]
#     This is for: progress_title, done, back, next, cancel...
#     """
#     loc = L10N.get(lang, {})
#     for ns in ("ui", "titles", "buttons", "common", "progress_panel"):
#         block = loc.get(ns, {})
#         if key in block:
#             return block[key]
#     return key
#
#
# def resolve_label(lang: str, country: str, step_key: str) -> str:
#     """
#     Fetch: steps_by_country[country][step].label
#            steps[step].label
#     """
#     loc = L10N.get(lang, {})
#
#     # country override
#     sbc = loc.get("steps_by_country", {})
#     cfg = sbc.get(country, {}).get(step_key)
#     if cfg and "label" in cfg:
#         return cfg["label"]
#
#     # global step
#     steps = loc.get("steps", {})
#     cfg = steps.get(step_key)
#     if cfg and "label" in cfg:
#         return cfg["label"]
#
#     return step_key
#
#
# # ============================================================
# # HTML panel generator
# # ============================================================
#
# def progress_panel_html(lang: str, country: str, steps: list[Step], answers: dict, idx: int) -> str:
#     # -------------------------
#     #   UI L10N
#     # -------------------------
#     title = resolve_text(lang, "progress_title")
#     done_h = resolve_text(lang, "done")
#     current_h = resolve_text(lang, "current")
#     bar_h = resolve_text(lang, "progress_bar")
#     step_word = resolve_text(lang, "step")
#     of_word = resolve_text(lang, "of")
#     no_data = resolve_text(lang, "no_data")
#
#     # -------------------------
#     #   Step info
#     # -------------------------
#     total = len(steps)
#     step_number = idx + 1
#     current_step = steps[idx]
#     current_label = resolve_label(lang, country, current_step.key)
#
#     # -------------------------
#     #   FIXED Emoji Progress Bar (10 cells)
#     # -------------------------
#     FULL = "🟩"   # completed
#     EMPTY = "🟦"  # remaining
#     BAR_LEN = 10  # fixed length bar
#
#     # ratio
#     ratio = step_number / total if total > 0 else 0
#     filled = int(round(ratio * BAR_LEN))
#
#     # guarantee at least 1 filled on step 1
#     if filled == 0 and step_number > 0:
#         filled = 1
#
#     # clamp to bounds
#     filled = max(1, min(BAR_LEN, filled))
#
#     bar = FULL * filled + EMPTY * (BAR_LEN - filled)
#
#     # -------------------------
#     #   Completed steps list
#     # -------------------------
#     rows = []
#
#     for i, s in enumerate(steps):
#         key = s.key
#         label = resolve_label(lang, country, key)
#
#         bullet = "➡️" if i == idx else "•"
#
#         entry = answers.get(key)
#         display_value = entry.get("display") if entry else None
#
#         if display_value:
#             rows.append(f"{bullet} <b>{label}</b>: <code>{_short(display_value)}</code>")
#         elif i == idx:
#             rows.append(f"{bullet} <b>{label}</b>: <i>{no_data}</i>")
#         else:
#             rows.append(f"{bullet} <b>{label}</b>")
#
#     completed_block = "\n".join(rows)
#
#     # -------------------------
#     #   Final HTML
#     # -------------------------
#     return f"""
# <b>📋 {title}</b>
#
# <b>{bar_h}:</b>
# {bar}
# <b>{step_word} {step_number} {of_word} {total}</b>
#
# <b>{current_h}:</b>
# • <b>{current_label}</b>
#
# <b>{done_h}:</b>
# {completed_block}
# """.strip()
#
# # ============================================================
# # Panel state handlers
# # ============================================================
#
# def _track_panel_id(context: ContextTypes.DEFAULT_TYPE, mid: int) -> None:
#     ids: List[int] = context.user_data.get(PROGRESS_MSG_IDS, [])
#     if mid not in ids:
#         ids.append(mid)
#     context.user_data[PROGRESS_MSG_IDS] = ids
#
#
# async def _cleanup_old_panels(msg, context: ContextTypes.DEFAULT_TYPE, keep: Set[int]):
#     ids: List[int] = context.user_data.get(PROGRESS_MSG_IDS, [])
#     remain = []
#
#     for mid in ids:
#         if mid in keep:
#             remain.append(mid)
#             continue
#
#         try:
#             await msg.chat.delete_message(mid)
#         except (BadRequest, Forbidden):
#             pass
#         except TelegramError as e:
#             log.warning(f"[progress_panel] TelegramError: {e}")
#
#     context.user_data[PROGRESS_MSG_IDS] = remain
#
#
# # ============================================================
# # Upsert panel
# # ============================================================
#
# async def upsert_progress_panel(msg, context: ContextTypes.DEFAULT_TYPE):
#     lang = context.user_data.get("lang") or "en"
#     country = context.user_data.get("country") or "US"
#
#     wizard = context.user_data.get("wizard")
#     if not wizard:
#         return
#
#     # <-- ключове!
#     steps = wizard.queue.steps     # <--- Step objects, not strings
#     answers = wizard.queue.answers
#     idx = wizard.queue.index
#
#     html = progress_panel_html(lang, country, steps, answers, idx)
#
#     kb = InlineKeyboardMarkup([
#         [
#             InlineKeyboardButton(resolve_text(lang, "back"), callback_data=CB_BACK),
#             InlineKeyboardButton(resolve_text(lang, "next"), callback_data=CB_NEXT),
#         ],
#         [
#             InlineKeyboardButton(resolve_text(lang, "cancel"), callback_data=CB_CANCEL),
#         ],
#     ])
#
#     pmid = context.user_data.get(PROGRESS_MSG_ID)
#
#     if pmid:
#         try:
#             await context.bot.edit_message_text(
#                 chat_id=msg.chat_id,
#                 message_id=pmid,
#                 text=html,
#                 parse_mode="HTML",
#                 reply_markup=kb
#             )
#             _track_panel_id(context, pmid)
#             await _cleanup_old_panels(msg, context, keep={pmid})
#             return
#         except Exception:
#             try:
#                 await msg.chat.delete_message(pmid)
#             except Exception:
#                 pass
#
#     sent = await msg.reply_text(text=html, parse_mode="HTML", reply_markup=kb)
#
#     context.user_data[PROGRESS_MSG_ID] = sent.message_id
#     _track_panel_id(context, sent.message_id)
#     await _cleanup_old_panels(msg, context, keep={sent.message_id})
#
#
# # ============================================================
# # Cleanup all
# # ============================================================
#
# async def wipe_all_progress_panels(chat, context: ContextTypes.DEFAULT_TYPE):
#     ids: List[int] = context.user_data.get(PROGRESS_MSG_IDS, [])
#
#     for mid in ids:
#         try:
#             await chat.delete_message(mid)
#         except Exception:
#             pass
#
#     context.user_data.pop(PROGRESS_MSG_IDS, None)
#     context.user_data.pop(PROGRESS_MSG_ID, None)
#
# #
# __all__ = [
#     "progress_panel_html",
#     "upsert_progress_panel",
#     "wipe_all_progress_panels",
# ]
