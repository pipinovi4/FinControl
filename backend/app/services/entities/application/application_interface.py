# backend/app/services/entities/application/application_interface.py
from app.models.entities.application import Application


class ApplicationInterfaceService:
    """Domain-level helper (high-level logic)."""

    def __init__(self, app: Application) -> None:
        self.app = app

    def has_worker(self) -> bool:
        return self.app.worker_id is not None

    def has_broker(self) -> bool:
        return self.app.broker_id is not None

    def get_basic_info(self):
        """Extract primary fields from canonical data."""
        d = self.app.data
        return {
            "full_name": d.get("full_name"),
            "phone_number": d.get("phone_number"),
            "email": d.get("email"),
        }
