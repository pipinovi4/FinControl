# ui/panel/base.py
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Set, List
from telegram.ext import ContextTypes
from telegram.error import BadRequest, Forbidden, TelegramError


class BasePanel(ABC):
    """
    Abstract panel class. Provides:
    - tracking panel message IDs
    - cleaning old panel messages
    - unified interface: render() + upsert()
    """

    def __init__(self, context: ContextTypes.DEFAULT_TYPE):
        self.context = context

    # ---------------------------------------------------------------------
    # Message tracking helpers
    # ---------------------------------------------------------------------
    def _track(self, message_id: int) -> None:
        ids: List[int] = self.context.user_data.get("panel_ids", [])
        if message_id not in ids:
            ids.append(message_id)
        self.context.user_data["panel_ids"] = ids

    async def _cleanup(self, chat, keep: Set[int]):
        ids: List[int] = self.context.user_data.get("panel_ids", [])
        remain = []

        for mid in ids:
            if mid in keep:
                remain.append(mid)
                continue

            try:
                await chat.delete_message(mid)
            except (BadRequest, Forbidden):
                pass
            except TelegramError:
                pass

        self.context.user_data["panel_ids"] = remain

    async def wipe_all(self, chat):
        ids: List[int] = self.context.user_data.get("panel_ids", [])
        for mid in ids:
            try:
                await chat.delete_message(mid)
            except Exception:
                pass

        self.context.user_data.pop("panel_ids", None)

    # ---------------------------------------------------------------------
    # Abstract methods
    # ---------------------------------------------------------------------
    @abstractmethod
    def render(self) -> str:
        """Returns HTML of the panel"""
        pass

    @abstractmethod
    async def upsert(self, msg):
        """Updates or creates panel message"""
        pass
