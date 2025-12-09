from __future__ import annotations

from telegram.ext import ContextTypes

from keyboards.panels import kb_edit_panel
from ui.panel.base import BasePanel
from ui.panel.utils import resolve_text, resolve_label, short
from core.logger import log   # 🔥 Логер


class EditPanel(BasePanel):

    def __init__(self, context: ContextTypes.DEFAULT_TYPE, wizard):
        super().__init__(context)
        self.wizard = wizard
        self.lang = context.user_data.get("lang") or "en"
        self.country = context.user_data.get("country") or "US"

    # ------------------------------------------------------
    # HTML (аналог progress-panel, но для Edit)
    # ------------------------------------------------------
    def render(self) -> str:
        steps = self.wizard.queue.steps
        draft = self.context.user_data.get("edit_draft")
        answers = draft if draft is not None else self.wizard.queue.answers
        idx = self.wizard.queue.index

        log.info("[EDIT PANEL] render() called")
        log.info(f"[EDIT PANEL] steps: {[s.key for s in steps]}")
        log.info(f"[EDIT PANEL] active index: {idx}")
        log.info(f"[EDIT PANEL] using answers: {answers}")

        title = resolve_text(self.lang, "edit_title")
        no_data = resolve_text(self.lang, "no_data")

        blocks = [f"<b>✏️ {title}</b>\n"]

        for i, step in enumerate(steps):
            key = step.key
            label = resolve_label(self.lang, self.country, key)
            entry = answers.get(key)
            display = entry.get("display") if entry else None

            log.info(f"[EDIT PANEL] Step {i} key='{key}', display='{display}'")

            if not display:
                display = f"<i>{no_data}</i>"
            else:
                display = f"<code>{short(display)}</code>"

            if i == idx:
                blocks.append(f"👉 <b>{label}</b>: {display}")
            else:
                blocks.append(f"{i+1}. <b>{label}</b>: {display}")

        html = "\n".join(blocks).strip()
        log.info(f"[EDIT PANEL] FINAL HTML:\n{html}")

        return html

    # ------------------------------------------------------
    # UPSERT — копія ProgressPanel.upsert
    # ------------------------------------------------------
    async def upsert(self, msg):
        bot = self.context.bot

        log.info("[EDIT PANEL] upsert() called")
        log.info(f"[EDIT PANEL] msg.chat_id={msg.chat_id}")
        log.info(f"[EDIT PANEL] current panel_id={self.context.user_data.get('panel_id')}")

        html = self.render()
        kb = kb_edit_panel(self.lang)

        panel_id = self.context.user_data.get("panel_id")

        # ---------- Пытаемся обновить существующую панель ----------
        if panel_id:
            log.info(f"[EDIT PANEL] Trying to edit existing panel_id={panel_id}")
            try:
                await bot.edit_message_text(
                    chat_id=msg.chat_id,
                    message_id=panel_id,
                    text=html,
                    parse_mode="HTML",
                    reply_markup=kb,
                )
                log.info("[EDIT PANEL] edit_message_text SUCCESS")
                self._track(panel_id)
                await self._cleanup(msg.chat, keep={panel_id})
                return
            except Exception as e:
                log.error(f"[EDIT PANEL] edit_message_text FAILED: {e}")
                try:
                    await msg.chat.delete_message(panel_id)
                    log.info(f"[EDIT PANEL] Deleted broken panel_id={panel_id}")
                except Exception as e2:
                    log.error(f"[EDIT PANEL] Failed to delete broken panel: {e2}")

        # ---------- Создаём новую панель ----------
        log.info("[EDIT PANEL] Sending NEW panel message")

        sent = await bot.send_message(
            chat_id=msg.chat_id,
            text=html,
            parse_mode="HTML",
            reply_markup=kb,
        )

        log.info(f"[EDIT PANEL] NEW panel created message_id={sent.message_id}")

        self.context.user_data["panel_id"] = sent.message_id
        self._track(sent.message_id)

        await self._cleanup(msg.chat, keep={sent.message_id})
        log.info("[EDIT PANEL] Cleanup done. Panel updated.")


__all__ = ["EditPanel"]
