from typing import Optional, List
from pydantic import Field, EmailStr
from uuid import UUID

from backend.app.schemas.entities import UserSchema

class BrokerCreate(UserSchema.Create):
    """
    Schema for creating a new Broker.

    Inherits:
      - UserSchema.Create  (email, password, full_name)
    Adds:
      - company_name       (optional)
      - region             (optional list of region names)
    """
    company_name: Optional[str] = Field(
        None,
        example="ACME Brokerage",
        description="Name of the broker’s company"
    )
    region: Optional[List[str]] = Field(
        None,
        example=["Mazovia", "Lesser Poland"],
        description="Regions where the broker will operate"
    )
