from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
import requests
from dotenv import load_dotenv

# Load token from .env
load_dotenv()
DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")

# Dropbox file path for finance JSON
DROPBOX_FILE_PATH = "/assembled_finance_dataframe.json"   # must start with "/"
DROPBOX_API_URL = "https://content.dropboxapi.com/2/files/download"

app = FastAPI(title="Finance API (Dropbox powered)")

class MultiQuery(BaseModel):
    contexts: list[str]  # list of transaction_ids or patient_ids

def load_finance_data():
    """Fetch finance JSON file from Dropbox each time (fresh data)."""
    headers = {
        "Authorization": f"Bearer {DROPBOX_TOKEN}",
        "Dropbox-API-Arg": json.dumps({"path": DROPBOX_FILE_PATH})
    }
    response = requests.post(DROPBOX_API_URL, headers=headers)
    response.raise_for_status()
    return json.loads(response.content.decode("utf-8"))

@app.post("/search_multiple")
def search_multiple(query: MultiQuery):
    finance_data = load_finance_data()  # always fresh from Dropbox
    results = []
    for ctx in query.contexts:
        # allow searching by transaction_id or patient_id
        matched = [
            row for row in finance_data 
            if str(row.get("transaction_id")) == ctx or str(row.get("patient_id")) == ctx
        ]
        matched_clean = [{k: v for k, v in row.items() if v not in [None, ""]} for row in matched]
        results.append({ctx: matched_clean if matched_clean else "No matching data found"})
    return results



""" RESULTS :

INFO:     Application startup complete.
INFO:     127.0.0.1:50837 - "POST /search_multiple HTTP/1.1" 200 OK
INFO:     127.0.0.1:50850 - "POST /search_multiple HTTP/1.1" 200 OK
"""

# Run with:
# uvicorn self_finance_api:app --reload --port 8002
