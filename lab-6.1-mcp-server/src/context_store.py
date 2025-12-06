import redis


def init_redis(config):
    return redis.Redis(host=config["host"], port=config["port"], db=config["db"], decode_responses=True)


def get_ctx(redis_client, key):
    return redis_client.get(f"ctx:{key}")


def set_ctx(redis_client, key, value):
    redis_client.set(f"ctx:{key}", value)
