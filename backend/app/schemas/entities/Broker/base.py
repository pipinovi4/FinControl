from typing import Optional, List
from pydantic import Field
from backend.app.schemas.entities import UserSchema
from backend.app.schemas.mixins import AuthSchema, TimeStampAuthSchema

class BrokerBase(
    UserSchema.Base,
    AuthSchema,
    TimeStampAuthSchema
):
    """
    Shared schema for the Broker entity.

    Inherits:
      - UserSchema.Base        (id, timestamps, full_name, telegram info)
      - AuthSchema             (email, password_hash [excluded on output])
      - TimeStampAuthSchema    (last_login_at)

    Adds:
      - company_name           (optional company affiliation)
      - region                 (optional list of regions)
    """
    company_name: Optional[str] = Field(
        None,
        example="ACME Brokerage",
        description="Name of the broker’s company, if any"
    )
    region: Optional[List[str]] = Field(
        None,
        example=["Mazovia", "Lesser Poland"],
        description="List of regions where the broker is active"
    )
