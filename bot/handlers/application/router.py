# from __future__ import annotations
#
# from telegram import Update
# from telegram.ext import ContextTypes
# from telegram.error import BadRequest, Forbidden, TimedOut, RetryAfter, NetworkError
#
# from handlers.application import _finish_wizard
# from handlers.application.prompt import send_step_prompt, wipe_last_prompt
# from handlers.application.utils import resolve_canonical
# from ui.panel.progress_panel import ProgressPanel
# from wizard.engine import WizardEngine
# from locales import L10N
# from core.logger import log
#
#
# async def update_file_progress_message(msg, context, safe_exceptions, text: str):
#     """Updates the '1/3', '2/3', ... message. Deletes previous one."""
#
#     old = context.user_data.get("file_progress_msg")
#     if old:
#         try:
#             await old.delete()
#         except safe_exceptions:
#             pass
#         context.user_data["file_progress_msg"] = None
#
#     new_msg = await msg.chat.send_message(text)
#     context.user_data["file_progress_msg"] = new_msg
#
# # =====================================================================
# # 🔥 UNIVERSAL ERROR HANDLER (removes repeated code)
# # =====================================================================
# async def handle_step_error(
#     msg,
#     context,
#     lang: str,
#     country: str,
#     step_key: str,
#     display: str,
#     safe_exceptions,
# ):
#     """Universal repeated step-error handling logic."""
#     try:
#         await msg.delete()
#     except safe_exceptions:
#         pass
#
#     prev = context.user_data.get("last_error_msg")
#     if prev:
#         try:
#             await prev.delete()
#         except safe_exceptions:
#             pass
#
#     err = await msg.chat.send_message(display)
#     context.user_data["last_error_msg"] = err
#
#     pending = context.user_data.get("file_progress_msg")
#     if pending:
#         try:
#             await pending.delete()
#         except safe_exceptions:
#             pass
#         context.user_data["file_progress_msg"] = None
#
#     await wipe_last_prompt(msg.chat, context)
#     await send_step_prompt(msg, context, lang, country, step_key)
#
#     return None
#
#
# # =====================================================================
# # 🔥 UNIVERSAL STEP SUCCESS HANDLER (also removes repeated code)
# # =====================================================================
# async def handle_step_success(
#     update: Update,
#     msg,
#     context,
#     engine: WizardEngine,
#     lang: str,
#     country: str,
#     next_step,
# ):
#     """Handles next step logic, progress panel, finish detection."""
#     SAFE_EXCEPTIONS = (BadRequest, Forbidden, TimedOut, RetryAfter, NetworkError)
#
#     pending = context.user_data.get("file_progress_msg")
#     if pending:
#         try:
#             await pending.delete()
#         except SAFE_EXCEPTIONS:
#             pass
#         context.user_data["file_progress_msg"] = None
#
#     try:
#         await msg.delete()
#     except SAFE_EXCEPTIONS:
#         pass
#
#     await wipe_last_prompt(msg.chat, context)
#
#     # Wizard finished?
#     if engine.is_finished():
#         log.info("[Router] Wizard finished 🎉")
#         await _finish_wizard(update, context, engine)
#         return None
#
#     # Update progress panel
#     panel = ProgressPanel(context, engine)
#     await panel.upsert(msg)
#
#     # Send next prompt
#     if next_step:
#         await send_step_prompt(msg, context, lang, country, next_step.key)
#
#     return None
#
#
# # =====================================================================
# # 🔵 MAIN ROUTER
# # =====================================================================
# async def handle_application_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if context.user_data.get("panel_mode") != "progress":
#         return None
#
#     SAFE_EXCEPTIONS = (BadRequest, Forbidden, TimedOut, RetryAfter, NetworkError)
#
#     msg = update.message
#     if not msg:
#         log.warning("[Router] No message object in update")
#         return None
#
#     # -----------------------------
#     # Wizard instance
#     # -----------------------------
#     engine: WizardEngine = context.user_data.get("wizard")
#     if not engine:
#         log.warning("[Router] No wizard engine in user_data")
#         return None
#
#     lang = engine.lang
#     country = engine.country
#     log.debug(f"[Router] Wizard context: country={country}, lang={lang}")
#
#     # -----------------------------
#     # Step detection
#     # -----------------------------
#     step = engine.current_step()
#     if not step:
#         log.warning("[Router] current_step() returned None")
#         return None
#
#     step_key = step.key
#     log.debug(f"[Router] Current step: {step_key}")
#
#     locale = L10N.get(lang, {})
#     steps = locale.get("steps", {})
#     steps_by_country = locale.get("steps_by_country", {})
#     step_cfg = steps_by_country.get(country, {}).get(step_key, {}) or steps.get(step_key, {})
#
#     expected_type = step_cfg.get("expected_type", "text")
#     max_files = step_cfg.get("max_files")
#
#     log.debug(f"[Router] StepCfg: expected_type={expected_type}, max_files={max_files}")
#     log.debug(f"[Router] StepCfg FULL: {step_cfg}")
#
#     # =====================================================================
#     # 🔥 FILE FLOW
#     # =====================================================================
#     if expected_type == "file":
#
#         log.debug(
#             f"[Router] File debug → document={msg.document}, "
#             f"photos={len(msg.photo or [])}, contact={msg.contact}"
#         )
#
#         # TEXT ON FILE STEP → reject
#         if msg.text:
#             return await handle_step_error(
#                 msg, context, lang, country, step_key,
#                 "📎 Прикрепите файл, а не текст.",
#                 SAFE_EXCEPTIONS
#             )
#
#         # CONTACT ON FILE STEP → reject
#         if msg.contact:
#             return await handle_step_error(
#                 msg, context, lang, country, step_key,
#                 "📎 Этот шаг принимает только документы / фото.",
#                 SAFE_EXCEPTIONS
#             )
#
#         # Extract file
#         if msg.document:
#             file_item = {
#                 "file_id": msg.document.file_id,
#                 "mime": msg.document.mime_type or "",
#                 "size": msg.document.file_size or 0,
#                 "name": msg.document.file_name or "Документ",
#             }
#         elif msg.photo:
#             p = msg.photo[-1]
#             file_item = {
#                 "file_id": p.file_id,
#                 "mime": "image/jpeg",
#                 "size": p.file_size or 0,
#                 "name": "Фото",
#             }
#         else:
#             return await handle_step_error(
#                 msg, context, lang, country, step_key,
#                 "📎 Прикрепите документ.",
#                 SAFE_EXCEPTIONS
#             )
#
#         log.debug(f"[Router] File received: {file_item}")
#
#         # -------------------------
#         # Storage
#         # -------------------------
#         files_key = f"files_{step_key}"
#         stored = context.user_data.setdefault(files_key, [])
#
#         if stored is None:
#             log.warning("[Router] stored=None found → fixing to []")
#             stored = []
#             context.user_data[files_key] = stored
#
#         stored.append(file_item)
#         log.debug(f"[Router] Files stored → {stored}")
#
#         # -------------------------
#         # LIMIT HANDLING
#         # -------------------------
#         if max_files:
#             if len(stored) < max_files:
#                 try:
#                     await msg.delete()
#                 except SAFE_EXCEPTIONS:
#                     pass
#
#                 await update_file_progress_message(
#                     msg,
#                     context,
#                     SAFE_EXCEPTIONS,
#                     f"Файл принят ({len(stored)}/{max_files}). Прикрепите следующий."
#                 )
#                 return None
#
#             pending = context.user_data.get("file_progress_msg")
#             if pending:
#                 try:
#                     await pending.delete()
#                 except SAFE_EXCEPTIONS:
#                     pass
#                 context.user_data["file_progress_msg"] = None
#
#             raw = stored
#             context.user_data[files_key] = None
#         else:
#             pending = context.user_data.get("file_progress_msg")
#             if pending:
#                 try:
#                     await pending.delete()
#                 except SAFE_EXCEPTIONS:
#                     pass
#                 context.user_data["file_progress_msg"] = None
#
#             raw = stored
#             context.user_data[files_key] = None
#
#         log.debug(f"[Router] Validation input (file): {raw}")
#
#         # -------------------------
#         # VALIDATION
#         # -------------------------
#         valid, canonical, display = await engine.validate_input(step_key, raw)
#         log.debug(f"[Router] FILE VALIDATION → valid={valid}, display={display}")
#
#         if not valid:
#             return await handle_step_error(
#                 msg, context, lang, country, step_key,
#                 display,
#                 SAFE_EXCEPTIONS
#             )
#
#         log.debug("[Router] ✔ FILE VALID")
#
#         ok, status = engine.process_answer(step_key, canonical, display)
#         log.debug(f"[Router] process_answer → ok={ok}, status={status}")
#
#         if not ok:
#             log.error("[Router] Engine.process_answer failed (file)")
#             return await handle_step_error(
#                 msg, context, lang, country, step_key,
#                 "Ошибка обработки ответа.",
#                 SAFE_EXCEPTIONS
#             )
#
#         success, next_step, _ = engine.next_step()
#         log.debug(f"[Router] Next step → {next_step}")
#
#         return await handle_step_success(
#             update, msg, context, engine, lang, country, next_step
#         )
#
#     # =====================================================================
#     # 📝 TEXT FLOW
#     # =====================================================================
#     log.debug(f"[Router] TEXT FLOW → raw_text={msg.text}")
#
#     if msg.contact and msg.contact.phone_number:
#         raw = msg.contact.phone_number.strip()
#     elif msg.text:
#         raw = msg.text.strip()
#     else:
#         raw = ""
#
#     value = resolve_canonical(step_cfg, raw)
#     raw_for_validation = value["canonical"]
#
#     valid, canonical, display = await engine.validate_input(step_key, raw_for_validation)
#
#     log.debug(f"[Router] TEXT VALIDATION → valid={valid}, display={display}")
#
#     if not valid:
#         return await handle_step_error(
#             msg, context, lang, country, step_key,
#             display,
#             SAFE_EXCEPTIONS
#         )
#
#     if canonical:
#         value["canonical"] = canonical
#     if display:
#         value["display"] = display
#
#     ok, status = engine.process_answer(step_key, value["canonical"], value["display"])
#     log.debug(f"[Router] process_answer → ok={ok}, status={status}")
#
#     if not ok:
#         log.error("[Router] Engine.process_answer failed (text)")
#         return await handle_step_error(
#             msg, context, lang, country, step_key,
#             "Ошибка обработки ответа.",
#             SAFE_EXCEPTIONS
#         )
#
#     success, next_step, _ = engine.next_step()
#     log.debug(f"[Router] Next step → {next_step}")
#
#     return await handle_step_success(
#         update, msg, context, engine, lang, country, next_step
#     )
#
#
# __all__ = ["handle_application_message"]
