from src.clients.k8s_client import load_k8s


def list_pods(config, args):
    namespace = args.get("namespace", "default")
    api = load_k8s()
    pods = api.list_namespaced_pod(namespace=namespace)
    return [p.metadata.name for p in pods.items]
