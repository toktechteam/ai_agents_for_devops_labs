import os
from functools import lru_cache


class Settings:
    def __init__(self) -> None:
        self.app_env = os.getenv("APP_ENV", "local")
        self.cpu_burn_ms = int(os.getenv("CPU_BURN_MS", "50"))
        self.max_batch_size = int(os.getenv("MAX_BATCH_SIZE", "1024"))

    def to_dict(self) -> dict:
        return {
            "app_env": self.app_env,
            "cpu_burn_ms": self.cpu_burn_ms,
            "max_batch_size": self.max_batch_size,
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
