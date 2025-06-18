from fastapi import FastAPI
from .app.routes import create_api_router

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(create_api_router())

    for route in app.routes:
        # У FastAPI всі HTTP-роути — це Starlette Route об'єкти
        methods = getattr(route, "methods", None)
        if methods:
            methods = ", ".join(sorted(methods))
        print(f"{route.name:<30} {route.path:<30} {methods}")

    return app

application = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:application", host="127.0.0.1", port=8000, reload=True)
