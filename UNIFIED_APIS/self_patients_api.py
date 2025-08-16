from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")

DROPBOX_FILE_PATH = "/assembled_patients.json"  
DROPBOX_API_URL = "https://content.dropboxapi.com/2/files/download"

app = FastAPI(title="Patients API")

class MultiQuery(BaseModel):
    contexts: list[str] 

def load_patients_data():
    """Fetch patients JSON file from Dropbox each time (fresh data)."""
    headers = {
        "Authorization": f"Bearer {DROPBOX_TOKEN}",
        "Dropbox-API-Arg": json.dumps({"path": DROPBOX_FILE_PATH})
    }
    response = requests.post(DROPBOX_API_URL, headers=headers)
    response.raise_for_status()
    return json.loads(response.content.decode("utf-8"))

@app.post("/search_multiple")
def search_multiple(query: MultiQuery):
    patients_data = load_patients_data()  
    results = []
    for pid in query.contexts:
        matched = [row for row in patients_data if str(row.get("patient_id")) == pid]
        matched_clean = [{k: v for k, v in row.items() if v not in [None, ""]} for row in matched]
        results.append({pid: matched_clean if matched_clean else "No matching data found"})
    return results


"""RESULTS :

INFO:     Application startup complete.
INFO:     127.0.0.1:52198 - "POST /search_multiple HTTP/1.1" 200 OK
"""

# Run with:
# uvicorn self_patients_api:app --reload --port 8000
