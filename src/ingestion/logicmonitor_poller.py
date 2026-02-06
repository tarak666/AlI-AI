import requests
from config.settings import settings


def fetch_logicmonitor_alerts(limit: int = 10):
    """
    Fetch recent alerts from LogicMonitor using Bearer token auth.
    """
    if not settings.LM_COMPANY:
        raise ValueError("LM_COMPANY not set in .env")

    if not settings.LM_BEARER_TOKEN:
        raise ValueError("LM_BEARER_TOKEN not set in .env")

    resource_path = "/alert/alerts"
    url = f"https://{settings.LM_COMPANY}.logicmonitor.com/santaba/rest{resource_path}"

    headers = {
        "Authorization": f"Bearer {settings.LM_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }

    params = {
        "size": limit,
        "sort": "-startEpoch"
    }

    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

