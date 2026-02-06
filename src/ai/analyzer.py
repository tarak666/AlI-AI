from src.ai.models import AIInsight


def analyze_incident(incident: dict) -> AIInsight:
    msg = str(incident.get("message", "")).lower()
    rule = str(incident.get("rule", "")).lower()
    resource = incident.get("resource", "unknown")

    root_cause = "Insufficient data to determine exact root cause"
    fixes = ["Check system logs", "Validate recent changes"]
    prevention = ["Improve monitoring thresholds"]
    confidence = "low"

    if "license" in msg:
        root_cause = (
            f"License associated with {resource} is nearing expiration or has "
            f"exceeded allocated capacity based on alert conditions."
        )
        fixes = [
            "Check license expiration date",
            "Renew or extend the license",
            "Verify license allocation and usage"
        ]
        prevention = [
            "Configure early license expiry alerts",
            "Track license usage trends"
        ]
        confidence = "high"

    elif "cpu" in msg or "cpu" in rule:
        root_cause = (
            f"CPU utilization on {resource} exceeded the configured threshold "
            f"for a sustained duration."
        )
        fixes = [
            "Identify high CPU processes",
            "Scale compute resources",
            "Review recent deployments"
        ]
        prevention = [
            "Enable autoscaling",
            "Tune CPU alert thresholds"
        ]
        confidence = "high"

    elif "memory" in msg or "mem" in rule:
        root_cause = (
            f"Memory utilization on {resource} exceeded safe operating limits."
        )
        fixes = [
            "Identify memory-heavy processes",
            "Increase memory allocation",
            "Check for memory leaks"
        ]
        prevention = [
            "Enable memory monitoring",
            "Set early warning alerts"
        ]
        confidence = "high"

    elif "disk" in msg:
        root_cause = (
            f"Disk usage on {resource} crossed the alert threshold."
        )
        fixes = [
            "Clean up unused files",
            "Expand disk volume",
            "Identify abnormal disk usage"
        ]
        prevention = [
            "Implement disk monitoring",
            "Schedule cleanup jobs"
        ]
        confidence = "high"

    return AIInsight(
        incident_id=incident["incident_id"],
        summary=f"Issue detected on {resource}",
        root_cause=root_cause,
        suggested_fixes=fixes,
        prevention_steps=prevention,
        confidence=confidence
    )


def classify_alert(incident: dict) -> str:
    msg = str(incident.get("message", "")).lower()
    rule = str(incident.get("rule", "")).lower()

    if "license" in msg:
        return "license"
    if "cpu" in msg or "cpu" in rule:
        return "cpu"
    if "memory" in msg or "mem" in rule:
        return "memory"
    if "disk" in msg:
        return "disk"
    return "generic"
