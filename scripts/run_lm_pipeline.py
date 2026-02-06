import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.workflows.incident_pipeline import run_logicmonitor_pipeline

if __name__ == "__main__":
    run_logicmonitor_pipeline(limit=3)
    print("✅ LogicMonitor pipeline executed")



#if __name__ == "__main__":
#    payload = fetch_logicmonitor_alerts(limit=5)
#
#    print("\n========== RAW LOGICMONITOR RESPONSE ==========\n")
#    print(json.dumps(payload, indent=2))
#    print("\n=============================================\n")

