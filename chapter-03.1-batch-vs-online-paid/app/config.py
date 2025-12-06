import os
from functools import lru_cache

class Settings:
    def __init__(self):
        self.cpu_burn_ms = int(os.getenv("CPU_BURN_MS", "20"))
        self.cost_per_1k_predictions = float(os.getenv("COST_PER_1K_PRED", "0.002"))

@lru_cache
def get_settings():
    return Settings()
