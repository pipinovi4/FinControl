from ui.panel.base import BasePanel

class CleanerPanel(BasePanel):
    def render(self):
        return ""

    async def upsert(self, msg):
        return None

__all__ = ["CleanerPanel"]