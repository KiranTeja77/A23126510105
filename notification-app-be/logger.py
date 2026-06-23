import httpx
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

AUTH_URL = "http://4.224.186.213/evaluation-service/auth"
LOG_URL = "http://4.224.186.213/evaluation-service/logs"

AUTH_BODY = {
    "email": os.getenv("EMAIL"),
    "name": os.getenv("NAME"),
    "rollNo": os.getenv("ROLL_NO"),
    "accessCode": os.getenv("ACCESS_CODE"),
    "clientID": os.getenv("CLIENT_ID"),
    "clientSecret": os.getenv("CLIENT_SECRET")
}

token = None
token_expiry = 0

def get_token():
    global token, token_expiry
    res = httpx.post(AUTH_URL, json=AUTH_BODY)
    data = res.json()
    token = data["access_token"]
    token_expiry = data["expires_in"]

def get_header():
    if token is None or datetime.now().timestamp() >= token_expiry:
        get_token()
    return {"Authorization": f"Bearer {token}"}

def log(stack, level, package, message):
    body = {"stack": stack, "level": level, "package": package, "message": message}
    try:
        response = httpx.post(LOG_URL, json=body, headers=get_header())
        return response.json()
    except Exception as e:
        print("Error:", e)
