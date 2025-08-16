import os
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer

# ==========
# CONFIG
# ==========
CHROMA_API_KEY = os.getenv("CHROMA_API_KEY", "ck-GsTUUjV1jnZBP3qogD1nZoLJZoc26i2vHoEVNZKd2NWD")
CHROMA_TENANT  = os.getenv("CHROMA_TENANT",  "f1a768d2-9630-4148-9eb5-6b3dca7469f8")
CHROMA_DB      = os.getenv("CHROMA_DB",      "try5")

COLLECTION_NAME = "vectorized_patients"
MODEL_NAME = "all-MiniLM-L6-v2"

# ==========
# INIT
# ==========
client = chromadb.CloudClient(
    api_key=CHROMA_API_KEY,
    tenant=CHROMA_TENANT,
    database=CHROMA_DB,
)
collection = client.get_collection(COLLECTION_NAME)
model = SentenceTransformer(MODEL_NAME)

app = FastAPI(title="Patients Search API")

class Query(BaseModel):
    context: str
    top_k: int = 1

class MultiQuery(BaseModel):
    contexts: List[str]
    top_k: int = 1

@app.get("/")
def root():
    return {"message": f"Search API ready for collection: {COLLECTION_NAME}"}

@app.post("/search")
def search(q: Query):
    emb = model.encode(q.context).tolist()
    res = collection.query(query_embeddings=[emb], n_results=q.top_k)
    results = []
    for i in range(len(res["ids"][0])):
        results.append({
            "id": res["ids"][0][i],
            "distance": res["distances"][0][i],
            "row": res["metadatas"][0][i].get("full_row", {}),
        })
    return results

@app.post("/search_multiple")
def search_multiple(q: MultiQuery):
    embs = [model.encode(c).tolist() for c in q.contexts]
    res = collection.query(query_embeddings=embs, n_results=q.top_k)
    all_results = []
    for i, ctx in enumerate(q.contexts):
        matches = []
        for j in range(len(res["ids"][i])):
            matches.append({
                "id": res["ids"][i][j],
                "distance": res["distances"][i][j],
                "row": res["metadatas"][i][j].get("full_row", {}),
            })
        all_results.append({"query": ctx, "matches": matches})
    return all_results
