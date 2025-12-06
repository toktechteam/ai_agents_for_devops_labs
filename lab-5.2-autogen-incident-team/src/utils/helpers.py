import json
import redis
from typing import Any, Dict, List

from src.utils.constants import REDIS_HOST, REDIS_PORT, REDIS_DB


def get_redis_client() -> redis.Redis:
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def cache_conversation(
    key: str,
    messages: List[Dict[str, Any]],
) -> None:
    """
    Store conversation messages in Redis for quick lookup and debugging.
    """
    client = get_redis_client()
    client.set(key, json.dumps(messages))


def load_conversation(key: str) -> List[Dict[str, Any]]:
    client = get_redis_client()
    data = client.get(key)
    if not data:
        return []
    try:
        return json.loads(data.decode("utf-8"))
    except Exception:
        return []
