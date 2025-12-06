from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.audit.models import Base, AuditRecord


_engine = None
_Session = None


def init_db(db_cfg):
    global _engine, _Session
    url = f"postgresql://{db_cfg['user']}:{db_cfg['password']}@{db_cfg['host']}:{db_cfg['port']}/{db_cfg['dbname']}"

    _engine = create_engine(url)
    Base.metadata.create_all(_engine)
    _Session = sessionmaker(bind=_engine)


def write_audit_log(request, response):
    session = _Session()
    try:
        record = AuditRecord(
            method=request.get("method"),
            request_json=str(request),
            response_json=str(response)
        )
        session.add(record)
        session.commit()
    finally:
        session.close()
