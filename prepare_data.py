# prepare_data.py

import json
import pandas as pd
import re
from tqdm import tqdm
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel

# Config
INPUT_PATH = "arxiv-metadata-oai-snapshot.json"
CSV_PATH = "cleaned_arxiv_subset.csv"
EMBED_PATH = "specter_embeddings.npz"
MAX_LINES = 1_000_000
MAX_PAPERS = 100_000
TARGET_CATEGORIES = ['cs.', 'stat.ML', 'eess.', 'q-bio.', 'math.', 'econ.', 'physics.', 'astro-ph', 'cond-mat', 'quant-ph']
MODEL_NAME = "allenai/specter2_base"
BATCH_SIZE = 16

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    text = re.sub(r'\$.*?\$', '', text)
    return text.strip()

def has_target_category(cat_str):
    return any(cat.startswith(prefix) for prefix in TARGET_CATEGORIES for cat in cat_str.split())

def process_arxiv_json():
    records = []
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        for i, line in enumerate(tqdm(f, desc="Reading JSON")):
            if i >= MAX_LINES:
                break
            try:
                paper = json.loads(line)
                cats = paper.get('categories', '')
                if not has_target_category(cats):
                    continue
                record = {
                    'id': paper.get('id'),
                    'title': clean_text(paper.get('title', '')),
                    'abstract': clean_text(paper.get('abstract', '')),
                    'authors': paper.get('authors', ''),
                    'categories': cats,
                }
                if record['title'] and record['abstract'] and len(record['abstract']) > 100:
                    records.append(record)
                if len(records) >= MAX_PAPERS:
                    break
            except json.JSONDecodeError:
                continue
    return pd.DataFrame(records)

def embed_batch(batch_texts, model, tokenizer, device):
    inputs = tokenizer(batch_texts, padding=True, truncation=True, max_length=512, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        return model(**inputs).last_hidden_state[:, 0, :].cpu().numpy()

if __name__ == "__main__":
    print("⏳ Loading and filtering dataset...")
    df = process_arxiv_json()
    df.to_csv(CSV_PATH, index=False)
    print(f"✅ Saved CSV: {CSV_PATH}")

    print("⏳ Generating embeddings...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    texts = (df['title'] + " " + df['abstract']).tolist()
    all_embeddings = []
    for i in tqdm(range(0, len(texts), BATCH_SIZE)):
        batch = texts[i:i+BATCH_SIZE]
        embeds = embed_batch(batch, model, tokenizer, device)
        all_embeddings.append(embeds)

    embeddings = np.vstack(all_embeddings)
    np.savez_compressed(EMBED_PATH, embeddings=embeddings, ids=np.array(df['id'].tolist()))
    print(f"✅ Saved embeddings: {EMBED_PATH}")