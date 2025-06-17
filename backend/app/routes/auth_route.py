def create_auth_router():
    from fastapi import APIRouter
    from .auth.register import get_register_routers
    from .auth.login import get_login_routers

    (admin_login_router, broker_login_router, worker_login_router, client_login_router) = get_login_routers()
    (admin_register_router, broker_register_router, worker_register_router, client_register_router) = get_register_routers()


    auth_router = APIRouter(prefix="/auth")

    # Login endpoints
    auth_router.include_router(admin_login_router, prefix="/login", tags=["Login"])
    auth_router.include_router(broker_login_router, prefix="/login", tags=["Login"])
    auth_router.include_router(worker_login_router, prefix="/login", tags=["Login"])
    auth_router.include_router(client_login_router, prefix="/login", tags=["Login"])

    # Register endpoints
    auth_router.include_router(admin_register_router, prefix="/register", tags=["Register"])
    auth_router.include_router(broker_register_router, prefix="/register", tags=["Register"])
    auth_router.include_router(worker_register_router, prefix="/register", tags=["Register"])
    auth_router.include_router(client_register_router, prefix="/register", tags=["Register"])

    return auth_router