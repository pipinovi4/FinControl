from backend.app.models import User
from backend.app.permissions import PermissionRole


class UserInterfaceService:
    """
    Interface class for interpreting user state and roles in a readable and reusable way.

    This class wraps around a User model instance and provides a high-level API
    for evaluating role-based permissions, deletion status, and display identity.

    Primary Use Cases:
    - Authorization logic based on user roles (admin, broker, etc.).
    - Display utilities for rendering usernames.
    - Logic branching depending on whether user is soft-deleted or internal staff.

    Methods:
        - is_admin(): True if user has admin role.
        - is_worker(): True if user has worker role.
        - is_broker(): True if user has broker role.
        - is_client(): True if user has client role.
        - is_internal(): True if user is staff (admin or worker).
        - is_deleted(): True if user is soft-deleted.
        - get_display_name(): Returns '@username' or fallback UUID-like ID.
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
