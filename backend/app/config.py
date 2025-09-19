import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# === PATH SETUP ===
# Ensure project root is in sys.path for imports
env_path = Path(__file__).resolve()
for _ in range(5):  # Look max 5 levels up for .env and project root
    if (env_path / ".env").exists():
        load_dotenv(dotenv_path=env_path / ".env")
        sys.path.append(str(env_path))
        break
    env_path = env_path.parent
else:
    raise FileNotFoundError("❌ .env file not found in parent directories.")

# === DATABASE CONFIGURATION ===
required_env = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
missing = [key for key in required_env if not os.getenv(key)]
if missing:
    raise EnvironmentError(f"❌ Missing required environment variables: {', '.join(missing)}")

SQLALCHEMY_DATABASE_URI = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
