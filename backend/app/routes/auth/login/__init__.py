def get_login_routers():
    from .admin import router as admin_login_router
    from .broker import router as broker_login_router
    from .worker import router as worker_login_router
    from .client import router as client_login_router

    return admin_login_router, broker_login_router, worker_login_router, client_login_router
