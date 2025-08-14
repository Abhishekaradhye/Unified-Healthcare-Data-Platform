from fastapi import FastAPI
from HIS_C.his_c_data import HIS_C_DataCreator
from HIS_C.dropbox_utils import DropboxUploader
import os
from dotenv import load_dotenv

load_dotenv()
DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")
BASE_DROPBOX_PATH = "/healthcare-data/HIS_C/"

app = FastAPI()
creator = HIS_C_DataCreator()
uploader = DropboxUploader(DROPBOX_TOKEN)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/his_c/create_and_upload")
def create_and_upload():
    try:
        patients_csv = creator.create_patients_csv(rows=500)
        staff_csv = creator.create_staff_csv(rows=50)
        finance_csv = creator.create_finance_csv(rows=200)

        uploader.upload_file(patients_csv, BASE_DROPBOX_PATH + "patients.csv")
        uploader.upload_file(staff_csv, BASE_DROPBOX_PATH + "staff.csv")
        uploader.upload_file(finance_csv, BASE_DROPBOX_PATH + "finance.csv")

        return {
            "status": "success",
            "uploaded_files": [
                BASE_DROPBOX_PATH + "patients.csv",
                BASE_DROPBOX_PATH + "staff.csv",
                BASE_DROPBOX_PATH + "finance.csv"
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}