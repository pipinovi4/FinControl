# handlers/application/routers/base.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional
import copy

from telegram import Update, Message
from telegram.ext import ContextTypes
from telegram.error import BadRequest, Forbidden, TimedOut, RetryAfter, NetworkError

from handlers.application.prompt import send_step_prompt, wipe_last_prompt
from core.logger import log


SAFE_EXCEPTIONS = (BadRequest, Forbidden, TimedOut, RetryAfter, NetworkError)


class BaseRouter(ABC):
    """
    Abstract base router for all 3 modes:
    - progress
    - edit
    - review

    Contains shared logic:
    ✔ delete helpers
    ✔ error handling
    ✔ success handling
    ✔ finishing wizard
    ✔ file-progress msg handling
    ✔ prompt helpers
    """

    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.update = update
        self.context = context
        self.msg: Message = update.message or update.callback_query.message

        self.engine = context.user_data.get("wizard")
        self.lang = self.engine.lang if self.engine else "en"
        self.country = self.engine.country if self.engine else "US"

    # ============================================================
    # HELPERS
    # ============================================================
    @staticmethod
    async def _safe_delete(msg: Optional[Message]):
        """Safely delete any message."""
        if not msg:
            return
        try:
            await msg.delete()
        except SAFE_EXCEPTIONS:
            pass
        except Exception:
            pass

    async def _clear_file_progress(self):
        """Remove '1/3 file uploaded' message."""
        pending = self.context.user_data.get("file_progress_msg")
        if pending:
            await self._safe_delete(pending)
            self.context.user_data["file_progress_msg"] = None

    async def _set_file_progress(self, text: str):
        """Update file upload progress message."""
        await self._clear_file_progress()
        new_msg = await self.msg.chat.send_message(text)
        self.context.user_data["file_progress_msg"] = new_msg

    # ============================================================
    # ERROR HANDLING
    # ============================================================
    async def error(self, step_key: str, display_text: str):
        """
        Unified error handler for ALL routers.
        Shows message → deletes old → resends prompt.
        """
        log.debug(f"[Router] ERROR on step '{step_key}': {display_text}")

        # remove user message
        await self._safe_delete(self.msg)

        # delete previous error
        prev = self.context.user_data.get("last_error_msg")
        if prev:
            await self._safe_delete(prev)

        # show new error
        err = await self.msg.chat.send_message(display_text)
        self.context.user_data["last_error_msg"] = err

        # clear pending file progress
        await self._clear_file_progress()

        # restore step prompt
        await wipe_last_prompt(self.msg.chat, self.context)
        await send_step_prompt(self.msg, self.context, self.lang, self.country, step_key)

        return None

    # ============================================================
    # SUCCESS HANDLING
    # ============================================================
    async def success(self, next_step):
        """Unified success logic after valid answer is processed."""
        await self._clear_file_progress()
        if self.update.message:
            await self._safe_delete(self.update.message)
        await wipe_last_prompt(self.msg.chat, self.context)

        # Wizard finished?
        if self.engine.is_finished():
            from handlers.application.finish import _finish_wizard  # <── РІШЕННЯ
            log.info("[Router] Wizard finished 🎉")
            await _finish_wizard(self.update, self.context)
            return None

        # if subclass wants → update panel
        await self.update_panel()

        # send next prompt
        if next_step:
            await send_step_prompt(self.msg, self.context,
                                   self.lang, self.country, next_step.key)

        return None

    # ============================================================
    # PANEL HANDLING FOR SUBCLASSES
    # ============================================================
    async def update_panel(self):
        """Routers override this to re-render their panel (Progress/Edit/Review)."""
        pass

    def take_snapshot(self):
        """Deep-clone SmartQueue to allow rollback during Edit."""
        if not self.engine:
            return

        q = self.engine.queue
        snapshot = {
            "steps": copy.deepcopy(q.steps),
            "index": q.index,
            "answers": copy.deepcopy(q.answers),
            "_inserted_by_parent": copy.deepcopy(q._inserted_by_parent),
        }

        self.context.user_data["wizard_snapshot"] = snapshot
        log.debug("[Router] Snapshot saved")

    def restore_snapshot(self):
        """Restore SmartQueue state from snapshot."""
        snapshot = self.context.user_data.get("wizard_snapshot")
        if not snapshot or not self.engine:
            log.warning("[Router] No snapshot to restore")
            return

        q = self.engine.queue
        q.steps = copy.deepcopy(snapshot["steps"])
        q.index = snapshot["index"]
        q.answers = copy.deepcopy(snapshot["answers"])
        q._inserted_by_parent = copy.deepcopy(snapshot["_inserted_by_parent"])

        log.debug("[Router] Snapshot restored")

    def reset_snapshot(self):
        """Erase saved snapshot after commit."""
        if "wizard_snapshot" in self.context.user_data:
            del self.context.user_data["wizard_snapshot"]
            log.debug("[Router] Snapshot cleared")


    # ============================================================
    # ABSTRACT API (each router implements its own logic)
    # ============================================================
    @abstractmethod
    async def on_text(self):
        pass

    @abstractmethod
    async def on_file(self):
        pass

    @abstractmethod
    async def on_callback(self, data: str):
        pass
