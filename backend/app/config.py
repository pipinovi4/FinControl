import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# === PATH SETUP ===
env_path = Path(__file__).resolve()
for _ in range(5):
    if (env_path / ".env.backend").exists():
        load_dotenv(dotenv_path=env_path / ".env.backend")
        sys.path.append(str(env_path))
        break
    env_path = env_path.parent

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
SQLALCHEMY_POOL_RECYCLE = int(os.getenv("SQLALCHEMY_POOL_RECYCLE", 1800))
SQLALCHEMY_POOL_SIZE = int(os.getenv("SQLALCHEMY_POOL_SIZE", 10))
SQLALCHEMY_MAX_OVERFLOW = int(os.getenv("SQLALCHEMY_MAX_OVERFLOW", 20))
SQLALCHEMY_POOL_TIMEOUT = int(os.getenv("SQLALCHEMY_POOL_TIMEOUT", 30))
