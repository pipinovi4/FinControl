def get_client_crud():
    from .create import router as create_client_router

    return create_client_router