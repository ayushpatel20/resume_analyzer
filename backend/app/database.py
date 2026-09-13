from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# For SQLite, check_same_thread needs to be False
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


_db_initialized = False


def init_db():
    """Create all database tables safely."""
    global _db_initialized
    try:
        from app.models import models  # noqa: F401
        Base.metadata.create_all(bind=engine)
        _db_initialized = True
    except Exception as e:
        print(f"init_db safe warning: {e}")


def get_db():
    """Dependency that yields a database session and closes it afterwards."""
    global _db_initialized
    if not _db_initialized:
        init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

