import argparse
import json
import threading
import time
from dataclasses import dataclass, field
from statistics import mean
from typing import List

import requests


@dataclass
class Stats:
    latencies: List[float] = field(default_factory=list)
    errors: int = 0


def worker(url: str, requests_per_worker: int, stats: Stats) -> None:
    payload = {"features": [0.5, 1.5, 2.0]}
    for _ in range(requests_per_worker):
        t0 = time.time()
        try:
            resp = requests.post(url, json=payload, timeout=5)
            latency_ms = (time.time() - t0) * 1000.0
            if resp.status_code == 200:
                stats.latencies.append(latency_ms)
            else:
                stats.errors += 1
        except Exception:
            stats.errors += 1


def run_load(url: str, total_requests: int, concurrency: int) -> None:
    stats = Stats()
    threads: List[threading.Thread] = []

    per_worker = max(1, total_requests // concurrency)
    remaining = total_requests - (per_worker * concurrency)

    start = time.time()
    for i in range(concurrency):
        # Distribute remaining requests to the first few workers
        extra = 1 if i < remaining else 0
        t = threading.Thread(
            target=worker,
            args=(url, per_worker + extra, stats),
            daemon=True,
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    total_time = time.time() - start

    if stats.latencies:
        avg_latency = mean(stats.latencies)
        p95 = sorted(stats.latencies)[int(0.95 * len(stats.latencies)) - 1]
    else:
        avg_latency = 0.0
        p95 = 0.0

    summary = {
        "url": url,
        "total_requests": total_requests,
        "concurrency": concurrency,
        "total_time_sec": round(total_time, 3),
        "avg_latency_ms": round(avg_latency, 2),
        "p95_latency_ms": round(p95, 2),
        "errors": stats.errors,
    }
    print(json.dumps(summary))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Concurrent load generator for Lab 2.1 PAID API"
    )
    parser.add_argument(
        "--url",
        required=True,
        help="Target /predict URL (e.g. http://localhost:9001/predict)",
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=50,
        help="Total number of requests (default: 50)",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=5,
        help="Number of concurrent workers (default: 5)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_load(args.url, args.requests, args.concurrency)


if __name__ == "__main__":
    main()
