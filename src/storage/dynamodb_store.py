import boto3
from datetime import datetime, timezone
from config.settings import settings


class IncidentStore:
    def __init__(self):
        self.ddb = boto3.resource(
            "dynamodb",
            region_name=settings.AWS_REGION
        )

        # ✅ SINGLE SOURCE OF TRUTH
        self.table = self.ddb.Table(settings.DDB_TABLE_NAME)

    # ---------------------------
    # Check if incident exists
    # ---------------------------
    def exists(self, incident_id: str) -> bool:
        resp = self.table.get_item(
            Key={"incident_id": incident_id}
        )
        return "Item" in resp

    # ---------------------------
    # Save raw incident
    # ---------------------------
    def save(self, incident: dict):
        self.table.put_item(
            Item={
                "incident_id": incident["incident_id"],
                "source": incident.get("source", "logicmonitor"),
                "severity": incident.get("severity"),
                "resource": incident.get("resource"),
                "rule": incident.get("rule"),
                "message": incident.get("message"),
                "alert_status": incident.get("alert_status"),
                "received_at": incident.get("received_at"),
            }
        )

    # ---------------------------
    # Save AI + Groq insight
    # ---------------------------
    def save_ai_insight(self, incident_id: str, ai, groq_text: str | None = None):
        update_expr = """
            SET
            rca_rule = :rca,
            confidence = :conf,
            ai_updated_at = :ts
        """

        values = {
            ":rca": ai.root_cause,
            ":conf": ai.confidence,
            ":ts": datetime.now(timezone.utc).isoformat()
        }

        if groq_text:
            update_expr += """,
            groq_raw = :graw
            """
            values[":graw"] = groq_text

        self.table.update_item(
            Key={"incident_id": incident_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=values
        )


    # ---------------------------
    # Fetch all incidents (API)
    # ---------------------------
    def get_all(self):
        resp = self.table.scan()
        return resp.get("Items", [])

