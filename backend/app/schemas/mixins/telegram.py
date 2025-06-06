from pydantic import BaseModel, Field

class TelegramSchema(BaseModel):
    telegram_id: str = Field(..., example="123456789")
    telegram_username: str = Field(..., example="pipin")

    class Config:
        orm_mode = True
