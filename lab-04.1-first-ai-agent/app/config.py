import os
from functools import lru_cache


class Settings:
    def __init__(self) -> None:
        self.env = os.getenv("AGENT_ENV", "local")
        self.sqlite_path = os.getenv("EPISODIC_DB_PATH", "episodic_memory.db")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.use_llm = bool(self.openai_api_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()
