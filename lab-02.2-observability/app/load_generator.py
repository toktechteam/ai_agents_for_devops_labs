import argparse
import time
import statistics
import requests


def run_load(url: str, count: int):
    latencies = []
    for i in range(count):
        t0 = time.time()
        r = requests.post(url, json={"features": [1, 2, 3]}, timeout=5)
        latencies.append((time.time() - t0) * 1000)

    print({
        "count": count,
        "avg_ms": round(statistics.mean(latencies), 2),
        "p95_ms": round(statistics.quantiles(latencies, n=20)[18], 2)
    })


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--count", type=int, default=50)
    args = ap.parse_args()
    run_load(args.url, args.count)
