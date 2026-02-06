import requests
from config.settings import settings

def send_teams_message(title: str, message: str):
    if not settings.TEAMS_WEBHOOK_URL:
        raise ValueError("TEAMS_WEBHOOK_URL not set in .env")

    payload = {
        "text": f"**{title}**\n\n{message}"
    }

    r = requests.post(settings.TEAMS_WEBHOOK_URL, json=payload, timeout=20)
    r.raise_for_status()
    return True
