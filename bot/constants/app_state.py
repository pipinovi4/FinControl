# =========================
# Application (wizard) state keys
# =========================
# These keys are stored inside context.user_data
# and define the current state of the multi-step application flow.

APP_FLOW  = "app_flow"     # flag: user is inside the application wizard
APP_STEPS = "steps"        # ordered list of step ids for this country/user
APP_IDX   = "idx"          # index of the current step in APP_STEPS
APP_ANS   = "answers"      # dict with all collected user answers


# =========================
# Fintech-style UI elements (progress panel & service messages)
# =========================
# We store message IDs to update or clear them later.
# Telegram does not provide update events → manual tracking is required.

PROGRESS_MSG_ID     = "progress_msg_id"      # ID of the *latest* progress panel (for editing)
PROGRESS_MSG_IDS    = "progress_msg_ids"     # IDs of *all* panels ever created (for cleanup)

LAST_PROMPT_MSG_ID  = "last_prompt_msg_id"   # last question sent to the user
LAST_SERVICE_MSG_ID = "last_service_msg_id"  # last technical / info message

ABOUT_PHOTO_MSG_ID  = "about_photo_msg_id"   # photo message from /about section
ABOUT_TEXT_MSG_ID   = "about_text_msg_id"    # text message from /about section

__all__ = [
    "APP_FLOW",
    "APP_STEPS",
    "APP_IDX",
    "APP_ANS",

    "PROGRESS_MSG_ID",
    "PROGRESS_MSG_IDS",
    "LAST_PROMPT_MSG_ID",
    "LAST_SERVICE_MSG_ID",
    "ABOUT_PHOTO_MSG_ID",
    "ABOUT_TEXT_MSG_ID",
]