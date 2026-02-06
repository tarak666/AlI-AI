from collections import defaultdict


class IncidentCorrelator:
    def __init__(self):
        self.groups = defaultdict(list)

    def add(self, key: str, incident: dict):
        self.groups[key].append(incident)

    def get_groups(self):
        return self.groups
