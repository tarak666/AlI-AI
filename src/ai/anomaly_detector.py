from datetime import datetime, timedelta, timezone


class AnomalyDetector:
    def __init__(self, incidents: list):
        self.incidents = incidents

    def frequency_anomaly(self, minutes=30, threshold=3):
        now = datetime.now(timezone.utc)  # ✅ timezone-aware
        recent = []

        for i in self.incidents:
            ts = i.get("received_at")
            if not ts:
                continue

            try:
                t = datetime.fromisoformat(ts)
                if t.tzinfo is None:
                    t = t.replace(tzinfo=timezone.utc)
            except Exception:
                continue

            if now - t <= timedelta(minutes=minutes):
                recent.append(i)

        return len(recent) >= threshold

    def repeating_resource(self, threshold=3):
        count = {}
        for i in self.incidents:
            r = i.get("resource")
            if not r:
                continue
            count[r] = count.get(r, 0) + 1

        return [r for r, c in count.items() if c >= threshold]
