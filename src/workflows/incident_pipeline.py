from src.ingestion.logicmonitor_poller import fetch_logicmonitor_alerts
from src.ingestion.parsers import normalize_lm_alert
from src.storage.dynamodb_store import IncidentStore
from src.ai.analyzer import analyze_incident, classify_alert
from src.ai.groq_client import GroqClient
from src.ai.correlation import build_correlation_key
from src.ai.correlator import IncidentCorrelator


def run_logicmonitor_pipeline(limit: int = 10):
    payload = fetch_logicmonitor_alerts(limit=limit)
    items = payload.get("data", {}).get("items", [])

    print(f"Fetched alerts: {len(items)}")

    store = IncidentStore()
    correlator = IncidentCorrelator()

    for alert in items:
        incident = normalize_lm_alert(alert)

        if store.exists(incident["incident_id"]):
            continue

        store.save(incident)

        alert_type = classify_alert(incident)
        key = build_correlation_key(incident, alert_type)
        correlator.add(key, incident)

    for key, incidents in correlator.get_groups().items():
        primary = incidents[0]
        ai = analyze_incident(primary)

        correlated = {
            **primary,
            "resource": ", ".join(i["resource"] for i in incidents),
            "message": f"{len(incidents)} related alerts detected"
        }

        groq_text = None
        try:
            groq_text = GroqClient().analyze_incident(correlated, ai)
        except Exception as e:
            print("Groq skipped:", e)

        store.save_ai_insight(primary["incident_id"], ai, groq_text)


