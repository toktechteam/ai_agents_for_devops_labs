import datetime
from src.audit.db import get_session
from src.audit.models import AuditRecord


def audit_log(agent: str, action: str, payload: str, correlation_id: str):
    """
    Stores every agent action, prompt, and decision in PostgreSQL.
    """

    session = get_session()

    record = AuditRecord(
        agent=agent,
        action=action,
        payload=payload,
        correlation_id=correlation_id,
        timestamp=str(datetime.datetime.utcnow()),
    )

    session.add(record)
    session.commit()

    return True
