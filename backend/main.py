from fastapi import FastAPI
from backend.app.routes.crud_route import create_crud_router
from backend.app.routes.sessions import create_refresh_router
from backend.app.routes.auth import create_login_router, create_register_router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(create_crud_router())
    app.include_router(create_register_router())
    app.include_router(create_login_router())
    app.include_router(create_refresh_router())

    return app

application = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:application", host="127.0.0.1", port=8000, reload=True)
