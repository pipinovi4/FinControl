def get_worker_crud():
    from .create import router as create_worker_router

    return create_worker_router