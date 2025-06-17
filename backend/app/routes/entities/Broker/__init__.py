def get_broker_crud():
    from .create import router as create_broker_router

    return create_broker_router