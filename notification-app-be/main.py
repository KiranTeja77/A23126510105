import httpx
from fastapi import FastAPI
from datetime import datetime
from logger import log, get_header

app = FastAPI()

API_URL = "http://4.224.186.213/evaluation-service"

TYPE_WEIGHT = {
    "Placement": 3,
    "Result": 2,
    "Event": 1
}

def get_score(notification):
    type_score = TYPE_WEIGHT.get(notification["Type"], 0)
    timestamp = datetime.fromisoformat(notification["Timestamp"].replace("Z", "+00:00"))
    now = datetime.now(timestamp.tzinfo)
    hours_old = (now - timestamp).total_seconds() / 3600
    score = 1 / (1 + hours_old)
    
    return type_score + score

@app.get("/")
def health():
    log("backend", "info", "route", "Health check called")
    return {"Health": "Running successfully", "port": 8000}

@app.get("/priority")
def priority_inbox():
    log("backend", "info", "route", "GET /priority called")

    log("backend", "info", "service", "Fetching notifications from API")
    res = httpx.get(f"{API_URL}/notifications", headers=get_header())
    notifications = res.json()["notifications"]
    log("backend", "info", "service", f"Fetched {len(notifications)} notifications")

    unread = [n for n in notifications if n["Message"] != ""]
    log("backend", "info", "service", f"Found {len(unread)} unread notifications")
    log("backend", "info", "service", "Scoring notifications by type and recency")
    scored = sorted(unread, key=get_score, reverse=True)

    top10 = scored[:10]
    log("backend", "info", "handler", "Returning top 10 priority notifications")

    return {
        "priorityInbox": [
            {
                "id": n["ID"],
                "type": n["Type"],
                "message": n["Message"],
                "timestamp": n["Timestamp"],
                "priorityScore": round(get_score(n), 4)
            }
            for n in top10
        ]
    }