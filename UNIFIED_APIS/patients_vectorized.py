# import pandas as pd
# import chromadb
# from sentence_transformers import SentenceTransformer

# client = chromadb.CloudClient(
#     api_key='ck-GsTUUjV1jnZBP3qogD1nZoLJZoc26i2vHoEVNZKd2NWD',
#     tenant='f1a768d2-9630-4148-9eb5-6b3dca7469f8',
#     database='try5'
# )

# df = pd.read_csv(r"D:\Projects\Unified Platform\UNIFIED_DATA\unified_patients.csv", encoding='ISO-8859-1')

# df.drop(columns=['dob'], inplace=True)

# model = SentenceTransformer('all-MiniLM-L6-v2')

# collection = client.get_or_create_collection(name="the_patients")

# def clean_dataframe_for_chromadb(df):
#     """Ensure all values are JSON serializable"""
#     for col in df.columns:
#         df[col] = df[col].apply(lambda x: str(x) if not isinstance(x, (str, int, float, bool, type(None))) else x)
#     return df

# df = clean_dataframe_for_chromadb(df)

# for idx, row in df.iterrows():
#     text = " ".join([str(v) for v in row.values])
#     embedding = model.encode(text).tolist()
#     collection.add(
#         ids=[row['patient_id']],
#         metadatas=[row.to_dict()],
#         embeddings=[embedding],
#         documents=[text]
#     )

# print("All patient rows ingested into ChromaDB collection 'the_patients'.")



import os
import json
import math
from typing import List, Dict, Any, Iterable

import chromadb
from sentence_transformers import SentenceTransformer

# ==========
# CONFIG
# ==========
# Set these via environment variables or paste them here.
CHROMA_API_KEY = os.getenv("CHROMA_API_KEY", "ck-GsTUUjV1jnZBP3qogD1nZoLJZoc26i2vHoEVNZKd2NWD")
CHROMA_TENANT  = os.getenv("CHROMA_TENANT",  "f1a768d2-9630-4148-9eb5-6b3dca7469f8")
CHROMA_DB      = os.getenv("CHROMA_DB",      "try5")

# Collection name for patients
COLLECTION_NAME = "vectorized_patients"

# Path to your unified patients JSON (already working in your project)
PATIENTS_JSON_PATH = r"D:\Projects\Unified Platform\UNIFIED_DATA\assembled_patients.json"

# Keep metadata simple and <=16 keys (Chroma Cloud limitation on query filters/metadata payloads)
# Choose the most useful columns for retrieval—adjust if needed.
METADATA_FIELDS = [
    "patient_id", "first_name", "last_name", "gender", "blood_group",
     "city", "phone",
    "email", "primary_physician", "disease", "patient_status", "severity", "bed_type",
]

# Text fields to compose the “document” (free text) to embed
DOC_TEXT_FIELDS = [
    "patient_id", "first_name", "last_name", "dob", "gender", "blood_group",
    "height_cm", "weight_kg", "country", "state", "city", "postal_code",
    "phone", "email", "emergency_contact_name", "emergency_contact_relation",
    "insurance_id", "insurance_provider", "primary_physician", "medical_history",
    "disease", "patient_status", "severity", "department_admitted",
    "current_department", "bed_type", "bp", "hb", "allergies", "chronic_conditions",
]

BATCH_SIZE = 256  # tune for your machine/network
MODEL_NAME = "all-MiniLM-L6-v2"

# ==========
# HELPERS
# ==========
def to_str(x: Any) -> str:
    if x is None:
        return ""
    # Ensure plain string (avoid lists/dicts in metadata)
    if isinstance(x, (dict, list, tuple)):
        return json.dumps(x, ensure_ascii=False)
    return str(x)

def build_document(row: Dict[str, Any]) -> str:
    # Join selected fields for embedding text
    parts = []
    for k in DOC_TEXT_FIELDS:
        if k in row and row[k] not in [None, ""]:
            parts.append(f"{k}: {to_str(row[k])}")
    return " | ".join(parts)

def chunked(iterable: Iterable[Any], size: int) -> Iterable[List[Any]]:
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch

# ==========
# MAIN
# ==========
def main():
    # Load JSON
    with open(PATIENTS_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Patients JSON must be a list of rows (objects).")

    # Init embedder
    model = SentenceTransformer(MODEL_NAME)

    # Chroma Cloud Client
    client = chromadb.CloudClient(
        api_key=CHROMA_API_KEY,
        tenant=CHROMA_TENANT,
        database=CHROMA_DB,
    )

    # Create/get collection
    collection = client.get_or_create_collection(name=COLLECTION_NAME, metadata={"source": "patients"})

    # (Optional) Clear prior “patients” load for idempotency
    try:
        collection.delete(where={"source": "patients"})
    except Exception:
        # ok if nothing to delete
        pass

    # Ingest in batches
    total = len(data)
    print(f"Ingesting {total} patient rows to Chroma collection: {COLLECTION_NAME}")

    for batch_idx, batch in enumerate(chunked(data, BATCH_SIZE), start=1):
        ids = []
        docs = []
        metas = []
        embeds = []

        # Prepare payload
        for row in batch:
            pid = to_str(row.get("patient_id"))
            if not pid:
                # Ensure a stable unique id; fallback if missing
                continue

            # Build metadata with whitelisted fields only
            md = {k: to_str(row.get(k)) for k in METADATA_FIELDS}
            md["source"] = "patients"  # add a simple tag for delete/filter

            doc = build_document(row)
            emb = model.encode(doc).tolist()

            ids.append(pid)
            docs.append(doc)
            metas.append(md)
            embeds.append(emb)

        if not ids:
            continue

        # Use upsert if available; otherwise add
        try:
            collection.upsert(ids=ids, documents=docs, metadatas=metas, embeddings=embeds)
        except AttributeError:
            collection.add(ids=ids, documents=docs, metadatas=metas, embeddings=embeds)

        done = min(batch_idx * BATCH_SIZE, total)
        print(f"  → Uploaded {done}/{total}")

    print("✅ Ingestion complete.")

if __name__ == "__main__":
    main()
