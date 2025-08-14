from fastapi import FastAPI
from HIS_B.his_b_data import HIS_B_DataCreator
from HIS_B.dropbox_utils import DropboxUploader
import os
from dotenv import load_dotenv

load_dotenv()
DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")
BASE_DROPBOX_PATH = "/healthcare-data/HIS_B/"

app = FastAPI()
creator = HIS_B_DataCreator()
uploader = DropboxUploader(DROPBOX_TOKEN)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/his_b/create_and_upload")
def create_and_upload():
    try:
        patients_path = creator.create_patients_json(rows=400)
        staff_path = creator.create_staff_json(rows=60)
        finance_path = creator.create_finance_json(rows=120)

        uploader.upload_file(patients_path, BASE_DROPBOX_PATH+"patients.json")
        uploader.upload_file(staff_path, BASE_DROPBOX_PATH+"staff.json")
        uploader.upload_file(finance_path, BASE_DROPBOX_PATH+"finance.json")

        return {
            "status": "success",
            "uploaded_files": [
                BASE_DROPBOX_PATH+"patients.json",
                BASE_DROPBOX_PATH+"staff.json",
                BASE_DROPBOX_PATH+"finance.json"
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
