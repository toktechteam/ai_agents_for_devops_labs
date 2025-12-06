from src.clients.prom_client import prom_query


def prom_query_simple(config, redis_client, args):
    query = args["query"]
    cache_key = f"prom:{query}"

    cached = redis_client.get(cache_key)
    if cached:
        return {"cached": True, "data": cached}

    result = prom_query(config["prometheus"]["base_url"], query)
    redis_client.set(cache_key, str(result))
    return {"cached": False, "data": result}
