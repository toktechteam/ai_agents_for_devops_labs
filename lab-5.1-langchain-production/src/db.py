from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = "postgresql://aiagent:aiagentpass@postgres:5432/auditdb"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)


def get_db_session():
    return SessionLocal()
