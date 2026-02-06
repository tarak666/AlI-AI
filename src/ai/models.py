from dataclasses import dataclass
from typing import List


@dataclass
class AIInsight:
    incident_id: str
    summary: str
    root_cause: str
    suggested_fixes: List[str]
    prevention_steps: List[str]
    confidence: str
