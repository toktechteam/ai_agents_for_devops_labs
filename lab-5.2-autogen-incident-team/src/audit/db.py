from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.audit.models import Base

DB_URL = "postgresql://aiagent:aiagentpass@postgres:5432/auditdb"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

_initialized = False


def _init_db():
    global _initialized
    if not _initialized:
        # Create tables if they don't exist.
        Base.metadata.create_all(engine)
        _initialized = True


def get_session():
    _init_db()
    return SessionLocal()
