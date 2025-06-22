from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from backend.app.utils.middlewares import limiter
from backend.app.routes import create_api_router
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict

class LimiterApp(FastAPI):
    state: dict

def create_app() -> FastAPI:
    app = LimiterApp()

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  # Adjust this to your frontend's URL
            "https://yourfrontend.com"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # SlowAPI middleware
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    # Rate limit exception handler
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"},
        )

    # Include API routes
    app.include_router(create_api_router())

    # Logging routes and stats
    print("\n📌 Registered routes:\n")
    print(f"{'METHODS':<10} {'PATH':<45} {'NAME':<30} {'TAGS'}")
    print("-" * 110)

    tag_priority = ["ANALYZE", "CRUD", "AUTH"]
    tag_counter = defaultdict(int)
    total_routes = 0

    for route in app.routes:
        methods = getattr(route, "methods", set())
        methods_str = ", ".join(sorted(methods))
        path = route.path
        name = route.name or "-"
        tags = [t.upper() for t in getattr(route, "tags", [])]

        # Determine main tag for the route
        main_tag = None
        for tag in tag_priority:
            if tag in tags:
                main_tag = tag
                break
        if main_tag is None:
            main_tag = "OTHER"

        tag_counter[main_tag] += 1
        total_routes += 1

        print(f"{methods_str:<10} {path:<45} {name:<30} {tags}")

    print("\n📊 Route stats:")
    for tag in tag_priority + ["OTHER"]:
        print(f"  • {tag:<8}: {tag_counter[tag]:>3} routes")
    print(f"  • {'TOTAL':<8}: {total_routes:>3} routes\n")

    return app


application = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:application", host="127.0.0.1", port=8000, reload=True)
