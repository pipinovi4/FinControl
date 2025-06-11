from fastapi import FastAPI
from backend.app.routes import users  # якщо лежить у app/routes/users.py

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(users.router)  # додаємо наш роутер
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
