<<<<<<< HEAD
<<<<<<< HEAD
# 📚 StudyMatch: Academic Paper Recommender

StudyMatch is a lightweight academic paper recommender system powered by the [SPECTER2](https://arxiv.org/abs/2004.07180) model. It helps researchers find relevant and diverse papers based on a query using semantic embeddings, keyword-aware reranking, and MMR-based diversification.

## 🚀 Features
- Semantic similarity via pretrained SPECTER2 embeddings
- TF-IDF keyword-based query expansion
- Re-ranking with domain-specific keyword boosts
- Maximal Marginal Relevance (MMR) for result diversity
- Simple and fast web interface via Streamlit

## 📦 Dataset
We use a filtered subset of arXiv metadata with:
- Titles, abstracts, categories, authors
- Precomputed SPECTER2 embeddings for fast inference

## 🧠 How It Works
1. Enter a research topic, phrase, or abstract.
2. The system embeds it using SPECTER2.
3. Top matches are selected based on cosine similarity.
4. Results are reranked using keyword bonuses.
5. MMR diversification reduces redundancy in suggestions.

## 🖥️ Try It Online
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

(Replace this with your real Streamlit link after deployment)

## 🛠️ Run Locally

```bash
git clone https://github.com/your-username/studymatch.git
cd studymatch
pip install -r requirements.txt
=======
# 📚 StudyMatch: Academic Paper Recommender

StudyMatch is a lightweight academic paper recommender system powered by the [SPECTER2](https://arxiv.org/abs/2004.07180) model. It helps researchers find relevant and diverse papers based on a query using semantic embeddings, keyword-aware reranking, and MMR-based diversification.

## 🚀 Features
- Semantic similarity via pretrained SPECTER2 embeddings
- TF-IDF keyword-based query expansion
- Re-ranking with domain-specific keyword boosts
- Maximal Marginal Relevance (MMR) for result diversity
- Simple and fast web interface via Streamlit

## 📦 Dataset
We use a filtered subset of arXiv metadata with:
- Titles, abstracts, categories, authors
- Precomputed SPECTER2 embeddings for fast inference

## 🧠 How It Works
1. Enter a research topic, phrase, or abstract.
2. The system embeds it using SPECTER2.
3. Top matches are selected based on cosine similarity.
4. Results are reranked using keyword bonuses.
5. MMR diversification reduces redundancy in suggestions.

## 🖥️ Try It Online
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

(Replace this with your real Streamlit link after deployment)

## 🛠️ Run Locally

```bash
git clone https://github.com/your-username/studymatch.git
cd studymatch
pip install -r requirements.txt
>>>>>>> 353e5d04834dbd8cf8a0c89d0c362f67fb7ace73
=======
# 📚 StudyMatch: Academic Paper Recommender

StudyMatch is a lightweight academic paper recommender system powered by the [SPECTER2](https://arxiv.org/abs/2004.07180) model. It helps researchers find relevant and diverse papers based on a query using semantic embeddings, keyword-aware reranking, and MMR-based diversification.

## 🚀 Features
- Semantic similarity via pretrained SPECTER2 embeddings
- TF-IDF keyword-based query expansion
- Re-ranking with domain-specific keyword boosts
- Maximal Marginal Relevance (MMR) for result diversity
- Simple and fast web interface via Streamlit

## 📦 Dataset
We use a filtered subset of arXiv metadata with:
- Titles, abstracts, categories, authors
- Precomputed SPECTER2 embeddings for fast inference

## 🧠 How It Works
1. Enter a research topic, phrase, or abstract.
2. The system embeds it using SPECTER2.
3. Top matches are selected based on cosine similarity.
4. Results are reranked using keyword bonuses.
5. MMR diversification reduces redundancy in suggestions.

## 🖥️ Try It Online
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

(Replace this with your real Streamlit link after deployment)

## 🛠️ Run Locally

```bash
git clone https://github.com/your-username/studymatch.git
cd studymatch
pip install -r requirements.txt
>>>>>>> 0fe2869d6a22b3da40b2e4445489603e0c42f7fd
streamlit run recommend.py