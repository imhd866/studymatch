from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from model_utils import generate_recommendations
from model_utils import recommend_papers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/api/recommend")
def recommend_endpoint(request: QueryRequest):
    query = request.query
    results = recommend_papers(query)

    response = []
    for paper in results:
        response.append({
            "id": paper["id"],
            "title": paper["title"],
            "authors": paper.get("authors", "Unknown"),
            "categories": paper.get("categories", "N/A"),
            "abstract": paper["abstract"],
            "score": float(paper["score"]),
            "url": f"https://arxiv.org/abs/{paper['id']}",
        })
    
    return {"results": response}
