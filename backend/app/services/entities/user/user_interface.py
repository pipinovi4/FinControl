from backend.app.models import User
from backend.app.permissions import PermissionRole


class UserInterfaceService:
    """
    Interface class for accessing and interpreting user-related state and properties.

    This class provides helper methods that abstract the interpretation of a User instance,
    such as role-checks, soft-delete status, and user identity resolution.
    """

    def __init__(self, user: User) -> None:
        """
        Initialize the interface with a User instance.

        :param user: The User model instance.
        """
        self.user = user

    def is_admin(self) -> bool:
        """
        Check if the user has the 'admin' role.

        :return: True if user is admin.
        """
        return self.user.role == PermissionRole.ADMIN

    def is_worker(self) -> bool:
        """
        Check if the user has the 'worker' role.

        :return: True if user is worker.
        """
        return self.user.role == PermissionRole.WORKER

    def is_broker(self) -> bool:
        """
        Check if the user has the 'broker' role.

        :return: True if user is broker.
        """
        return self.user.role == PermissionRole.BROKER

    def is_client(self) -> bool:
        """
        Check if the user has the 'client' role.

        :return: True if user is client.
        """
        return self.user.role == PermissionRole.CLIENT

    def is_internal(self) -> bool:
        """
        Check if the user is considered internal staff (admin or worker).

        :return: True if user is admin or worker.
        """
        return self.user.role in {PermissionRole.ADMIN, PermissionRole.WORKER}

    def is_deleted(self) -> bool:
        """
        Check if the user is soft-deleted.

        :return: True if the user is marked as deleted.
        """
        return self.user.is_deleted

    def get_display_name(self) -> str:
        """
        Return a user-friendly display name.

        Prefers the Telegram username, falls back to a partial UUID-based identifier.

        :return: The display name string.
        """
        if self.user.telegram_username:
            return f"@{self.user.telegram_username}"
        return f"User#{str(self.user.id)[:6]}"
