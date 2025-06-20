from typing import Optional, List
from pydantic import Field

from backend.app.schemas.entities import UserSchema
from backend.app.schemas.mixins import TimeStampAuthSchema


class BrokerCreate(UserSchema.Create, TimeStampAuthSchema):
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
