from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator
from backend.app.config import SQLALCHEMY_DATABASE_URI

# Create SQLAlchemy engine using your database URL
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()

# Dependency used by FastAPI routes to get a DB session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
