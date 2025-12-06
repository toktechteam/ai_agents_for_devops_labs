import os

LOG_PATH = "/var/log/"
LOG_FILE = "syslog"


def log_search(args):
    term = args["term"]
    max_lines = int(args.get("max_lines", 50))
    path = os.path.join(LOG_PATH, LOG_FILE)

    if not os.path.exists(path):
        # In container or dev environments, syslog may not exist.
        # For safety and portability, just return an empty list.
        return []

    results = []
    with open(path, "r", errors="ignore") as f:
        for line in f:
            if term in line:
                results.append(line.strip())
                if len(results) >= max_lines:
                    break

    return results
