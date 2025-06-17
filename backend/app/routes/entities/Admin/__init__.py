def get_admin_crud():
    from .create import router as create_admin_router

    return create_admin_router