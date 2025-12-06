import requests


def prom_query(base_url, query):
    url = f"{base_url}/api/v1/query"
    resp = requests.get(url, params={"query": query})
    resp.raise_for_status()
    return resp.json()
