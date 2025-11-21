import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# ==========================================
# ALWAYS LOAD .env FROM PROJECT ROOT
# ==========================================

# /app/app/config.py → go 2 levels up → /app → go 1 more → / (FinControl root in Docker)
project_root = Path(__file__).resolve().parents[2]

env_file = project_root / ".env"

if env_file.exists():
    print(f"🔧 Loading .env from: {env_file}")
    load_dotenv(env_file)
else:
    print("⚠️ .env NOT FOUND in project root, using environment variables")


# add project root to PYTHONPATH
sys.path.append(str(project_root))

# === DATABASE CONFIGURATION ===
required_env = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
missing = [key for key in required_env if not os.getenv(key)]
if missing:
    raise EnvironmentError(f"❌ Missing required environment variables: {', '.join(missing)}")

# базовий URI без параметрів
SQLALCHEMY_DATABASE_URI = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# === Optional SQLAlchemy pool settings ===
SQLALCHEMY_POOL_PRE_PING = os.getenv("SQLALCHEMY_POOL_PRE_PING", "True")
SQLALCHEMY_POOL_SIZE = int(os.getenv("SQLALCHEMY_POOL_SIZE", 10))
SQLALCHEMY_MAX_OVERFLOW = int(os.getenv("SQLALCHEMY_MAX_OVERFLOW", 20))
SQLALCHEMY_POOL_TIMEOUT = int(os.getenv("SQLALCHEMY_POOL_TIMEOUT", 30))
