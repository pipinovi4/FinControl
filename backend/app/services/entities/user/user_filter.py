from sqlalchemy import select
from sqlalchemy.sql import Select
from backend.app.models import User
from backend.app.permissions import PermissionRole


class UserFilterService:
    """
    Async-compatible query builder for filtering User records.

    This service enables dynamic, chainable construction of SQLAlchemy Select queries
    targeting the User model. Designed to be used with async sessions for efficient,
    non-blocking database operations.

    Methods:
        - by_role(role): Filter users by their role (e.g., ADMIN, BROKER).
        - apply(): Finalize and retrieve the built query.
    """
    def __init__(self):
        # Start with a basic select statement for the User model
        self.query: Select = select(User)

    def by_role(self, role: PermissionRole):
        """
        Add a filter clause to restrict users by role.

        :param role: The PermissionRole enum value to filter by.
        :return: Self for fluent chaining.
        """
        self.query = self.query.where(User.role == role)
        return self

    def apply(self) -> Select:
        """
        Return the final SQLAlchemy Select query to be executed.

        :return: The fully constructed Select object.
        """
        return self.query
