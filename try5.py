import sqlite3
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

# Chroma Cloud client
client = chromadb.CloudClient(
    api_key='ck-GsTUUjV1jnZBP3qogD1nZoLJZoc26i2vHoEVNZKd2NWD',
    tenant='f1a768d2-9630-4148-9eb5-6b3dca7469f8',
    database='try5'
)

# 1. Create or get collection
collection = client.get_or_create_collection(name="trial_patients")

# 2. Create a sample SQL table (15x10) locally
conn = sqlite3.connect("united_patients.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    dob TEXT,
    gender TEXT,
    blood_group TEXT,
    height_cm REAL,
    weight_kg REAL,
    city TEXT,
    country TEXT
)
""")

# Insert sample data
for i in range(1, 16):
    cursor.execute("""
    INSERT OR REPLACE INTO patients 
    (patient_id, first_name, last_name, dob, gender, blood_group, height_cm, weight_kg, city, country)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f"P{i:03d}", f"First{i}", f"Last{i}", f"1990-01-{i:02d}", 
        "Male" if i % 2 == 0 else "Female",
        "O+" if i % 2 == 0 else "A-",
        160 + i, 55 + i, f"City{i}", "Europe"
    ))
conn.commit()

# 3. Read table as DataFrame
df = pd.read_sql_query("SELECT * FROM patients", conn)

# 4. Initialize embedding model (open-source)
model = SentenceTransformer('all-MiniLM-L6-v2')

# 5. Ingest each row as metadata and vector
for idx, row in df.iterrows():
    text = " ".join([str(v) for v in row.values])  # simple text from row
    embedding = model.encode(text).tolist()
    
    collection.add(
        ids=[row['patient_id']],
        metadatas=[row.to_dict()],
        embeddings=[embedding],
        documents=[text]
    )

print("All patient rows ingested into ChromaDB collection 'patients'.")


# JUST SAVE & RUN IN TERMINAL