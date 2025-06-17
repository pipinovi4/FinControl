"""
AdminService handles all CRUD operations for Admin users.

Inherits:
    UserService – Provides shared user logic (e.g. deletion, querying)

Public Methods:
    - get_admin_by_id(admin_id): Fetch a specific Admin by UUID.
    - get_all_admins(): Retrieve a list of all Admins.
    - create_admin(admin_data): Create a new Admin user (hashes password).
    - update_admin(admin_id, updates): Apply updates to an existing Admin.
    - delete_admin(admin_id): Permanently delete Admin from database.
"""

from sqlalchemy.orm import Session
from typing import TypeVar, cast, Sequence
from uuid import UUID

from backend.app.services.auth_service import AuthService
from backend.app.services.entities import UserService
from backend.app.permissions import PermissionRole
from backend.app.models.entities import Admin
from backend.app.utils.decorators import handle_exceptions
from backend.app.schemas.entities.Admin import AdminSchema

T = TypeVar("T", bound=Admin)


class AdminService(UserService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.db = db  # if UserService doesn't define it itself

    @handle_exceptions(raise_404=True)
    def get_admin_by_id(self, admin_id: UUID) -> T:
        """
        Fetch a specific Admin user by their unique ID.

        Args:
            admin_id (UUID): Unique identifier of the admin.

        Returns:
            Admin instance if found, otherwise raises 404.
        """
        return cast(
            T,
            self.db.query(Admin)
            .filter_by(id=admin_id, is_deleted=False)
            .first()
        )

    @handle_exceptions(default_return=[])
    def get_all_admins(self) -> Sequence[T]:
        """
        Fetch all users with the ADMIN role.

        Returns:
            List of Admin instances.
        """
        return cast(
            Sequence[T],
            self.db.query(Admin)
            .filter_by(role=PermissionRole.ADMIN)
            .all()
        )

    @handle_exceptions()
    def create_admin(self, admin_data: AdminSchema.Create) -> T:
        """
        Create a new Admin user.

        Steps:
            - Extract raw password from input schema.
            - Hash the password and replace the plain password.
            - Save the Admin to the database.

        Args:
            admin_data (AdminSchema.Create): Incoming validated schema.

        Returns:
            The newly created Admin instance.
        """
        updated_admin_data = admin_data.model_dump()
        updated_admin_data["password_hash"] = AuthService.hash_password(updated_admin_data.pop("password"))

        admin = Admin(**updated_admin_data)
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return cast(T, admin)

    @handle_exceptions()
    def update_admin(self, admin_id: UUID, updates: AdminSchema.Update) -> T:
        """
        Update an existing Admin's fields.

        Args:
            admin_id (UUID): Admin's unique identifier.
            updates (AdminSchema.Update): Pydantic model with changes.

        Returns:
            The updated Admin instance.
        """
        admin = self.get_admin_by_id(admin_id)
        for key, value in updates.model_dump(exclude_unset=True).items():
            setattr(admin, key, value)
        self.db.commit()
        self.db.refresh(admin)
        return cast(T, admin)

    @handle_exceptions()
    def delete_admin(self, admin_id: UUID) -> T:
        """
        Permanently delete an Admin from the database.

        Args:
            admin_id (UUID): Admin's unique identifier.

        Returns:
            The deleted Admin instance.
        """
        admin = self.get_admin_by_id(admin_id)
        self.db.delete(admin)
        self.db.commit()
        return cast(T, admin)
