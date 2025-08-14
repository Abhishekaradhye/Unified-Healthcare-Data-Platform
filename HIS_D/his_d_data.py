import sqlite3
import os
from faker import Faker
from random import choice, randint, uniform
from datetime import date, timedelta

fake = Faker()

def _ensure_dir(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def _rand_date(start_year=1970, end_year=2024):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta = (end - start).days
    return (start + timedelta(days=randint(0, delta))).isoformat()

class HIS_D_DataCreator:
    def __init__(self, base_dir="tmp_his_d"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def create_patients_db(self, rows=400):
        path = os.path.join(self.base_dir, "patients.db")
        _ensure_dir(path)
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            name TEXT,
            dob TEXT,
            gender TEXT,
            blood_group TEXT,
            height_cm INTEGER,
            weight_kg INTEGER,
            location TEXT,
            contact TEXT,
            emergency_person TEXT,
            insurance_id TEXT,
            insurance_provider TEXT,
            primary_physician TEXT,
            medical_history TEXT,
            disease TEXT,
            patient_status TEXT,
            severity TEXT,
            department_admitted TEXT,
            current_department TEXT,
            bed_type TEXT,
            stage_danger TEXT,
            surgery_required TEXT,
            treatment_protocol TEXT,
            followup_date TEXT
        )
        """)

        depts = ["Oncology","Neurosurgery","TB Care","HIV Clinic","Radiotherapy","ICU"]
        statuses = ["Admitted","Discharged","Critical","Observation"]
        severities = ["Mild","Moderate","Severe","Critical", "treating"]
        bed_types = ["General","ICU","Severe Ward"]

        surgery_opts = ["Yes","No","Under Consideration"]

        for _ in range(rows):
            pid = fake.uuid4()[:8]
            c.execute("""
            INSERT INTO patients VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                pid,
                fake.name(),
                _rand_date(1930, 2022),
                choice(["Male","Female"]),
                choice(["A+","A-","B+","B-","O+","O-","AB+","AB-"]),
                randint(150, 200),
                randint(40, 120),
                f"{fake.city()}, {fake.state()}, {fake.country()}",
                f"{fake.phone_number()}, {fake.email()}",
                f"{fake.name()} ({choice(['Spouse','Parent','Sibling','Friend','Offspring'])})",
                f"INS{randint(10000,99999)}",
                choice(["ABC Insurance","XYZ Health","CarePlus","Aarogya Kavach"]),
                "Dr. " + fake.last_name(),
                choice(["Diabetes","Hypertension","Asthma","Cancer","HIV","TB"]),
                choice(["Flu","Covid-19","Fracture","Heart Disease","Cancer","Neural Disorder"]),
                choice(statuses),
                choice(severities),
                choice(depts),
                choice(depts),
                choice(bed_types),
                choice(["Stage I","Stage II","Stage III","Stage IV","Critical"]),
                choice(surgery_opts),
                choice(["Chemotherapy","Surgery","Medication","Radiotherapy","Observation"]),
                _rand_date(2024, 2026)
            ))

        conn.commit()
        conn.close()
        return path

    def create_staff_db(self, rows=100):
        path = os.path.join(self.base_dir, "staff.db")
        _ensure_dir(path)
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            staff_id TEXT PRIMARY KEY,
            name TEXT,
            dob TEXT,
            gender TEXT,
            position TEXT,
            department TEXT,
            contact TEXT,
            salary REAL,
            date_joined TEXT,
            specialization TEXT,
            experience_years INTEGER,
            certifications TEXT,
            shift TEXT,
            email TEXT,
            address TEXT,
            emergency_contact TEXT,
            emergency_relation TEXT
        )
        """)
        positions = ["Doctor","Nurse","Technician","Support Staff","Admin"]
        depts = ["Oncology","Neurosurgery","TB Care","HIV Clinic","Radiotherapy","ICU"]
        shifts = ["Day","Night","Rotational"]

        for _ in range(rows):
            sid = fake.uuid4()[:8]
            c.execute("""
            INSERT INTO staff VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                sid,
                fake.name(),
                _rand_date(1960, 2000),
                choice(["Male","Female"]),
                choice(positions),
                choice(depts),
                f"{fake.phone_number()}, {fake.email()}",
                round(uniform(30000,150000),2),
                _rand_date(2000,2024),
                choice(["Cancer","Neurosurgery","TB","HIV","Radiotherapy","ICU"]),
                randint(1,40),
                f"{fake.job()}, {fake.company()}",
                choice(shifts),
                fake.email(),
                f"{fake.city()}, {fake.state()}, {fake.country()}",
                fake.name(),
                choice(["Spouse","Parent","Sibling","Friend","Offspring"])
            ))
        conn.commit()
        conn.close()
        return path


    def create_finance_db(self, rows=200):
        path = os.path.join(self.base_dir, "finance.db")
        _ensure_dir(path)
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS finance (
            record_id TEXT PRIMARY KEY,
            patient_id TEXT,
            treatment_cost REAL,
            insurance_claim REAL,
            hospital_charges REAL,
            miscellaneous_charges REAL,
            tax REAL,
            discount REAL,
            payment_method TEXT,
            payment_status TEXT,
            date TEXT
        )
        """)
        payment_methods = ["Cash","Card","UPI","Insurance"]
        payment_status = ["Paid","Pending","Partial","Overdue"]

        for _ in range(rows):
            rid = fake.uuid4()[:8]
            pid = fake.uuid4()[:8]
            c.execute("""
            INSERT INTO finance VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (
                rid,
                pid,
                round(uniform(5000,200000),2),
                round(uniform(1000,100000),2),
                round(uniform(1000,50000),2),
                round(uniform(500,10000),2),
                round(uniform(100,5000),2),
                round(uniform(0,10000),2),
                choice(payment_methods),
                choice(payment_status),
                _rand_date(2020,2024)
            ))
        conn.commit()
        conn.close()
        return path
