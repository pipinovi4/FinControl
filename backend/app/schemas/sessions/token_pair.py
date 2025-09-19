from pydantic import BaseModel

class TokenPair(BaseModel):
    """
    Represents a pair of access and refresh tokens returned upon successful authentication.

    Fields:
        access_token (str): JWT access token used for authenticated requests.
        refresh_token (str): Secure token used to obtain a new access token when expired.
        token_type (str): Token type, usually set to "bearer" for HTTP Authorization headers.
        expires_in (int): Time (in seconds) until the access token expires.
    """
    access_token: str  # JWT for accessing protected routes
    refresh_token: str  # Token to refresh the access token
    token_type: str = "bearer"  # Indicates Bearer token type (used in headers)
    expires_in: int  # Access token lifetime in seconds
