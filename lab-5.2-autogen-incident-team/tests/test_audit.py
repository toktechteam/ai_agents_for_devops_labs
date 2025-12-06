from src.audit.models import AuditRecord
from src.audit import logger as audit_logger


def test_audit_record_model_fields():
    rec = AuditRecord(
        agent="test_agent",
        action="test_action",
        payload="payload",
        correlation_id="abc-123",
        timestamp="2025-01-01T00:00:00Z",
    )

    assert rec.agent == "test_agent"
    assert rec.action == "test_action"
    assert rec.payload == "payload"
    assert rec.correlation_id == "abc-123"


def test_audit_log_uses_session_without_real_db():
    captured = {}

    def dummy_get_session():
        class DummySession:
            def __init__(self):
                self.add_called = False
                self.commit_called = False
                self.last_obj = None

            def add(self, obj):
                self.add_called = True
                self.last_obj = obj

            def commit(self):
                self.commit_called = True

        sess = DummySession()
        captured["session"] = sess
        return sess

    # Patch logger to use dummy session
    audit_logger.get_session = dummy_get_session

    result = audit_logger.audit_log(
        agent="unit_test_agent",
        action="unit_test_action",
        payload="test payload",
        correlation_id="cid-123",
    )

    assert result is True
    assert "session" in captured
    sess = captured["session"]
    assert sess.add_called is True
    assert sess.commit_called is True
    assert isinstance(sess.last_obj, AuditRecord)
