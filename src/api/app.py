from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from src.storage.dynamodb_store import IncidentStore
from src.workflows.incident_pipeline import run_logicmonitor_pipeline
import threading
from src.ai.anomaly_detector import AnomalyDetector
from src.ai.anomaly_explainer import AnomalyExplainer




app = FastAPI(title="Cloud-ALI AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parents[1]
UI_DIR = BASE_DIR / "ui"
store = IncidentStore()


@app.get("/api/incidents")
def get_incidents():
    items = store.get_all()

    # Sort newest first
    items.sort(key=lambda x: x.get("received_at", ""), reverse=True)

    return items



@app.post("/api/run")
def run_pipeline():
    threading.Thread(target=run_logicmonitor_pipeline, daemon=True).start()
    return {"status": "started"}


@app.get("/dashboard", response_class=HTMLResponse)
@app.get("/", response_class=HTMLResponse)
def dashboard():
    return (UI_DIR / "dashboard.html").read_text()
@app.get("/api/anomaly")
def anomaly_api():
    items = store.get_all()

    detector = AnomalyDetector(items)
    explainer = AnomalyExplainer()

    anomaly_data = {
        "total_incidents": len(items),
        "frequency_spike": detector.frequency_anomaly(),
        "repeating_resources": detector.repeating_resource(),
    }

    # Optional: explain anomalies using Groq-style text
    anomaly_data["explanation"] = explainer.explain(
    frequency_spike=anomaly_data["frequency_spike"],
    repeating_resources=anomaly_data["repeating_resources"],
    total_incidents=anomaly_data["total_incidents"],
)


    return anomaly_data
@app.get("/anomaly", response_class=HTMLResponse)
def anomaly_page():
    html = UI_DIR / "anomaly.html"

    if not html.exists():
        return HTMLResponse(
            content="<h3>anomaly.html not found</h3>",
            status_code=500
        )

    return html.read_text()


