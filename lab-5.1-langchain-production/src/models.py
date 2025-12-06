from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    alert = Column(String(255))
    result = Column(Text)
    logs = Column(Text)
    metrics = Column(Text)
    remediation = Column(Text)
    cost = Column(Float)


## Your DB will need table creation.
## You can add this after first startup:
#from src.models import Base
#from src.db import engine
#Base.metadata.create_all(engine)