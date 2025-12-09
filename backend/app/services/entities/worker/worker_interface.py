from app.models import Worker
from app.services.entities.user import UserInterfaceService


class WorkerInterfaceService(UserInterfaceService):
    """
    High-level interface for Worker entity in the APPLICATION-based architecture.

    Provides helper methods for UI, API responses, templates:
        - has_applications()
        - get_applications_count()
        - get_applications_display()
        - is_active()
        - get_username()
        - get_last_login()
        - get_dynamic_link()
    """

    def __init__(self, worker: Worker):
        super().__init__(worker)
        self.worker: Worker = worker

    # ---------------------------------------------------------
    # APPLICATIONS
    # ---------------------------------------------------------
    def has_applications(self) -> bool:
        """Return True if worker has at least one application."""
        return bool(self.worker.applications)

    def get_applications_count(self) -> int:
        """Return number of assigned applications."""
        return len(self.worker.applications or [])

    def get_applications_display(self) -> list[str]:
        """
        Return display names for applications.
        Uses Application.data["full_name"] if available,
        otherwise fallback like Application#ABC123.
        """
        result = []
        for app in self.worker.applications:
            full_name = app.data.get("full_name") if app.data else None
            if full_name:
                result.append(full_name)
            else:
                result.append(f"Application#{str(app.id)[:6]}")
        return result

    # ---------------------------------------------------------
    # BASIC FIELDS
    # ---------------------------------------------------------
    def get_username(self) -> str:
        """Return internal worker username."""
        return self.worker.username

    def is_active(self) -> bool:
        """True if worker is NOT soft-deleted."""
        return not self.worker.is_deleted

    # ---------------------------------------------------------
    # AUTH / META
    # ---------------------------------------------------------
    def get_last_login(self) -> str:
        """
        Return last login timestamp as string.
        If not available — return 'N/A'.
        """
        last_login = getattr(self.worker, "last_login", None)
        return str(last_login) if last_login else "N/A"

    def get_dynamic_link(self) -> str:
        """
        Return one-time dynamic login link if supported.
        """
        if hasattr(self.worker, "generate_dynamic_link"):
            return self.worker.generate_dynamic_link()
        return ""

    # ---------------------------------------------------------
    # STR
    # ---------------------------------------------------------
    def __str__(self) -> str:
        return f"Worker(username={self.worker.username}, id={self.worker.id})"
