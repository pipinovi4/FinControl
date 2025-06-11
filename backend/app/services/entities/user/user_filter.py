from sqlalchemy.orm import Query
from backend.app.models import User
from backend.app.permissions import PermissionRole


class UserFilterService:
    """
    Service for filtering User queries based on dynamic conditions.
    """

    def __init__(self, base_query: Query):
        self.query = base_query

    def by_role(self, role: PermissionRole):
        """
        Filter users by role.
        """
        self.query = self.query.filter(User.role == role)
        return self

    def by_telegram_id(self, telegram_id: int):
        self.query = self.query.filter(User.telegram_id == telegram_id)
        return self

    def apply(self):
        """
        Finalize and return the query.
        """
        return self.query
