from fastapi import FastAPI
from HIS_A.his_a_data import HIS_A_DataCreator
from HIS_A.dropbox_utils import DropboxUploader
import os
from dotenv import load_dotenv

load_dotenv()
DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")
BASE_DROPBOX_PATH = "/healthcare-data/HIS_A/"

app = FastAPI()
creator = HIS_A_DataCreator()
uploader = DropboxUploader(DROPBOX_TOKEN)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/his_a/create_and_upload")
def create_and_upload():
    try:
        patients_db = creator.create_patients_db(rows=400)
        staff_db = creator.create_staff_db(rows=60)
        finance_db = creator.create_finance_db(rows=120)

        uploader.upload_file(patients_db, BASE_DROPBOX_PATH + "patients.db")
        uploader.upload_file(staff_db, BASE_DROPBOX_PATH + "staff.db")
        uploader.upload_file(finance_db, BASE_DROPBOX_PATH + "finance.db")

        return {
            "status": "success",
            "uploaded_files": [
                BASE_DROPBOX_PATH + "patients.db",
                BASE_DROPBOX_PATH + "staff.db",
                BASE_DROPBOX_PATH + "finance.db"
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
