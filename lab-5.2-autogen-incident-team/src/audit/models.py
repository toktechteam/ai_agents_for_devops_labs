from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()


class AuditRecord(Base):
    __tablename__ = "audit_records"

    id = Column(Integer, primary_key=True, index=True)
    agent = Column(String(100))
    action = Column(String(100))
    payload = Column(Text)
    correlation_id = Column(String(100))
    timestamp = Column(String(100))
