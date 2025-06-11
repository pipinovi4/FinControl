from typing import Type, TypeVar

from backend.app.models import User
from backend.app.permissions import PermissionRole
from backend.app.schemas import SchemaBase

T = TypeVar("T", bound=SchemaBase)


class UserUtilService:
    """
    Utility functions for working with user-related data.
    All methods are static and operate on raw inputs or lists of users.
    """

    @staticmethod
    def get_display_name(user: User) -> str:
        """
        Return a display-friendly name for a user.

        If the user has a Telegram username, return it as '@username'.
        Otherwise, return a shortened version of their UUID (e.g., 'User#abc123').

        :param user: A User instance.
        :return: Display name string.
        """
        if user.telegram_username:
            return f"@{user.telegram_username}"
        return f"User#{str(user.id)[:6]}"

    @staticmethod
    def filter_by_role(users: list[User], role: PermissionRole) -> list[User]:
        """
        Filter a list of User instances by a specific role.

        :param users: List of User objects to filter.
        :param role: Role to match against (e.g., PermissionRole.ADMIN).
        :return: Filtered list of users matching the given role.
        """
        return [user for user in users if user.role == role]

    @staticmethod
    def to_schema(users: list[User], schema: Type[T]) -> list[T]:
        """
        Convert a list of User ORM instances to a list of Pydantic schemas.

        :param users: List of User instances (SQLAlchemy models).
        :param schema: A Pydantic schema class that supports `model_validate`.
        :return: List of schema instances representing the users.

        :raises TypeError: If the provided schema does not support model_validate.
        """
        if not hasattr(schema, 'model_validate'):
            raise TypeError("Schema class must support model_validate()")

        return [schema.model_validate(user) for user in users]

    @staticmethod
    def to_schema_one(user: User, schema: Type[T]) -> T:
        """
        Convert a single User ORM instance to a Pydantic schema instance.

        :param user: A single User instance (SQLAlchemy model).
        :param schema: A Pydantic schema class that supports `model_validate`.
        :return: A schema instance representing the user.

        :raises TypeError: If the provided schema does not support model_validate.
        """
        if not hasattr(schema, 'model_validate'):
            raise TypeError("Schema class must support model_validate()")

        return schema.model_validate(user)
