def get_register_routers():
    from .admin import router as admin_register_router
    from .broker import router as broker_register_router
    from .worker import router as worker_register_router
    from .client import router as client_register_router

    return admin_register_router, broker_register_router, worker_register_router, client_register_router