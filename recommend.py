import streamlit as st
import pandas as pd
import numpy as np
import torch
import re
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# ========== Config ========== #
MODEL_NAME = "allenai/specter2_base"
TOP_N = 10
KEYWORDS = ['spiking', 'neuromorphic', 'Josephson', 'superconduct', 'quantum', 'edge']
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ========== Streamlit UI Setup ========== #
st.title("📚 StudyMatch: Academic Paper Recommender")
st.markdown("""
Enter a research interest, paper title, or abstract to get scholarly recommendations.
This version uses semantic embeddings (SPECTER), TF-IDF keyword expansion, MMR diversification, and keyword-aware reranking.
""")

# ========== Sidebar File Uploads ========== #
st.sidebar.header("📁 Upload Files")

uploaded_csv = st.sidebar.file_uploader("Upload cleaned_arxiv_large.csv", type=["csv"])
uploaded_part1 = st.sidebar.file_uploader("Upload specter_embeddings_part1.npz", type=["npz"])
uploaded_part2 = st.sidebar.file_uploader("Upload specter_embeddings_part2.npz", type=["npz"])

if uploaded_csv and uploaded_part1 and uploaded_part2:
    df = pd.read_csv(uploaded_csv)
    data1 = np.load(uploaded_part1)
    data2 = np.load(uploaded_part2)

    embeddings = np.vstack([data1["embeddings"], data2["embeddings"]])
    ids = np.concatenate([data1["ids"], data2["ids"]])
else:
    st.warning("Please upload the `.csv`, `part1.npz`, and `part2.npz` files in the sidebar.")
    st.stop()

# ========== Load Model ========== #
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME).to(DEVICE)
    model.eval()
    return tokenizer, model

tokenizer, model = load_model()

# ========== Core Functions ========== #
def embed_text(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.no_grad():
        return model(**inputs).last_hidden_state[:, 0, :].squeeze().cpu().numpy()

def expand_query_with_top_keywords(query_text, df, embeddings, top_n=10, max_terms=5):
    q_vec = embed_text(query_text).reshape(1, -1)
    sims = cosine_similarity(q_vec, embeddings)[0]
    top_docs = df.iloc[sims.argsort()[::-1][:top_n]]
    corpus = top_docs['abstract'].tolist()
    tfidf = TfidfVectorizer(stop_words='english', max_features=50)
    tfidf.fit(corpus)
    keywords = tfidf.get_feature_names_out()[:max_terms]
    expanded_query = query_text + " " + " ".join(keywords)
    return expanded_query, q_vec

def rerank(results, scores, query):
    reranked = []
    for idx, (_, row) in enumerate(results.iterrows()):
        bonus = sum(1 for kw in KEYWORDS if kw.lower() in row['title'].lower() or kw.lower() in row['abstract'].lower())
        reranked.append((idx, scores[idx] + 0.01 * bonus))
    reranked.sort(key=lambda x: x[1], reverse=True)
    return [i for i, _ in reranked]

def mmr_diversify(query_vec, candidate_vecs, top_k=10, lambda_param=0.7):
    selected = []
    remaining = list(range(len(candidate_vecs)))
    sims_to_query = cosine_similarity(candidate_vecs, query_vec).flatten()
    first = np.argmax(sims_to_query)
    selected.append(first)
    remaining.remove(first)
    for _ in range(1, top_k):
        mmr_scores = []
        for i in remaining:
            sim_to_query = sims_to_query[i]
            sim_to_selected = max(cosine_similarity(candidate_vecs[i].reshape(1, -1), candidate_vecs[selected])[0])
            mmr_score = lambda_param * sim_to_query - (1 - lambda_param) * sim_to_selected
            mmr_scores.append((i, mmr_score))
        if not mmr_scores:
            break
        next_doc = max(mmr_scores, key=lambda x: x[1])[0]
        selected.append(next_doc)
        remaining.remove(next_doc)
    return selected

def recommend(query_text, df, embeddings, top_n=TOP_N):
    df_filtered = df.reset_index(drop=True)
    expanded_query, _ = expand_query_with_top_keywords(query_text, df_filtered, embeddings)
    query_vec = embed_text(expanded_query).reshape(1, -1)
    sims = cosine_similarity(query_vec, embeddings)[0]
    top_indices = sims.argsort()[::-1][:50]
    reranked = rerank(df_filtered.iloc[top_indices], sims[top_indices], expanded_query)
    candidate_vecs = embeddings[top_indices]
    diversified = mmr_diversify(query_vec, candidate_vecs, top_k=top_n)
    final_indices = [top_indices[i] for i in diversified]
    return df_filtered.iloc[final_indices].assign(score=sims[final_indices])

# ========== UI Input & Output ========== #
query = st.text_area("Enter your research topic or abstract:", height=200)

if st.button("Get Recommendations") and query:
    with st.spinner("Generating recommendations..."):
        results = recommend(query, df, embeddings)
    st.success(f"Top {TOP_N} Recommended Papers")
    for _, row in results.iterrows():
        arxiv_url = f"https://arxiv.org/abs/{row['id']}"
        st.markdown(f"**[{row['title']}]({arxiv_url})**")
        st.markdown(f"*{row.get('authors', 'Unknown Author')}*  ")
        st.markdown(f"Category: `{row.get('categories', 'N/A')}`  ")
        st.markdown(f"Similarity Score: `{row['score']:.4f}`")
        st.markdown(row['abstract'][:500] + "...\n")
        st.markdown("---")