from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")

DROPBOX_FILE_PATH = "/assembled_staff.json"   
DROPBOX_API_URL = "https://content.dropboxapi.com/2/files/download"

app = FastAPI(title="Staff API (Dropbox powered)")

class MultiQuery(BaseModel):
    contexts: list[str]  

def load_staff_data():
    """Fetch staff JSON file from Dropbox each time (fresh data)."""
    headers = {
        "Authorization": f"Bearer {DROPBOX_TOKEN}",
        "Dropbox-API-Arg": json.dumps({"path": DROPBOX_FILE_PATH})
    }
    response = requests.post(DROPBOX_API_URL, headers=headers)
    response.raise_for_status()
    return json.loads(response.content.decode("utf-8"))

@app.post("/search_multiple")
def search_multiple(query: MultiQuery):
    staff_data = load_staff_data()  
    results = []
    for sid in query.contexts:
        matched = [row for row in staff_data if str(row.get("staff_id")) == sid]
        matched_clean = [{k: v for k, v in row.items() if v not in [None, ""]} for row in matched]
        results.append({sid: matched_clean if matched_clean else "No matching data found"})
    return results


"""RESULTS :

INFO:     Application startup complete.
INFO:     127.0.0.1:53297 - "POST /search_multiple HTTP/1.1" 200 OK
"""

# Run with:
# uvicorn self_staff_api:app --reload --port 8001
