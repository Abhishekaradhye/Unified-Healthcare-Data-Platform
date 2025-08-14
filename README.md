## Unified-Healthcare-Data-Platform


This project simulates four different Healthcare Information Systems (HIS) to demonstrate synthetic data generation, structured storage, and centralized uploading to Dropbox using FastAPI and Python. Each HIS is modeled after real-world scenarios and uses different file formats (SQLite, JSON, CSV) with domain-specific data. The project also maintains APIs to create, upload, and eventually retrieve data for each HIS.


# HIS_A (General Hospital – SQL/SQLite)

Purpose: Represents a typical hospital with general specialties.
Data Format: SQLite database (patients.db).

Datasets & Columns:

Patients – 400+ rows
patient_id, first_name, last_name, dob, gender, blood_group
height_cm, weight_kg, country, state, city, postal_code
phone, email, emergency_contact_name, emergency_contact_relation, emergency_contact_phone
insurance_id, insurance_provider, primary_physician, medical_history, disease, patient_status
severity, department_admitted, current_department, bed_type

Staff – doctors, nurses, admins, support staff
staff_id, first_name, last_name, department, role, experience_years\
phone, email, qualification, joining_date, shift_timing, salary, address

Finance – hospital finance data
transaction_id, patient_id, amount, payment_type, insurance_covered
billing_date, due_date, status, remarks


Process:
Data created locally in SQLite using Faker.
Uploaded to Dropbox using FastAPI endpoint /his_a/create_and_upload.
Server can be stopped after upload; data persists on Dropbox.


# HIS_B (Private Specialty Clinic – JSON)

Purpose: Represents a private clinic with nested structured data.
Data Format: JSON (patients.json, staff.json, finance.json)

Datasets & Columns:
Patients – 400+ rows, nested structure
name: {first_name, last_name}
dob, gender
location: {country, state, city, postal_code}
contact: {phone, email}
emergency_person: {name, relation, phone}
insurance: {id, provider}
primary_physician, medical_info: {diseases, allergies, blood_group, basic_tests}
patient_status, severity, department_admitted, current_department, bed_type

Staff – nested fields
name, contact, department, role, qualifications, experience_years, shift_timing

Finance – nested fields
transaction_id, patient_id, amount, payment_type, insurance_covered, billing_date, status

Process:
JSON data generated in nested format to mirror complex hierarchical data.
Uploaded to Dropbox via /his_b/create_and_upload.


# HIS_C (Cosmetic & Skincare Clinic – CSV)

Purpose: Represents beauty, cosmetic, and skincare-focused clinic.
Data Format: CSV (patients.csv, staff.csv, finance.csv)

Datasets & Columns:
Patients – 500+ rows
Standard fields (patient_id, name, dob, gender)
contact, location, emergency_person
Specialty fields: specialty (skincare, haircare, eye care, etc.), treatment_duration_days, care_instructions, time_bound
department_admitted, current_department, bed_type, severity, patient_status

Staff – expanded for cosmetic specialties
staff_id, name, department, role, experience_years, qualification, shift, salary, contact, address, specialty_handled

Finance – detailed billing
transaction_id, patient_id, amount, payment_type, insurance_covered, billing_date, due_date, status, remarks, special_services_charges

Process:
Data created in CSV format to reflect time-bound care and cosmetic specialties.
Uploaded via /his_c/create_and_upload.


# HIS_D (Critical Care & Oncology Hospital – SQL/SQLite)

Purpose: Represents a hospital treating serious illnesses (Cancer, TB, HIV, Neurosurgery).
Data Format: SQLite database (patients.db)

Datasets & Columns:
Patients – 500+ rows

Standard fields (patient_id, name, dob, gender, contact, location)
Specialty fields: disease, stage_or_danger, need_of_surgery, primary_physician, department_admitted, current_department, bed_type, severity, patient_status
insurance_id, insurance_provider, medical_history, allergies, test_results, treatment_plan

Staff – expanded for oncology and critical care
staff_id, name, department, role, experience_years, qualification, shift, contact, salary, specialty_handled, research_publications

Finance – detailed critical care billing
transaction_id, patient_id, amount, payment_type, insurance_covered, billing_date, due_date, status, remarks, surgery_charges, medication_charges

Process:
Data generated locally in SQLite.
Uploaded via FastAPI endpoint /his_d/create_and_upload.

