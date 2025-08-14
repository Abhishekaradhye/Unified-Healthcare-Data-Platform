import pandas as pd
from faker import Faker
from random import choice, randint, uniform
from datetime import date, timedelta
import os

fake = Faker()

SPECIALTIES = ["Dermatology – Skincare", "Ophthalmology – Eye Care", "Trichology – Hair Care", "Otolaryngology (ENT) – Ear Care", 
               "Otolaryngology (ENT)", "– Throat & Nasal Care","Oral & Dental Medicine – Mouth Care", "Gynecology – Women’s Reproductive Health", 
               "Mycology – Fungal Infections", "Dermatology – Rash Management", "Dermatology – Skin Disorders"]

STAFF_ROLES = ["Doctor","Nurse","Therapist","Assistant"]
FINANCE_CATEGORIES = ["Consultation","Procedure","Treatment","Medication"]

def _rand_date(start_year=1960, end_year=2025):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta = (end - start).days
    return (start + timedelta(days=randint(0, delta))).isoformat()

class HIS_C_DataCreator:
    def __init__(self, base_dir="tmp_his_c"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def create_patients_csv(self, rows=500):
        data = []
        for _ in range(rows):
            specialty = choice(SPECIALTIES)
            data.append({
                "patient_id": fake.uuid4()[:8],
                "name": fake.name(),
                "dob": _rand_date(1950, 2023),
                "gender": choice(["Male","Female"]),
                "blood_group": choice(["A+","A-","B+","B-","O+","O-","AB+","AB-"]),
                "height_cm": randint(150,200),
                "weight_kg": randint(40,120),
                "medical_history": choice(["Diabetes","Hypertension","Asthma","None"]),
                "allergies": choice(["None","Penicillin","Pollen","Dust","Food"]),
                "insurance_id": f"INS{randint(10000,99999)}",
                "insurance_provider": choice(["ABC Insurance","XYZ Health","CarePlus","Aarogya Kavach"]),
                "primary_physician": "Dr. " + fake.last_name(),
                "specialty": specialty,
                "duration_days": randint(1,30),
                "care_instructions": fake.sentence(nb_words=6),
                "time_bound": _rand_date(2024,2025),
                "contact_phone": fake.msisdn(),
                "contact_email": fake.email(),
                "emergency_person_name": fake.name(),
                "emergency_person_relation": choice(["Spouse","Parent","Sibling","Friend","Offspring"]),
                "emergency_person_phone": fake.msisdn(),
                "department_admitted": specialty,
                "current_department": specialty,
                "bed_type": choice(["General","ICU","Severe Ward"]),
                "patient_status": choice(["Admitted","Discharged","Critical","Observation"]),
                "severity": choice(["Mild","Moderate","Severe","Critical"])
            })
        df = pd.DataFrame(data)
        path = os.path.join(self.base_dir, "patients.csv")
        df.to_csv(path, index=False)
        return path

    def create_staff_csv(self, rows=50):
        data = []
        for _ in range(rows):
            data.append({
                "staff_id": fake.uuid4()[:8],
                "name": fake.name(),
                "role": choice(STAFF_ROLES),
                "specialty_assigned": choice(SPECIALTIES),
                "joining_date": _rand_date(2000,2025),
                "experience_years": randint(1,30),
                "qualification": choice(["MBBS","BDS","Nursing","Physiotherapy","Dermatology Cert","Cosmetology Cert"]),
                "shift": choice(["Morning","Evening","Night"]),
                "contact_phone": fake.msisdn(),
                "contact_email": fake.email(),
                "address": fake.address(),
                "emergency_person_name": fake.name(),
                "emergency_person_relation": choice(["Spouse","Parent","Sibling","Friend","Offspring"]),
                "emergency_person_phone": fake.msisdn()
            })
        df = pd.DataFrame(data)
        path = os.path.join(self.base_dir, "staff.csv")
        df.to_csv(path, index=False)
        return path

    def create_finance_csv(self, rows=200):
        data = []
        for _ in range(rows):
            data.append({
                "transaction_id": fake.uuid4()[:8],
                "patient_id": fake.uuid4()[:8],
                "category": choice(FINANCE_CATEGORIES),
                "amount": round(uniform(100,5000),2),
                "transaction_date": _rand_date(2023,2025),
                "payment_method": choice(["Cash","Card","UPI","Insurance"]),
                "insurance_claim_id": f"CLM{randint(1000,9999)}",
                "remarks": fake.sentence(nb_words=5),
                "processed_by_staff_id": fake.uuid4()[:8]
            })
        df = pd.DataFrame(data)
        path = os.path.join(self.base_dir, "finance.csv")
        df.to_csv(path, index=False)
        return path
