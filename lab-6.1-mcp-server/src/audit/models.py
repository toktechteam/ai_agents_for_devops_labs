from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func

Base = declarative_base()


class AuditRecord(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    method = Column(String(200))
    request_json = Column(String(2000))
    response_json = Column(String(2000))
    timestamp = Column(DateTime, server_default=func.now())
