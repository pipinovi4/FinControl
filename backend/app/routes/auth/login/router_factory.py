from typing import Awaitable, Callable, List, Type, TypeVar
from fastapi import APIRouter, HTTPException, Request, Depends, status, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from uuid import UUID

from app.routes.auth.login.types import LoginTypes
from app.routes.auth.login.config import ROLE_REGISTRY
from app.schemas.sessions import TokenPair
from app.services.auth import PasswordService, generate_token_pair
from app.utils.cookies import set_auth_cookies
from db.session import get_async_db
from app.routes.auth.login._base import generate_login_endpoints
from app.permissions import PermissionRole
from app.models.entities import Admin, Worker, Broker, Client

ModelT = TypeVar("ModelT", Admin, Worker, Broker, Client)

def make_login_handler(
        role: PermissionRole,
        login_type: LoginTypes,
        input_schema: Type[BaseModel],
        model: Type[ModelT]
) -> Callable[..., Awaitable]:
    async def _handler(
        request: Request,
        data: input_schema = Body(...),
        db=Depends(get_async_db),
    ) -> JSONResponse | TokenPair:
        password_service = PasswordService(db)
        user = await password_service.authenticate(data.email, data.password, model)

        print(user)

        if user is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        if user.role != role:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Not a {role.name.lower()}")

        access, refresh, ttl = await generate_token_pair(
            UUID(str(user.id)),
            db,
            request.client.host,
            request.headers.get("User-Agent"),
        )

        response: JSONResponse | TokenPair

        if LoginTypes.WEB is login_type:
            response = JSONResponse(content={"status": 200})
            set_auth_cookies(response, access, refresh, ttl)
        elif LoginTypes.BOT is login_type:
            return TokenPair(access_token=access, refresh_token=refresh, expires_in=ttl)
        else:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid login type provided")

        return response

    return _handler

def create_login_routers() -> List[APIRouter]:
    routers: List[APIRouter] = []

    for role, (path, service, schema, model, login_types_cls) in ROLE_REGISTRY.items():
        router = APIRouter()

        for login_type_key in ("web", "bot"):
            login_type_tuple = getattr(login_types_cls, login_type_key)
            if not login_type_tuple:
                continue

            login_type, input_schema, response_schema = login_type_tuple

            handler = make_login_handler(
                role=role,
                login_type=login_type,
                input_schema=input_schema,
                model=model
            )

            login_path = f"{path}/{login_type.name.lower()}"
            tag_name = f"{role.value.lower()}-{login_type.name.lower()}"

            generate_login_endpoints(
                router=router,
                path=login_path,
                handler=handler,
                tags=[tag_name],
                rate_limit_rule="10/minute",
                input_model=input_schema,
                response_model=response_schema,
                name=f"login_{role.value.lower()}_{login_type.name.lower()}"
            )

        routers.append(router)

    return routers
