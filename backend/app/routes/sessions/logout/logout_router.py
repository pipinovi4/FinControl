from fastapi import APIRouter, Depends, Response, status
from backend.app.utils.decorators import handle_route_exceptions

router = APIRouter(tags=["Logout"])


@handle_route_exceptions()
async def logout(response: Response):
    response.delete_cookie("access_token", path="/", httponly=True)
    response.delete_cookie("refresh_token", path="/", httponly=True)
    return {"detail": "Successfully logged out."}

logout._meta = {"input_schema": None, "output_schema": "string"}

router.post("", status_code=status.HTTP_200_OK)(logout)
