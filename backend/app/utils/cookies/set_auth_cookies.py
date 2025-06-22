from fastapi.responses import JSONResponse

def set_auth_cookies(response: JSONResponse, access_token: str, refresh_token: str, ttl: int):
    """
    Sets the access_token and refresh_token in the cookies.
    """
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  # For HTTPS in production
        samesite="strict",
        expires=ttl
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        expires=ttl
    )
