import os
import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

json_file = r"D:\Projects\Unified Platform\UNIFIED_DATA\assembled_finance_dataframe.json"

df = pd.read_json(json_file, lines=True)

client = chromadb.CloudClient(
    api_key='ck-GsTUUjV1jnZBP3qogD1nZoLJZoc26i2vHoEVNZKd2NWD',
    tenant='f1a768d2-9630-4148-9eb5-6b3dca7469f8',
    database='try5'
)

collection = client.get_or_create_collection(name="finance")

model = SentenceTransformer('all-MiniLM-L6-v2')

for idx, row in df.iterrows():
    metadata = {k: str(v) for k, v in row.to_dict().items()}

    text = " ".join([str(v) for v in row.values])
    embedding = model.encode(text).tolist()

    collection.add(
        ids=[row['transaction_id']],
        metadatas=[metadata],
        embeddings=[embedding],
        documents=[text]
    )

print("All patient rows ingested into ChromaDB collection 'finance'.")
