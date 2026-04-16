import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
import requests
from chromadb.config import Settings

# Load dataset
df = pd.read_excel("thesis.xlsx")
df.columns = df.columns.str.strip()

def row_to_text(row):
    return f"""
Title: {row['title_clean']}
Journal: {row['journal_clean']}
Year: {row['year']}
Authors: {row['authors']}
Keywords: {row['keyword']}
"""

texts = [row_to_text(row) for _, row in df.iterrows()]

# Model and Chroma setup (idempotent)
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client(Settings(persist_directory="./chroma_db"))
try:
    collection = client.get_collection("thesis_db")
except:
    collection = client.create_collection("thesis_db")
    embeddings = model.encode(texts).tolist()
    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=[str(i) for i in range(len(texts))]
    )

def semantic_search(query, n_results=5):
    """Semantic search for relevant theses."""
    results = collection.query(
        query_embeddings=[model.encode(query).tolist()],
        n_results=n_results
    )
    return results["documents"][0]

def recommend_topics(query):
    """Recommend research topics based on search."""
    docs = semantic_search(query)
    context = "\n\n".join(docs)
    
    prompt = f"""You are a research topic recommender. Based on the user's interest "{query}" and these similar theses:

{context}

Suggest 5-8 related research topics that would be good to explore next. 
Focus on topics, not specific titles. 
Output ONLY the list, one topic per line, numbered 1-8:"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3.5:latest",
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"].strip()
    except Exception as e:
        return f"Error generating recommendations: {e}. Ensure Ollama is running."

if __name__ == "__main__":
    print("Topic Recommender (Ctrl+C to exit)")
    while True:
        try:
            user_topic = input("\nEnter a topic to search (or 'quit'): ").strip()
            if user_topic.lower() == 'quit':
                break
            if not user_topic:
                continue
            print("\nSearching theses...")
            recs = recommend_topics(user_topic)
            print("\nRecommended Topics:")
            print(recs)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

