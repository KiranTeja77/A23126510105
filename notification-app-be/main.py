from fastapi import FastAPI
from logger import log

app = FastAPI()

@app.get("/")
def health():
    log("backend", "info", "route", "Health check called")
    return {"Health" : "Running successfully", "port" : 8000}

