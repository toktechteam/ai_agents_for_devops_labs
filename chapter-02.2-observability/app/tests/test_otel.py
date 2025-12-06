from otel_setup import configure_otel


def test_otel_initialization():
    """
    Ensures OTel tracer & meter initialize without errors.
    No real collector connection is attempted during tests.
    """
    tracer, meter = configure_otel("test-service")

    # Basic sanity checks
    assert tracer is not None
    assert meter is not None

    # Ensure tracer has a valid class name
    assert tracer.__class__.__name__.lower().find("tracer") != -1

    # Ensure meter has a valid class name
    assert meter.__class__.__name__.lower().find("meter") != -1


def test_otel_histogram_creation():
    """Ensure histogram instrument is created successfully."""
    tracer, meter = configure_otel("test-service")

    hist = meter.create_histogram(
        name="test_latency_ms",
        description="Testing histogram"
    )

    assert hist is not None

    # Ensure .record() does not raise errors
    hist.record(12.5)
    hist.record(50)
