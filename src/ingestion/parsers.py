from datetime import datetime, timezone

def normalize_lm_alert(alert: dict) -> dict:
    return {
        "incident_id": str(alert.get("id")),
        "source": "logicmonitor",
        "severity": alert.get("severity", "unknown"),
        "resource": (
            alert.get("monitorObjectName")
            or alert.get("resourceName")
            or alert.get("instanceName")
            or "unknown"
        ),
        "rule": (
            alert.get("name")
            or alert.get("ruleName")
            or alert.get("monitorName")
            or "unknown"
        ),
        "message": (
            alert.get("message")
            or alert.get("alertValue")
            or "No message"
        ),
        "alert_status": alert.get("alertStatus", "unknown"),
        "start_epoch": alert.get("startEpoch"),
        "received_at": datetime.now(timezone.utc).isoformat()
    }

