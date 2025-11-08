from typing import Type, TypeVar

from app.models import User
from app.permissions import PermissionRole
from app.schemas import SchemaBase

T = TypeVar("T", bound=SchemaBase)


class UserUtilService:
    """
    A utility class for common user-related operations on ORM instances and schema conversions.

    This class contains only static methods and is designed to:
    - Extract user-friendly display names.
    - Filter user collections by role.
    - Convert SQLAlchemy User models into typed Pydantic schemas (bulk or single).

    Methods:
        - get_display_name(user): Returns '@username' or UUID-based fallback.
        - filter_by_role(users, role): Filters a list of User objects by role.
        - to_schema(users, schema): Maps a list of User models to Pydantic schema instances.
        - to_schema_one(user, schema): Converts one User model to a Pydantic schema.

    Usage:
        These methods are typically used in services, responses, or export utilities
        where model transformation and display-friendly data are needed.
    """

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
