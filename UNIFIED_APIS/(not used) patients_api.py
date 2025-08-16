from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import chromadb

client = chromadb.CloudClient(
    api_key='ck-GsTUUjV1jnZBP3qogD1nZoLJZoc26i2vHoEVNZKd2NWD',
    tenant='f1a768d2-9630-4148-9eb5-6b3dca7469f8',
    database='try5'
)
collection = client.get_collection("patients")

model = SentenceTransformer('all-MiniLM-L6-v2')

app = FastAPI()

class Query(BaseModel):
    context: str

@app.post("/search")
def search_patient(query: Query):
    embedding = model.encode(query.context).tolist()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=1  
    )
    return results['metadatas'][0] if results['metadatas'] else {}
