"""
Alembic migration environment configuration.

Loads environment variables, wires up SQLAlchemy models, and runs migrations
both in offline and online modes.
"""

from pathlib import Path
import sys
import importlib
import os
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv


sys.path.append(str(Path(__file__).resolve().parents[3]))


# --------------------------------------------------------------------------- #
# 1)  Locate project root and .env                                            #
# --------------------------------------------------------------------------- #

ROOT_DIR = Path(__file__).resolve()
for _ in range(5):              # підіймаємось угору максимум на 5 рівнів
    if (ROOT_DIR / ".env").exists():
        load_dotenv(ROOT_DIR / ".env")
        break
    ROOT_DIR = ROOT_DIR.parent
else:
    raise FileNotFoundError(".env not found — check project structure.")

# --------------------------------------------------------------------------- #
# 2)  Database URI from env                                                   #
# --------------------------------------------------------------------------- #

required = ("DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME")
missing = [k for k in required if not os.getenv(k)]
if missing:
    raise EnvironmentError(f"Missing env variables: {', '.join(missing)}")

SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# --------------------------------------------------------------------------- #
# 3)  Alembic config & logging                                                #
# --------------------------------------------------------------------------- #

config = context.config
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URI)

if config.config_file_name:
    fileConfig(config.config_file_name)

# --------------------------------------------------------------------------- #
# 4)  Import models so their tables register in Base.metadata                 #
# --------------------------------------------------------------------------- #

MODEL_MODULES = [
    "backend.app.models.entities.user",
    "backend.app.models.entities.client",
    "backend.app.models.entities.worker",
    "backend.app.models.entities.broker",
    "backend.app.models.entities.admin",
    "backend.app.models.entities.credit",
    "backend.app.models.entities.promotion",
]

for m in MODEL_MODULES:
    importlib.import_module(m)

from db.session import Base  # тепер Base.metadata заповнений
from app.app.models import *

print("DEBUG tables =>", list(Base.metadata.tables.keys()))

target_metadata = Base.metadata

# --------------------------------------------------------------------------- #
# 5)  Migration routines                                                      #
# --------------------------------------------------------------------------- #

def run_migrations_offline() -> None:
    """Run migrations without a DB connection."""
    context.configure(
        url=SQLALCHEMY_DATABASE_URI,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations with an active DB connection."""
    connectable = create_engine(SQLALCHEMY_DATABASE_URI, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,            # корисно для майбутніх змін
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()

# --------------------------------------------------------------------------- #
# 6)  Entry point                                                             #
# --------------------------------------------------------------------------- #

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()