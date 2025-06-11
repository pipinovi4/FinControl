from backend.app.models import Worker
from backend.app.services.entities.user_interface import UserInterfaceService


class WorkerInterfaceService(UserInterfaceService):
    """
    Interface class for accessing and interpreting worker-related state and properties.

    Extends UserInterfaceService, adding worker-specific logic based on the Worker model fields.
    """

    def __init__(self, worker: Worker) -> None:
        """
        Initialize the interface with a Worker instance.

        :param worker: The Worker model instance.
        """
        super().__init__(worker)
        self.worker = worker

    def has_clients(self) -> bool:
        """
        Check if the worker has any assigned clients.

        :return: True if the worker has at least one client, False otherwise.
        """
        return bool(self.worker.clients)

    def is_active(self) -> bool:
        """
        Check if the worker is active (exists and is not marked as deleted).

        :return: True if the worker is active, False if deleted.
        """
        return not self.worker.is_deleted

    def get_username(self) -> str:
        """
        Retrieve the worker's username.

        :return: The username (e.g., "john.smith").
        """
        return self.worker.username

    def get_telegram_username(self) -> str:
        """
        Retrieve the worker's Telegram username if available.

        :return: The Telegram username as a string, or an empty string if not set.
        """
        return self.worker.telegram_username or ""

    def get_clients_count(self) -> int:
        """
        Retrieve the number of clients assigned to the worker.

        :return: The count of clients.
        """
        return len(self.worker.clients) if self.worker.clients else 0

    def get_clients_display(self) -> list[str]:
        """
        Retrieve a list of display names for all clients assigned to the worker.

        For each client, returns its full name if available, or a fallback like "Client#<id>".

        :return: List of display names for clients.
        """
        return [
            client.full_name if client.full_name else f"Client#{str(client.id)[:6]}"
            for client in self.worker.clients
        ]

    def get_last_login(self) -> str:
        """
        Retrieve the worker's last login timestamp as a string.

        This relies on the TimeStampAuthMixin providing a 'last_login' attribute.

        :return: The last login timestamp as a string or "N/A" if not available.
        """
        return str(self.worker.last_login) if hasattr(self.worker, 'last_login') and self.worker.last_login else "N/A"

    def get_dynamic_link(self) -> str:
        """
        Retrieve a one-time dynamic login link for the worker.

        This method assumes the DynamicLinkAuthMixin provides a `generate_dynamic_link` method.

        :return: The dynamic link as a string, or an empty string if not available.
        """
        if hasattr(self.worker, 'generate_dynamic_link'):
            return self.worker.generate_dynamic_link()
        return ""

    def __str__(self) -> str:
        """
        Developer-friendly string representation of the worker.

        :return: A string representing the worker.
        """
        return f"Worker(username={self.worker.username}, id={self.worker.id})"