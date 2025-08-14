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

class HIS_A_DataCreator:
    def __init__(self, base_dir="tmp_his_a"):
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
            first_name TEXT,
            last_name TEXT,
            dob TEXT,
            gender TEXT,
            blood_group TEXT,
            height_cm INTEGER,
            weight_kg INTEGER,
            country TEXT,
            state TEXT,
            city TEXT,
            postal_code TEXT,
            phone TEXT,
            email TEXT,
            emergency_contact_name TEXT,
            emergency_contact_relation TEXT,
            emergency_contact_phone TEXT,
            insurance_id TEXT,
            insurance_provider TEXT,
            primary_physician TEXT,
            medical_history TEXT,
            disease TEXT,
            patient_status TEXT,
            severity TEXT,
            department_admitted TEXT,
            current_department TEXT,
            bed_type TEXT
        )
        """)
        depts = ["Cardiology","Radiology","Orthopedics","Emergency","Oncology","Pediatrics","Neurology","Gastroenterology"]
        statuses = ["Admitted","Discharged","Critical","Observation"]
        severities = ["Mild","Moderate","Severe","Critical","treating"]
        bed_types = ["General","ICU","Severe Ward"]

        for _ in range(rows):
            pid = fake.uuid4()[:8]
            c.execute("""
            INSERT INTO patients VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                pid,
                fake.first_name(),
                fake.last_name(),
                _rand_date(1930, 2022),
                choice(["Male","Female"]),
                choice(["A+","A-","B+","B-","O+","O-","AB+","AB-"]),
                randint(150, 200),
                randint(40, 120),
                "India",
                "Maharashtra",
                choice(["Pune","Mumbai","Nagpur","Nashik","Nanded","Kolhapur","Ahmedabad","Delhi","Bidar"]),
                fake.postcode(),
                fake.msisdn(),
                fake.email(),
                fake.name(),
                choice(["Spouse","Parent","Sibling","Friend","Offspring"]),
                fake.msisdn(),
                f"INS{randint(10000,99999)}",
                choice(["ABC Insurance","XYZ Health","CarePlus","Aarogya Kavach"]),
                "Dr. " + fake.last_name(),
                choice(["Diabetes","Hypertension","Asthma","None"]),
                choice(["Flu","Covid-19","Fracture","Heart Disease","Malaria"]),
                choice(statuses),
                choice(severities),
                choice(depts),
                choice(depts),
                choice(bed_types)
            ))

        conn.commit()
        conn.close()
        return path

    def create_staff_db(self, rows=60):
        path = os.path.join(self.base_dir, "staff.db")
        _ensure_dir(path)
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            staff_id TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            dob TEXT,
            gender TEXT,
            department TEXT,
            designation TEXT,
            joining_date TEXT,
            salary INTEGER,
            phone TEXT,
            email TEXT,
            address_line1 TEXT,
            address_line2 TEXT,
            city TEXT,
            state TEXT,
            country TEXT,
            postal_code TEXT,
            emergency_contact_name TEXT,
            emergency_contact_relation TEXT,
            emergency_contact_phone TEXT,
            work_shift TEXT
        )
        """)
        depts = ["Cardiology","Radiology","Orthopedics","Emergency","Oncology","Pediatrics"]
        roles = ["Doctor","Senior Nurse","Technician","Resident","Admin"]
        shifts = ["Morning","Evening","Night"]

        for _ in range(rows):
            sid = "S" + fake.uuid4()[:7]
            c.execute("""
            INSERT INTO staff VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                sid,
                fake.first_name(),
                fake.last_name(),
                _rand_date(1958, 2001),
                choice(["Male","Female"]),
                choice(depts),
                choice(roles),
                _rand_date(2005, 2025),
                randint(30000, 150000),
                fake.msisdn(),
                fake.company_email(),
                fake.street_address(),
                fake.secondary_address(),
                choice(["Pune","Mumbai","Nagpur","Nashik"]),
                "Maharashtra",
                "India",
                fake.postcode(),
                fake.name(),
                choice(["Spouse","Parent","Sibling","Friend"]),
                fake.msisdn(),
                choice(shifts)
            ))

        conn.commit()
        conn.close()
        return path

    def create_finance_db(self, rows=120):
        path = os.path.join(self.base_dir, "finance.db")
        _ensure_dir(path)
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS finance (
            transaction_id TEXT PRIMARY KEY,
            patient_id TEXT,
            billing_date TEXT,
            amount REAL,
            currency TEXT,
            payment_method TEXT,
            insurance_claimed TEXT,
            insurance_id TEXT,
            insurance_provider TEXT,
            service_code TEXT,
            service_description TEXT,
            department TEXT,
            staff_id TEXT,
            discount_applied REAL,
            net_amount REAL,
            tax REAL,
            total_amount REAL,
            payment_status TEXT,
            due_date TEXT,
            receipt_number TEXT
        )
        """)
        pay_methods = ["UPI","Credit Card","Debit Card","Cash"]
        statuses = ["Paid","Unpaid","Pending"]
        depts = ["Radiology","Orthopedics","Emergency","Oncology","Pediatrics"]
        services = [("SRV100","Consultation"),("SRV101","MRI Scan"),("SRV102","X-Ray"),
                    ("SRV103","Blood Test"),("SRV104","Surgery")]

        for _ in range(rows):
            tid = "T" + fake.uuid4()[:7]
            base = round(uniform(200, 20000), 2)
            disc = round(uniform(0, base*0.15), 2)
            net = round(base - disc, 2)
            tax = round(net * 0.09, 2)
            total = round(net + tax, 2)
            svc = choice(services)
            c.execute("""
            INSERT INTO finance VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                tid,
                fake.uuid4()[:8],
                _rand_date(2022, 2025),
                base,
                "INR",
                choice(pay_methods),
                choice(["Yes","No"]),
                f"INS{randint(10000,99999)}",
                choice(["ABC Insurance","XYZ Health","CarePlus"]),
                svc[0],
                svc[1],
                choice(depts),
                "S" + fake.uuid4()[:7],
                disc,
                net,
                tax,
                total,
                choice(statuses),
                _rand_date(2022, 2026),
                "RCPT" + str(randint(100000, 999999))
            ))

        conn.commit()
        conn.close()
        return path
