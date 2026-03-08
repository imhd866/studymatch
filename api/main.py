from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from model_utils import generate_recommendations

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

@app.post("/recommend")
def recommend(request: QueryRequest):
    try:
        df = pd.read_csv("backend/embeddings/cleaned_arxiv_large.csv")
        embeddings = np.load("backend/embeddings/specter_embeddings_combined.npz")["embeddings"]
        results = generate_recommendations(request.query, df, embeddings)
        return results.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}
