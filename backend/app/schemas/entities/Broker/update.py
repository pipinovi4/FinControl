from typing import Optional, List
from pydantic import Field, EmailStr

from backend.app.schemas.entities import UserSchema

class BrokerUpdate(UserSchema.Update):
    """
    Schema for updating an existing Broker.

    Inherits all optional user-update fields, then adds:
      - company_name
      - region
    """
    company_name: Optional[str] = Field(
        None,
        example="ACME Brokerage",
        description="Updated company name"
    )
    region: Optional[List[str]] = Field(
        None,
        example=["Mazovia"],
        description="Updated list of active regions"
    )
