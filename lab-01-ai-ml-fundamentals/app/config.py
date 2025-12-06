import os
from functools import lru_cache


class Settings:
    app_env: str
    default_latency_ms: int
    max_batch_size: int

    def __init__(self) -> None:
        self.app_env = os.getenv("APP_ENV", "local")
        self.default_latency_ms = int(os.getenv("DEFAULT_LATENCY_MS", "100"))
        self.max_batch_size = int(os.getenv("MAX_BATCH_SIZE", "1024"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
