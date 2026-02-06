import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.notifications.teams_notifier import send_teams_message

send_teams_message(
    title="Resolve AI Test ✅",
    message="Hello Tarak! Teams webhook is working 🎉"
)
print("✅ Teams message sent")
