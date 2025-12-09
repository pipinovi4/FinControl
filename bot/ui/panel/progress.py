# ui/panel/progress.py
from __future__ import annotations

from telegram.ext import ContextTypes

from keyboards.panels import kb_progress_panel
from ui.panel.base import BasePanel
from ui.panel.utils import resolve_text, resolve_label, short


class ProgressPanel(BasePanel):

    def __init__(self, context: ContextTypes.DEFAULT_TYPE, wizard):
        super().__init__(context)
        self.wizard = wizard
        self.lang = context.user_data.get("lang") or "en"
        self.country = context.user_data.get("country") or "US"

    # ------------------------------------------------------------------
    # HTML generator (old function -> now method)
    # ------------------------------------------------------------------
    def render(self) -> str:
        steps = self.wizard.queue.steps
        answers = self.wizard.queue.answers
        idx = self.wizard.queue.index

        title = resolve_text(self.lang, "progress_title")
        done_h = resolve_text(self.lang, "done")
        current_h = resolve_text(self.lang, "current")
        bar_h = resolve_text(self.lang, "progress_bar")
        step_word = resolve_text(self.lang, "step")
        of_word = resolve_text(self.lang, "of")
        no_data = resolve_text(self.lang, "no_data")

        total = len(steps)
        step_num = idx + 1
        current_step = steps[idx]

        label = resolve_label(self.lang, self.country, current_step.key)

        FULL = "🟩"
        EMPTY = "🟦"
        BAR_LEN = 10

        ratio = step_num / total if total else 0
        filled = max(1, min(BAR_LEN, int(round(ratio * BAR_LEN))))
        bar = FULL * filled + EMPTY * (BAR_LEN - filled)

        rows = []
        for i, s in enumerate(steps):
            key = s.key
            l = resolve_label(self.lang, self.country, key)
            bullet = "➡️" if i == idx else "•"

            entry = answers.get(key)
            disp = entry.get("display") if entry else None

            if disp:
                rows.append(f"{bullet} <b>{l}</b>: <code>{short(disp)}</code>")
            elif i == idx:
                rows.append(f"{bullet} <b>{l}</b>: <i>{no_data}</i>")
            else:
                rows.append(f"{bullet} <b>{l}</b>")

        done_block = "\n".join(rows)

        return f"""
<b>📋 {title}</b>

<b>{bar_h}:</b>
{bar}
<b>{step_word} {step_num} {of_word} {total}</b>

<b>{current_h}:</b>
• <b>{label}</b>

<b>{done_h}:</b>
{done_block}
""".strip()

    # ------------------------------------------------------------------
    # Upsert (old upsert_progress_panel)
    # ------------------------------------------------------------------
    async def upsert(self, msg):
        html = self.render()

        kb = kb_progress_panel(self.lang)

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
    "ProgressPanel",
]