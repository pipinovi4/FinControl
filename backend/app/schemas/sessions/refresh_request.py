from pydantic import BaseModel, Field

class RefreshRequest(BaseModel):
    """
    Schema for requesting a new access token using a refresh token.

    Fields:
        refresh_token (str): The raw refresh token issued during login.
            - Minimum length: 10
            - Maximum length: 200
            - Must be a valid token previously issued by the system.
    """
    refresh_token: str = Field(
        ...,
        min_length=10,
        max_length=200,
        description="Raw refresh token used to generate a new access token"
    )
