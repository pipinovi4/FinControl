from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    """
    Schema for login requests.

    Attributes:
        login (str): A flexible login field that can accept email, username, or Telegram username.
        password (str): User password, must be at least 8 characters long.
    """
    login: str = Field(..., description="Email, username, or Telegram username")
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")
