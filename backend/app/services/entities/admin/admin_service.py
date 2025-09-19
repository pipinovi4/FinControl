from typing import TypeVar, cast, Sequence
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.app.models.entities.registration_invite import RegistrationInvite
from backend.app.services.auth import PasswordService
from backend.app.services.auth.invite_service import InviteService
from backend.app.services.entities import UserService
from backend.app.permissions import PermissionRole
from backend.app.models.entities import Admin
from backend.app.utils.decorators import handle_exceptions
from backend.app.schemas.entities.admin_schema import AdminSchema
from backend.db.session import get_async_db

AdminT = TypeVar("AdminT", bound=Admin)

class AdminService(UserService):
    """
    AdminService handles all async CRUD operations for Admin users.

    Inherits:
        UserService – Provides shared user logic (e.g. deletion, querying)

    Public Methods:
        - get_by_id(admin_id): Fetch a specific Admin by UUID.
        - get_all_admins(): Retrieve a list of all Admins.
        - create(admin_data): Create a new Admin user (hashes password).
        - update(admin_id, updates): Apply updates to an existing Admin.
        - delete(admin_id): Permanently delete Admin from a database.
    """
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.db = db

    @handle_exceptions(raise_404=True)
    async def get_by_id(self, admin_id: UUID) -> AdminT:
        """Fetch a specific Admin user by their unique ID."""
        result = await self.db.execute(
            select(Admin).where(Admin.id == admin_id, Admin.is_deleted == False)
        )
        return cast(AdminT, result.scalar_one_or_none())

    @handle_exceptions()
    async def get_by_email(self, email: str) -> AdminT | None:
        """
        Fetch a broker by their email.
        """
        stmt = select(Admin).where(Admin.email == email)
        result = await self.db.execute(stmt)
        return cast(AdminT, result.scalar_one_or_none())

    @handle_exceptions()
    async def get_all_admins(self) -> Sequence[AdminT]:
        """Fetch all users with the ADMIN role."""
        result = await self.db.execute(
            select(Admin).where(Admin.role == PermissionRole.ADMIN)
        )
        return cast(Sequence[AdminT], result.scalars().all())

    @handle_exceptions()
    async def create(self, admin_data: AdminSchema.Create) -> AdminT:
        """Create a new Admin user. Hashes the password before saving."""
        updated_admin_data = admin_data.model_dump()
        updated_admin_data["password_hash"] = PasswordService.hash(updated_admin_data.pop("password"))
        admin = Admin(**updated_admin_data)
        self.db.add(admin)
        await self.db.commit()
        await self.db.refresh(admin)
        return cast(AdminT, admin)

    @handle_exceptions()
    async def update(self, admin_id: UUID, updates: AdminSchema.Update) -> AdminT:
        """Update an existing Admin's fields — skip null values."""
        admin = await self.get_by_id(admin_id)

        for key, value in updates.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(admin, key, value)

        await self.db.commit()
        await self.db.refresh(admin)
        return cast(AdminT, admin)

    @handle_exceptions()
    async def delete(self, admin_id: UUID) -> AdminT:
        """Permanently delete an Admin from the database."""
        admin = await self.get_by_id(admin_id)
        await self.db.delete(admin)
        await self.db.commit()
        return cast(AdminT, admin)
