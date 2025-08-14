from fastapi import FastAPI, HTTPException, Query
import sqlite3
import dropbox
import io
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_TOKEN")
DROPBOX_PATH = "/healthcare-data/test_db.sqlite"  
LOCAL_DB = "temp_local.db"
TABLE_NAME = "patients"

def create_and_upload_db():
    conn = sqlite3.connect(LOCAL_DB)
    cur = conn.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            city TEXT,
            condition TEXT
        )
    """)
    data = [(f"Patient{i}", 20+i, f"City{i}", f"Condition{i}") for i in range(1,11)]
    cur.executemany(f"INSERT INTO {TABLE_NAME} (name, age, city, condition) VALUES (?, ?, ?, ?)", data)
    conn.commit()
    conn.close()
    print(f"Created local DB '{LOCAL_DB}' with {len(data)} rows.")

    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open(LOCAL_DB, "rb") as f:
        dbx.files_upload(f.read(), DROPBOX_PATH, mode=dropbox.files.WriteMode("overwrite"))
    print(f"Uploaded DB to Dropbox at '{DROPBOX_PATH}'.")


app = FastAPI()
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def get_db_connection():
    metadata, res = dbx.files_download(DROPBOX_PATH)
    file_like = io.BytesIO(res.content)
    conn = sqlite3.connect(":memory:")  
    conn.executescript(file_like.getvalue().decode(errors='ignore'))
    return conn

@app.get("/patients")
def get_patient(id: int = Query(None), name: str = Query(None)):
    if id is None and name is None:
        raise HTTPException(status_code=400, detail="Provide id or name")

    conn = get_db_connection()
    cur = conn.cursor()
    if id is not None:
        cur.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = ?", (id,))
    else:
        cur.execute(f"SELECT * FROM {TABLE_NAME} WHERE name = ?", (name,))
    row = cur.fetchone()
    conn.close()

    if row:
        return {"patient": row}
    else:
        raise HTTPException(status_code=404, detail="Not found")

@app.get("/patients/all")
def get_all_patients():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {TABLE_NAME}")
    all_rows = cur.fetchall()
    conn.close()
    return {"patients": all_rows}

if __name__ == "__main__":
    create_and_upload_db()  
    uvicorn.run(app, host="127.0.0.1", port=8000)  
