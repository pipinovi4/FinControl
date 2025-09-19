# backend/app/schemas/auth/invite_schema.py
from datetime import datetime, UTC, timedelta
from pydantic import Field
from typing import Optional

from backend.app.permissions import PermissionRole
from backend.app.schemas import SchemaBase


class InviteInfoOut(SchemaBase):
    """
    Відповідь на GET /auth/invite/<role>/<token>

    • role        — роль, під яку призначено інвайт
    • expires_at  — UTC-момент, коли посилання стане недійсним
    """
    role: PermissionRole = Field(..., description="Роль, під яку видано інвайт")
    expires_at: datetime = Field(..., description="Час (UTC), коли інвайт протерміновується")

def default_expiration():
    return datetime.now(UTC) + timedelta(hours=24)

class InviteIn(SchemaBase):
    role: PermissionRole = Field(..., description="Роль, під яку видано інвайт")
    expires_at: Optional[datetime] = Field(
        default_factory=default_expiration,
        description="Час (UTC), коли інвайт протерміновується; якщо не вказано — 24 години від тепер."
    )

class InviteOut(SchemaBase):
    raw: str = Field(...)
