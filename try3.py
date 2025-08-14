import sqlite3
from fastapi import FastAPI, Query
import dropbox
import os
from dotenv import load_dotenv

load_dotenv()
DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")
DROPBOX_PATH = "/healthcare-data/test_db.sqlite"
LOCAL_DB = "downloaded_test.db"

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

metadata, res = dbx.files_download(DROPBOX_PATH)
with open(LOCAL_DB, "wb") as f:
    f.write(res.content)

app = FastAPI()

TABLE_NAME = "patients"

@app.get("/patients/self_aware")
def get_patients_by_ids(ids: str = Query(..., description="Comma-separated IDs")):
    id_list = [int(i.strip()) for i in ids.split(",")]
    conn = sqlite3.connect(LOCAL_DB)
    cur = conn.cursor()
    placeholders = ",".join("?" for _ in id_list)
    cur.execute(f"SELECT * FROM {TABLE_NAME} WHERE id IN ({placeholders})", id_list)
    rows = cur.fetchall()
    conn.close()
    
    print(f"Fetched rows for IDs {id_list}: {rows}")  
    return {"requested_ids": id_list, "rows": rows}

