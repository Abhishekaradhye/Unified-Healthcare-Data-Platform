import os
import json
from faker import Faker
from random import choice, randint, uniform
from datetime import date, timedelta

fake = Faker()

def _rand_date(start_year=1970, end_year=2024):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta = (end - start).days
    return (start + timedelta(days=randint(0, delta))).isoformat()

class HIS_B_DataCreator:
    def __init__(self, base_dir="tmp_his_b"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def create_patients_json(self, rows=400):
        path = os.path.join(self.base_dir, "patients.json")
        patients = []
        depts = ["Cardiology","Radiology","Orthopedics","Emergency","Oncology","Pediatrics","Neurology","Gastroenterology"]
        statuses = ["Admitted","Discharged","Critical","Observation"]
        severities = ["Mild","Moderate","Severe","Critical","treating"]
        bed_types = ["General","ICU","Severe Ward"]

        for _ in range(rows):
            patient = {
                "patient_id": fake.uuid4()[:8],
                "name": {"first": fake.first_name(), "last": fake.last_name()},
                "dob": _rand_date(1930, 2022),
                "gender": choice(["Male","Female"]),
                "location": {
                    "country": "India",
                    "state": "Maharashtra",
                    "city": choice(["Pune","Mumbai","Nagpur","Nashik","Nanded","Kolhapur","Ahmedabad","Delhi","Bidar"]),
                    "postal_code": fake.postcode()
                },
                "contact": {"phone": fake.msisdn(), "email": fake.email()},
                "emergency_person": {
                    "name": fake.name(),
                    "relation": choice(["Spouse","Parent","Sibling","Friend","Offspring"]),
                    "phone": fake.msisdn()
                },
                "insurance": {"id": f"INS{randint(10000,99999)}", "provider": choice(["ABC Insurance","XYZ Health","CarePlus","Aarogya Kavach"])},
                "primary_physician": "Dr. " + fake.last_name(),
                "medical_info": {
                    "blood_group": choice(["A+","A-","B+","B-","O+","O-","AB+","AB-"]),
                    "allergies": choice(["None","Penicillin","Dust","Peanuts"]),
                    "bp": f"{randint(100,140)}/{randint(60,90)}",
                    "hb": round(uniform(11,17),1),
                    "chronic_conditions": choice(["Diabetes","Hypertension","Asthma","None"])
                },
                "disease": choice(["Flu","Covid-19","Fracture","Heart Disease","Malaria"]),
                "patient_status": choice(statuses),
                "severity": choice(severities),
                "department_admitted": choice(depts),
                "current_department": choice(depts),
                "bed_type": choice(bed_types)
            }
            patients.append(patient)

        with open(path, "w") as f:
            json.dump(patients, f, indent=4)
        return path

    def create_staff_json(self, rows=60):
        path = os.path.join(self.base_dir, "staff.json")
        staff_list = []
        depts = ["Cardiology","Radiology","Orthopedics","Emergency","Oncology","Pediatrics"]
        roles = ["Doctor","Senior Nurse","Technician","Resident","Admin"]
        shifts = ["Morning","Evening","Night"]

        for _ in range(rows):
            staff = {
                "staff_id": "S" + fake.uuid4()[:7],
                "name": {"first": fake.first_name(), "last": fake.last_name()},
                "dob": _rand_date(1958,2001),
                "gender": choice(["Male","Female"]),
                "department": choice(depts),
                "designation": choice(roles),
                "joining_date": _rand_date(2005,2025),
                "salary": randint(30000,150000),
                "contact": {"phone": fake.msisdn(), "email": fake.company_email()},
                "address": {"line1": fake.street_address(), "line2": fake.secondary_address(), "city": choice(["Pune","Mumbai","Nagpur","Nashik"]), "state":"Maharashtra","country":"India","postal_code":fake.postcode()},
                "emergency_person": {
                    "name": fake.name(),
                    "relation": choice(["Spouse","Parent","Sibling","Friend"]),
                    "phone": fake.msisdn()
                },
                "work_shift": choice(shifts)
            }
            staff_list.append(staff)

        with open(path,"w") as f:
            json.dump(staff_list,f,indent=4)
        return path

    def create_finance_json(self, rows=120):
        path = os.path.join(self.base_dir, "finance.json")
        finance_list = []
        pay_methods = ["UPI","Credit Card","Debit Card","Cash"]
        statuses = ["Paid","Unpaid","Pending"]
        depts = ["Radiology","Orthopedics","Emergency","Oncology","Pediatrics"]
        services = [("SRV100","Consultation"),("SRV101","MRI Scan"),("SRV102","X-Ray"),
                    ("SRV103","Blood Test"),("SRV104","Surgery")]

        for _ in range(rows):
            svc = choice(services)
            base = round(uniform(200,20000),2)
            disc = round(uniform(0,base*0.15),2)
            net = round(base-disc,2)
            tax = round(net*0.09,2)
            total = round(net+tax,2)

            finance = {
                "transaction_id": "T"+fake.uuid4()[:7],
                "patient_id": fake.uuid4()[:8],
                "billing_date": _rand_date(2022,2025),
                "amount": base,
                "currency": "INR",
                "payment_method": choice(pay_methods),
                "insurance_claimed": choice(["Yes","No"]),
                "insurance_id": f"INS{randint(10000,99999)}",
                "insurance_provider": choice(["ABC Insurance","XYZ Health","CarePlus"]),
                "service_code": svc[0],
                "service_description": svc[1],
                "department": choice(depts),
                "staff_id": "S"+fake.uuid4()[:7],
                "discount_applied": disc,
                "net_amount": net,
                "tax": tax,
                "total_amount": total,
                "payment_status": choice(statuses),
                "due_date": _rand_date(2022,2026),
                "receipt_number": "RCPT"+str(randint(100000,999999))
            }
            finance_list.append(finance)

        with open(path,"w") as f:
            json.dump(finance_list,f,indent=4)
        return path
