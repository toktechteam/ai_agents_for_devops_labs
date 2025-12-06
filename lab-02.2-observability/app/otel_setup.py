from opentelemetry import trace, metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader


def configure_otel(service_name: str = "ai-lab-2-2-paid"):
    resource = Resource.create({"service.name": service_name})

    # Tracing
    trace_provider = TracerProvider(resource=resource)
    span_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces")
    trace_provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(trace_provider)

    # Metrics
    metric_exporter = OTLPMetricExporter(
        endpoint="http://otel-collector:4318/v1/metrics"
    )
    reader = PeriodicExportingMetricReader(metric_exporter)
    metrics_provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(metrics_provider)

    return trace.get_tracer(__name__), metrics.get_meter(__name__)
