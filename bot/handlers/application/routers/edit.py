from __future__ import annotations

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest, Forbidden, TimedOut, RetryAfter, NetworkError
from copy import deepcopy

from constants.callbacks import CB_SAVE, CB_GOTO, CB_CANCEL
from handlers.application.routers.base import BaseRouter
from handlers.application.utils import resolve_canonical
from ui.panel.utils import resolve_label
from locales import translate as t, L10N

from handlers.application.prompt import (
    send_step_prompt,
    wipe_last_prompt,
    wipe_all_prompts,
)

SAFE_EX = (BadRequest, Forbidden, TimedOut, RetryAfter, NetworkError)


class EditRouter(BaseRouter):

    # ============================================================
    # UPDATE PANEL + SEND PROMPT
    # ============================================================
    async def update_panel(self):
        # 0) Якщо вперше заходимо — скидаємо активне поле
        wizard = self.engine
        if not self.context.user_data.get("edit_intro_shown"):
            wizard.queue.index = None  # <-- НІЯКЕ поле не вибране

            intro = t(self.lang, "bodies.edit_mode_intro")
            msg = await self.msg.chat.send_message(intro)
            self.context.user_data["edit_intro_shown"] = True
            self.context.user_data["edit_intro_msg_id"] = msg.message_id

        # 1) Чистимо старі промпти
        await wipe_all_prompts(self.msg.chat, self.context)
        await self._safe_delete_user_msg()

        # 2) Панель
        from ui.panel.edit import EditPanel  # lazy import to avoid circular
        panel = EditPanel(self.context, self.engine)
        await panel.upsert(self.msg)

        # 3) Якщо поле НЕ вибране → НЕ надсилаємо промпт
        if wizard.queue.index is None:
            return

        # 4) Якщо поле вибране → надсилаємо промпт
        step = wizard.current_step()
        await send_step_prompt(
            msg=self.msg,
            context=self.context,
            lang=self.lang,
            country=self.country,
            step_key=step.key,
        )

    # ============================================================
    # UNIVERSAL DELETE
    # ============================================================
    async def _delete_msg_obj(self, msg_obj):
        if not msg_obj:
            return
        if hasattr(msg_obj, "delete"):
            try:
                await msg_obj.delete()
            except SAFE_EX:
                pass
            return
        try:
            await self.msg.chat.delete_message(msg_obj)
        except SAFE_EX:
            pass

    # ============================================================
    # TEMP CLEANUP (errors, progress, selector)
    # ============================================================
    async def _cleanup_temp(self):
        keys = [
            "edit_error_msg",
            "edit_file_msg",
            "last_error_msg",
            "file_progress_msg",
            "enum_error_msg",
            "progress_error_msg",
            "selector_msg_id",
        ]
        for key in keys:
            msg_obj = self.context.user_data.pop(key, None)
            await self._delete_msg_obj(msg_obj)

    # ============================================================
    # NOTIFICATION CLEANER
    # ============================================================
    async def _clear_notifications(self):
        keys = [
            "edit_intro_msg_id",
            "edit_select_msg_id",
            "edit_updated_msg_id",
        ]
        for key in keys:
            msg_id = self.context.user_data.pop(key, None)
            if msg_id:
                try:
                    await self.msg.chat.delete_message(msg_id)
                except SAFE_EX:
                    pass

    @staticmethod
    def _is_user_message(msg):
        return msg and msg.reply_markup is None

    async def _safe_delete_user_msg(self):
        if self._is_user_message(self.msg):
            try:
                await self.msg.delete()
            except SAFE_EX:
                pass

    # ============================================================
    # VALIDATION HELP
    # ============================================================
    def _get_step_cfg(self, step_key):
        locale = L10N.get(self.lang, {})
        return (
            locale.get("steps_by_country", {}).get(self.country, {}).get(step_key, {})
            or locale.get("steps", {}).get(step_key, {})
        )

    # ============================================================
    # TEXT INPUT
    # ============================================================
    async def on_text(self):
        wizard = self.engine

        # 🛑 Якщо поле не вибрано
        if wizard.queue.index is None:
            await self._delete_msg_obj(self.context.user_data.pop("edit_error_msg", None))
            await self._delete_msg_obj(self.context.user_data.pop("edit_select_msg_id", None))
            await self._delete_msg_obj(self.context.user_data.pop("edit_updated_msg_id", None))
            await self._delete_msg_obj(self.context.user_data.pop("selector_msg_id", None))
            return await self._show_error(
                t(self.lang, "bodies.edit_no_field_selected")
            )

        step = wizard.current_step()
        key = step.key

        # 🔥 FIX: support Telegram contact input
        if self.msg.contact and self.msg.contact.phone_number:
            raw = self.msg.contact.phone_number.strip()
        elif self.msg.text:
            raw = self.msg.text.strip()
        else:
            raw = ""

        cfg = self._get_step_cfg(key)

        value = resolve_canonical(cfg, raw)

        ok, error = wizard.process_answer(key, value["canonical"], value["display"])
        if not ok:
            return await self._show_error(error)

        label = resolve_label(self.lang, self.country, key)

        wizard.queue.index = None
        self.context.user_data.pop("edit_intro_shown", None)

        await self._delete_msg_obj(self.context.user_data.pop("edit_error_msg", None))
        await self._delete_msg_obj(self.context.user_data.pop("edit_select_msg_id", None))
        await self._delete_msg_obj(self.context.user_data.pop("edit_updated_msg_id", None))
        await self._delete_msg_obj(self.context.user_data.pop("selector_msg_id", None))

        await self.update_panel()

        await self._notify_field_updated(label)

        return None
    # ============================================================
    # FILE INPUT
    # ============================================================
    async def on_file(self):
        msg = self.msg
        ctx = self.context
        wizard = self.engine

        # 🛑 Якщо поле не вибрано
        if wizard.queue.index is None:
            await self._delete_msg_obj(self.context.user_data.pop("edit_error_msg", None))
            await self._delete_msg_obj(self.context.user_data.pop("edit_select_msg_id", None))
            await self._delete_msg_obj(self.context.user_data.pop("edit_updated_msg_id", None))
            await self._delete_msg_obj(self.context.user_data.pop("selector_msg_id", None))
            return await self._show_error(
                t(self.lang, "bodies.edit_no_field_selected")
            )

        step = wizard.current_step()
        key = step.key
        cfg = self._get_step_cfg(key)
        max_files = cfg.get("max_files")

        # reject non-files
        if msg.text:
            return await self._show_error("📎 Прикрепите файл, а не текст.")
        if msg.contact:
            return await self._show_error("📎 Здесь принимаются только документы / фото.")

        # extract file
        if msg.document:
            file_item = {
                "file_id": msg.document.file_id,
                "mime": msg.document.mime_type or "",
                "size": msg.document.file_size or 0,
                "name": msg.document.file_name or "Документ",
            }
        elif msg.photo:
            p = msg.photo[-1]
            file_item = {
                "file_id": p.file_id,
                "mime": "image/jpeg",
                "size": p.file_size or 0,
                "name": "Фото",
            }
        else:
            return await self._show_error("📎 Прикрепите документ.")

        files_key = f"edit_files_{key}"
        stored = ctx.user_data.get(files_key)
        if not isinstance(stored, list):
            stored = []
            ctx.user_data[files_key] = stored

        stored.append(file_item)

        # incomplete?
        if max_files and len(stored) < max_files:
            try:
                await msg.delete()
            except SAFE_EX:
                pass

            prev = ctx.user_data.pop("file_progress_msg", None)
            await self._delete_msg_obj(prev)

            progress = await self.msg.chat.send_message(
                f"Файл принят ({len(stored)}/{max_files}). Прикрепите следующий."
            )
            ctx.user_data["file_progress_msg"] = progress.message_id
            return None

        # enough → validate
        prev = ctx.user_data.pop("file_progress_msg", None)
        await self._delete_msg_obj(prev)

        raw = stored
        ctx.user_data[files_key] = None

        valid, canonical, display = await wizard.validate_input(key, raw)
        if not valid:
            return await self._show_error(display)

        wizard.queue.answers[key] = {
            "canonical": canonical,
            "display": display,
        }

        label = resolve_label(self.lang, self.country, key)

        wizard.queue.index = None
        self.context.user_data.pop("edit_intro_shown", None)

        # 🧹 DELETE incomplete-warning if exists or prompts
        await self._delete_msg_obj(self.context.user_data.pop("edit_error_msg", None))
        await self._delete_msg_obj(self.context.user_data.pop("edit_select_msg_id", None))
        await self._delete_msg_obj(self.context.user_data.pop("edit_updated_msg_id", None))
        await self._delete_msg_obj(self.context.user_data.pop("selector_msg_id", None))

        # update + prompt
        await self.update_panel()

        # notify
        await self._notify_field_updated(label)

        return None

    # ============================================================
    # CALLBACKS
    # ============================================================
    async def on_callback(self, data: str):
        wizard = self.engine

        # RETURN → back to review
        if data == CB_SAVE:
            # перевіряємо незаповнені поля
            empty = await self._check_unfilled_fields()

            if empty:
                # не даємо повернутись
                await self._clear_notifications()
                await wipe_last_prompt(self.msg.chat, self.context)

                # локалізований заголовок
                warn = t(self.lang, "bodies.edit_incomplete_warning")

                # будуємо список кнопок
                rows = []
                for key in empty:
                    label = resolve_label(self.lang, self.country, key)
                    step_index = next(i for i, s in enumerate(self.engine.queue.steps) if s.key == key)

                    rows.append([
                        InlineKeyboardButton(
                            f"⚠️ {label}",
                            callback_data=f"{CB_GOTO}{step_index}"
                        )
                    ])

                kb = InlineKeyboardMarkup(rows)

                msg = await self.msg.chat.send_message(warn, reply_markup=kb, parse_mode="HTML")
                self.context.user_data["edit_error_msg"] = msg.message_id
                return None

            # якщо всі поля заповнені → в Review
            await self._clear_notifications()
            await wipe_all_prompts(self.msg.chat, self.context)

            self.context.user_data["panel_mode"] = "review"
            self.reset_snapshot()

            from handlers.application.router_selector import get_router
            return await get_router(self.update, self.context).update_panel()

        # ============================================================
        # CANCEL → вихід у головне меню
        # ============================================================
        if data == CB_CANCEL:
            chat = self.msg.chat
            ud = self.context.user_data

            # Видаляємо ВСІ промпти
            try:
                await wipe_all_prompts(chat, self.context)
            except:
                pass

            # Видаляємо всі повідомлення EditMode
            for key in [
                "edit_intro_msg_id",
                "edit_select_msg_id",
                "edit_updated_msg_id",
                "edit_error_msg",
                "selector_msg_id",
                "file_progress_msg",
                "progress_error_msg",
                "enum_error_msg",
            ]:
                msg_id = ud.pop(key, None)
                if msg_id:
                    try:
                        await chat.delete_message(msg_id)
                    except:
                        pass

            # Видаляємо Панель Edit
            panel_id = ud.pop("panel_id", None)
            if panel_id:
                try:
                    await chat.delete_message(panel_id)
                except:
                    pass

            # Відновлюємо старі відповіді (rollback)
            self.restore_snapshot()
            self.reset_snapshot()

            # Очистити флаг intro
            ud.pop("edit_intro_shown", None)

            # Повертаємо назад у REVIEW
            ud["panel_mode"] = "review"

            from handlers.application.router_selector import get_router
            return await get_router(self.update, self.context).update_panel()

        # choose field
        if data.startswith(CB_GOTO):
            arg = data[len(CB_GOTO):]

            if arg == "menu":
                return await self._show_field_selector()

            try:
                index = int(arg)
            except:
                return None

            sel = self.context.user_data.pop("selector_msg_id", None)
            await self._delete_msg_obj(sel)

            if 0 <= index < len(wizard.queue.steps):
                wizard.queue.index = index
                label = resolve_label(self.lang, self.country, wizard.queue.steps[index].key)

                # notify selected
                await self._notify_field_selected(label)

                # update + prompt
                await self.update_panel()
            return None

        return None

    # ============================================================
    # FIELD SELECTOR POPUP
    # ============================================================
    async def _show_field_selector(self):
        steps = self.engine.queue.steps
        rows = []
        for i, step in enumerate(steps):
            label = resolve_label(self.lang, self.country, step.key)
            rows.append([
                InlineKeyboardButton(
                    f"{i+1}. {label}",
                    callback_data=f"{CB_GOTO}{i}"
                )
            ])

        kb = InlineKeyboardMarkup(rows)
        popup = await self.msg.chat.send_message(
            t(self.lang, "titles.select_field_title"),
            reply_markup=kb,
            parse_mode="HTML",
        )

        self.context.user_data["selector_msg_id"] = popup.message_id

    # ============================================================
    # ERROR
    # ============================================================
    async def _show_error(self, text: str):
        if self._is_user_message(self.msg):
            try:
                await self.msg.delete()
            except SAFE_EX:
                pass

        await self._cleanup_temp()
        await wipe_last_prompt(self.msg.chat, self.context)

        err = await self.msg.chat.send_message(text)
        self.context.user_data["edit_error_msg"] = err
        return

    # ============================================================
    # NOTIFICATIONS
    # ============================================================
    async def _notify_field_selected(self, label: str):
        await self._clear_notifications()
        msg = await self.msg.chat.send_message(
            t(self.lang, "bodies.field_selected", label=label)
        )
        self.context.user_data["edit_select_msg_id"] = msg.message_id

    async def _notify_field_updated(self, label: str):
        await self._clear_notifications()
        msg = await self.msg.chat.send_message(
            t(self.lang, "bodies.field_updated", label=label)
        )
        self.context.user_data["edit_updated_msg_id"] = msg.message_id

    async def _check_unfilled_fields(self):
        wizard = self.engine
        steps = wizard.queue.steps
        answers = wizard.queue.answers

        empty = []
        for s in steps:
            key = s.key
            entry = answers.get(key)
            display = entry.get("display") if entry else None
            if not display:
                empty.append(key)

        return empty

__all__ = ["EditRouter"]
