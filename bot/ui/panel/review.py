from __future__ import annotations

from telegram.ext import ContextTypes

from ui.panel.base import BasePanel
from ui.panel.utils import resolve_text, resolve_label, short
from keyboards.panels import kb_review_panel


class ReviewPanel(BasePanel):

    def __init__(self, context: ContextTypes.DEFAULT_TYPE, wizard):
        super().__init__(context)
        self.wizard = wizard
        self.lang = context.user_data.get("lang") or "en"
        self.country = context.user_data.get("country") or "US"

    # ------------------------------------------------------
    # Render full static preview of ALL fields
    # ------------------------------------------------------
    def render(self) -> str:
        steps = self.wizard.queue.steps
        answers = self.wizard.queue.answers

        title = resolve_text(self.lang, "review_title")
        no_data = resolve_text(self.lang, "no_data")

        rows = []

        for s in steps:
            key = s.key
            label = resolve_label(self.lang, self.country, key)

            entry = answers.get(key)
            disp = entry.get("display") if entry else None

            if disp:
                rows.append(f"• <b>{label}</b>: <code>{short(disp)}</code>")
            else:
                rows.append(f"• <b>{label}</b>: <i>{no_data}</i>")

        content = "\n".join(rows)

        return f"""
<b>📄 {title}</b>

{content}
""".strip()

    # ------------------------------------------------------
    # Upsert preview panel (edit/cancel/submit)
    # ------------------------------------------------------
    async def upsert(self, msg):

        html = self.render()
        kb = kb_review_panel(self.lang)

        panel_id = self.context.user_data.get("panel_id")

        if panel_id:
            try:
                await msg.bot.edit_message_text(
                    chat_id=msg.chat_id,
                    message_id=panel_id,
                    text=html,
                    parse_mode="HTML",
                    reply_markup=kb,
                )
                self._track(panel_id)
                await self._cleanup(msg.chat, keep={panel_id})
                return
            except Exception:
                try:
                    await msg.chat.delete_message(panel_id)
                except Exception:
                    pass

        sent = await msg.reply_text(html, parse_mode="HTML", reply_markup=kb)
        self.context.user_data["panel_id"] = sent.message_id
        self._track(sent.message_id)
        await self._cleanup(msg.chat, keep={sent.message_id})

__all__ = [
    "ReviewPanel"
]