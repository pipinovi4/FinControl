from alembic import context
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
import os
from dotenv import load_dotenv
from pathlib import Path
import sys

# ==========================================
# 🔥 ALWAYS LOAD ROOT .env (FinControl/.env)
# ==========================================

project_root = Path(__file__).resolve().parents[2]
env_file = project_root / ".env"

if env_file.exists():
    print(f"🔧 [alembic] Loading .env from {env_file}")
    load_dotenv(env_file)
else:
    print("⚠️ [alembic] .env NOT FOUND — using environment variables")

# Ensure root is importable
sys.path.append(str(project_root))

# ==========================================
# 🔥 BUILD SQLALCHEMY URL
# ==========================================

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise RuntimeError("❌ Alembic: Missing database environment variables!")

SQLALCHEMY_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Inject URL into alembic config
config = context.config
config.set_main_option("sqlalchemy.url", SQLALCHEMY_URL)

# Setup logging
fileConfig(config.config_file_name)

# ==========================================
# 🔥 IMPORT MODELS METADATA
# ==========================================
# Now imports will work because PYTHONPATH changed
from app.models import RefreshToken, User, Admin, Client, Broker, Worker, Credit, RegistrationInvite, Promotion

from db.session import Base

target_metadata = Base.metadata

# ==========================================
# 🔥 RUN MIGRATIONS
# ==========================================

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
