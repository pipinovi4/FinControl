# handlers/application/routers/progress_router.py
from __future__ import annotations

from constants import CB_BACK, CB_NEXT, CB_CANCEL
from handlers.application.prompt import wipe_all_prompts
from handlers.application.routers.base import BaseRouter
from handlers.application.utils import resolve_canonical
from locales import L10N


class ProgressRouter(BaseRouter):
    """
    Handles ONLY normal step filling mode.
    """

    async def update_panel(self):
        from ui.panel.progress import ProgressPanel

        panel = ProgressPanel(self.context, self.engine)
        await panel.upsert(self.msg)

    # ============================================================
    # FILE FLOW
    # ============================================================
    async def on_file(self):
        msg = self.msg
        context = self.context
        engine = self.engine
        lang = self.lang
        country = self.country

        step = engine.current_step()
        step_key = step.key

        locale = L10N.get(lang, {})
        step_cfg = (
            locale.get("steps_by_country", {}).get(country, {}).get(step_key, {})
            or locale.get("steps", {}).get(step_key, {})
        )

        max_files = step_cfg.get("max_files")
        # expected_type = step_cfg.get("expected_type", "text")

        # Reject wrong input
        if msg.text:
            return await self.error(step_key, "📎 Прикрепите файл, а не текст.")

        if msg.contact:
            return await self.error(step_key, "📎 Этот шаг принимает только документы / фото.")

        # Extract file
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
            return await self.error(step_key, "📎 Прикрепите документ.")

        # Store
        files_key = f"files_{step_key}"

        stored = context.user_data.get(files_key)

        if not isinstance(stored, list):
            stored = []
            context.user_data[files_key] = stored

        stored.append(file_item)

        # Not enough yet?
        if max_files and len(stored) < max_files:
            await self._safe_delete(msg)
            await self._set_file_progress(
                f"Файл принят ({len(stored)}/{max_files}). Прикрепите следующий."
            )
            return None

        # Enough files → validate
        await self._clear_file_progress()
        raw = stored
        context.user_data[files_key] = None

        valid, canonical, display = await engine.validate_input(step_key, raw)
        if not valid:
            return await self.error(step_key, display)

        ok, _ = engine.process_answer(step_key, canonical, display)
        if not ok:
            return await self.error(step_key, "Ошибка обработки ответа.")

        success, next_step, _ = engine.next_step()
        return await self.success(next_step)

    # ============================================================
    # TEXT FLOW
    # ============================================================
    async def on_text(self):
        msg = self.msg
        context = self.context
        engine = self.engine

        step = engine.current_step()
        step_key = step.key

        lang = self.lang
        country = self.country

        locale = L10N.get(lang, {})
        step_cfg = (
            locale.get("steps_by_country", {}).get(country, {}).get(step_key, {})
            or locale.get("steps", {}).get(step_key, {})
        )

        # Extract string
        if msg.contact and msg.contact.phone_number:
            raw = msg.contact.phone_number.strip()
        elif msg.text:
            raw = msg.text.strip()
        else:
            raw = ""

        value = resolve_canonical(step_cfg, raw)
        raw_for_validation = value["canonical"]

        # Validate
        valid, canonical, display = await engine.validate_input(step_key, raw_for_validation)
        if not valid:
            return await self.error(step_key, display)

        if canonical:
            value["canonical"] = canonical
        if display:
            value["display"] = display

        ok, _ = engine.process_answer(step_key, value["canonical"], value["display"])
        if not ok:
            return await self.error(step_key, "Ошибка обработки ответа.")

        success, next_step, _ = engine.next_step()
        return await self.success(next_step)

    # ============================================================
    # CALLBACKS (next/back/cancel)
    # ============================================================
    # ============================================================
    # CALLBACKS (next/back/cancel)
    # ============================================================
    async def on_callback(self, data: str):
        engine = self.engine
        msg = self.msg
        lang = self.lang

        # -----------------------------
        # CANCEL → вихід у головне меню
        # -----------------------------
        if data == CB_CANCEL:
            chat = msg.chat
            ud = self.context.user_data

            # 1) Видаляємо ВСІ промпти
            try:
                await wipe_all_prompts(chat, self.context)
            except:
                pass

            # 2) Видаляємо file-progress
            try:
                await self._clear_file_progress()
            except:
                pass

            # 3) Видаляємо user-сообщення
            try:
                if self.update.message:
                    await self.update.message.delete()
            except:
                pass

            # 4) Видаляємо панель (panel_id)
            panel_id = ud.pop("panel_id", None)
            if panel_id:
                try:
                    await chat.delete_message(panel_id)
                except:
                    pass

            # 5) Видаляємо всі Edit/Review повідомлення
            for key in [
                "edit_intro_msg_id",
                "edit_select_msg_id",
                "edit_updated_msg_id",
                "selector_msg_id",
                "edit_error_msg",
                "progress_error_msg",
                "enum_error_msg",
                "file_progress_msg",
            ]:
                msg_id = ud.pop(key, None)
                if msg_id:
                    try:
                        await chat.delete_message(msg_id)
                    except:
                        pass

            # 6) Скидаємо wizard та всі прапори панелей
            ud.pop("wizard", None)
            ud.pop("panel_mode", None)
            ud.pop("edit_intro_shown", None)

            # 7) Додаткове очищення user_data (всі files_*)
            keys_to_delete = [k for k in ud.keys() if k.startswith("files_") or k.startswith("edit_files_")]
            for k in keys_to_delete:
                ud.pop(k, None)

            # 8) Повертаємо на головне меню
            from keyboards import kb_main_menu
            from locales import translate as t

            return await chat.send_message(
                t(lang, "titles.menu_title"),
                reply_markup=kb_main_menu(lang),
                parse_mode="HTML"
            )

        # -----------------------------
        # NEXT → наступний крок
        # -----------------------------
        if data == CB_NEXT:
            self.context.user_data["panel_mode"] = "progress"
            success, next_step, _ = engine.next_step()
            if not success:
                return await self.error(None, "Ошибка навигации.")
            return await self.success(next_step)

        # -----------------------------
        # BACK → попередній крок
        # -----------------------------
        if data == CB_BACK:
            self.context.user_data["panel_mode"] = "progress"
            success, prev_step, _ = engine.prev_step()
            if not success:
                return await self.error(None, "Вы на первом шаге.")
            return await self.success(prev_step)

        return None


__all__ = [
    "ProgressRouter",
]