from fastapi import FastAPI
from backend.app.routes.crud_route import create_crud_router
from backend.app.routes.auth_route import create_auth_router
from fastapi.routing import APIRoute

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(create_auth_router())
    app.include_router(create_crud_router())

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
