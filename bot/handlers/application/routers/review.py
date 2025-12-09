from __future__ import annotations

from handlers.application.routers.base import BaseRouter
from ui.panel.cleaner import CleanerPanel
from constants.callbacks import CB_EDIT, CB_CANCEL, CB_SUBMIT

class ReviewRouter(BaseRouter):
    """
    Router for REVIEW MODE:
    - Shows static summary of all fields
    - Handles: Edit / Cancel / Submit
    """

    async def update_panel(self):
        from ui.panel.review import ReviewPanel
        panel = ReviewPanel(self.context, self.engine)
        await panel.upsert(self.msg)

    async def on_text(self):
        return None

    async def on_file(self):
        return None

    # ---------------------------------------------------------
    # UNIVERSAL CLEANUP BEFORE EXIT
    # ---------------------------------------------------------
    async def _cleanup_wizard(self):

        chat = self.msg.chat

        # 1) remove all panel messages
        try:
            cleaner = CleanerPanel(self.context)
            await cleaner.wipe_all(chat)
        except:
            pass

        # 2) remove last prompt
        pid = self.context.user_data.pop("last_prompt_msg_id", None)
        if isinstance(pid, int):
            try:
                await chat.delete_message(pid)
            except:
                pass

        # 4) remove error messages
        err = self.context.user_data.pop("edit_error_msg", None)
        if hasattr(err, "delete"):
            try:
                await err.delete()
            except:
                pass

    # ---------------------------------------------------------
    # CALLBACK HANDLING
    # ---------------------------------------------------------
    async def on_callback(self, data: str):

        # -------- EDIT MODE --------
        if data == CB_EDIT:
            self.context.user_data["panel_mode"] = "edit"

            # Зберігаємо відповіді щоб якщо юзер захоче скасувати зміни ми могли повернути початковий queue
            self.take_snapshot()

            from handlers.application.router_selector import get_router
            router = get_router(self.update, self.context)

            return await router.update_panel()

        # -------- CANCEL → MY APPLICATIONS --------
        if data == CB_CANCEL:
            lang = self.context.user_data.get("lang", "en")

            await self._cleanup_wizard()

            from keyboards import kb_main_menu
            from locales import translate as t

            return await self.msg.chat.send_message(
                t(lang, "titles.menu_title"),
                reply_markup=kb_main_menu(lang),
                parse_mode="HTML"
            )

        # -------- SUBMIT → MY APPLICATIONS --------
        if data == CB_SUBMIT:
            lang = self.context.user_data.get("lang", "en")

            print("ANSWERS: ", self.engine.queue.answers)

            # TODO: send application to backend
            await self._cleanup_wizard()

            from keyboards import kb_applications
            from locales import translate as t

            return await self.msg.chat.send_message(
                t(lang, "bodies.my_apps_stub")
                + "\n\n"
                + t(lang, "titles.menu_title"),
                reply_markup=kb_applications(lang),
                parse_mode="HTML"
            )

        return None


__all__ = ["ReviewRouter"]
