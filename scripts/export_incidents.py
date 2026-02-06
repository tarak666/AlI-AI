import boto3
import csv
from config.settings import settings

ddb = boto3.resource("dynamodb", region_name=settings.AWS_REGION)
table = ddb.Table(settings.DDB_TABLE_NAME)

resp = table.scan()
items = resp.get("Items", [])

with open("resolve_ai_incidents.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "incident_id",
        "resource",
        "severity",
        "ai_root_cause",
        "ai_confidence",
        "received_at",
        "ai_analyzed_at"
    ])

    for i in items:
        writer.writerow([
            i.get("incident_id"),
            i.get("resource"),
            i.get("severity"),
            i.get("ai_root_cause"),
            i.get("ai_confidence"),
            i.get("received_at"),
            i.get("ai_analyzed_at")
        ])

print("✅ Exported resolve_ai_incidents.csv")
