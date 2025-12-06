import os
from functools import lru_cache


class Settings:
    def __init__(self):
        self.app_env = os.getenv("APP_ENV", "local")
        self.cpu_burn_ms = int(os.getenv("CPU_BURN_MS", "40"))

    def dict(self):
        return {"app_env": self.app_env, "cpu_burn_ms": self.cpu_burn_ms}


@lru_cache
def get_settings():
    return Settings()
