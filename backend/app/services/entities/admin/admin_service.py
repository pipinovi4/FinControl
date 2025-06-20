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

from backend.app.services.auth import PasswordService
from backend.app.services.entities import UserService
from backend.app.permissions import PermissionRole
from backend.app.models.entities import Admin
from backend.app.utils.decorators import handle_exceptions
from backend.app.schemas.entities.Admin import AdminSchema

T = TypeVar("T", bound=Admin)

class AdminService(UserService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.db = db  # in case UserService doesn't define it

    @handle_exceptions(raise_404=True)
    def get_by_id(self, admin_id: UUID) -> T:
        """
        Fetch a specific Admin user by their unique ID.
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
        """
        return cast(
            Sequence[T],
            self.db.query(Admin)
            .filter_by(role=PermissionRole.ADMIN)
            .all()
        )

    @handle_exceptions()
    def create(self, admin_data: AdminSchema.Create) -> T:
        """
        Create a new Admin user. Hashes the password before saving.
        """
        updated_admin_data = admin_data.model_dump()
        updated_admin_data["password_hash"] = PasswordService.hash(updated_admin_data.pop("password"))
        admin = Admin(**updated_admin_data)
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return cast(T, admin)

    @handle_exceptions()
    def update(self, admin_id: UUID, updates: AdminSchema.Update) -> T:
        """
        Update an existing Admin's fields.
        """
        admin = self.get_admin_by_id(admin_id)
        for key, value in updates.model_dump(exclude_unset=True).items():
            setattr(admin, key, value)
        self.db.commit()
        self.db.refresh(admin)
        return cast(T, admin)

    @handle_exceptions()
    def delete(self, admin_id: UUID) -> T:
        """
        Permanently delete an Admin from the database.
        """
        admin = self.get_admin_by_id(admin_id)
        self.db.delete(admin)
        self.db.commit()
        return cast(T, admin)
