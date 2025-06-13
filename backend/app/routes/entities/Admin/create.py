from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from backend.db.session import get_db
from backend.app.schemas.entities.Admin import AdminSchema
from backend.app.services.entities import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post(
    "/",
    summary="Create a new Admin",
    response_model=AdminSchema.Out,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Admin successfully created"},
        409: {"description": "Admin with this email or Telegram ID already exists"},
        500: {"description": "Internal server error"},
    }
)
def create_admin(
    user: AdminSchema.Create,
    db: Session = Depends(get_db)
):
    """
    Create a new admin user with optional super admin privileges.

    - **email**: login email (must be unique)
    - **telegram_id**: Telegram ID (must be unique)
    - **telegram_username**: Telegram handle (must be unique)
    - **is_super_admin**: optional elevated permissions
    - **password_hash**: pre-hashed password or optional if using dynamic login
    """
    service = AdminService(db)

    if service.get_user_by_telegram_id(telegram_id=UUID(user.telegram_id)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Admin with given email or telegram_id already exists"
        )

    new_admin = service.create_admin(user)

    return new_admin
