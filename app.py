import streamlit as st
import requests

st.set_page_config(page_title="📚 StudyMatch", layout="centered")

st.title("📚 StudyMatch: Academic Paper Recommender")
st.markdown("""
Paste a research topic, abstract, or interest below to get personalized paper recommendations.
""")

# === Input Area ===
query = st.text_area("Enter your research topic or abstract:", height=200)

if st.button("Get Recommendations") and query.strip():
    with st.spinner("Fetching recommendations..."):
        try:
            response = requests.post(
                "http://localhost:8000/api/recommend",  # change to render URL after deploy
                json={"query": query}
            )
            if response.status_code == 200:
                results = response.json()["results"]
                st.success("Top Recommendations")
                for paper in results:
                    st.markdown(f"**[{paper['title']}]({paper['url']})**")
                    st.markdown(f"*{paper['authors']}*  ")
                    st.markdown(f"Category: `{paper['categories']}`  ")
                    st.markdown(f"Similarity Score: `{paper['score']:.4f}`")
                    st.markdown(paper['abstract'][:500] + "...\n")
                    st.markdown("---")
            else:
                st.error("Failed to fetch recommendations.")
        except Exception as e:
            st.error(f"Error: {e}")