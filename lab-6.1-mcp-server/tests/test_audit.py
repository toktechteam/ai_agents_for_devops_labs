from src.audit.db import init_db, write_audit_log
from src.audit.models import AuditRecord
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def test_audit_write():
    db_cfg = {
        "host": "localhost",
        "port": 5432,
        "user": "aiagent",
        "password": "aiagentpass",
        "dbname": "mcpaudit"
    }

    init_db(db_cfg)

    example_req = {"method": "mcp.tools.list"}
    example_resp = {"jsonrpc": "2.0", "id": 1, "result": []}

    write_audit_log(example_req, example_resp)

    # Verify by connecting manually
    url = f"postgresql://{db_cfg['user']}:{db_cfg['password']}@{db_cfg['host']}:{db_cfg['port']}/{db_cfg['dbname']}"
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)

    sess = Session()
    rows = sess.query(AuditRecord).all()
    sess.close()

    assert len(rows) >= 1
