"""
AdminService handles operations specific to Admin users.

Methods:
    get_admin_by_id(admin_id): Fetch admin by UUID, raise 404 if not found.
    get_all_admins(): Return all users with ADMIN role.
    create_admin(admin_data): Create a new admin user.
    update_admin(admin_id, updates): Update admin fields.
    delete_admin(admin_id): Hard delete admin user.
"""

from sqlalchemy.orm import Session
from typing import TypeVar, cast, Sequence
from uuid import UUID

from backend.app.services.entities import UserService
from backend.app.permissions import PermissionRole
from backend.app.models.entities import Admin
from backend.app.utils.decorators import handle_exceptions
from backend.app.schemas.entities.Admin import AdminSchema

T = TypeVar("T", bound=Admin)


class AdminService(UserService):
    def __init__(self, db: Session):
        super().__init__(db)
        self.db = db

    @handle_exceptions(raise_404=True)
    def get_admin_by_id(self, admin_id: UUID) -> T:
        return cast(
            T,
            self.db.query(Admin)
            .filter_by(id=admin_id, is_deleted=False)
            .first()
        )

    @handle_exceptions(default_return=[])
    def get_all_admins(self) -> Sequence[T]:
        return cast(
            Sequence[T],
            self.db.query(Admin)
            .filter_by(role=PermissionRole.ADMIN)
            .all()
        )

    @handle_exceptions()
    def create_admin(self, admin_data: AdminSchema.Create) -> T:
        admin = Admin(**admin_data.model_dump())
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return cast(T, admin)

    @handle_exceptions()
    def update_admin(self, admin_id: UUID, updates: AdminSchema.Update) -> T:
        admin = self.get_admin_by_id(admin_id)
        for key, value in updates.model_dump(exclude_unset=True).items():
            setattr(admin, key, value)
        self.db.commit()
        self.db.refresh(admin)
        return cast(T, admin)

    @handle_exceptions()
    def delete_admin(self, admin_id: UUID) -> T:
        admin = self.get_admin_by_id(admin_id)
        self.db.delete(admin)
        self.db.commit()
        return cast(T, admin)
