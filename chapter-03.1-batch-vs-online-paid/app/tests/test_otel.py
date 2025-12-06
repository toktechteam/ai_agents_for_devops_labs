from otel_setup import setup_otel


def test_otel_initializes():
    tracer, meter = setup_otel()
    assert tracer is not None
    assert meter is not None

    # Create metric instruments to ensure no errors
    hist = meter.create_histogram("test_metric")
    hist.record(10)
