def create_crud_router():
    from fastapi import APIRouter

    from .entities.Worker import get_worker_crud
    from .entities.Client import get_client_crud
    from .entities.Admin import get_admin_crud
    from .entities.Broker import get_broker_crud

    crud_router = APIRouter(prefix="/crud")

    # CRUD

    crud_router.include_router(get_admin_crud(), prefix="/entity", tags=["Entities"])
    crud_router.include_router(get_broker_crud(), prefix="/entity", tags=["Entities"])
    crud_router.include_router(get_worker_crud(), prefix="/entity", tags=["Entities"])
    crud_router.include_router(get_client_crud(), prefix="/entity", tags=["Entities"])

    return crud_router