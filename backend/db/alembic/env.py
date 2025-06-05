from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# === PYTHONPATH ===
sys.path.append(str(Path(__file__).resolve().parents[2]))

# === Load environment variables ===
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

# === Build DB URI ===
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# === Alembic config ===
config = context.config
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URI)

# === Logging ===
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# === Import Base metadata ===
from backend.db.session import Base
from backend.app.models import User, Client, Worker, Broker, Admin  # ensure models are imported and registered

target_metadata = Base.metadata

# === Run migrations ===

def run_migrations_offline():
    context.configure(
        url=SQLALCHEMY_DATABASE_URI,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
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
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
