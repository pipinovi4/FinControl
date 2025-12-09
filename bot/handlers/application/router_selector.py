from handlers.application.routers import ProgressRouter, EditRouter, ReviewRouter


def get_router(update, context):
    """
    Returns an instantiated router class based on panel_mode.
    """

    mode = context.user_data.get("panel_mode", "progress")

    if mode == "edit":
        return EditRouter(update, context)

    if mode == "review":
        return ReviewRouter(update, context)

    return ProgressRouter(update, context)


__all__ = ["get_router"]
