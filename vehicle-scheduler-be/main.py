import httpx
from fastapi import FastAPI
from logger import log, get_header

app = FastAPI()

API_URL = "http://4.224.186.213/evaluation-service"

def efficient(vehicle, cap):
    n = len(vehicle)
    dp = [[0] * (cap + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        duration = vehicle[i-1]["Duration"]
        impact = vehicle[i-1]["Impact"]
        for j in range(cap + 1):
            dp[i][j] = dp[i-1][j]
            if duration <= j:
                dp[i][j] = max(dp[i][j], dp[i-1][j-duration] + impact)
    selected = []
    j = cap
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i-1][j]:
            selected.append(vehicle[i-1]["TaskID"])
            j -= vehicle[i-1]["Duration"]
    return dp[n][cap], selected

@app.get("/")
def health():
    log("backend", "info", "route", "Health check called")
    return {"Health": "Running successfully", "port": 8000}

@app.get("/schedule")
def schedule():
    log("backend", "info", "route", "GET /schedule called")

    log("backend", "info", "service", "Fetching depots from API")
    depot_res = httpx.get(f"{API_URL}/depots", headers=get_header())
    depots = depot_res.json()["depots"]
    log("backend", "info", "service", f"Fetched {len(depots)} depots")

    log("backend", "info", "service", "Fetching vehicles from API")
    vehicle_res = httpx.get(f"{API_URL}/vehicles", headers=get_header())
    vehicles = vehicle_res.json()["vehicles"]
    log("backend", "info", "service", f"Fetched {len(vehicles)} vehicles")

    results = []
    for depot in depots:
        depot_id = depot["ID"]
        cap = depot["MechanicHours"]
        log("backend", "info", "service", f"Running knapsack for depot {depot_id} with {cap} mechanic hours")
        total_impact, selected_tasks = efficient(vehicles, cap)
        log("backend", "info", "service", f"Depot {depot_id} - Total impact: {total_impact}, Tasks: {len(selected_tasks)}")
        results.append({
            "depotID": depot_id,
            "mechanicHours": cap,
            "totalImpact": total_impact,
            "selectedTasks": selected_tasks
        })

    log("backend", "info", "handler", "Schedule computed successfully for all depots")
    return {"results": results}