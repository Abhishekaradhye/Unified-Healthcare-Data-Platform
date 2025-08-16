from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import chromadb
from typing import List

client = chromadb.CloudClient(
    api_key='ck-GsTUUjV1jnZBP3qogD1nZoLJZoc26i2vHoEVNZKd2NWD',
    tenant='f1a768d2-9630-4148-9eb5-6b3dca7469f8',
    database='try5'
)
collection = client.get_collection("trial_patients")
model = SentenceTransformer('all-MiniLM-L6-v2')

app = FastAPI()

class MultiQuery(BaseModel):
    contexts: List[str]  # list of context strings
    top_k: int = 3

@app.post("/search_multiple")
def search_multiple(query: MultiQuery):
    embeddings = [model.encode(c).tolist() for c in query.contexts]
    results = collection.query(
        query_embeddings=embeddings,
        n_results=query.top_k
    )
    # results['metadatas'] is a list of lists, each corresponding to one context
    response = {}
    for ctx, metadata_list in zip(query.contexts, results['metadatas']):
        response[ctx] = metadata_list
    return response

# Run: uvicorn try6:app --reload --port 8000

# BROUGHT OUT EXCELLENT RESULTS BUT ON TEST DATA, WHICH WAS IN SMALLER NUMBER, ROUGHLY 15-20 ROWS