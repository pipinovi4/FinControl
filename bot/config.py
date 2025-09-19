"""Centralised config."""
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = "8141477114:AAHnyYuamVB0qQ8FodClq20LHbtkJkUN_mY"
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/auth/register/client")