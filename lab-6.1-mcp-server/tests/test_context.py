from src.context_store import set_ctx, get_ctx, init_redis


def test_context_write_read():
    client = init_redis({"host": "localhost", "port": 6379, "db": 0})

    set_ctx(client, "unit-test-key", "hello-world")
    value = get_ctx(client, "unit-test-key")

    assert value == "hello-world"
