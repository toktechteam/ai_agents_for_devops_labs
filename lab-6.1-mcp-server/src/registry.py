import yaml

TOOL_REGISTRY_GLOBAL = {}


def load_tool_registry(path):
    global TOOL_REGISTRY_GLOBAL
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    for tool in data["tools"]:
        TOOL_REGISTRY_GLOBAL[tool["name"]] = tool

    return data["tools"]
