import argparse


def estimate_cost(node_hourly: float, nodes: int, hours: int) -> float:
    """
    Estimate monthly cost for a small lab cluster.

    This is intentionally simple. Example:
    - node_hourly = 0.01 USD
    - nodes = 1
    - hours = 20
    => 0.01 * 1 * 20 = 0.20 USD
    """
    return node_hourly * nodes * hours


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simple cost estimator for Lab 2.1 cluster"
    )
    parser.add_argument(
        "--node-hourly",
        type=float,
        default=0.01,
        help="Hourly cost per node in USD (default: 0.01)",
    )
    parser.add_argument(
        "--nodes",
        type=int,
        default=1,
        help="Number of nodes (default: 1)",
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=20,
        help="Total hours per month (default: 20)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cost = estimate_cost(args.node_hourly, args.nodes, args.hours)
    print(
        f"Estimated monthly cost: ${cost:.2f} "
        f"(node_hourly={args.node_hourly}, nodes={args.nodes}, hours={args.hours})"
    )
    if cost <= 10.0:
        print("✅ This design stays under the $10/month target.")
    else:
        print("⚠️ This design exceeds the $10/month target. Consider fewer nodes or hours.")


if __name__ == "__main__":
    main()
