import os

# LLM configuration
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

# PostgreSQL configuration (audit DB is configured in src/audit/db.py)
AUDIT_DB_URL = "postgresql://aiagent:aiagentpass@postgres:5432/auditdb"

# Default incident scenarios
DEFAULT_SCENARIOS = ["memory_leak", "cascading_failure"]
