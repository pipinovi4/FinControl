from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.utils.middlewares import AccessTokenMiddleware, WebSocketAuthMiddleware
from app.routes import create_api_router
from app.core.settings import settings
from fastapi.middleware.cors import CORSMiddleware
from slowapi.util import get_remote_address
from db.session import Base

# Initialize the rate limiter with the key function
limiter = Limiter(key_func=get_remote_address)

def create_app() -> FastAPI:
    app = FastAPI(strict_slashes=False)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[o.strip() for o in settings.ALLOWED_ORIGINS.split(",")],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add SlowAPI middleware for rate-limiting
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    # Add Access Token Middleware
    app.add_middleware(AccessTokenMiddleware)

    # Add WebSocket Auth Middleware
    app.add_middleware(WebSocketAuthMiddleware)

    # Rate limit exception handler
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"},
        )

    # Include API routes
    app.include_router(create_api_router())

    return app


application = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:application", host="0.0.0.0", port=8000, reload=False)
