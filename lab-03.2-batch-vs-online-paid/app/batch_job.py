import json
import time
from pathlib import Path
from typing import Dict, List

from config import get_settings
from otel_setup import setup_otel
from cost_model import estimate_batch_cost

DATA_PATH = Path(__file__).parent / "data" / "input.jsonl"

tracer, meter = setup_otel()
record_latency = meter.create_histogram("record_latency_ms")
batch_processing_time = meter.create_histogram("batch_processing_ms")
batch_records_count = meter.create_counter("batch_total_records")
batch_cost_metric = meter.create_histogram("batch_cost_usd")


def process_record(record: Dict) -> Dict:
    start = time.time()
    features = record["features"]
    prediction = float(sum(features))
    latency = (time.time() - start) * 1000
    record_latency.record(latency)
    return {"id": record["id"], "prediction": prediction}


def run_batch(path: Path = DATA_PATH) -> List[Dict]:
    settings = get_settings()

    start_batch = time.time()
    results = []

    with path.open("r") as f:
        for line in f:
            if not line.strip():
                continue

            rec = json.loads(line.strip())
            with tracer.start_as_current_span("process_record"):
                res = process_record(rec)
                results.append(res)

    batch_ms = (time.time() - start_batch) * 1000
    batch_processing_time.record(batch_ms)
    batch_records_count.add(len(results))

    # Cost calculation
    cost = estimate_batch_cost(len(results), settings.cost_per_1k_predictions)
    batch_cost_metric.record(cost)

    return results


def main():
    results = run_batch()
    for r in results:
        print(json.dumps(r))

    print(json.dumps({
        "summary": {
            "records": len(results),
            "estimated_cost_usd": estimate_batch_cost(
                len(results), get_settings().cost_per_1k_predictions
            )
        }
    }))


if __name__ == "__main__":
    main()
