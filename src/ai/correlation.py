from datetime import datetime, timedelta


def build_correlation_key(incident: dict, alert_type: str) -> str:
    """
    Groups alerts into logical incidents
    """
    resource_scope = incident["resource"].split(":")[0]  # e.g. EU-W1
    rule_family = incident["rule"].split("-")[0]

    return f"{alert_type}|{resource_scope}|{rule_family}"
