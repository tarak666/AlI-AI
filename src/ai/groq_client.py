import requests
from config.settings import settings


class GroqClient:
    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not set")

        self.api_key = settings.GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    def analyze_incident(self, incident: dict, rule_ai, alert_type: str = "generic"):
        prompt = f"""
            You are a senior Site Reliability Engineer responding to a production incident.

            Write a clear, structured incident response.

            Incident Context:
            Resource(s): {incident['resource']}
            Severity: {incident.get('severity')}
            Rule: {incident.get('rule')}
            Message: {incident.get('message')}

            Rule-Based Assessment:
            {rule_ai.root_cause}

            RESPONSE FORMAT:

            **Incident Summary**
            Describe what is happening and the impact.

            **Root Cause Analysis**
            Explain the most likely root cause using available evidence.
            If evidence is missing, explicitly state what is missing.

            **Why This Alert Triggered**
            Explain the alert condition that was breached.

            **Recommended Fixes**
            Provide actionable remediation steps.

            **Prevention & Follow-up**
            How to prevent recurrence.

            **Escalation Guidance**
            When and who to escalate to.
            """

        return self._send(prompt)
    def raw_prompt(self, prompt: str) -> str:
        return self._send(prompt)

    def _send(self, prompt: str) -> str:
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a senior SRE."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        r = requests.post(self.base_url, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
 
    