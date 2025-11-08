from app.schemas.entities.admin_schema import AdminSchema
from pydantic import Field

class AdminFilterSchema(AdminSchema.Base):
    """
    Filter schema for querying Admins.
    Excludes technical or sensitive fields.
    """

    password_hash: None = Field(exclude=True)
    dynamic_login_token: None = Field(exclude=True)
    last_login_at: None = Field(exclude=True)
    created_at: None = Field(exclude=True)
    updated_at: None = Field(exclude=True)
