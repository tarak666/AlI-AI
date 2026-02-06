from src.ai.groq_client import GroqClient


class AnomalyExplainer:
    def __init__(self):
        self.llm = GroqClient()

    def explain(
        self,
        frequency_spike: bool,
        repeating_resources: list,
        total_incidents: int
    ) -> str:

        summary_parts = []

        if frequency_spike:
            summary_parts.append(
                f"A sudden spike in incidents was detected "
                f"(total incidents: {total_incidents})."
            )

        if repeating_resources:
            summary_parts.append(
                f"The following resources are repeatedly alerting: "
                f"{', '.join(repeating_resources)}."
            )

        if not summary_parts:
            return "No significant anomalies detected at this time."

        context = " ".join(summary_parts)

        prompt = f"""
You are a senior SRE.

An anomaly has been detected in the monitoring system.

Context:
{context}

Explain:
1. Likely causes
2. What to check immediately
3. Whether this could be systemic
4. Clear next actions

Be concise, practical, and operational.
"""

        response = self.llm.raw_prompt(prompt)
        return response
